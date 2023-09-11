import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
import os
import base64
from dash.exceptions import PreventUpdate
from PIL import Image
import numpy as np

UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

dash.register_page(__name__)

def is_thermal_image(image_path, temperature_threshold=100):
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert the image to grayscale
        img_gray = img.convert('L')
        
        # Convert the grayscale image to a numpy array
        img_array = np.array(img_gray)
        
        # Calculate the mean pixel value
        mean_pixel_value = np.mean(img_array)
        
        # Check if the mean pixel value exceeds the temperature threshold
        return mean_pixel_value >= temperature_threshold
    except Exception as e:
        # Error occurred while processing the image
        return False

def get_error_type(filename, image_path):
    # Define custom error types based on filename characteristics
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        return "Not an image"
    
    # Check if the image is not a thermal image
    if not is_thermal_image(image_path):
        return "Not a thermal image"
    
    # Add more conditions for other error types as needed
    return None

upload_component = dcc.Upload(
    id="upload-image",
    children=[
        html.Div(
            id="upload-area",
            children=[
                html.Img(
                    id="upload-preview",
                    src="assets/png-clipart-font-awesome-upload-computer-icons-font-computers-blue-text-thumbnail-removebg-preview.png",
                    style={
                        'height': '200px',
                        'width': '200px',
                        'display': 'block',
                        "fill": "currentColor",
                    },
                ),
                html.P("Drag and drop or click to select a file to upload."),
            ],
            className="upload-content",
            style={
                "display": "flex",
                "flexDirection": "column",
                "justifyContent": "center",
                "alignItems": "center",
            },
        ),
    ],
    style={
        "width": "100%",
        "borderWidth": "2px",
        "borderStyle": "dashed",
        "borderRadius": "10px",
        "textAlign": "center",
        "margin": "20px auto",
        'margin-top': '50px',
        "padding": "40px",
        'background-color': '#F5F9FD',
    },
    multiple=True,
)

alert = dbc.Alert(
    [
        html.H4("Upload Information", className="alert-heading", style={'font-family': 'Caudex, sans-serif',
                                                                        "textAlign": "center",}),
        html.Hr(),
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            "1",
                            style={
                                "width": "50px",
                                "height": "50px",
                                "borderRadius": "50%",
                                "backgroundColor": "blue",
                                "color": "white",
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                            }
                        ),
                        html.Div(
                            "File type: Since this is a web-app for diagnosing your solar panel problem, please upload your thermal image.",
                            style={"margin-left": "10px"}
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center"}
                ),
            ),
        ),
    ],
    color="info"
)

# -------------------------Main Upload layout-----------------------------#

layout = html.Div([
    dbc.Row(dbc.Col(html.H1('Upload your thermal image', style={'font-family': 'Caudex, sans-serif',"textAlign": "center",}),)),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(alert, xs=12, sm=12, md=30, lg=30, xl=30, className="mx-auto"),  # Adjust column sizes
            dbc.Col(upload_component, xs=12, sm=12, md=30, lg=30, xl=30, className="mx-auto"),  # Adjust column sizes
            # Display success alert
            dbc.Col(
                [
                    dbc.Alert(
                        id="success-alert",
                        color="success",
                        style={"margin-top": "10px"},
                        is_open=False,  # Start with the alert closed
                    ),
                    # Add a button to the Diagnosis page
                    html.Div(id="diagnosis-button", style={"margin-top": "10px"}),
                ],
                xs=12, sm=12, md=12, lg=12, xl=12, className="mx-auto"
            ),
            # Display error alert for invalid files
            dbc.Col(
                dbc.Alert(
                    id="invalid-file-alert",
                    color="danger",
                    style={"margin-top": "10px"},
                    is_open=False,  # Start with the alert closed
                ),
                xs=12, sm=12, md=12, lg=12, xl=12, className="mx-auto"
            ),
            dbc.Row(dbc.Col(html.H2('Uploaded images', style={'font-family': 'Caudex, sans-serif',"textAlign": "center",}),)),
            # Add a new div to display the list of uploaded filenames
            dbc.Row(
                dbc.Col(
                    html.Div(
                        id="uploaded-filenames",
                        children=[],
                        style={'font-family': 'Caudex, sans-serif',
                               "textAlign": "center",
                               "margin-top": "10px",
                               "overflowY": "scroll",
                               "height": "100px"
                               },
                    )
                )
            ),
        ]
    ),
],
style={
    'height': '100%',
    'width': '100%',
}
)

def save_uploaded_image(contents):
    decoded = base64.b64decode(contents)
    file_path = os.path.join(UPLOAD_FOLDER, "uploaded_image.png")
    with open(file_path, "wb") as f:
        f.write(decoded)

@callback(
    Output("upload-image", "filename"),
    Output("success-alert", "children"),
    Output("success-alert", "is_open"),
    Output("invalid-file-alert", "children"),
    Output("invalid-file-alert", "is_open"),
    Output("diagnosis-button", "children"),
    Output("session", "data"),
    Output("uploaded-filenames", "children"),
    Input("upload-image", "contents"),
    State("upload-image", "filename"),
    State('session', 'data')
)
def save_uploaded_file(content, filenames, session_data):
    if content is not None:
        upload_folder = "static/uploads/"
        os.makedirs(upload_folder, exist_ok=True)

        valid_filenames = []
        invalid_filenames = []
        filename_elements = []  # Initialize as an empty list

        for filename, content in zip(filenames, content):
            filepath = os.path.join(upload_folder, filename)
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(content.split(",")[1]))

            # Check if the uploaded file is a valid thermal image
            error_type = get_error_type(filename, filepath)
            if error_type:
                invalid_filenames.append(filename)
            else:
                valid_filenames.append(filename)

        if valid_filenames:
            filename_elements = [html.P(f"Uploaded: {filename}") for filename in valid_filenames]
            success_message = f"Files uploaded successfully:"
            success_alert_children = [success_message]
            is_success_alert_open = True
            diagnosis_button = html.Div(
                dbc.Button(
                    "Diagnosis Page",
                    href="/diagnosis",
                    color="warning",
                    className="me-1",
                ),
                className="text-center",
            )
            session_data = valid_filenames
        else:
            success_alert_children = []
            is_success_alert_open = False
            diagnosis_button = None

        if invalid_filenames:
            error_messages = set()
            for filename in invalid_filenames:
                error_type = get_error_type(filename, filepath)
                if error_type:
                    error_messages.add(error_type)
            
            error_messages = list(error_messages)
            invalid_alert_children = [f"Invalid files: {', '.join(error_messages)}"]
            is_invalid_alert_open = True
        else:
            invalid_alert_children = []
            is_invalid_alert_open = False

        return (
            valid_filenames,
            success_alert_children,
            is_success_alert_open,
            invalid_alert_children,
            is_invalid_alert_open,
            diagnosis_button,
            valid_filenames,
            filename_elements
        )
    raise PreventUpdate


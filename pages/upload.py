import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
import os
import base64
from dash.exceptions import PreventUpdate
from PIL import Image


UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

dash.register_page(__name__)



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
                        'height': '200px',  # Five times bigger than before
                        'width': '200px',   # Five times bigger than before
                        'display': 'block',  # Remove any extra spacing
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
        "borderRadius": "10px",  # Adjust border radius for aesthetics
        "textAlign": "center",
        "margin": "20px auto",  # Center the component horizontally,
        'margin-top': '50px',
        "padding": "40px",  # Adjust padding for better spacing
        'background-color': '#F5F9FD',
    },
    multiple=True,  # Allow multiple file uploads
)


layout = html.Div([
    dbc.Row(dbc.Col(html.H1('Upload your thermal image', style={'font-family': 'Caudex, sans-serif',"textAlign": "center",}),)),
    dbc.Row(
        [
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
        ]
    ),
],
style={
        'height': '100%',
        'width': '100%',
       
    })



def save_uploaded_image(contents):
    decoded = base64.b64decode(contents)
    file_path = os.path.join(UPLOAD_FOLDER, "uploaded_image.png")  # You can modify the filename and extension
    with open(file_path, "wb") as f:
        f.write(decoded)



@callback(
    Output("upload-image", "filename"),
    Output("success-alert", "children"),
    Output("success-alert", "is_open"),
    Output("invalid-file-alert", "children"),
    Output("invalid-file-alert", "is_open"),
    Output("diagnosis-button", "children"),
    Output("session", "data"),  # Update the stored data
    Input("upload-image", "contents"),
    State("upload-image", "filename"),
    State('session', 'data')  # Get the current stored data
)
def save_uploaded_file(content, filenames, session_data):
    if content is not None:
        # Save the uploaded image to the upload folder
        upload_folder = "static/uploads/"
        os.makedirs(upload_folder, exist_ok=True)  # Create the folder if it doesn't exist
        
        valid_filenames = []
        invalid_filenames = []
        
        for filename, content in zip(filenames, content):
            # Save the uploaded file with its original filename
            filepath = os.path.join(upload_folder, filename)
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(content.split(",")[1]))
            
            # Check if the uploaded file is a valid image using PIL's Image class
            try:
                image = Image.open(filepath)
                valid_filenames.append(filename)
            except Exception as e:
                invalid_filenames.append(filename)

        if valid_filenames:
            # Notify the users about successful uploads
            success_message = f"Files uploaded successfully:"
            success_alert_children = [success_message]
            is_success_alert_open = True
            # Show the Diagnosis button
            diagnosis_button = html.Div(
                dbc.Button(
                    "Diagnosis Page",
                    href="/diagnosis",  # Change this to the actual URL of your Diagnosis page
                    color="warning",
                    className="me-1",
                ),
                className="text-center",  # Center-align contents horizontally
            )
            session_data = valid_filenames
            # print(valid_filenames)
            # session_data = {'upload_image': valid_filenames}
        else:
            success_alert_children = []
            is_success_alert_open = False
            diagnosis_button = None
        
        if invalid_filenames:
            # Notify the users about invalid files
            invalid_file_message = f"Invalid files: {', '.join(invalid_filenames)}"
            invalid_alert_children = [invalid_file_message]
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
            valid_filenames,  # Return the updated list of filenames
        )
    raise PreventUpdate



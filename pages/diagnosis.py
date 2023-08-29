import dash
from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import cv2
import plotly.express as px
from Image_Processing.image_preprocessing import *
import pandas as pd
import plotly.graph_objs as go
import base64




# Register the diagnosis page
dash.register_page(__name__)
table_header = [
    html.Thead(html.Tr([html.Th("Name"), html.Th("Value"), html.Th("Unit")]))
]


table_body = [
    html.Tbody([
        html.Tr([html.Td("Current file:"), html.Td(id="current-file"), html.Td("")]),
        html.Tr([html.Td("Normal temperature:"), html.Td(id="normal-temperature"), html.Td("C Degree")]),
        html.Tr([html.Td("Defective percentage:"), html.Td(id="defective-percentage"), html.Td("")]),
        html.Tr([html.Td("Defective counts:"), html.Td(id="defective-counts"), html.Td("")]),
        html.Tr([html.Td("Number of defective panel:"), html.Td(id="defective-pannel"), html.Td("")]),

    ])
]
table = dbc.Table(table_header + table_body, bordered=True)


table_col = dbc.Col(table, width=4)

def create_figure(image):
    # Convert the BGR image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    fig = px.imshow(rgb_image)
    fig.update_layout(
        dragmode="drawrect",
        xaxis_visible=False,
        yaxis_visible=False,
    )
    return fig

## Drop down to select image to display
dropdown = html.Div(
    [
        dcc.Dropdown(
            id="image-dropdown",
            options=[],
            value=None,
            persistence = False,
            persistence_type = 'session'
        ),
    ],
)

# Add a new dcc.Graph element for the normal temperature plot
normal_temp_graph_all = dcc.Graph(
    id="normal-temp-graph-all",
    config={'staticPlot': False},  # Allow interaction with the plot
)

def update_normal_temp_graph_all(selected_filenames):
    normal_temps = []
    image_labels = []
    
    for idx, filename in enumerate(selected_filenames):
        # Load the selected image using the filename and its path
        input_img = "static/uploads/" + filename
        selected_image = read_thermal_image(input_img)

        # Process the selected image using image_visualization function
        normal_temp, _, _ = image_visualization(selected_image, tmax=60, tmin=30)

        normal_temps.append(normal_temp)
        image_labels.append(f"Image {idx + 1}")
    
    df = pd.DataFrame({'Image': image_labels, 'Normal Temperature (°C)': normal_temps})
    
    fig = px.bar(df, x='Image', y='Normal Temperature (°C)', title='Normal Temperatures of Uploaded Images')
    return fig


switches = html.Div(
    [
        dbc.Checklist(
            options=[
                {"label": "Show Summary", "value": 1},
            ],
            value=[1],
            id="switches-input",
            switch=True,
        ),
    ], 
)

dropdown_and_switches_row = dbc.Row(
    [
        dbc.Col(dropdown, width=5),
        dbc.Col(switches, width=6),  # Set the width for switches as well
    ],
)

# Hidden graph for displaying the panel
hidden_image = html.Img(id="hidden-image", style={
                                                    "max-width": "300px",
                                                    "width": "10%",
                                                    "height": "10%",
                                                    "display": "flex",
                                                    "justify-content": "center",
                                                    "align-items": "center",
                                                    "margin": "auto",
                                                  
                                                  })


# Summary div
summary_div = html.Div(
    id="summary-div",
    children=[
        normal_temp_graph_all,
        # Add more HTML elements here for summary information
    ],
    style={"display": "none"},  # Initially hide the div
)

# Create a dcc.Link component to redirect to the diagnosis page
image_link = dcc.Link("View Image Diagnosis", id="image-link", href="",)


# -------------------------Main Diagnosis layout-----------------------------#

layout = html.Div([
    dbc.Col([
        dbc.Row(
            dbc.Col(html.H1("Get your solar diagnosed:", className="text-center")),
            style={"margin-top": "1px","font-family": "Caudex, sans-serif"
                   },  # Add a top margin
        ),  # Center-align the text

        dbc.Col([
            dbc.Col([
                dbc.Row(
                    [                         
                        dbc.Row([
                            dcc.Graph(
                                id="image-display",
                                config={'staticPlot': False},
                                clickData={'points': [{'x': None, 'y': None}]},  # Initialize with None values
                            ), 
                            
                        ],),
                        hidden_image,

                        dbc.Row([
                            dbc.Col(
                                dbc.Button(
                                    "Pre",
                                    id="pre-button",  # Assign an ID to the button
                                    color="warning",
                                    className="me-1",
                                ),
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Next",
                                    id="next-button",  # Assign an ID to the button
                                    color="warning",
                                    className="me-1",
                                ),
                                width="auto",  # Set width to auto to allow button to expand
                                style={"margin-left": "auto"},  # Move button to right corner
                            ),
                        ], justify="end"), 

                    ]),
                dbc.Row(
                    [
                        dbc.Col([
                            dropdown_and_switches_row,
                            table_col,
                            image_link
                        ]),

                        dbc.Col(summary_div),
                        # dbc.Col([
                        #     dbc.Col(summary_div)
                        # ]),
                    ],
                ),
                dbc.Col(summary_div),
            ])
        ])
    ])
])

@callback(
    Output("hidden-image", "src"),
    Input("image-display", "clickData"),
    State("image-dropdown", "value"),
)
def update_hidden_graph(click_data, selected_filename):
    encoded_image = None
    if click_data and 'points' in click_data and click_data['points']:
        x = click_data['points'][0]['x']
        y = click_data['points'][0]['y']
        if selected_filename:
            input_img = "static/uploads/" + selected_filename
            selected_image = read_thermal_image(input_img)
            # Call the necessary functions and generate the figure for the hidden graph
            # For example:
            # save_deltaT_results(input_img, f'./{"output_folder"}/', save_as_csv=True)

            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            img_sharpened = cv.filter2D(selected_image, -1, kernel)    # sharpened thermal rgb image
            # customized greyscal conversion -----------------------------------
            coefficients = [0.2, 0.25, 0.55]  # Gives blue channel all the weight
            # for standard gray conversion, coefficients = [0.114, 0.587, 0.299]
            m = np.array(coefficients).reshape((1, 3))
            img_grey = cv.transform(img_sharpened, m)

            # Binary thresholding is to remove panels from background
            # Binary thresholding Stage 1
            thresh1 = cv.threshold(img_grey, 0.95*np.mean(img_grey), 255, cv.THRESH_BINARY)[1]
            kernel_d = np.ones([2, 3], np.uint8)
            kernel_r = np.ones([3, 4], np.uint8)
            dilation = cv.dilate(~thresh1, kernel_d, iterations=2)
            erosion = cv.erode(dilation, kernel_r, iterations=1)

            contours, _ = cv.findContours(~erosion, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            filtered_contours = [cnt for cnt in contours if
                                (cv.contourArea(cnt) > 400 and cv.contourArea(cnt) < 3000)]

            # Sort filtered contours from left to right and top to bottom
            filtered_contours = sorted(filtered_contours, key=lambda c: cv.boundingRect(c)[1])

            panels_dict, defect_panels_pinpointed = save_deltaT_results(input_img, f'./{"static/output_folder"}/', save_as_csv=False)


            '''create specify directory. 
            NOTE: os.getcwd() is to find current working directory'''
            create_dir(parent_dir=os.getcwd(), output_dir="output_folder", remove_old_data=False) # DO NOT delete data again, because it's already deleted!
            save_processed_image(filtered_image_dict=defect_panels_pinpointed,
                                input_therm_img=input_img,
                                parent_dir = f'./{"output_folder/"}/')


            # If a point is clicked, display panel information
            panel_number = find_panel_number(filtered_contours, [x,y])

            print(panel_number)

            snap_number = get_snap_number(output_folder = input_img)

            panel_number_file = f"{'output_folder'}/snap({snap_number})/panel({panel_number}).png"

            print(panel_number_file)

            panel_number_file_image = cv.imread(panel_number_file)

            encoded_image = cv2.imencode('.jpg', panel_number_file_image)[1].tobytes()
    if encoded_image is not None:
        return f"data:image/jpeg;base64,{base64.b64encode(encoded_image).decode()}"
    return None



@callback(
    Output("normal-temp-graph-all", "figure"),
    Input("image-dropdown", "options"),
)
def update_normal_temp_graph_all_callback(options):
    if options:
        selected_filenames = [option["value"] for option in options]
        return update_normal_temp_graph_all(selected_filenames)
    return go.Figure()




@callback(
    Output("image-dropdown", "options"),  # Update the list of filenames
    Input('session', 'data'),  # Trigger the callback on page load by changing a dummy input value
)
def update_uploaded_filenames_list(session_data):
    options = [{"label": filename, "value": filename} for filename in session_data]
    return options




def load_default_image():
    default_image_path = "assets/DroneThermography.png"
    with open(default_image_path, "rb") as f:
        default_image_bytes = f.read()
    default_image = cv2.imdecode(np.frombuffer(default_image_bytes, np.uint8), 1)
    return default_image

show_original = True

@callback(
    Output("image-display", "figure"),
    Input("pre-button", "n_clicks"),
    Input("next-button", "n_clicks"),
    Input("image-dropdown", "value"),
)
def update_image(previous_clicks, next_clicks, selected_filename):
    global show_original
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    show_original = not show_original

    if selected_filename:
        input_img = "static/uploads/" + selected_filename
    else:
        input_img = None

    if input_img and not show_original:
        processed_thermal_image, img_panel_label, defect_panel_no_pinpoint = get_defected_panel(input_img=input_img)
        return create_figure(img_panel_label)
    elif input_img and show_original:
        selected_image = read_thermal_image(input_img)
        return create_figure(selected_image)
    else:
        if show_original:
            default_image = load_default_image()
            default_fig = create_figure(default_image)
            return default_fig
        else:
            return create_figure(load_default_image())
        


# Create a bar plot for defects
def create_defects_bar_plot(defect_counts_dict):
    defect_labels = list(defect_counts_dict.keys())
    defect_counts = list(defect_counts_dict.values())
    
    df = pd.DataFrame({
        "Defect Type": defect_labels,
        "Defect Count": defect_counts
    })
    
    fig = px.bar(df, x="Image", y="Defect Count", color="Defect Type", barmode="stack")
    return fig


@callback(
    # Output("hidden-graph", "figure"),
    Output("current-file", "children"),
    Output("normal-temperature", "children"),
    Output("defective-percentage", "children"),  # Add this line
    Output("defective-counts", "children"),       # Add this line
    Input("image-dropdown", "value"),
    Input("image-display", "clickData"),          # Add this line
)
def update_table_info(selected_filename, click_data):  # Add click_data as an argument
    x, y = None, None  # Initialize x and y to None
    normal_temp = 0.0
    if click_data and 'points' in click_data and click_data['points']:
        x = click_data['points'][0]['x']
        y = click_data['points'][0]['y']

    if selected_filename:
        # Load the selected image using the filename and its path
        input_img = "static/uploads/" + selected_filename
        selected_image = read_thermal_image(input_img)

        normal_temp, _, _ = image_visualization(selected_image, tmax=60, tmin=30)

        if x is None or y is None:
            # If no point is clicked, display overall information
            return (
                selected_filename,
                f"{normal_temp:.2f}",
                "",  
                "",     
            )
        else:
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            img_sharpened = cv.filter2D(selected_image, -1, kernel)    # sharpened thermal rgb image
            # customized greyscal conversion -----------------------------------
            coefficients = [0.2, 0.25, 0.55]  # Gives blue channel all the weight
            # for standard gray conversion, coefficients = [0.114, 0.587, 0.299]
            m = np.array(coefficients).reshape((1, 3))
            img_grey = cv.transform(img_sharpened, m)

            # Binary thresholding is to remove panels from background
            # Binary thresholding Stage 1
            thresh1 = cv.threshold(img_grey, 0.95*np.mean(img_grey), 255, cv.THRESH_BINARY)[1]
            kernel_d = np.ones([2, 3], np.uint8)
            kernel_r = np.ones([3, 4], np.uint8)
            dilation = cv.dilate(~thresh1, kernel_d, iterations=2)
            erosion = cv.erode(dilation, kernel_r, iterations=1)

            contours, _ = cv.findContours(~erosion, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            filtered_contours = [cnt for cnt in contours if
                                (cv.contourArea(cnt) > 400 and cv.contourArea(cnt) < 3000)]

            # Sort filtered contours from left to right and top to bottom
            filtered_contours = sorted(filtered_contours, key=lambda c: cv.boundingRect(c)[1])



            # If a point is clicked, display panel information
            panel_number = find_panel_number(filtered_contours, [x,y])

            _, processed_thermal_img, temp_map = image_visualization(selected_image, tmax=60, tmin=30)

            _, defect_coords = defect_location(processed_thermal_img)
            

            _, failed_panel_dict, temp_dict = get_defected_panel_labeled(selected_image,
                                                                        processed_thermal_img, temp_map,
                                                                        defect_coords)

            # Temperature difference post-processing
            panels_dict, _ = deltaT_processing(temp_dict, failed_panel_dict)
            
            # # for panel_number in list(panels_dict.keys()):
            panel_info = panels_dict[panel_number]['panel_info']

            return (
                selected_filename,
                f"{normal_temp:.2f}",
                panel_info['defects percentage'],
                panel_info['defect counts'],
            )

    return "", "", "", ""


@callback(
    Output("summary-div", "style"),  # Update the style of the summary div
    Input("switches-input", "value"),  # Listen to the switch value
)
def update_summary_visibility(switch_value):
    if 1 in switch_value:  # Check if the switch is turned on
        return {"display": "block"}  # Show the div
    return {"display": "none"}  # Hide the div


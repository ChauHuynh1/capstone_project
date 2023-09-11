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
table_header = [
    html.Thead(html.Tr([html.Th("Name"), html.Th("Value"), html.Th("Unit")]))
]


table_body = [
    html.Tbody([
        html.Tr([html.Td("Current file:"), html.Td(id="current-file"), html.Td("")]),
        html.Tr([html.Td("Normal temperature:"), html.Td(id="normal-temperature"), html.Td("Celsius")]),
        html.Tr([html.Td("Defective percentage:"), html.Td(id="defective-percentage"), html.Td("%")]),
        html.Tr([html.Td("Number of defective panel:"), html.Td(id="defective-pannel"), html.Td("")]),

    ])
]
table = dbc.Table(table_header + table_body, bordered=True)


table_col = dbc.Col(table, width=4)

def create_figure(image):
    # Convert the BGR image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    fig = px.imshow(rgb_image)
    fig.update_layout(width=800, height=600, margin=dict(l=10, r=10, b=50, t=50))
    fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
    return fig


color_bar = dcc.Graph(
    id="color-bar",
    config={'staticPlot': True},  # Make the color bar static (non-interactive)
    style={'width': '1000px', 'height': '30px'}  # Set the width and height as desired
)

def create_color_bar(image):
     # Convert the BGR image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    fig = px.imshow(rgb_image)

    # Add a dummy scatter plot with color scale to generate the color bar
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 0], mode='markers', marker=dict(showscale=True, colorscale='jet', cmin=30, cmax=60)))

    # Customize the layout of the color bar
    fig.update_layout(
        showlegend=False,  # Hide legend
        margin=dict(l=10, r=10, b=10, t=10),  # Adjust margins as needed
        xaxis=dict(showticklabels=False, showgrid=False),  # Hide x-axis labels and grid
        yaxis=dict(showticklabels=False, showgrid=False),  # Hide y-axis labels and grid
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
    style={'width': '1000px', 'height': '1000px'}  # Set the width and height as desired
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
    fig.update_layout(
            autosize=False,
            width=1000,
            height=1000,
        )

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

table_modal_header = [
    html.Thead(html.Tr([html.Th("Name"), html.Th("Value"), html.Th("Unit")]))
]

table_modal_row1 = html.Tr([html.Td("Panel temperature:"), html.Td(id="normal-temperature-modal"), html.Td("Celsius")])
table_modal_row2 = html.Tr([html.Td("Defective counts:"), html.Td(id="defective-counts-modal")])


table_modal_table_body = [html.Tbody([table_modal_row1, table_modal_row2])]

table_modal = dbc.Table(table_modal_header + table_modal_table_body, bordered=True)

deltaT_graph_all = dcc.Graph(
    id="deltaT-graph-all",
    config={'staticPlot': False},  # Allow interaction with the plot
)

defect_type_chart_all = dcc.Graph(
    id="defect-type-chart-all",
)

def update_defect_type_chart_all(selected_filenames):
    defect_types = ['Hotspot', 'Junction box', 'Connection']
    type_counts = [0, 0, 0]
    for filename in selected_filenames:
        input_img = "static/uploads/" + filename
        panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)
        for panel_number in list(panels_dict.keys()):
            dT_info = panels_dict[panel_number]['dT_info']
            for key in list(dT_info.keys()):
                type = dT_info[key][2]

                if type == 'Hotspot':
                    type_counts[0]+=1
                elif type == 'Junction box':
                    type_counts[1]+=1
                elif type == 'Connection':
                    type_counts[2]+=1
    
    data = {
        'Defect type': defect_types,
        'Counts': type_counts,
    }

    pie_chart = px.pie(data, values = 'Counts', names = 'Defect type', title='Percentages of Defect Types Detected in Uploaded Images')
    return pie_chart

@callback(
    Output("defect-type-chart-all", "figure"),
    Input("image-dropdown", "options"),
)
def update_defect_type_chart_all_callback(options):
    if options:
        selected_filenames = [option["value"] for option in options]
        return update_defect_type_chart_all(selected_filenames)
    return go.Figure()

# Add a new dcc.Graph element for the delta T trend plot
deltaT_graph_all = dcc.Graph(
    id="deltaT-graph-all",
    config={'staticPlot': False},  # Allow interaction with the plot
)

def update_deltaT_graph_all(selected_filenames):
    defect_labels = []
    deltaT_vals = []
    img_deltaTs = []

    for filename in selected_filenames:
        snap_number = get_snap_number(filename)
        input_img = "static/uploads/" + filename
        panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)
        for panel_number in list(panels_dict.keys()):
            dT_info = panels_dict[panel_number]['dT_info']
            for key in list(dT_info.keys()): 
                deltaT = dT_info[key][0]
                img_deltaTs.append(deltaT)
        maxDeltaT = np.max(img_deltaTs)
        deltaT_vals.append(maxDeltaT)
        defect_labels.append(str(snap_number))
    
    df = {
        'Defect label': defect_labels,
        'ΔT': deltaT_vals,
    }

    fig = px.bar(df, x='Defect label', y='ΔT', title='Maximum Temperature Differences of Uploaded Images')
    fig.update_layout(title_x=0.5)

    return fig

@callback(
    Output("deltaT-graph-all", "figure"),
    Input("image-dropdown", "options"),
)
def update_deltaT_graph_all_callback(options):
    if options:
        selected_filenames = [option["value"] for option in options]
        return update_deltaT_graph_all(selected_filenames)
    return go.Figure()



summary_button =dbc.Button("Summary Page", color="warning", className="me-1", href="/summary",)

# Center-align the summary button horizontally and vertically
summary_button_col = dbc.Col(
    summary_button,
    width="auto",  # Set the width to "auto" to allow the button to determine its own width
    className="justify-content-center text-center",  # Center-align both horizontally and vertically
    style={"margin-top": "1rem"},  # Add top margin as needed
)

# Summary div
summary_div = html.Div(
    id="summary-div",
    children=[
        deltaT_graph_all,
        # defect_count_by_severity_bar_chart,
        summary_button_col
        
        # Add more HTML elements here for summary information
    ],
    style={"display": "none",  
           "width": "10%",
           "height": "10%",},  # Initially hide the div
)

@callback(
    Output("modal", "is_open"),
    Output("modal-content", "children"),
    [Input("image-display", "clickData")],
    [State("image-dropdown", "value")],
    [State("modal", "is_open")],
)
def toggle_modal(click_data, selected_filename, is_modal_open):
    try:
        if click_data and 'points' in click_data and click_data['points']:
            x = click_data['points'][0]['x']
            y = click_data['points'][0]['y']

            # Your logic here to generate the cropped image
            if selected_filename:
                input_img = "static/uploads/" + selected_filename
                # Generate the cropped image based on x and y coordinates
                selected_image = read_thermal_image(input_img)

                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                img_sharpened = cv.filter2D(selected_image, -1, kernel)    # sharpened thermal RGB image
                # Customized grayscale conversion
                coefficients = [0.2, 0.25, 0.55]  # Gives the blue channel all the weight
                m = np.array(coefficients).reshape((1, 3))
                img_grey = cv.transform(img_sharpened, m)

                # Binary thresholding to remove panels from background (Stage 1)
                thresh1 = cv.threshold(img_grey, 0.95 * np.mean(img_grey), 255, cv.THRESH_BINARY)[1]
                kernel_d = np.ones([2, 3], np.uint8)
                kernel_r = np.ones([3, 4], np.uint8)
                dilation = cv.dilate(~thresh1, kernel_d, iterations=2)
                erosion = cv.erode(dilation, kernel_r, iterations=1)

                contours, _ = cv.findContours(~erosion, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

                filtered_contours = [cnt for cnt in contours if (cv.contourArea(cnt) > 400 and cv.contourArea(cnt) < 3000)]

                # Sort filtered contours from left to right and top to bottom
                filtered_contours = sorted(filtered_contours, key=lambda c: cv.boundingRect(c)[1])

                # If a point is clicked, display panel information
                panel_number = find_panel_number(filtered_contours, [x, y])

                snap_number = get_snap_number(output_folder=input_img)
                image_src = f"static/output_folder/snap({snap_number})/panel({panel_number}).png"

                # You can also create formatted HTML content for the modal
                modal_content = html.Div([
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=image_src, style={"width": "100%", "height": "100%"})),
                        ]
                    ),
                ])

                if (panel_number is not None):
                    return True, modal_content
    except Exception as e:
        pass

    # If no image is clicked or an error occurs, return False for "is_open"
    return False, None



left_arrow_image_path = "assets/left_arrow.png"
right_arrow_image_path = "assets/right_arrow.png"

pre_button = html.Img(src=left_arrow_image_path, id="pre-button", className="clickable-image", style={"width": "90px"})
next_button = html.Img(src=right_arrow_image_path, id="next-button", className="clickable-image", style={"width": "90px"})

# Define recommendations based on defect type and severity
recommendations = {
    "Hotspot": {
            "Medium": "Recommendation for medium severity hotspot.",
            "Severe": "Recommendation for severe severity hotspot."
    },
    "Junction box": {
            "Medium": "Recommendation for medium severity junction box.",
            "Severe": "Recommendation for severe severity junction box."
    },
    "Connection": {
            "Medium": "Recommendation for medium severity connection.",
            "Severe": "Recommendation for severe severity connection."
    }
 }
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
                            dbc.Col(
                                dcc.Graph(
                                    id="image-display",
                                    config={'staticPlot': False},
                                    clickData={'points': [{'x': None, 'y': None}]},  # Initialize with None values
                                ),
                                width=8,  # Adjust the width as needed
                                style={"margin-left": "90px"}
                            ),

                            dbc.Modal(
                                [
                                    dbc.ModalHeader("More information about selected row"),
                                    dbc.Row([
                                        dbc.Col([

                                            dbc.ModalBody([
                                                html.Div(id="modal-content"),
                                            ], style = {
                                                "width": "400px"
                                            }),
                                        
                                        ]),

                                        dbc.Col([
                                            table_modal,
                                             html.Div(id="defect-table"),
                                        ]),
                                        dbc.Col([
                                            html.Div(id="recommendation"),
                                        ]),

                                    ]),
                                    
                                    dbc.ModalFooter(dbc.Button("Close", id="close", className="ml-auto")),
                                    
                                ],
                                id="modal",
                                size="lg",
                            ),
                            
                        ],),

                        dbc.Row(
                            [
                                dbc.Col(pre_button, style={"margin-right": "900px", "margin-top": "-50px"}),
                                dbc.Col(next_button, width="auto", style={"margin-left": "900px", "margin-top": "-230px"}),
                            ],
                            justify="end",
                            style={"margin-top": "-300px", "margin-left": "-1px"},
                        )

                    ]),
                dbc.Row(
                    [
                        dbc.Col([
                            dropdown_and_switches_row,
                            table_col,                           

                        ], width=5),
                        dbc.Col(defect_type_chart_all, width=7),
                        dbc.Col(summary_div),
                        
                    ],
                ),
            ])
        ])
    ])
])

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
        return create_color_bar(img_panel_label)
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


# Define a function to generate the table modal content based on panel defects
def generate_table_modal_content(defects):
    # Create an empty list to store the table rows
    defect_table_rows = []

    for defect in defects:
        defect_temperature, defect_severity, defect_type = defect
        row = html.Tr([
            html.Td(f"{defect_temperature:.2f}"),
            html.Td(f"{defect_severity}"),
            html.Td(f"{defect_type}")
        ])
        defect_table_rows.append(row)


    defect_table_header = [
        html.Thead(html.Tr([html.Th("Temperature"), html.Th("Severity"), html.Th("Type")]))
    ]

    # Create the table body with the rows
    defect_modal_table_body = [html.Tbody(defect_table_rows)]

    # Create the table modal with the updated content
    defect_table_modal = dbc.Table(defect_table_header + defect_modal_table_body, bordered=True,)
    return defect_table_modal


@callback(
    Output("current-file", "children"),
    Output("normal-temperature", "children"),
    Output("normal-temperature-modal", "children"),
    Output("defective-counts-modal", "children"),
    Output("defective-percentage", "children"), 
    Output("defective-pannel", "children"),  
    Output("defect-table", "children"),
    Input("image-dropdown", "value"),
    Input("image-display", "clickData"),         
)
def update_table_info(selected_filename, click_data):  # Add click_data as an argument
    x, y = None, None  # Initialize x and y to None
    normal_temp = 0.0
    panel_info = None  # Initialize panel_info to None

    if click_data and 'points' in click_data and click_data['points']:
        x = click_data['points'][0]['x']
        y = click_data['points'][0]['y']

    if selected_filename:
        # Load the selected image using the filename and its path
        input_img = "static/uploads/" + selected_filename
        selected_image = read_thermal_image(input_img)

        normal_temp, _, _ = image_visualization(selected_image, tmax=60, tmin=30)

        processed_thermal_image, thermal_img_label, defect_panels_no_pinpoint = get_defected_panel(input_img=input_img)

        _, processed_thermal_img, temp_map = image_visualization(selected_image, tmax=60, tmin=30)

        _, defect_coords = defect_location(processed_thermal_img)

        _, failed_panel_dict, temp_dict, all_panels_dict = get_defected_panel_labeled(selected_image,
                                                                            processed_thermal_img, temp_map,
                                                                            defect_coords)
        
        # Calculate the percentage of defected panels for this image
        if len(all_panels_dict) > 0:
            defected_percentage = (len(failed_panel_dict) / len(all_panels_dict)) * 100
        else:
            defected_percentage = 0.0

        if x is None or y is None:
            # If no point is clicked, display overall information
            return (
                selected_filename,
                f"{normal_temp:.2f}",
                "", 
                "",
                f"{defected_percentage:.2f}", 
                  ", ".join(str(panel_num) for panel_num in defect_panels_no_pinpoint.keys()),  # Display the list as a comma-separated string
                ""
            )
        else:
            try:
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                img_sharpened = cv.filter2D(selected_image, -1, kernel)    # sharpened thermal rgb image
                # customized greyscal conversion -----------------------------------
                coefficients = [0.2, 0.25, 0.55]  # Gives blue channel all the weight
                # for standard gray conversion, coefficients = [0.114, 0.587, 0.299]
                m = np.array(coefficients).reshape((1, 3))
                img_grey = cv.transform(img_sharpened, m)

                # Binary thresholding is to remove panels from background
                # Binary thresholding Stage 1
                thresh1 = cv.threshold(img_grey, 0.95 * np.mean(img_grey), 255, cv.THRESH_BINARY)[1]
                kernel_d = np.ones([2, 3], np.uint8)
                kernel_r = np.ones([3, 4], np.uint8)
                dilation = cv.dilate(~thresh1, kernel_d, iterations=2)
                erosion = cv.erode(dilation, kernel_r, iterations=1)

                contours, _ = cv.findContours(~erosion, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

                filtered_contours = [cnt for cnt in contours if (cv.contourArea(cnt) > 400 and cv.contourArea(cnt) < 3000)]

                # Sort filtered contours from left to right and top to bottom
                filtered_contours = sorted(filtered_contours, key=lambda c: cv.boundingRect(c)[1])

                # If a point is clicked, display panel information
                panel_number = find_panel_number(filtered_contours, [x, y])

                

                # Temperature difference post-processing
                panels_dict, _ = deltaT_processing(temp_dict, failed_panel_dict, all_panels_dict)
                
                # # for panel_number in list(panels_dict.keys()):
                panel_info = panels_dict[panel_number]['panel_info']

                number_defect = panel_info['defect counts']
                dT_info = panels_dict[panel_number]['dT_info']

                defect_table_modal = generate_table_modal_content(dT_info.values())

                output_folder = "static/output_folder"

                panels_dict, defect_panels_pinpointed = save_deltaT_results(input_img, f'./{output_folder}/', save_as_csv=False)

                '''create specify directory. 
                NOTE: os.getcwd() is to find current working directory'''
                create_dir(parent_dir=os.getcwd(), output_dir=output_folder, remove_old_data=False) # DO NOT delete data again, because it's already deleted!
                save_processed_image(filtered_image_dict=defect_panels_pinpointed,
                                    input_therm_img=input_img,
                                    parent_dir = f'./{output_folder}/')
                # 2/ Save delta T processing results of defective panels to cvs files
                _, _ = save_deltaT_results(input_img, f'./{output_folder}/', save_as_csv=True)


            except KeyError:
                pass  # Handle KeyError gracefully

            if panel_info:
                return (
                    selected_filename,
                    f"{normal_temp:.2f}",
                    f"{panel_info['normal temperature']:.2f}",
                    panel_info['defect counts'],
                    f"{defected_percentage:.2f}",
                    ", ".join(str(panel_num) for panel_num in defect_panels_no_pinpoint.keys()),
                    defect_table_modal
                )
            
            else:
                # If panel_info is still None, return empty values
                return (selected_filename, 
                        f"{normal_temp:.2f}",
                        "", 
                        "", 
                        f"{defected_percentage:.2f}", 
                        ", ".join(str(panel_num) for panel_num in defect_panels_no_pinpoint.keys()), 
                        ""
                        )

    return "", "", "", "", "", "", ""


@callback(
    Output("summary-div", "style"),  # Update the style of the summary div
    Input("switches-input", "value"),  # Listen to the switch value
)
def update_summary_visibility(switch_value):
    if 1 in switch_value:  # Check if the switch is turned on
        return {"display": "block"}  # Show the div
    return {"display": "none"}  # Hide the div


# Update your recommendations dictionary with recommendations for different defect types and severity levels
recommendations = {
    "Hotspot": {
        "Medium": "Recommendation for medium severity hotspot.",
        "Severe": "Recommendation for severe severity hotspot."
    },
    "Junction box": {
        "Medium": "Recommendation for medium severity junction box.",
        "Severe": "Recommendation for severe severity junction box."
    },
    "Connection": {
        "Medium": "Recommendation for medium severity connection.",
        "Severe": "Recommendation for severe severity connection."
    }
}

# Modify your callback function that updates the modal content to include recommendations
@callback(
    Output("recommendation", "children"),  # Update the content of the "recommendation" div
    Input("image-dropdown", "value"),
    Input("image-display", "clickData"),
)
def update_modal_content(selected_filename, click_data):
    # ... (other code for extracting panel information)
    
    # Get the defect type and severity based on your panel_info or other data
    defect_type = "Hotspot"  # Replace with actual defect type
    defect_severity = "Medium"  # Replace with actual defect severity

    # Fetch the recommendation from the recommendations dictionary
    recommendation = recommendations.get(defect_type, {}).get(defect_severity, "")

    # Create HTML content for the recommendation
    recommendation_content = html.Div([
        html.H4("Recommendation:"),
        html.P(recommendation)
    ])

    # Return the recommendation_content to be displayed in the modal
    return recommendation_content

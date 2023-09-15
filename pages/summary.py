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

# Common function to calculate total defect count
def calculate_total_defect_count(selected_filenames):
    total_defect_count = 0

    for filename in selected_filenames:
        input_img = "static/uploads/" + filename
        panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)

        for panel_number in list(panels_dict.keys()):
            panel_info = panels_dict[panel_number]['panel_info']
            total_defect_count = panel_info['defect counts'] + total_defect_count

    return total_defect_count

# Common function to calculate defect counts by severity
def calculate_defect_counts_by_severity(selected_filenames):
    data = {
        'Image Name': [],
        'Medium Defect': [],
        'Severe Defect': []
    }

    for filename in selected_filenames:
        input_img = "static/uploads/" + filename
        panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)

        medium_defect_count = 0
        severe_defect_count = 0

        for panel_number in list(panels_dict.keys()):
            dT_info = panels_dict[panel_number]['dT_info']

            for key in list(dT_info.keys()):
                severity = dT_info[key][1]

                if severity == 'Medium':
                    medium_defect_count += 1
                elif severity == 'Severe':
                    severe_defect_count += 1

        data['Image Name'].append(filename)
        data['Medium Defect'].append(medium_defect_count)
        data['Severe Defect'].append(severe_defect_count)

    return data

# Common function to create a bar chart
def create_bar_chart(data, x_column, y_columns, title, color_discrete_map):
    df = pd.DataFrame(data)

    fig = px.bar(df, x=x_column, y=y_columns,
                 title=title,
                 color_discrete_map=color_discrete_map,
                 barmode='group')
    
    fig.update_layout(legend_title_text='Severity', legend_traceorder="normal")


    return fig

# Plot 1: Number of total defect number
total_defects_number = html.Div(
    id="total-defects-number",
    children=[
        html.H3("N.O Defects", className="text-center"),
        html.H4("0", id="defect-count", className="text-center"),  # Initialize with 0 defects
    ],
    style={
        "margin-top": "20px",
        "width": "100%",
        "height": "100%",
        "background-color": "#E97777",  # Change the color as needed
        "display": "inline-block",
        "margin-right": "5px",  # Adjust spacing
        "box-shadow": "2px 2px 5px gray", "border": "1px solid #ccc", "border-radius": "5px"
    },
)

@callback(
    Output("defect-count", "children"),
    Input("session", "data"),  # Listen to the selected filenames
)
def update_total_defect_count(session_data):
    total_defect_count = calculate_total_defect_count(session_data)
    return total_defect_count

#Plot 2: Defected Percentage:
total_defects_percentage = html.Div(
    id="total-defects-percentage",
    children=[
        html.H3("Defects %", className="text-center"),
        html.H4("0%", id="defect-percentage", className="text-center"),  # Initialize with 0% defects
    ],
    style={ 
        "margin-top": "20px",
        "width": "100%",
        "height": "100%",
        "background-color": "#FDFDBD",  # Change the color as needed
        "display": "inline-block",
        "margin-right": "5px",  # Adjust spacing
        "box-shadow": "2px 2px 5px gray", "border": "1px solid #ccc", "border-radius": "5px"
    },
)

@callback(
    Output("defect-percentage", "children"),
    Input("session", "data"),  # Listen to the selected filenames
)
def update_total_defect_percentage(session_data):
    total_defect_count = calculate_total_defect_count(session_data)
    total_panels_count = 0

    for filename in session_data:
        input_img = "static/uploads/" + filename
        panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)

        for panel_number in list(panels_dict.keys()):
            total_panels_count += 1

    if total_panels_count > 0:
        defect_percentage = (total_defect_count / total_panels_count) * 100
    else:
        defect_percentage = 0.0

    return f"{defect_percentage:.2f}%"

# Plot 3: Total Severity Percentage
total_severity_percentage = html.Div(
    id="total-severity-percentage",
    children=[
        html.H3("Severity %", className="text-center"),
        html.H4("0%", id="severity-percentage", className="text-center"),  # Initialize with 0% severity
    ],
    style={
        "margin-top": "20px",
        "width": "100%",
        "height": "100%",
        "background-color": "#B6E2A1",  # Change the color as needed
        "display": "inline-block",
        "margin-right": "5px",  # Adjust spacing
        "box-shadow": "2px 2px 5px gray", "border": "1px solid #ccc", "border-radius": "5px"
    },
)

@callback(
    Output("severity-percentage", "children"), 
    Input("session", "data"),  # Listen to the selected filenames
)
def update_total_severity_percentage(session_data):
    severe_count = 0
    total_defect_count = 0
    total_severity_percentage_percentage = 0.0

    for filename in session_data:
        input_img = "static/uploads/" + filename
        panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)

        for panel_number in list(panels_dict.keys()):
            dT_info = panels_dict[panel_number]['dT_info']
            for key in list(dT_info.keys()):
                type = dT_info[key][1]

                if type == 'Severe':
                    severe_count += 1

    for filename in session_data:
        input_img = "static/uploads/" + filename
        panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)

        for panel_number in list(panels_dict.keys()):
            panel_info = panels_dict[panel_number]['panel_info']

            total_defect_count = panel_info['defect counts'] + total_defect_count

    if total_defect_count > 0:
        total_severity_percentage_percentage = severe_count * 100 / total_defect_count
    
    return f"{total_severity_percentage_percentage:.2f}%"

# Plot 4: The type of defect has the highest count
type_of_defect_highest_count = html.Div(
    id="type-of-defect-highest-count",
    children=[
        html.H3("Type of Defect", className="text-center"),
        html.H4("", id="highest-defect-type", className="text-center"),  # Initialize with empty text
    ],
    style={
        "margin-top": "20px",
        "width": "100%",
        "height": "100%",
        "background-color": "#B1AFFF",  # Change the color as needed
        "display": "inline-block",
        "margin-right": "5px",  # Adjust spacing
        "box-shadow": "2px 2px 5px gray", "border": "1px solid #ccc", "border-radius": "5px"
    },
)

@callback(
    Output("highest-defect-type", "children"),
    Input("session", "data"),  # Listen to the selected filenames
)
def update_highest_defect_type(session_data):
    defect_counts = {}

    for filename in session_data:
        input_img = "static/uploads/" + filename
        panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)

        for panel_number in list(panels_dict.keys()):
            dT_info = panels_dict[panel_number]['dT_info']
            for key in list(dT_info.keys()):
                type = dT_info[key][2]
                defect_counts[type] = defect_counts.get(type, 0) + 1

    if defect_counts:
        highest_defect_type = max(defect_counts, key=defect_counts.get)
    else:
        highest_defect_type = "No defects found"

    return highest_defect_type

# Plot 5: Defect counts by severity
defect_counts_by_severity = dcc.Graph(
    id="defect-counts-by-severity",
    config={"displayModeBar": False},  # Hide the mode bar for this plot
    style={"box-shadow": "2px 2px 5px gray", "border": "1px solid #ccc", "border-radius": "5px"},

)

@callback(
    Output("defect-counts-by-severity", "figure"),
    Input("session", "data"),  # Listen to the selected filenames
)
def update_defect_counts_by_severity(session_data):
    data = calculate_defect_counts_by_severity(session_data)

    color_discrete_map = {'Medium Defect': 'blue', 'Severe Defect': 'red'}

    fig = create_bar_chart(data, 'Image Name', ['Medium Defect', 'Severe Defect'],
                           'Defect Counts by Severity for Each Image', color_discrete_map)
    
    fig.update_xaxes(title_text='Image Name')
    fig.update_yaxes(title_text='Defect Count') 

    fig.update_layout(title_x=0.5)


    return fig

#Plot 6:
defect_count_by_image_name = dcc.Graph(
    id="defect-count-by-image-name",
    config={"displayModeBar": False},  # Hide the mode bar for this plot
    style={"box-shadow": "2px 2px 5px gray", "border": "1px solid #ccc", "border-radius": "5px"},

)

@callback(
    Output("defect-count-by-image-name", "figure"),
    Input("session", "data"),  # Listen to the selected filenames
)
def update_defect_count_by_image_name(session_data):
    data = {
        'Image Name': [],
        'Hotspot Count': [],
        'Connection Count': [],
        'Junction Box Count': []
    }

    for filename in session_data:
        input_img = "static/uploads/" + filename
        panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)

        hotspot_count = 0
        connection_count = 0
        junction_box_count = 0

        for panel_number in list(panels_dict.keys()):
            dT_info = panels_dict[panel_number]['dT_info']

            for key in list(dT_info.keys()):
                defect_type = dT_info[key][2]

                if defect_type == 'Hotspot':
                    hotspot_count += 1
                elif defect_type == 'Connection':
                    connection_count += 1
                elif defect_type == 'Junction box':
                    junction_box_count += 1

        data['Image Name'].append(filename)
        data['Hotspot Count'].append(hotspot_count)
        data['Connection Count'].append(connection_count)
        data['Junction Box Count'].append(junction_box_count)

    df = pd.DataFrame(data)
    fig = px.bar(df, x='Image Name', y=['Hotspot Count', 'Connection Count', 'Junction Box Count'],
                 title='Defect Count by Image Name and Defect Type',
                 labels={'Image Name': 'Image Name', 'value': 'Defect Count', 'variable': 'Defect Type'},
                 color_discrete_map={'Hotspot Count': 'blue', 'Connection Count': 'red', 'Junction Box Count': 'green'})
    
    fig.update_layout(title_x=0.5)

    return fig

#Plot 7:
total_severity_level_percentage = dcc.Graph(
    id="total-severity-level-percentage",
    config={"displayModeBar": False},  # Hide the mode bar for this plot
)
total_severity_level_percentage = dcc.Graph(
    id="total-severity-level-percentage",
    config={"displayModeBar": False},  # Hide the mode bar for this plot
    style={"box-shadow": "2px 2px 5px gray", "border": "1px solid #ccc", "border-radius": "5px"},
)


@callback(
    Output("total-severity-level-percentage", "figure"),
    Input("session", "data"),  # Listen to the selected filenames
)
def update_total_severity_level_percentage(session_data):
    severe_count = 0
    medium_count = 0

    for filename in session_data:
        input_img = "static/uploads/" + filename
        panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)

        for panel_number in list(panels_dict.keys()):
            dT_info = panels_dict[panel_number]['dT_info']
            for key in list(dT_info.keys()):
                severity = dT_info[key][1]

                if severity == 'Severe':
                    severe_count += 1
                elif severity == 'Medium':
                    medium_count += 1

    data = [go.Pie(labels=['Severe', 'Medium'], values=[severe_count, medium_count], hole=0.3)]

    layout = go.Layout(title='Severity Level Distribution', height=420, width=420)  # Adjust height and width here
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(title_x=0.5)


    return fig


# Common function to calculate defect counts by type
def calculate_defect_counts_by_type(selected_filenames):
    defect_counts = {}

    for filename in selected_filenames:
        input_img = "static/uploads/" + filename
        panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)

        for panel_number in list(panels_dict.keys()):
            dT_info = panels_dict[panel_number]['dT_info']
            for key in list(dT_info.keys()):
                defect_type = dT_info[key][2]
                defect_counts[defect_type] = defect_counts.get(defect_type, 0) + 1

    return defect_counts

# Plot 7: Total Defect Type Percentage (Pie Chart)
total_defect_type_percentage = dcc.Graph(
    id="total-defect-type-percentage",
    config={"displayModeBar": False},  # Hide the mode bar for this plot
    style={"box-shadow": "2px 2px 5px gray", "border": "1px solid #ccc", "border-radius": "5px"},

    
)

@callback(
    Output("total-defect-type-percentage", "figure"),
    Input("session", "data"),  # Listen to the selected filenames
)
def update_total_defect_type_percentage(session_data):
    defect_counts = calculate_defect_counts_by_type(session_data)

    labels = list(defect_counts.keys())
    values = list(defect_counts.values())

    data = [go.Pie(labels=labels, values=values, hole=0.3)]

    layout = go.Layout(title='Defect Type Distribution', height=420, width=420)  # Adjust height and width here
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(title_x=0.5)


    return fig

#Plot 8:
# Add a div element to hold the highest severity panel bar chart
highest_severity_panel_chart = dcc.Graph(
    id="highest-severity-panel-chart",
    config={"displayModeBar": False},  # Hide the mode bar for this plot
    style={"box-shadow": "2px 2px 5px gray", "border": "1px solid #ccc", "border-radius": "5px"},

)

# Function to calculate the total number of severe defects for each panel
def calculate_severe_defect_counts(selected_filenames):
    severe_defect_counts = {}

    for filename in selected_filenames:
        input_img = "static/uploads/" + filename
        panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)

        for panel_number in list(panels_dict.keys()):
            dT_info = panels_dict[panel_number]['dT_info']

            severe_count = sum(1 for info in dT_info.values() if info[1] == 'Severe')

            # Use a tuple of (image_name, panel_number) as the key
            key = (filename, panel_number)

            if key not in severe_defect_counts:
                severe_defect_counts[key] = severe_count
            else:
                severe_defect_counts[key] += severe_count

    return severe_defect_counts


defect_type_colors = {
    'Hotspot': 'red',
    'Connection': 'blue',
    'Junction box': 'green',
    # Add more colors and defect types as needed
}

# Callback to update the top 3 highest severity panels bar chart
@callback(
    Output("highest-severity-panel-chart", "figure"),
    Input("session", "data"),  # Listen to the selected filenames
)
def update_top_severity_panels_chart(session_data):
    if session_data:
        severe_defect_counts = calculate_severe_defect_counts(session_data)

        if severe_defect_counts:
            # Find the top 3 panels with the highest severe defect counts
            top_severity_panels = sorted(severe_defect_counts.items(), key=lambda x: x[1], reverse=True)[:3]

            # Extract image names and panel numbers, and create labels and colors based on defect type
            labels = [f"Panel {panel_number} {image_name}" for (image_name, panel_number), _ in top_severity_panels]
            panel_numbers, defect_counts = zip(*top_severity_panels)

            # Initialize defect type counters for each defect type
            hotspot_count = 0
            junctionBox_count = 0
            connection_count = 0

            for (image_name, panel_number), _ in top_severity_panels:
                input_img = "static/uploads/" + image_name
                panels_dict, _ = save_deltaT_results(input_img, r'.\static\output_folder', save_as_csv=False)
                dT_info = panels_dict[panel_number]['dT_info']

                # Iterate through defect info and count defect types
                for info in dT_info.values():
                    if info[1] == 'Severe':
                        defect_type = info[2]

                        if defect_type == 'Hotspot':
                            hotspot_count += 1
                        elif defect_type == 'Junction Box':
                            junctionBox_count += 1
                        elif defect_type == 'Connection':
                            connection_count += 1

            # Create a color list based on defect types
            defect_types = ['Hotspot', 'Junction Box', 'Connection']
            colors = [defect_type_colors.get(defect_type, 'gray') for defect_type in defect_types]

            data = {'Label': labels, 'Severe Defect Count': defect_counts, 'Defect Type': defect_types}

            df = pd.DataFrame(data)

            fig = px.bar(df, x='Label', y='Severe Defect Count',
                         title='Top 3 Panels with Highest Severe Defect Counts by Defect Type',
                         labels={'Label': 'Panel', 'Severe Defect Count': 'Severe Defect Count'},
                         color='Defect Type', color_discrete_map=defect_type_colors)
            fig.update_layout(title_x=0.5)

            return fig

    return go.Figure()  # Return an empty figure if there is no data



# Define the width of each plot
plot1_width = 3
plot2_width = 3
plot3_width = 3
plot4_width = 3
plot5_width = 12


diagnosis_button =dbc.Button([
                        html.I(className="fas fa-search"),  # Add the FontAwesome icon here (e.g., search icon)
                        " Diagnosis Page"
                    ], color="warning", className="me-1", href="/diagnosis",  style={'width': '30%', 'font-family': 'Teko, sans-serif',
                                                            'font-size': '20px'}),

# -------------------------Main Summary layout-----------------------------#
layout = html.Div(
    [
        dbc.Row(dbc.Col(html.H1('Get your solar diagnosed:', style={'font-family': 'Teko, sans-serif',"textAlign": "center",'font-size': '50px'}),)),
        dbc.Row(
            [
                dbc.Col(total_defects_number, width=plot1_width),
                dbc.Col(total_defects_percentage, width=plot2_width),
                dbc.Col(total_severity_percentage, width=plot3_width),
                dbc.Col(type_of_defect_highest_count, width=plot4_width),
                
            ],
            # justify="start",  # Adjust the justify property to move columns to the left,
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(total_severity_level_percentage, width=6),
                dbc.Col(total_defect_type_percentage, width=6),
            ],
            # justify="start",  # Adjust the justify property to move columns to the left
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(defect_counts_by_severity),

            ],
            # justify="start",  # Adjust the justify property to move columns to the left
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(highest_severity_panel_chart),

            ],
            # justify="start",  # Adjust the justify property to move columns to the left
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(diagnosis_button, className="d-flex justify-content-center"),  # Center-align the button
            ],
        ),

    ],    

)

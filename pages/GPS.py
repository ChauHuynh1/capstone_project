import dash
from dash import html, dcc, callback, Input, Output, State  # Import dcc here
import dash_html_components as html
import dash_leaflet as dl
import dash_bootstrap_components as dbc
import dash_leaflet.express as dlx
from urllib.parse import urlparse, parse_qs

from Image_Processing.image_preprocessing import *

dash.register_page(__name__)

# Read the coordinates from the file
coordinates = []
with open('preproc/GPSdata.txt', 'r') as file:
    for line in file:
        parts = line.split()
        if len(parts) >= 3:
            latitude = float(parts[1])
            longitude = float(parts[2])
            image_name = parts[0]
            coordinates.append((latitude, longitude, image_name))

img_style = {
    "width": "150px",   # Set the desired width
    "height": "auto",   # Maintain aspect ratio
}

# Calculate the center coordinates based on the average of all coordinates
center_latitude = sum(lat for lat, _, _ in coordinates) / len(coordinates)
center_longitude = sum(lon for _, lon, _ in coordinates) / len(coordinates)
zoom = 100  # Adjust this value as needed

def calculate_defected_percentage(image_file):
    try:
        image_file_path ="static/data/Thermal/" + image_file
        selected_image = read_thermal_image(image_file_path)

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

        return defected_percentage
    

    except Exception as e:
        print(f"Error processing {image_file}: {str(e)}")
        return None


# Define a custom colorscale
colorscale = [
    (20, "green"),   # Lower defected percentage (0%) corresponds to green
    (50, "yellow"),  # 50% defected percentage corresponds to yellow
    (100, "red")     # Higher defected percentage (100%) corresponds to red
]

# Calculate marker colors based on defected percentages
def calculate_marker_color(defected_percentage):
    if defected_percentage is not None:
        for threshold, color in colorscale:
            if defected_percentage <= threshold:
                return color
        return "red"  # Default to red for values exceeding the colorscale
    else:
        return "gray"  # Default to gray for None values


classes = [20, 50, 100]
color_scale = ['green', 'yellow', 'red']
ctg = ["{}% defected".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{} % defected".format(classes[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=color_scale, width=300, height=30, position="bottomleft")

# Create a LayerGroup for the colorbar
colorbar_layer = dl.LayerGroup([colorbar])

markers = []
link_elements = []
for lat, lon, image_name in coordinates:
    defected_percentage = calculate_defected_percentage(image_name)
    
    # Calculate marker color based on defected percentage
    marker_color = calculate_marker_color(defected_percentage)
    link_elements = image_name

    # Format the defected percentage with two digits after the decimal point
    defected_percentage_formatted = "{:.2f}%".format(defected_percentage) if defected_percentage is not None else "N/A"

    marker = dl.Marker(
        position=(lat, lon),
        icon={
            "iconUrl": f"assets/{marker_color}_mark.png",
            "iconSize": [40, 40],
        },
        children=[
            dl.Popup([
                html.Img(src=f'static/data/Thermal/{image_name}', style=img_style),
                html.P(image_name),
                dcc.Link("Diagnose Image", href=f"/diagnosis?image={image_name}", id=image_name),
                html.P(f"Defected Percentage: {defected_percentage_formatted}"),
            ]),
        ],
        id={'type': 'marker', 'image_name': image_name},
    )
    markers.append(marker)


# -------------------------Main GPS layout-----------------------------#
layout = html.Div(
    [
        dbc.Row(dbc.Col(html.H1('Locate the defected solar panel:', style={'font-family': 'Teko, sans-serif',"textAlign": "center",'font-size': '50px'}),)),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dl.Map(
                            [dl.TileLayer()] + markers + [colorbar_layer],  # Add the markers and colorbar_layer to the map
                            center=(center_latitude, center_longitude),  # Set the initial center
                            zoom=zoom,  # Set the initial zoom level
                            style={'width': '970px', 'maxWidth': '230%', 'height': '650px', 'margin': '0 auto', 'margin-left': '2px',},
                        ),
                    ],
                    xs=8, sm=8, md=8, lg=100, xl=100
                ),
            ]
        ),
    ]
)



@callback(
    Output('gps_image', 'data'),  # Update the data property of the dcc.Store component
    Input('image_name_link', 'href'),  # Listen to the href property of the dcc.Link component
)
def update_store_data(image_href):
    # Here, you can fetch and return the data you want to store in the dcc.Store
    # For example, you can return a list of data or a dictionary
    data_to_store = []

    # Parse the URL
    parsed_url = urlparse(image_href)
    print(image_href)

    # Extract the image filename from the query parameters
    query_params = parse_qs(parsed_url.query)
    image_filename = query_params.get('image', [])[0] if 'image' in query_params else None



    # Print the extracted image filename

    data_to_store.append(image_filename)

    # Fetch your data based on the image_href and populate data_to_store

    return data_to_store
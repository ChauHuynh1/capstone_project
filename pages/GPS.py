import dash
from dash import html, dcc, callback, Input, Output
from dash.dependencies import Input, Output
import os
import dash_html_components as html
import dash_leaflet as dl
from flask import url_for
import dash_bootstrap_components as dbc


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

# Create a list of dl.Marker components using the coordinates
markers = [
    dl.Marker(
        position=(lat, lon),
        children=[
            dl.Popup([html.Img(src=f'static/data/Thermal/{image_name}', style=img_style), html.P(image_name)]),
        ],
    )
    for lat, lon, image_name in coordinates
]

# Calculate the center and zoom level for the map
center_latitude = sum(lat for lat, _, _ in coordinates) / len(coordinates)
center_longitude = sum(lon for _, lon, _ in coordinates) / len(coordinates)
zoom = 10  # Adjust this value as needed


layout = html.Div(
    [
        dbc.Row(dbc.Col(html.H1('This is our GPS page'))),
        dbc.Col(
            [
                dl.Map(
                    [dl.TileLayer()] + markers,  # Add the markers to the map
                    center=(center_latitude, center_longitude),  # Set the initial center
                    zoom=zoom,  # Set the initial zoom level

                    style={'width': '250%', 'maxWidth': '230%', 'height': '500px', 'margin': '0 auto', 'margin-left': '-70px',},
                ),
            ], xs=8, sm=8, md=8, lg=100, xl=100
        ),
    ]
)


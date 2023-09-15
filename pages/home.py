import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State  # Import dcc here

dash.register_page(__name__, path='/')

layout = html.Div([
    dbc.Row(
        [
            # dbc.Col(html.H1('Aerial IRT - Solar Panel Prognosis', style={'font-size': '50px'}), className="text-center"),  # Increase the font size here
            html.Img(
                    src="assets/landing_page.png",
                    style={
                        'height': '20%',
                        'width': '30%',
                        'display': 'block',
                        "fill": "currentColor",
                    },
                ),
        ],
        justify="center",  # Horizontally center the row content
        align="center",  # Vertically center the row content
        # Adjust the height for vertical centering
        style={
            'color': 'white',
            'font-family': 'Teko, sans-serif',
        },
    ),
    dbc.Row(
        [
            dbc.Col([

                html.Br(),

                dbc.Row(dbc.Button(
                                    [html.I(className="fas fa-upload"), " Upload"],  # Add an icon using html.I
                                    color="warning",
                                    className="me-1",
                                    href="/upload",
                                    style={'width': '30%', 'font-family': 'Teko, sans-serif',
                                            'font-size': '23px'}
                                ), justify="center",),
                html.Br(),
                dbc.Row(dbc.Button(
                            [html.I(className="fas fa-map-marker-alt"), " GPS"],  # Add an icon using html.I
                            color="warning",
                            className="me-1",
                            href="/gps",
                            style={'width': '30%', 'font-family': 'Teko, sans-serif',
                                            'font-size': '23px'}
                        ), justify="center",),

            ], 
                # justify="center",  # Horizontally center the row content
                # align="center", 
            ),
        ],
        justify="center",  # Horizontally center the row content
        align="center",  # Vertically center the row content
    ),
]
)

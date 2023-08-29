import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State  # Import dcc here

dash.register_page(__name__, path='/')

layout = html.Div([
    dbc.Row(
        [
            dbc.Col(html.H1('Aerial IRT - Solar Panel Prognosis'), className="text-center"),  # Center-align the heading
        ],
        justify="center",  # Horizontally center the row content
        align="center",  # Vertically center the row content
        # Adjust the height for vertical centering
        style={
            'color': 'white',
            'font-family': 'Caudex, sans-serif',
        },
    ),
    dbc.Row(
        [
            dbc.Button("Upload", color="warning", className="me-1", href="/upload",style={'width': '50%'}),
            html.Br(),
            html.Br(),
            dbc.Button("GPS", color="warning", className="me-1", href="/gps",style={'width': '50%'}),
            html.Br(),
        ],
        justify="center",  # Horizontally center the row content
        align="center",  # Vertically center the row content
    ),
]
)

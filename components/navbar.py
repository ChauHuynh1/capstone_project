import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, State


def create_navbar():
    navbar = dbc.Row(
        dbc.Row([
            dbc.Col(html.H1("Helios Negotiator", style={
                'width': '100%',
                'height': '40%',
                'float': 'left',
                'margin': '13px 0px 10px 0',  # Add margin for spacing
            })),
        ], style={
            'width': '100%',  # Ensure the row spans the entire width of the page
            'background-color': '#11009E',  # Set your desired background color here
        })
    )
    return navbar
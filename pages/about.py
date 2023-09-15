import dash
from dash import html, dcc, callback, Input, Output
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


dash.register_page(__name__)

intro_text = html.Div(
    [
        dbc.Row(dbc.Col(html.H1('About our group project', style={'font-family': 'Teko, sans-serif', "textAlign": "center", 'font-size': '50px'}),)),
        html.P(
            "While solar panels offer a reliable energy source, their efficiency and performance can be compromised by various factors over time. For instance, dust accumulation, microcracks, corrosion, hotspots, and degradation due to environmental conditions are among the challenges that can diminish energy output and overall system effectiveness. Traditional manual inspection techniques, involving personnel traversing large arrays, are not only time-consuming but also limited in their ability to detect these subtle defects comprehensively.",
            className="text-center",
        ),
        html.P(
            "On the contrary, the use of drones for solar panel inspection is a promising new technology that has the potential to revolutionize the way solar panels are inspected. Drones can be used to inspect solar panels quickly and safely, reducing the risk of injury to workers and increasing the productivity of the inspection process.",
            className="text-center",
        ),
        html.P(
            "The project will use a drone equipped with a thermal camera to inspect solar panels for defects and performance problems. The thermal camera will allow the drone to detect areas of the solar panels that are hotter or colder than others, which can indicate problems such as hot spots, shading, or damaged cells.",
            className="text-center",
        ),
    ],
    style={"margin-top": "-20px", "font-family": "Caudex, sans-serif"},
)

layout = html.Div(
    [
        dbc.Row(
            dbc.Row(dbc.Col(html.H1('Welcome to our group project', style={'font-family': 'Teko, sans-serif', "textAlign": "center", 'font-size': '50px'}),)),
            style={"margin-top": "1px", "font-family": "Caudex, sans-serif"},  # Add a top margin
        ),  # Center-align the text,
        html.Hr(),
        dbc.Row(
            [
                intro_text
            ],
            justify="center",  # Horizontally center-align the row content
            align="center",  # Vertically center-align the row content
            style={"height": "40vh"},  # Set a fixed height to vertically center content
        ),

        html.Hr(),

        dbc.Row(
            [
                dbc.Row(
                    dbc.Row(dbc.Col(html.H1('Our Team Members', style={'font-family': 'Teko, sans-serif', "textAlign": "center", 'font-size': '50px'}),)),

                    style={"margin-top": "1px", "font-family": "Caudex, sans-serif"},  # Add a top margin
                ),
            ],
            justify="center",  # Horizontally center-align the row content
            align="center",  # Vertically center-align the row content
            # style={"height": "80vh"},  # Set a fixed height to vertically center content
        ),

        dbc.Row(
            [
                dbc.Col(
                    html.Img(src="assets/272269612_2758719031089935_4692998497357016630_n.jpg", alt="Image 1", style={"width": "100%", "height": "100%"}),
                    width=6,
                ),
                dbc.Col(
                    html.Img(src="assets/tung.jpeg", alt="Image 2", style={"width": "100%", "height": "100%"}),
                    width=6,
                ),
            ],
            justify="center",
            style={"margin-top": "20px"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Img(src="assets/Phuc.jpeg", alt="Image 1", style={"width": "100%", "height": "100%"}),
                    width=6,
                ),
                dbc.Col(
                    html.Img(src="assets/Tan.jpg", alt="Image 2", style={"width": "100%", "height": "100%"}),
                    width=6,
                ),
            ],
            justify="center",
            style={"margin-top": "20px"},
        ),
    ]
)


import dash
from dash import html, dcc, callback, Input, Output
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


dash.register_page(__name__)

intro_text = html.Div(
    [
        html.H2("ABOUT OUR PROJECT", className="text-center"),
        html.P(
            "Discover a brighter future with our solar panel defect detection project. "
            "In our quest to harness clean energy efficiently, we're focusing on identifying defects in solar panels. "
            "These imperfections, often invisible to the naked eye, can undermine energy production.",
            className="text-center",
        ),
        html.P(
            "Our project employs cutting-edge technology, including image processing and machine learning, to analyze "
            "solar panel images. By pinpointing defects like cracks and hotspots, we're ensuring solar panels operate "
            "at their best. This not only maximizes energy output but also minimizes maintenance costs.",
            className="text-center",
        ),
        html.P(
            "Join us in advancing sustainable energy by making solar panels more reliable and effective. "
            "Embrace innovation as we pave the way for greener tomorrows.",
            className="text-center",
        ),
    ],
    style={"margin-top": "-20px", "font-family": "Caudex, sans-serif"},
)


layout = html.Div(
    [
        dbc.Row(
            dbc.Col(html.H1("Welcome to our group project", className="text-center")),
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
                    dbc.Col(html.H1("Our team", className="text-center")),
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
                    html.Img(src="assets/272269612_2758719031089935_4692998497357016630_n.jpg", alt="Image 1", style={"width": "100%"}),
                    width=6,
                ),
                dbc.Col(
                    html.Img(src="assets/272269612_2758719031089935_4692998497357016630_n.jpg", alt="Image 2", style={"width": "100%"}),
                    width=6,
                ),
            ],
            justify="center",
            style={"margin-top": "20px"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Img(src="assets/272269612_2758719031089935_4692998497357016630_n.jpg", alt="Image 1", style={"width": "100%"}),
                    width=6,
                ),
                dbc.Col(
                    html.Img(src="assets/272269612_2758719031089935_4692998497357016630_n.jpg", alt="Image 2", style={"width": "100%"}),
                    width=6,
                ),
            ],
            justify="center",
            style={"margin-top": "20px"},
        ),
    ]
)


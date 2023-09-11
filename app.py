import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


from components.navbar import *

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://fonts.googleapis.com/css?family=Caudex&display=swap'], use_pages=True, suppress_callback_exceptions=True)


# sidebar header include the rmit loogo and 
sidebar_header = dbc.Row(
    [
        dbc.Col(
            html.Img(
                src='assets/rmitLogo_white.png',
                className="img-fluid",  # Use Bootstrap's responsive image class
                style={'margin-right': '20px'}
            ),
        ),
        dbc.Col(
            html.Button(
                # use the Bootstrap navbar-toggler classes to style the toggle
                className="navbar-toggler",
                # the navbar-toggler classes don't set color, so we do it here
                style={
                    "color": "rgba(0,0,0,.5)",
                    "border-color": "rgba(0,0,0,.1)",
                },
                id="toggle",
            ),
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)


sidebar = html.Div(
    [
        sidebar_header,
        html.Div(
            [
                html.Hr(),
                html.H2('Engineering Capstone project', style={'color': '#FFFFFF', "font-family": "Caudex, sans-serif"}),
                html.Hr(),
                html.H4('Group name: Helios Negotiator', style={'color': '#FFFFFF', "font-family": "Caudex, sans-serif"}),

            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [                    
                    dbc.Button("Home", color="warning", className="me-1", href="/",),
                    html.Br(),
                    dbc.Button("Upload", color="warning", className="me-1", href="/upload",),
                    html.Br(),
                    dbc.Button("GPS", color="warning", className="me-1", href="/gps",),
                    html.Br(),
                    dbc.Button("About", color="warning", className="me-1", href="/about",),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse", 
        ),
    ],
    id="sidebar",
    style={
            'background-color': '#06367A',  
           'color': 'white'} 
)

app.layout = html.Div(
    [
        dcc.Store(id='session', storage_type='session'),
        dcc.Location(id='url'),
        dbc.Row(
            [
                dbc.Col(
                    sidebar,
                    width={"size": 3, "order": 1, "offset": 0},
                    xs=10, sm=10, md=10, lg=3
                ),  # Width of the sidebar

                # Inside your app.layout function
                dbc.Col(
                    html.Div(
                        id='content-wrapper',
                        children=[
                            dash.page_container,
                        ],
                        style={
                            'background-color': 'white',
                            'height': '100%',
                            'margin': 'auto',
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'box-shadow': '0px 0px 10px rgba(0, 0, 0, 0.1)',
                            'padding': '0px',
                            'width': '110%',  # Set the initial width to 100%
                            'margin-left': '40px',  # Adjust the left margin as needed
                        }
                    ),
                    width={"size": 12, "order": 2, "offset": 0},  # Adjust the size and order as needed
                    xs=13, sm=13, md=13, lg=8,  # Smaller width on larger screens (adjust as needed)
                    style={
                        'background-color': 'white',
                        'height': '50%',
                        'margin': 'auto',
                        'display': 'flex',
                        'align-items': 'center',
                        'justify-content': 'center',
                        'box-shadow': '0px 0px 10px rgba(0, 0, 0, 0.1)',
                        'padding': '0px',
                    }
                )



            ],
            style={
                # 'background-image': 'url("assets/DroneThermography.png")',
                'background-repeat': 'no-repeat',
                'background-color': '#ADC4CE',
                
                'background-size': 'cover',
                'height': '100vh',
            }
        ),
    ]
)

@app.callback(
    Output("collapse", "is_open"),
    [Input("toggle", "n_clicks")],  # Corrected ID here
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('content-wrapper', 'style'),
    Input('url', 'pathname')  # Use the current page pathname
)
def update_content_style(pathname):
    if pathname == '/':  # Check if the current page is the home page
        return {
            'background-color': '#11009E',  # Replace with the desired background color
            'height': '100%',
            'width': '100%',
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'center',
        }
    elif pathname == '/upload' or pathname == '/diagnosis' or pathname == '/about' or pathname == '/gps' or pathname == '/summary': 
        return {
                'background-color': 'white',
                'height': '180%',
                'width': '180%',
                'margin': '10px auto',  # Add top margin and center horizontally
                'display': 'flex',
                'align-items': 'flex-start',  # Align content to the top
                'justify-content': 'center',
                'overflowY': 'scroll',
                'padding': '20px',
                # 'margin-top': '100px',
        }
    else:
        return {
            'background-color': 'white',
            'height': '50%',
            'width': '50%',
            'margin': 'auto',
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'center',
            'box-shadow': '0px 0px 10px rgba(0, 0, 0, 0.1)',
            'padding': '20px'
        }



if __name__ == '__main__':
    app.run_server(debug=True)
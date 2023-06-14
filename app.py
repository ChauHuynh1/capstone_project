from dash import Dash
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc 
import dash_html_components as html
from dash.dependencies import Input, Output, State
from functions import file_operations
from functions.upload import upload_component


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

download_button = html.Div(
    dbc.Button(
        "Download Files",
        id="btn-download",
        outline=True,
        color="primary",
        disabled=True,
        className="me-1",
    ),
    style={"display": "flex", "justify-content": "center", "margin-top": "20px"},
)

# Left navigation bar
left_navbar = html.Div(
    className='four columns div-user-controls',
    style={
        'backgroundColor': 'black',
        'color': 'white',
        'padding': '20px',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'flex-start',
        'height': '100vh',
    },
    children=[
        html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
            },
            children=[
                html.Img(
                    src='/assets/rmitLogo.jpg',
                    style={'width': '200px', 'height': 'auto', 'margin-top': '10px'}
                ),
                html.H2('Engineering Capstone project', style={'color': 'white'}),
                html.H3('Group name: Helios Negotiator'),
                html.Br(),
            ]
        ),
        
        # Add tabs to the left navbar
        dbc.Tabs(
            [
                dbc.Tab(label="Project Description", tab_id="tab-1", labelClassName="nav-link", activeLabelClassName="active"),
                dbc.Tab(label="Project Team", tab_id="tab-2", labelClassName="nav-link", activeLabelClassName="active"),
            ],
            id="tabs",
            className="nav nav-pills mt-4",
            active_tab="tab-1",
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
        
        # Content for each tab
        html.Div(id="tab-content"),
    ]
)

tab_1 = html.Div(
    children=[
        html.Div(
            [
                html.P(
                    "This project proposal aims to detect and reduce losses in solar panels caused by damaged cells. "
                    "By utilizing UAV-based thermal imaging processing, we can quickly spot and identify faulty cells, "
                    "streamlining the maintenance process. Through data augmentation and machine learning algorithms, "
                    "subsequent images can be automatically analyzed for faults, significantly reducing downtime "
                    "and increasing overall efficiency for solar power generation.",
                    style={'text-align': 'justify'}
                )
            ],
            style={
                'display': 'flex',
                'flex-direction': 'column',
                'justify-content': 'center',
                'align-items': 'center',
                'height': '400px',
                'width': '300px',
                'margin': 'auto',
            },
        )
    ],
    style={'height': '100vh'},
)

tab_2 = html.Div(
    children=[
        html.Div(
            [
                html.H5('Student name: Nguyen Dang Huynh Chau (s3777214)'),
                html.H5('Student name: To Vu Phuc (s3758272)'),
                html.H5('Student name: Nguyen Nhat Tan (s3818559)'),
                html.H5('Student name: Tong Son Tung (s3818153)'),
            ],
            style={
                'display': 'flex',
                'flex-direction': 'column',
                'justify-content': 'center',
                'align-items': 'center',
                'height': '300px',
                'width': '300px',
                'margin': 'auto',
            },
        )
    ],
    style={'height': '100vh'},
)



# Callback to update the content based on the selected tab
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    if active_tab == "tab-1":
        return tab_1
    elif active_tab == "tab-2":
        return tab_2
    else:
        return html.P("No content available for this tab.")



app.layout = html.Div(
    style={'display': 'flex'},
    children=[
        left_navbar,
        html.Div(
            className='content',
            style={'flex': '1', 'backgroundColor': 'white', 'padding': '20px'},
            children=[
                html.H2("Upload your image:", style={'textAlign': 'center'}),
                upload_component,  # Use the upload_component from functions.upload
                html.H2("File List"),
                html.Ul(id="file-list"),
                download_button,
                dcc.Location(id="url", refresh=False),
                dcc.Download(id="download"),
            ]
        )
    ]
)



@app.callback(
    Output("file-list", "children"),
    Output("btn-download", "disabled"),
    Input("upload-data", "filename"),
    State("upload-data", "contents"),
)
def update_file_list(filenames, contents):
    if filenames is None or contents is None:
        raise dash.exceptions.PreventUpdate

    file_list_items = file_operations.update_file_list(filenames, contents)
    return file_list_items, False


@app.callback(
    Output("download", "data"),
    Input("btn-download", "n_clicks"),
    State("file-list", "children"),
)
def download_files(n_clicks, file_list_items):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    filenames = [item["props"]["children"] for item in file_list_items]
    return file_operations.download_files(filenames)

# Add callback for tab selection
@app.callback(
    Output("tab-1", "active"),
    Output("tab-2", "active"),
    Input("url", "pathname")
)
def toggle_tab(pathname):
    if pathname == "/tab-1":
        return True, False
    elif pathname == "/tab-2":
        return False, True
    return False, False


if __name__ == "__main__":
    app.css.append_css({"external_url": "/assets/styles.css"})
    app.run_server(debug=True)

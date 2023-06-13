from dash import Dash
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc 
import dash_html_components as html
from dash.dependencies import Input, Output, State
import file_operations


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

upload_component = dcc.Upload(
    id="upload-data",
    children=[
        html.Div([
            html.Img(src="https://via.placeholder.com/150", id="upload-preview"),
            html.P("Drag and drop or click to select a file to upload."),
        ], id="upload-area"),
    ],
    style={
        "width": "100%",
        "height": "200px",
        "borderWidth": "2px",
        "borderStyle": "dashed",
        "borderRadius": "5px",
        "textAlign": "center",
        "margin": "10px",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "center",
        "alignItems": "center",
    },
    multiple=True,  # Allow multiple file uploads
)

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
        'height': '100vh',
        'display': 'flex',
        'flexDirection': 'row',
        'justifyContent': 'flex-start',
    },
    children=[
        html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'column',
            },
            children=[
                html.Img(
                            src='/assets/rmitLogo.jpg',
                            style={'width': '200px', 'height': 'auto', 'margin-top': '10px', 'marginLeft': 'auto'}
                        ),
                html.H2('Engineering Capstone project', style={'color': 'white'}),
                html.H3('Group name: Helios Negotiator'),
                html.Br(),
                html.H5('Student name: Nguyen Dang Huynh Chau (s3777214)'),
                html.H5('Student name: To Vu Phuc (s3758272)'),
                html.H5('Student name: Nguyen Nhat Tan (s3818559)'),
                html.H5('Student name: Tong Son Tung (s3818153)'),
            ]
        ),
        
    ]
)

app.layout = html.Div(
    style={'display': 'flex'},
    children=[
        left_navbar,
        html.Div(className='content', style={'flex': '1', 'backgroundColor': 'white', 'padding': '20px'}, children=[
            html.H2("Upload your image:", style={'textAlign': 'center'}),
            upload_component,
            html.H2("File List"),
            html.Ul(id="file-list"),
            download_button,
            dcc.Location(id="url", refresh=False),
            dcc.Download(id="download"),
        ])
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


if __name__ == "__main__":
    app.css.append_css({"external_url": "/assets/styles.css"})
    app.run_server(debug=True)

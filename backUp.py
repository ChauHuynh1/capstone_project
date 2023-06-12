import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import file_list
import file_operations

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = dash.Dash(__name__)

upload_component = dcc.Upload(
    id="upload-data",
    children=html.Div(["Drag and drop or click to select a file to upload."]),
    style={
        "width": "100%",
        "height": "60px",
        "lineHeight": "60px",
        "borderWidth": "1px",
        "borderStyle": "dashed",
        "borderRadius": "5px",
        "textAlign": "center",
        "margin": "10px",
    },
    multiple=False,  # Allow only single file upload
)

download_button = html.Button("Download File", id="btn-download", disabled=True)

# Left navigation bar
left_navbar = html.Div(
    className='four columns div-user-controls',
    style={
        'backgroundColor': 'black',
        'color': 'white',
        'padding': '20px',
        'height': '100vh',
    },
    children=[
        html.H2('Assignment 1: Data Preparation and Exploration', style={'color': 'white'}),
        html.P('Student Name: Nguyen Dang Huynh Chau'),
        html.P('Student ID: s3777214'),
        html.P('Lecturer: Vo Ngoc Yen Nhi'),
        html.Br(),
    ]
)

app.layout = html.Div(
    style={'display': 'flex'},
    children=[
        left_navbar,
        html.Div(className='content', style={'flex': '1', 'backgroundColor': 'white', 'padding': '20px'}, children=[
            html.H2("Upload"),
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
def update_file_list(filename, contents):
    return file_operations.update_file_list(filename, contents)


@app.callback(
    Output("download", "data"),
    Input("btn-download", "n_clicks"),
    State("upload-data", "filename"),
)
def download_file(n_clicks, filename):
    return file_operations.download_file(n_clicks, filename)


@app.server.route("/download/<path:path>")
def download(path):
    return file_operations.download(path)


if __name__ == "__main__":
    app.run_server(debug=True)

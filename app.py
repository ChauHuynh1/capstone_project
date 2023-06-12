import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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
    multiple=True,  # Allow multiple file uploads
)

download_button = html.Button("Download Files", id="btn-download", disabled=True)

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
    app.run_server(debug=True)

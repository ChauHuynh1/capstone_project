import os
import base64
import zipfile
from urllib.parse import quote as urlquote
import dash_html_components as html
import imghdr
import dash_bootstrap_components as dbc 


UPLOAD_DIRECTORY = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def save_file(filename, contents):
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as f:
        f.write(contents.encode())


def update_file_list(filenames, contents):
    file_list = []
    alert_message = None

    for filename, content in zip(filenames, contents):
        save_file(filename, content)

        if not is_allowed_extension(filename):
            alert_message = dbc.Alert(
                "One or more files have invalid extensions!",
                color="danger",
                dismissable=True,
            )
            break

        file_list_item = generate_file_list(filename)
        file_list.append(file_list_item)

    if alert_message is None:
        alert_message = dbc.Alert(
            "Files successfully uploaded!",
            color="success",
            dismissable=True,
        )

    return [alert_message] + file_list


def generate_file_list(filename):
    return html.Div(
        children=[
            html.Main(
                children=[
                    html.Ol(
                        className="gradient-list",
                        children=[
                            html.Li(
                                children=[
                                    html.Span(className="circle", style={
                                        'borderRadius': '50%',
                                        'height': '50px',
                                        'width': '50px',
                                        'background-color': '#11009E',
                                        'display': 'inline-block',
                                        'padding': '5px 10px',
                                        'margin': '0 10px 0 0',  # Adjusted margin here
                                        'cursor': 'pointer',
                                        'color': '#fff',
                                        'text-align': 'center',
                                        'line-height': '40px',
                                        'font-weight': 'bold',
                                        'font-size': '20px',
                                    }, children=1),
                                    filename
                                ]
                            )
                        ],
                        style={
                            "counter-reset": "gradient-counter",
                            "list-style": "none",
                            "margin": "2rem 0",
                            "padding-left": "4rem"
                        }
                    ),
                    html.Div()
                ],
                style={
                    "display": "block",
                    "margin": "0 auto",
                    "max-width": "100rem",
                    "padding": "0.5rem"
                }
            )
        ],
        style={
            "font-family": "'Raleway', sans-serif",
            "background-color": "#fafafa",
            "color": "#1d1f20"
        }
    )

def is_allowed_extension(filename):
    _, extension = os.path.splitext(filename)
    return extension[1:].lower() in ALLOWED_EXTENSIONS


def download_files(filenames):
    zip_filename = "files.zip"
    zip_path = os.path.join(UPLOAD_DIRECTORY, zip_filename)

    with zipfile.ZipFile(zip_path, "w") as zip_file:
        for filename in filenames:
            file_path = os.path.join(UPLOAD_DIRECTORY, filename.props.children)
            zip_file.write(file_path, filename)

    with open(zip_path, "rb") as f:
        encoded_zip = base64.b64encode(f.read()).decode()

    return f"data:application/zip;base64,{encoded_zip}"

import os
import base64
import zipfile
from urllib.parse import quote as urlquote
import dash_html_components as html

UPLOAD_DIRECTORY = "uploads"


def save_file(filename, contents):
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as f:
        f.write(contents.encode())



def update_file_list(filenames, contents):
    file_list = []

    for filename, content in zip(filenames, contents):
        save_file(filename, content)
        file_list_item = generate_file_list(filename)
        file_list.append(file_list_item)

    return file_list


def generate_file_list(filename):
    return html.Li(
        html.A(
            filename,
            href=f"/download/{urlquote(filename)}",
            id={"type": "download-link", "index": urlquote(filename)},
        )
    )


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

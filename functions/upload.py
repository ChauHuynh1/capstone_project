import base64
import dash_html_components as html
import dash_core_components as dcc

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

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


def save_file(name, content):
    """Decode and save the file content."""
    extension = name.rsplit(".", 1)[1].lower()
    if extension in ALLOWED_EXTENSIONS:
        data = content.encode("utf8").split(b";base64,")[1]
        try:
            # Check if the base64 data is valid
            base64.decodebytes(data)
        except base64.binascii.Error as e:
            raise ValueError("Invalid file content. Unable to decode base64 data.") from e

        return base64.decodebytes(data)
    else:
        raise ValueError("Invalid file format. Only images (png, jpg, jpeg, gif) are allowed.")

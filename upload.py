import base64

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

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

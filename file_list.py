import dash_html_components as html

def generate_file_list(filename):
    return html.Li(html.A(filename, href="", id={"type": "download-link", "index": filename}))

# import dash_html_components as html

# def generate_file_list(filename):
#     return html.Li(html.A(filename, href="", id={"type": "download-link", "index": filename}))


import dash
import dash_html_components as html

def generate_file_list(filename):
    return html.Div(
        children=[
            html.Ol(
                className="gradient-list",
                children=[
                    html.Li(html.A(filename, href="", id={"type": "download-link", "index": filename}))
                ]
            )
        ],
        style={
            "font-family": "'Raleway', sans-serif",
            "max-width": "40rem",
            "margin": "0 auto",
            "padding": "1rem"
        }
    )


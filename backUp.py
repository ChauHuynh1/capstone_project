import dash
from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import cv2
import plotly.express as px


dash.register_page(__name__)

table_header = [
    html.Thead(html.Tr([html.Th("Name"), html.Th("Value"), html.Th("Unit")]))
]


table_body = [
    html.Tbody([
        html.Tr([html.Td("Current file:"), html.Td(id="current-file"), html.Td("")]),
        html.Tr([html.Td("Normal temperature:"), html.Td(id="normal-temperature"), html.Td("C Degree")]),
        html.Tr([html.Td("Defective percentage:"), html.Td(id="defective-percentage"), html.Td("")]),
        html.Tr([html.Td("Defective counts:"), html.Td(id="defective-counts"), html.Td("")]),
    ])
]
table = dbc.Table(table_header + table_body, bordered=True)


table_col = dbc.Col(table, width=4)

def create_figure(image):
    # Convert the BGR image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    fig = px.imshow(rgb_image)
    fig.update_layout(
        dragmode="drawrect",
        xaxis_visible=False,
        yaxis_visible=False,
        width=800,
    )
    return fig

## Drop down to select image to display
dropdown = html.Div(
    [
        dcc.Dropdown(
            id="image-dropdown",
            options=[],
            value=None,
        ),
    ],
)



#-------------------------Main Diagnosis layout-----------------------------#


layout = html.Div([
    dcc.Store(id='session', storage_type='session'),
    dbc.Row(dbc.Col(html.H1("Get your solar diagnosed:"))),
    html.Br(),
    dbc.Row(
        [
            dbc.Col([
                table_col,
                dropdown,
            ]),
            dbc.Col([
                dcc.Graph(
                    id="image-display",
                    config={'staticPlot': False},
                ),
            ]),
        ]
    ),
])

@callback(
    Output("image-dropdown", "options"),
    Input('session', 'data'),  # Trigger the callback on page load by changing a dummy input value
    State('session', 'data') 
)
def update_image_dropdown_options(session_data, _):
    if session_data and 'upload_image' in session_data:
        filenames_list = session_data['upload_image']
        options = [{"label": filename, "value": filename} for filename in filenames_list]
        return options
    return []


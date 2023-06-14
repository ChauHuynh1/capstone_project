import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

tab_1 = html.Div(
    children=[
        html.Div(
            [
                html.P(
                    "This project proposal aims to detect and reduce losses in solar panels caused by damaged cells. "
                    "By utilizing UAV-based thermal imaging processing, we can quickly spot and identify faulty cells, "
                    "streamlining the maintenance process. Through data augmentation and machine learning algorithms, "
                    "subsequent images can be automatically analyzed for faults, significantly reducing downtime "
                    "and increasing overall efficiency for solar power generation.",
                    style={'text-align': 'justify', 'font-weight': 'bold', 'color': '#FFE7A0'}
                )
            ],
            style={
                'display': 'flex',
                'flex-direction': 'column',
                'justify-content': 'center',
                'align-items': 'center',
                'height': '400px',
                'width': '300px',
                'margin': 'auto',
            },
        )
    ],
    style={'height': '100vh'},
)

tab_style = {
    'background-color': '#11009E',
}

tab_selected_style = {
    'backgroundColor': '#119DFF',
}

tab_2 = html.Div(
    children=[
        html.Div(
            [
                html.H5('Student name: Nguyen Dang Huynh Chau (s3777214)', style={'text-align': 'justify', 'font-weight': 'bold', 'color': '#FFE7A0'}),
                html.H5('Student name: To Vu Phuc (s3758272)', style={'text-align': 'justify', 'font-weight': 'bold', 'color': '#FFE7A0'}),
                html.H5('Student name: Nguyen Nhat Tan (s3818559)', style={'text-align': 'justify', 'font-weight': 'bold', 'color': '#FFE7A0'}),
                html.H5('Student name: Tong Son Tung (s3818153)', style={'text-align': 'justify', 'font-weight': 'bold', 'color': '#FFE7A0'}),
            ],
            style={
                'display': 'flex',
                'flex-direction': 'column',
                'justify-content': 'center',
                'align-items': 'center',
                'height': '300px',
                'width': '300px',
                'margin': 'auto',
            },
        )
    ],
    style={'height': '100vh'},
)

left_navbar = html.Div(
    className='four columns div-user-controls',
    style={
        'backgroundColor': '#11009E',  # Update the background color here
        'color': 'white',
        'padding': '20px',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'flex-start',
        'height': '100vh',
    },
    children=[
        html.Div(
            style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
            },
            children=[
                html.Img(
                    src='/assets/rmitLogo_white.png',
                    style={'width': '200px', 'height': 'auto', 'margin-top': '10px'}
                ),
                html.Br(),
                html.H2('Engineering Capstone project', style={'color': '#FFE7A0'}),
                html.H3('Group name: Helios Negotiator', style={'color': '#FFE7A0'}),
                html.Br(),
            ]
        ),
        
        # Add tabs to the left navbar
         html.Div([
                        dcc.Tabs(id = "tabs-styled-with-inline", value = 'tab-1', 
                                 children = [
                                                dcc.Tab(label = 'Tab 1', value = 'tab-1', style = tab_style, selected_style = tab_selected_style),
                                                dcc.Tab(label = 'Tab 2', value = 'tab-2', style = tab_style, selected_style = tab_selected_style),
                                            ]),
                        html.Div(id = 'tabs-content-inline')
                    ], className = "create_container3 eight columns", 
                ),

        # Content for each tab
        html.Div(id="tab-content"),
    ]
)

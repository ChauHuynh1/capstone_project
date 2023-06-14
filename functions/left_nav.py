import dash_bootstrap_components as dbc
import dash_html_components as html

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
                    style={'text-align': 'justify'}
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

tab_2 = html.Div(
    children=[
        html.Div(
            [
                html.H5('Student name: Nguyen Dang Huynh Chau (s3777214)'),
                html.H5('Student name: To Vu Phuc (s3758272)'),
                html.H5('Student name: Nguyen Nhat Tan (s3818559)'),
                html.H5('Student name: Tong Son Tung (s3818153)'),
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
        'backgroundColor': '#a9dce3',  # Update the background color here
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
                'color': '#FFFC7',  # Update the text color here

            },
            children=[
                html.Img(
                    src='/assets/rmitLogo.jpg',
                    style={'width': '200px', 'height': 'auto', 'margin-top': '10px'}
                ),
                html.H2('Engineering Capstone project', style={'color': '#7689de'}),
                html.H3('Group name: Helios Negotiator', style={'color': '#7689de'}),
                html.Br(),
            ]
        ),
        
        # Add tabs to the left navbar
        dbc.Tabs(
            [
                dbc.Tab(label="Project Description", tab_id="tab-1", labelClassName="nav-link", activeLabelClassName="active"),
                dbc.Tab(label="Project Team", tab_id="tab-2", labelClassName="nav-link", activeLabelClassName="active"),
            ],
            id="tabs",
            className="nav nav-pills mt-4",
            active_tab="tab-1",
            style={'display': 'flex', 'flexDirection': 'row'},
        ),
        
        # Content for each tab
        html.Div(id="tab-content"),
    ]
)

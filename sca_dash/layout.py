from dash import dcc
from dash import html
from sca_dash.setup import sca_dash
import numpy as np

sca = sca_dash()

# layout = html.Div(id='main', children=[
#     html.H1(id='username'),
#     html.H1(f'Stock Tickers - {sca.app_title}'),
#     dcc.Dropdown(
#         id='my-dropdown',
#         options=[
#             {'label': 'Coke', 'value': 'COKE'},
#             {'label': 'Tesla', 'value': 'TSLA'},
#             {'label': 'Apple', 'value': 'AAPL'}
#         ],
#         value='COKE'
#     ),
#     dcc.Graph(id='my-graph'),
#     dcc.Store(id='user-store'),
# ], style={'width': '500'})

layout = html.Div(
    children=[
        html.Div(
            children=[
              
                html.H1(
                    children="SCA Inferred Audience Dashboard", className="header-title"
                ),
            ],
            className="header",
        ),
        html.Div([
            html.Div(
                children=[
                 html.Div(
                    children=[
                        html.Div(children="TXMarket", className="menu-title"),
                        dcc.Dropdown(
                            id="TXMarket-filter",
                           options=[
                                {"label": TXMarket, "value": TXMarket}
                                for TXMarket in np.sort(sca.df_TXMarket.TXRegion)
                            ],
                            optionHeight=50,
                            value="NSW-Regional",
                            clearable=False,
                            className="dropdown",
                            maxHeight=1000
                        ),
                        dcc.Loading(id="loading-2", type="default",
                        children=html.Div(id="TXMarket_loading_output_1")),
                        
                    ]
                    ), 
                 html.Div(
                    children=[
                        html.Div(children="Category-SSDemo", className="menu-title"),
                        dcc.Dropdown(
                            id="Category-SSDemo-filter",
                            options=list(sca.all_options.keys()),
                            optionHeight=50,
                            value="Purchase_Intent_N12Mnths",
                            clearable=False,
                            className="dropdown",
                            maxHeight=1000
                        ),
                     
                    ]
                ), 
                 html.Div(
                    children=[
                        html.Div(children="SSDemo", className="menu-title"),
                        dcc.Dropdown(
                            id="SSDemo-filter",
                            optionHeight=50,
                            clearable=False,
                            className="dropdown",
                            maxHeight=1000
                        ),
                       
                    ]
                ), 
                 html.Div(
                    children=[
                        html.Div(children="StnBrand", className="menu-title"),
                        dcc.Dropdown(
                            id="StnBrand-filter",
                            options=[
                                {"label": StnBrand, "value": StnBrand}
                                for StnBrand in np.sort(sca.df_StnBrand.StnBrand.unique())
                            ],
                            multi = False,
                            value="Hit!",
                            clearable=False,
                            className="dropdown",
                            maxHeight=300
                        ),
                      
                    ]
                    ),
                 html.Div(
                    children=[
                        html.Div(children="Demo", className="menu-title"),
                        dcc.Dropdown(
                            id="Demo-filter",
                            options=[
                                {"label": Demo, "value": Demo}
                                for Demo in np.sort(sca.df_Demo.Demo.unique())
                            ],
                            multi = True,
                            value="F18-24",
                            clearable=False,
                            className="dropdown",
                            maxHeight=300
                        ),
                        
                    ]
                ),
                 html.Div(
                    children=[
                        html.Div(children="Daypart", className="menu-title"),
                        dcc.Dropdown(
                            id="Daypart-filter",
                            options=[
                                {"label": Daypart, "value": Daypart}
                                for Daypart in np.sort(sca.df_Daypart.Daypart.unique())
                            ],
                            multi = True,
                            value="M-F 0530-0900",
                            clearable=False,
                            className="dropdown",
                            maxHeight=300
                        ),
                        
                    ]
                )             
            ],
            className="menu",
            ),
            dcc.Tabs([
                dcc.Tab(label='UE and Listening Share', children=[
                    html.Div(
                        children=[
                                    
                            html.Div(
                                children=dcc.Graph(
                                    id="bar_chart", config={"displayModeBar": False},
                                ),
                                className="card",
                            )    
                        ],
                        className="wrapper",
                    )
                ]),
                dcc.Tab(label='SSDemo Trend', children=[   
            
                    html.Div(
                    children=[
                    
                        html.Div(
                            children=dcc.Graph(
                                id="bar_chart_2", config={"displayModeBar": False},
                            ),
                            className="card",
                        ),
                    ],
                    className="wrapper",
                )
            

            ]),
                dcc.Tab(label='Demo Profile', children=[         
    
                    html.Div(
                        children=[

                            dcc.RadioItems(["Total People", "Total Minutes"], "Total People", id="people_mins_radio"),
                        
                            html.Div(
                                children=dcc.Graph(
                                    id="bar_chart_3", config={"displayModeBar": False},
                                ),
                                className="card",
                            ),
                        ],
                        className="wrapper",
                    )
                ]),
                dcc.Tab(label='Daypart Minutes', children=[

                html.Div(
                    children=[
                    
                        html.Div(
                            children=dcc.Graph(
                                id="bar_chart_4", config={"displayModeBar": False},
                            ),
                            className="card",
                        ),
                    ],
                    className="wrapper",
                ),
            

            ]),
                dcc.Tab(label='Daypart Profile', children=[
      
            html.Div(
                    children=[
                    
                        html.Div(
                            children=dcc.Graph(
                                id="bar_chart_5", config={"displayModeBar": False},
                            ),
                            className="card",
                        ),
                    ],
                    className="wrapper",
                ),

     ])
            ])
        ])
    ])
#---------------------------------------------------------------

import io
import base64
import datetime
from tkinter.tix import InputOnly
from dash import Dash, html, dcc, dash_table, callback_context
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from utils.Anonymization import Anonymization


# GLOBAL VARIABLES
columns_names = []
identifiers = []
quasi_identifiers = []
sensitive_attributes = []
columns_names_like_identifiers = []
columns_names_like_quasi_identifiers = []
columns_names_like_sensitive_attributes = []
original_df = None
final_df = None


app = Dash(external_stylesheets=[dbc.themes.SKETCHY])

queries_nav_link = dbc.NavItem(dbc.NavLink(
    'Queries', href="/queries", external_link=True, className='navlinks'))

navbar = dbc.NavbarSimple(
    children=[
        dbc.Collapse(dbc.Nav([queries_nav_link, plot_nav_link], className='ml-auto work-sans', navbar=True),
                     id="navbar-collapse", navbar=True),
    ],
    brand="Anonymization Service",
    color="primary",
    dark=True
)

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
    navbar,
    # content will be rendered in this element
    html.Div(id='page-content')
])

queries_layout =  html.Div(
    [
        dbc.Container(
            children=[
                html.H1("Welcome to the anonymization service"),
                html.P("Upload your csv and start anonymizing data"),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div(
                        children=[
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    multiple=False
                ),
                html.Div(id='output-data-upload'),
                html.Div(id='output-data-processed'),
            ],
            style={
                'textAlign': 'center',
                'marginTop': '60px'
            }
        )
    ]
)

app.layout =  html.Div(
    [
        dbc.Container(
            children=[
                html.P("Upload your csv and start anonymizing data"),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div(
                        children=[
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    multiple=False
                ),
                html.Div(id='output-data-upload'),
                html.Div(id='output-data-processed'),
            ],
            style={
                'textAlign': 'center',
                'marginTop': '60px'
            }
        )
    ]
)


def parse_and_save_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    global original_df
    decoded = base64.b64decode(content_string)
    try:
        print(filename)
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        global columns_names
        original_df = df
        columns_names = list(df.columns)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dbc.Row([
            dbc.Col(
                children=[
                    dash_table.DataTable(
                        df.to_dict('records'),
                         [{'name': i, 'id': i} for i in df.columns],
                    ),

                    html.Hr(),  # horizontal line

                    # For debugging, display the raw contents provided by the web browser
                    html.Div('Raw Content'),
                    html.Pre(contents[0:200] + '...', style={
                        'whiteSpace': 'pre-wrap',
                        'wordBreak': 'break-all'
                    })

                ]
            ),
            dbc.Col(
                children=[
                    dbc.Label("Identifiers:"),
                    dcc.Dropdown(
                        options=columns_names,
                        placeholder="Select the identifiers",
                        multi=True,
                        id="identifiers-dropdown"
                    ),
                    dbc.Label("Quasi-identifiers:"),
                    dcc.Dropdown(
                        options=columns_names,
                        placeholder="Select the quasi-identifiers",
                        multi=True,
                        id="quasi-identifiers-dropdown"
                    ),
                    dbc.Label("Sensitive attributes:"),
                    dcc.Dropdown(
                        options=columns_names,
                        placeholder="Select the sensitive attributes",
                        multi=True,
                        id="sensitive-attributes-dropdown"
                    ),
                    dbc.Label("K:"),
                    dcc.Input(
                            id="k", type="number", 
                    ),
                    dbc.Label("L:"),
                    dcc.Input(
                            id="l", type="number", 
                    ),
                    dbc.Label("T:"),
                    dcc.Input(
                            id="t", type="number",
                    ),
                    dbc.Label("Stop utility:"),
                    dcc.Input(
                            id="stop_utility", type="number",
                    ),
                    dbc.Label("Max iter:"),
                    dcc.Input(
                            id="max_iter", type="number",
                    ),
                    dbc.Label("Add the necessary structure to categorize the column you want. Indicate the column in \"COLUMN NAME\" and the different categories (\"CATEGORY 1\", \"CATEGORY 2\", etc.), then within each category identify the column values that belong to that category."),
                    dcc.Input(
                            id="semantic", type="text",
                    ),
                    html.Button('Anonymize', id='btn-anonymize', n_clicks=0),
                    html.Div(id='container-button-basic',children='Enter a value and press submit')
                ]
            )
        ]
        )


    ])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(contents, filename, last_modified):
    if contents is not None:
        children = [
            parse_and_save_contents(contents, filename, last_modified)
        ]
        return children

@app.callback(
    Output('quasi-identifiers-dropdown', 'options'),
    [Input('identifiers-dropdown', 'value'),
    Input('sensitive-attributes-dropdown', 'value')],
    [State('quasi-identifiers-dropdown', 'options')],
)
def update_quasi_identidiers_dropdown(identifiers_value,sensitive_value, options):
    global columns_names
    if identifiers_value:
       return [{'label':c, 'value':c} for c in columns_names if c not in identifiers_value]
    elif sensitive_value:
       return [{'label':c, 'value':c} for c in columns_names if c not in sensitive_value]
    else:
       return [ c for c in columns_names]

@app.callback(
    Output('identifiers-dropdown', 'options'),
    [Input('quasi-identifiers-dropdown', 'value'),
     Input('sensitive-attributes-dropdown', 'value')],
    [State('identifiers-dropdown', 'options')],
)
def update_identifiers_dropdown(quasidentifiers_value,sensitive_value, options):
    global columns_names
    if quasidentifiers_value:
       return [{'label':c, 'value':c} for c in columns_names if c not in quasidentifiers_value]
    elif sensitive_value:
       return [{'label':c, 'value':c} for c in columns_names if c not in sensitive_value]
    else:
       return [ c for c in columns_names]

@app.callback(
    Output('sensitive-attributes-dropdown', 'options'),
    [Input('quasi-identifiers-dropdown', 'value'),
     Input('identifiers-dropdown', 'value')],
    [State('sensitive-attributes-dropdown', 'options')],
)
def update_sensitive_attributes_dropdown(quasidentifiers_value,identifiers_value, options):
    global columns_names
    if quasidentifiers_value:
       return [{'label':c, 'value':c} for c in columns_names if c not in quasidentifiers_value]
    elif identifiers_value:
       return [{'label':c, 'value':c} for c in columns_names if c not in identifiers_value]
    else:
       return [ c for c in columns_names]


@app.callback(
    Output('output-data-processed','children'),
    [Input('quasi-identifiers-dropdown', 'value'),
     Input('identifiers-dropdown', 'value'),
     Input('sensitive-attributes-dropdown', 'value'),
     Input('semantic', 'value'),
     Input('k', 'value'),
     Input('l', 'value'),
     Input('t', 'value'),
     Input('max_iter', 'value'),
     Input('stop_utility', 'value'),
     Input('btn-anonymize', 'n_clicks')],
)
def update_output(quasidentifiers,identifiers,sensitive_attributes,semantics,k,l,t,max_iter,stop_utility,n_clicks):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-anonymize' in changed_id:
        model = Anonymization(original_df,identifiers, quasidentifiers,sensitive_attributes, semantics)
        global final_df
        final_df = model.achieve_klt_random(k,l,t,stop_utility,max_iter)[0]
        return dbc.Row([
            dbc.Col(
                children=[
                    dash_table.DataTable(
                        final_df.to_dict('records'),
                         [{'name': i, 'id': i} for i in final_df.columns],
                    ),
                    html.Hr(),  # horizontal line
                    # For debugging, display the raw contents provided by the web browser
                    html.Div('Dataset anonimyzed'),
                ]
            )],)








if __name__ == '__main__':
    app.run_server(debug=True)

import dash
from dash import dash_table
import plotly.express as px
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import dash_html_components as html
import dash_cytoscape as cyto
from PIL import Image
from neo4jconnection import fetch_pagerank_data,fetch_cytoscape_data,fetch_trx_data
#
tmp=fetch_trx_data()
dff = fetch_pagerank_data()
cy_elements = fetch_cytoscape_data()


##table visualization 

dash_table.DataTable(
    id="table",
    data=tmp.to_dict('records'),  # Converts DataFrame to a dictionary
    columns=[{"name": i, "id": i} for i in tmp.columns],  # Correct format for columns
    page_size=10
)




# Bar chart figure
fig = px.bar(dff, x="nama", y="score", color="nama")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO], suppress_callback_exceptions=True)

# Update layout for bar chart
fig.update_layout(
    plot_bgcolor='#111111',
    paper_bgcolor='#111111',
    font_color='#7FDBFF'
)

tablecard = dbc.Card(
    [
        dbc.CardBody([
        html.H1("Priority Customer", className='card-title'),
        html.P("", className='card-body'),
        html.Div(
            dash_table.DataTable(
            id="table",
            data=tmp.to_dict('records'),  # Converts DataFrame to a dictionary
            columns=[{"name": i, "id": i} for i in tmp.columns],
               style_header={
                'backgroundColor': 'Black',
                'fontWeight': 'Bold',
                'fontcolor':'white',
                'textAlign' :'center',
            }, 
              style_cell={
                        'backgroundColor': 'black',
                        'color': 'white',
                        'textAlign' :'center',
                    }, 
            page_size=10
            )

        )
        ])
    ],
    outline=True, color='secondary',
    style={
        "width": "100%",
        "height": "600px",  # Adjust this height as needed
        "margin-bottom": "1rem"
    }
)




# Layout components for barchart

titlecard = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col(html.Center(html.H1("Overview GoldenID Relation")), style={'fontColor':'text'})
        
        ]),
    ])
], color="#ff9100",
    style={
        "width": "100rem",
        "margin-top": "1rem",
        "margin-bottom": "1rem",
        "margin-right": "0rem"
    })

barchartcard = dbc.Card([
    dbc.CardBody([
        html.H1("Pagerank Score", className='card-title'),
        html.P("", className='card-body'),
        dcc.Graph(id='bar', figure=fig)
    ])
], outline=True, color='secondary',
    style={
        "width": "100%",
        "margin-bottom": "1rem"
    })

##Layout for cytoscape_card
cytoscape_card = dbc.Card([
    dbc.CardBody([
        html.H1("Graph Visualization", className='card-title', style={'text-align': 'center'}),
        html.P("", className='card-body'),

        # Container for Cytoscape with flexbox for centering
        html.Div(
            cyto.Cytoscape(
                id='cytoscape',
                elements=cy_elements,
                layout={'name': 'cose'},
                style={'width': '100%', 'height': '60rem'},  # Ensure Cytoscape fills width
                stylesheet=[
                    {
                        'selector': 'node',
                        'style': {
                            'label': 'data(label)',
                            'background-color': '#0074D9',
                            'color': 'white',
                            'text-valign': 'center',
                            'text-halign': 'center',
                            'width': '10px',
                            'height': '10px',
                            'font-size': '5px'
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'label': 'data(label)',
                            'width': 2,
                            'line-color': '#ccc',
                            'target-arrow-color': '#ccc',
                            'target-arrow-shape': 'triangle',
                            'curve-style': 'bezier'
                        }
                    }
                ]
            ),
            style={
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
                'height': '100%',
                'width': '100%',  # Ensure container fills the available width
            }
        )
    ])
], outline=False, color='secondary',
    style={
        "width": "100%",
        "height": "100%",  # Adjust this height as needed
        "margin-bottom": "1rem"
    }
)

page = html.Center(html.Div([
    titlecard,
    dbc.Row([
        dbc.Col(barchartcard, width=6),
        dbc.Col(tablecard, width=6),
        dbc.Col(cytoscape_card, width=12),  # Adjust width to ensure proper alignment
    ], justify='center'),
], style={"width": "100%"})
)






# Layout 1 
page = html.Center(html.Div([
    titlecard,
    dbc.Row([
        dbc.Col(barchartcard, width=6),
        dbc.Col(cytoscape_card, width=6)
    ], justify='center'),
], style={"width": "100rem"}))



SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#424242",
}

WHITE = "#fffff8"
TG_LOGO = "https://i.pinimg.com/originals/98/c7/e9/98c7e95ea1207eef6f70f0ae9e694e67.png"
sidebar = dbc.Card([
    html.Div([
        html.H2("GenIO", className="display-4"),
        html.Hr(),
        html.Label("MDM Advanced enterprised", className="display-9"),
        html.Hr(),
        dbc.Nav([
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Page 1", href="/page-1", active="exact"),
            dbc.NavLink("Page 2", href="/page2", active="exact"),
            dbc.NavLink("Page 3", href="/page3", active="exact"),
        ], vertical=True, pills=True),
        html.Hr(),
        html.Li(html.A("Introduction to Product", href='https://simian.co.id/master-data-management', target="_blank", style={'color': WHITE}), style={'color': WHITE}),
        html.Br(),
        html.Li(html.A("Introduction to Graph", href='https://www.geeksforgeeks.org/introduction-to-graphs-data-structure-and-algorithm-tutorials/', target="_blank", style={'color': WHITE}), style={'color': WHITE}),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Label(["Achmad Irfandi Darmawan"], style={"fontcolor": "black"})
    ],
    style=SIDEBAR_STYLE,
    className="card"
)])

CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "0rem",
    "padding": "1rem 1rem",
}

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar,
    html.Div(id='page-content', style=CONTENT_STYLE)
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')], suppress_callback_exceptions=True)
def display_page(pathname):
    if pathname == "/":
        return page

if __name__ == "__main__":
    app.run_server(debug=True)

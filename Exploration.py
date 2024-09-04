import dash
from dash import dcc, html, Input, Output, State
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from neomodel import db, config
from neo4jconnection import fetch_pagerank_data,fetch_cytoscape_data,fetch_trx_data
tmp=fetch_trx_data()
dff = fetch_pagerank_data()

# Set up Neo4j connection
config.DATABASE_URL = 'bolt://neo4j:simian123@localhost:7687'

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("GenIO - Graph Analytics", href="#"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
                    dbc.NavItem(dbc.NavLink("Page 1", href="#")),
                    dbc.NavItem(dbc.NavLink("Page 2", href="#")),
                ],
                className="ml-auto",  # Align to the right
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    sticky="bottom",
)

def fetch_cytoscape_data(cypher_query):
    print(f"Executing Cypher Query: {cypher_query}")  # Debugging: print the query
    cy_records, _ = db.cypher_query(cypher_query)
    
    nodes = {}
    edges = []

    for record in cy_records:
        print(f"Record: {record}")  # Debugging: print each record
        node1 = record[0]  # Assuming g is the first column
        node2 = record[2]  # Assuming g2 is the third column
        relationship = record[1]  # Assuming r is the second column

        nodes[node1.id] = {
            "data": {"id": node1.id, "label": node1.get("crn", "nama_lengkap")}
        }
        nodes[node2.id] = {
            "data": {"id": node2.id, "label": node2.get("crn", "nama_lengkap")}
        }
        edges.append({
            "data": {"source": node1.id, "target": node2.id, "label": relationship.type}
        })

    # Combine nodes and edges into a single list
    return list(nodes.values()) + edges

cytoscape_card = dbc.Card([
    dbc.CardBody([
        html.H1("Graph Exploration", className='card-title', style={'text-align': 'center'}),
        html.P("", className='card-body'),
        html.Div([
            dcc.Input(id='query-input', type='text', placeholder='Enter Cypher Query', style={'width': '100%'}),
            html.Button('Search', id='search-button', n_clicks=0),
            html.Div(id='search-results')
        ]),
        html.Div(
            cyto.Cytoscape(
                id='cytoscape',
                elements=[],
                layout={'name': 'cose'},
                style={'width': '100%', 'height': '80rem'}, 
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
                            'width': 1.5,
                            'line-color': '#ccc',
                            'target-arrow-color': '#ccc',
                            'target-arrow-shape': 'triangle',
                            'curve-style': 'bezier',
                            'font-size': '4px'
                        }
                    }
                ]   # Adjust height as needed
            ),
        )
    ])
])

app.layout = dbc.Container([
    cytoscape_card
], fluid=True)

# Callback to update the graph based on the search query
@app.callback(
    Output('cytoscape', 'elements'),
    Input('search-button', 'n_clicks'),
    State('query-input', 'value')
)
def update_cytoscape_graph(n_clicks, query_input):
    if n_clicks > 0 and query_input:
        try:
            cy_elements = fetch_cytoscape_data(query_input)
            print(f"Elements: {cy_elements}")  # Debugging: print the elements
            return cy_elements
        except Exception as e:
            print(f"Error: {e}")  # Debugging: print any error
            return []  # Return an empty graph if there's an error
    return []

if __name__ == '__main__':
    app.run_server(debug=True)

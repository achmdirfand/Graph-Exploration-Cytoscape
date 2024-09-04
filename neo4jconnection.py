from neo4j import GraphDatabase
import pandas as pd

uri = "bolt://localhost:7687"
username = "neo4j"
password = "simian123"

driver = GraphDatabase.driver(uri, auth=(username, password))


def fetch_pagerank_data():
    with driver.session() as session:
        records = session.run(
            "MATCH (g:GoldenID) RETURN g.nama_lengkap AS nama, g.pagerank AS pg_score ORDER BY pg_score DESC LIMIT 50"
        )
        
        data = []
        for record in records:
            nama = record["nama"]
            score = record["pg_score"]
            data.append([nama, score])
      
        
        df = pd.DataFrame(data, columns=['nama', 'score'])
    return df

def fetch_cytoscape_data():

    with driver.session() as session:
        cy_records = session.run(
            "MATCH (g:GoldenID)-[r:NODE_SIM]-(g2:GoldenID) RETURN g, r, g2 LIMIT 200"
        )
        
        nodes = {}
        edges = []
        
        for record in cy_records:
            node1 = record["g"]
            node2 = record["g2"]
            relationship = record["r"]

            nodes[node1.id] = {
                "data": {"id": node1.id, "label": node1.get("nama_lengkap", "Unnamed")}
            }
            nodes[node2.id] = {
                "data": {"id": node2.id, "label": node2.get("nama_lengkap", "Unnamed")}
            }
            edges.append({
                "data": {"source": node1.id, "target": node2.id, "label": relationship.type}
            })

        # Combine nodes and edges into a single list
        cy_elements = list(nodes.values()) + edges

    return cy_elements


def fetch_trx_data():
    with driver.session() as session:
        records= session.run("match (t:TmpNode) return t.crn  as crn, t.Totamount as Tot_Amount , t.Totfreq as Total_occurance limit 10")

        data1 = []
        for record in records:
            crn  = record["crn"]
            total_amount = record["Tot_Amount"]
            total_occurance = record["Total_occurance"]
            data1.append([crn, total_amount,total_occurance])
      
        
        df2 = pd.DataFrame(data1, columns=['crn', 'total_amount','total_occurance'])
    return df2
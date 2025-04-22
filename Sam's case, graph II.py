import json
!pip install pyvis
from pyvis.network import Network
import networkx as nx

G = nx.DiGraph()

conclusions = ["N1 applies to Sam's Case", "N2 applies to Sam's Case"]
G.add_nodes_from(conclusions)

reasons = ["F1: N1 is applicable to Sam's case", "F2: N2 is applicable to Sam's case"]
G.add_nodes_from(reasons)

relationships = [
    ("F1: N1 is applicable to Sam's case","N1 applies to Sam's Case", {'type': 'pro'}),
    ("F1: N1 is applicable to Sam's case","N2 applies to Sam's Case", {'type': 'con'}),
    ("F2: N2 is applicable to Sam's case","N1 applies to Sam's Case", {'type': 'con'}),
    ("F2: N2 is applicable to Sam's case","N2 applies to Sam's Case", {'type': 'pro'}),
    ]

G.add_edges_from(relationships)

for relationship in relationships:
    G.add_edge(relationship[0], relationship[1], label=relationship[2]['type'])

net = Network(notebook=True, directed=True)

net.toggle_physics(True) 

net.from_nx(G)

for node in net.nodes:
    node['size'] = 30 

for edge in net.edges:
    edge['title'] = edge['label'] 

net.show_buttons(filter_=['physics'])

for node in net.nodes:
    node['shape'] = 'text'  
    node['color'] = {
        'background': 'white',  
        'border': 'white',     
        'highlight': {         
            'background': 'white',
            'border': 'white'
        }
    }
    node['font'] = {
        'color': 'black',   
        'size': 20,        
        'background': 'white' 
    }

for edge in net.edges:
    edge['color'] = 'black'    

net.toggle_physics(False)

net.show("network_with_physics.html")

from google.colab import files
files.download("network_with_physics.html")

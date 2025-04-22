import json
!pip install pyvis 
from pyvis.network import Network
import networkx as nx

G = nx.DiGraph()

conclusions = ["N1 applies to Sam's case", "N2 applies to Sam's case"]
G.add_nodes_from(conclusions)

reasons = ["F1: N1 is applicable to Sam's case", "F2: N2 is applicable to Sam's case", "F3: N2 is more specific than N1","F4: applying N2 to Sam's case violates the aims of IHL"]
G.add_nodes_from(reasons)

relationships = [
    ("F1: N1 is applicable to Sam's case","N1 applies to Sam's case", {'type': 'pro'}),
    ("F1: N1 is applicable to Sam's case","N2 applies to Sam's case", {'type': 'con'}),
    ("F2: N2 is applicable to Sam's case","N1 applies to Sam's case", {'type': 'con'}),
    ("F2: N2 is applicable to Sam's case","N2 applies to Sam's case", {'type': 'pro'}),
    ("F3: N2 is more specific than N1","F2: N2 is applicable to Sam's case",{'type': 'pro'}),
    ("F3: N2 is more specific than N1","F1: N1 is applicable to Sam's case",{'type': 'con'}),
    ("F4: applying N2 to Sam's case violates the aims of IHL","F2: N2 is applicable to Sam's case",{'type': 'con'}),
    ("F4: applying N2 to Sam's case violates the aims of IHL","F1: N1 is applicable to Sam's case",{'type': 'pro'})
    ]

G.add_edges_from(relationships)

def evaluate_norms(graph):
    
    status = {node: 'out' for node in graph}

    for node in graph:
        if not any(graph[pred][node]['type'] == 'con' for pred in graph.predecessors(node)):
            status[node] = 'in'

    changes = True
    while changes:
        changes = False
        new_status = status.copy()
        for node in graph:
            active = status[node] == 'in'
            for neighbour in graph[node]:
                edge_data = graph[node][neighbour]
                if edge_data['type'] == 'con' and active:
                    if new_status[neighbour] != 'out':
                        new_status[neighbour] = 'out'
                        changes = True
                elif edge_data['type'] == 'pro' and active:
                    if new_status[neighbour] != 'in':
                        new_status[neighbour] = 'in'
                        changes = True

        status = new_status

    return status

final_status = evaluate_norms(G)
print(final_status)

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

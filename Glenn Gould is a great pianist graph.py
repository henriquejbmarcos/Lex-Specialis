import json
!pip install pyvis 
from pyvis.network import Network
import networkx as nx

G = nx.DiGraph()

conclusions = ['Glenn Gould is a Great Pianist']
G.add_nodes_from(conclusions)

reasons = ['Technique','Humming','Brilliant Technique']
G.add_nodes_from(reasons)

relationships = [
    ('Technique', 'Glenn Gould is a Great Pianist', {'type': 'pro'}),
    ('Humming', 'Glenn Gould is a Great Pianist', {'type': 'con'}),
    ('Brilliant Technique', 'Technique', {'type': 'pro'}),
    ('Brilliant Technique', 'Humming', {'type': 'con'}),
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

for node in net.nodes:
    if node['id'] in conclusions:  
        node['label'] += " (" + final_status[node['id']] + ")"  
        
net.show("network_with_physics.html")

from google.colab import files
files.download("network_with_physics.html")

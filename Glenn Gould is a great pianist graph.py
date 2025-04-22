import json
!pip install pyvis # installing the pyvis module
from pyvis.network import Network
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add norms as nodes
conclusions = ['Glenn Gould is a Great Pianist']
G.add_nodes_from(conclusions)

# Add reasons as nodes
reasons = ['Technique','Humming','Brilliant Technique']
G.add_nodes_from(reasons)

# Add relationships as edges with attributes for 'con' or 'pro'
relationships = [
    ('Technique', 'Glenn Gould is a Great Pianist', {'type': 'pro'}),
    ('Humming', 'Glenn Gould is a Great Pianist', {'type': 'con'}),
    ('Brilliant Technique', 'Technique', {'type': 'pro'}),
    ('Brilliant Technique', 'Humming', {'type': 'con'}),
]
G.add_edges_from(relationships)

# Function to evaluate norms
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

# Evaluate and print the final status of norms
final_status = evaluate_norms(G)
print(final_status)

# Add edges with pro and con labels
for relationship in relationships:
    G.add_edge(relationship[0], relationship[1], label=relationship[2]['type'])

# Create a PyVis network
net = Network(notebook=True, directed=True)

# Increase the size of the nodes
net.toggle_physics(True)  # Enable physics for better layout

# Convert NetworkX graph to PyVis
net.from_nx(G)

# Increase the size of the nodes
for node in net.nodes:
    node['size'] = 30  # Set a larger size for nodes so that the text fits inside

# Add edge labels for pro and con
for edge in net.edges:
    edge['title'] = edge['label']  # Add pro/con label to edge title for display

# Enable controls for zoom, and interaction buttons
net.show_buttons(filter_=['physics'])

# Set node shape to 'text' and font color to black with white background
for node in net.nodes:
    node['shape'] = 'text'  # Display nodes as text
    node['color'] = {
        'background': 'white',  # Set background to white for better contrast
        'border': 'white',     # Hide node border
        'highlight': {         # Maintain black font color on highlight
            'background': 'white',
            'border': 'white'
        }
    }
    node['font'] = {
        'color': 'black',    # Set font color to black
        'size': 20,          # Adjust font size as needed
        'background': 'white' # Add white background behind text
    }

# Set edge color to black and keep arrows
for edge in net.edges:
    edge['color'] = 'black'    # Set edge color to black
    # Keep the default arrow style or customize if needed:
    # edge['arrows'] = 'to'    # Example: Only arrow on the 'to' side


# Disable physics for a cleaner layout 
net.toggle_physics(False)

# Add in/out labels to conclusion nodes
for node in net.nodes:
    if node['id'] in conclusions:  # Check if the node is a conclusion node
        node['label'] += " (" + final_status[node['id']] + ")"  # Append status to label
        
# Show the network
net.show("network_with_physics.html")

# Download the HTML file in Google Colab to view in browser
from google.colab import files
files.download("network_with_physics.html")

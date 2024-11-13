import json
!pip install pyvis # installing the pyvis module
from pyvis.network import Network
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add conclusions as nodes
conclusions = ["N1 applies to Sam's case", "N2 applies to Sam's case"]
G.add_nodes_from(conclusions)

# Add reasons as nodes
reasons = ["F1: N1 is applicable to Sam's case", "F2: N2 is applicable to Sam's case", "F3: N2 is more specific than N1","F4: applying N2 to Sam's case violates the aims of IHL"]
G.add_nodes_from(reasons)

# Add relationships as edges with attributes for 'con' or 'pro'
relationships = [
    ("F1: N1 is applicable to Sam's case","N1 applies to Sam's case", {'type': 'pro'}),
    ("F1: N1 is applicable to Sam's case","N2 applies to Sam's case", {'type': 'con'}),
    ("F2: N2 is applicable to Sam's case","N1 applies to Sam's case", {'type': 'con'}),
    ("F2: N2 is applicable to Sam's case","N2 applies to Sam's case", {'type': 'pro'}),
    ("F3: N2 is more specific than N1","F2: N2 is applicable to Sam's case",{'type': 'pro'}),
    ("F3: N2 is more specific than N1","F1: N1 is applicable to Sam's case",{'type': 'con'}),
    ("F4: applying N2 to Sam's case violates the aims of IHL","F2: N2 is applicable to Sam's case",{'type': 'con'}),
    ("F4: applying N2 to Sam's case violates the aims of IHL","F1: N1 is applicable to Sam's case",{'type': 'pro'}),
    ]

G.add_edges_from(relationships)
def evaluate_norms(graph):
    # Start with all nodes as unknown, and update based on no cons or all cons
    status = {node: 'unknown' for node in graph}

    # Nodes with no incoming edges should be set to 'in'
    for node in graph:
        if not graph.predecessors(node):  # No incoming edges
            status[node] = 'in'
        # Nodes with only con edges and no pro should be 'out'
        elif all(graph[pred][node]['type'] == 'con' for pred in graph.predecessors(node)) and not any(graph[pred][node]['type'] == 'pro' for pred in graph.predecessors(node)):
            status[node] = 'out'

    changes = True
    while changes:
        changes = False
        new_status = status.copy()
        for node in graph:
            active = status[node] == 'in'
            for neighbor in graph[node]:
                edge_data = graph[node][neighbor]

                if edge_data['type'] == 'con' and active:
                    if new_status[neighbor] != 'out':
                        new_status[neighbor] = 'out'
                        changes = True
                elif edge_data['type'] == 'pro' and active:
                    if new_status[neighbor] != 'in':
                        if new_status[neighbor] == 'out':  # Conflict, set to 'unknown'
                            new_status[neighbor] = 'unknown'
                        else:
                            new_status[neighbor] = 'in'
                        changes = True

        status = new_status

    return status

# Evaluate and print the final status of norms
final_status = evaluate_norms(G)
print(final_status)

# MODIFICATIONS FROM HERE ONWARD

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

# ... (Your existing code for creating the network) ...

# Before net.show():

# 1. Set node shape to 'text' and font color to black with white background
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

# 2. Set edge color to black and keep arrows
for edge in net.edges:
    edge['color'] = 'black'    # Set edge color to black
    # Keep the default arrow style or customize if needed:
    # edge['arrows'] = 'to'    # Example: Only arrow on the 'to' side


# 3. Disable physics for a cleaner layout (optional)
net.toggle_physics(False)

# Add status labels to nodes
for node in net.nodes:
    node_id = node['id'] 
    if node_id in conclusions:  # Check if the node is a conclusion
        status = final_status.get(node_id, 'unknown')  
        node['label'] += f" ({status})"  # Append status to label


# ... (net.show() and files.download() as before) ...

# Show the network
net.show("network_with_physics.html")

# Download the HTML file in Google Colab to view in browser
from google.colab import files
files.download("network_with_physics.html")

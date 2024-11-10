import json
!pip install pyvis # installing the pyvis module
from pyvis.network import Network
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add conclusions as nodes
conclusions = ["N1 applies to Sam's Case", "N2 applies to Sam's Case"]
G.add_nodes_from(conclusions)

# Add reasons as nodes
reasons = ["F1: N1 is applicable to Sam's case", "F2: N2 is applicable to Sam's case"]
G.add_nodes_from(reasons)

# Add relationships as edges with attributes for 'con' or 'pro'
relationships = [
    ("F1: N1 is applicable to Sam's case","N1 applies to Sam's Case", {'type': 'pro'}),
    ("F1: N1 is applicable to Sam's case","N2 applies to Sam's Case", {'type': 'con'}),
    ("F2: N2 is applicable to Sam's case","N1 applies to Sam's Case", {'type': 'con'}),
    ("F2: N2 is applicable to Sam's case","N2 applies to Sam's Case", {'type': 'pro'}),
    ]

G.add_edges_from(relationships)

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


# ... (net.show() and files.download() as before) ...

# Show the network
net.show("network_with_physics.html")

# Download the HTML file in Google Colab to view in browser
from google.colab import files
files.download("network_with_physics.html")

import matplotlib.pyplot as plt
import networkx as nx
import os

def read_data(filename):
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' does not exist. Please run the C++ code first.")
        exit(1)
    with open(filename, 'r') as f:
        n = int(f.readline())  # Number of disks (nodes)
        disks = []
        for _ in range(n):
            x, y, r = map(float, f.readline().split())  # Read disk data (x, y, r)
            disks.append((x, y, r))
        m = int(f.readline())  # Number of edges
        edges = []
        for _ in range(m):
            u, v = map(int, f.readline().split())  # Read edges (connections)
            edges.append((u, v))
        _ = int(f.readline())                     # Clique size (not used here)
        clique_nodes = list(map(int, f.readline().split()))  # Read the nodes in the clique
    return disks, edges, clique_nodes

def plot_graph(disks, edges, clique_nodes):
    G = nx.Graph()
    
    # Add nodes and their positions
    for i in range(len(disks)):
        G.add_node(i, pos=(disks[i][0], disks[i][1]))

    # Add edges
    G.add_edges_from(edges)

    # Get positions of nodes
    pos = nx.get_node_attributes(G, 'pos')

    # Set node colors based on clique membership
    colors = ['red' if i in clique_nodes else 'skyblue' for i in G.nodes()]

    # Create plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw circles representing the disks (no conflict with edgecolor and facecolor)
    for i, (x, y, r) in enumerate(disks):
        circle = plt.Circle((x, y), r, facecolor=colors[i], edgecolor='black', alpha=0.5, lw=1)
        ax.add_artist(circle)

    # Draw the graph itself
    nx.draw(G, pos, node_color=colors, with_labels=True, ax=ax, edge_color='gray', node_size=500, font_size=12)

    # Dynamically adjust the plot limits to fit all disks (padding to avoid cutting off)
    min_x = min([d[0] - r for d, r in zip(disks, [disk[2] for disk in disks])])
    max_x = max([d[0] + r for d, r in zip(disks, [disk[2] for disk in disks])])
    min_y = min([d[1] - r for d, r in zip(disks, [disk[2] for disk in disks])])
    max_y = max([d[1] + r for d, r in zip(disks, [disk[2] for disk in disks])])

    # Add padding for better visibility
    padding = 5
    ax.set_xlim(min_x - padding, max_x + padding)
    ax.set_ylim(min_y - padding, max_y + padding)

    # Ensure equal aspect ratio and tight layout
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Maximum Clique Highlighted")

    # Show the plot
    plt.tight_layout()
    plt.show()

# Ensure you have the correct path to the file or it's in the same directory
filename = "graph_data.txt"
disks, edges, clique_nodes = read_data(filename)
plot_graph(disks, edges, clique_nodes)

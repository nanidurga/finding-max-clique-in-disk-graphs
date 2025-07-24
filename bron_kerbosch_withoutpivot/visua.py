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
            x, y, r = map(float, f.readline().split())  # Disk: (x, y, radius)
            disks.append((x, y, r))
        m = int(f.readline())  # Number of edges
        edges = []
        for _ in range(m):
            u, v = map(int, f.readline().split())  # Edge: (u, v)
            edges.append((u, v))
        _ = int(f.readline())  # Clique size (unused here)
        clique_nodes = list(map(int, f.readline().split()))  # Clique nodes
    return disks, edges, clique_nodes

def plot_graph(disks, edges, clique_nodes):
    G = nx.Graph()

    # Add nodes with positions
    for i, (x, y, _) in enumerate(disks):
        G.add_node(i, pos=(x, y))

    # Add edges
    G.add_edges_from(edges)

    pos = nx.get_node_attributes(G, 'pos')
    colors = ['red' if i in clique_nodes else 'skyblue' for i in G.nodes()]

    fig, ax = plt.subplots(figsize=(12, 12))

    # Draw disks as circles
    for i, (x, y, r) in enumerate(disks):
        circle = plt.Circle((x, y), r, facecolor=colors[i], edgecolor='black', alpha=0.5, lw=1)
        ax.add_patch(circle)

    # Draw edges and labels
    nx.draw(G, pos, node_color=colors, with_labels=True, ax=ax,
            edge_color='gray', node_size=500, font_size=8)

    # Add padding to limits to prevent cropping
    xs, ys, rs = zip(*disks)
    padding = 5
    min_x = min(x - r for x, r in zip(xs, rs)) - padding
    max_x = max(x + r for x, r in zip(xs, rs)) + padding
    min_y = min(y - r for y, r in zip(ys, rs)) - padding
    max_y = max(y + r for y, r in zip(ys, rs)) + padding

    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Maximum Clique Highlighted", fontsize=16)

    plt.subplots_adjust(left=0, right=1, top=0.95, bottom=0)

    # Maximize window (works for some backends like TkAgg)
    try:
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')
    except Exception:
        pass

    plt.show()

# Main execution
filename = "graph_data.txt"  # Ensure this file is in the current directory
disks, edges, clique_nodes = read_data(filename)
plot_graph(disks, edges, clique_nodes)

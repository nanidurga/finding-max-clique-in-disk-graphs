import matplotlib.pyplot as plt
import networkx as nx
import os

def read_data(filename):
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' does not exist. Please run the C++ code first.")
        exit(1)
    with open(filename, 'r') as f:
        n = int(f.readline())
        disks = []
        for _ in range(n):
            x, y, r = map(float, f.readline().split())
            disks.append((x, y, r))
        m = int(f.readline())
        edges = []
        for _ in range(m):
            u, v = map(int, f.readline().split())
            edges.append((u, v))
        _ = int(f.readline())
        clique_nodes = list(map(int, f.readline().split()))
    return disks, edges, clique_nodes

def plot_graph(disks, edges, clique_nodes):
    G = nx.Graph()

    for i in range(len(disks)):
        G.add_node(i, pos=(disks[i][0], disks[i][1]))
    G.add_edges_from(edges)
    pos = nx.get_node_attributes(G, 'pos')

    colors = ['red' if i in clique_nodes else 'skyblue' for i in G.nodes()]

    # Portrait-style figure (taller)
    fig, ax = plt.subplots(figsize=(6, 10))

    # Draw disks as circles
    for i, (x, y, r) in enumerate(disks):
        circle = plt.Circle((x, y), r, facecolor=colors[i], edgecolor='black', alpha=0.5, lw=1)
        ax.add_artist(circle)

    nx.draw(G, pos, node_color=colors, with_labels=True, ax=ax, edge_color='gray', node_size=500, font_size=12)

    # Auto-scale to fit disks with padding
    min_x = min([d[0] - d[2] for d in disks])
    max_x = max([d[0] + d[2] for d in disks])
    min_y = min([d[1] - d[2] for d in disks])
    max_y = max([d[1] + d[2] for d in disks])
    padding = 5
    ax.set_xlim(min_x - padding, max_x + padding)
    ax.set_ylim(min_y - padding, max_y + padding)

    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Maximum Clique Highlighted (Portrait View)")

    plt.tight_layout()
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    plt.show()

filename = "graph_data.txt"
disks, edges, clique_nodes = read_data(filename)
plot_graph(disks, edges, clique_nodes)

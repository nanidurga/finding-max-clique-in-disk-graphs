import random
import math
import itertools
import matplotlib.pyplot as plt
import networkx as nx
import time

# --------------------------------
# Random Disk Generation & Graph
# --------------------------------
def generate_random_disks(n, radius_range=(1.0, 1.5), coord_range=(0, 10)):
    disks = []
    for _ in range(n):
        x = random.uniform(*coord_range)
        y = random.uniform(*coord_range)
        r = random.uniform(*radius_range)
        disks.append((x, y, r))
    return disks

def disks_intersect(d1, d2):
    x1, y1, r1 = d1
    x2, y2, r2 = d2
    return math.hypot(x1 - x2, y1 - y2) <= r1 + r2

def build_intersection_graph(disks):
    G = nx.Graph()
    for i in range(len(disks)):
        G.add_node(i)
    for i in range(len(disks)):
        for j in range(i + 1, len(disks)):
            if disks_intersect(disks[i], disks[j]):
                G.add_edge(i, j)
    return G

# --------------------------------
# Maximum Clique Algorithms
# --------------------------------
def brute_force_max_clique(graph):
    nodes = list(graph.nodes)
    max_clique = []
    for r in range(1, len(nodes)+1):
        for subset in itertools.combinations(nodes, r):
            if all(graph.has_edge(u, v) or u == v for u in subset for v in subset):
                if len(subset) > len(max_clique):
                    max_clique = subset
    return list(max_clique)

def bron_kerbosch(R, P, X, graph, cliques):
    if not P and not X:
        cliques.append(R)
        return
    for v in list(P):
        bron_kerbosch(R.union({v}),
                      P.intersection(graph.neighbors(v)),
                      X.intersection(graph.neighbors(v)),
                      graph, cliques)
        P.remove(v)
        X.add(v)

def bron_kerbosch_pivot(R, P, X, graph, cliques):
    if not P and not X:
        cliques.append(R)
        return
    u = max(P.union(X), key=lambda v: len(set(graph.neighbors(v))), default=None)
    if u is None:
        u = next(iter(P), None)
    for v in P - set(graph.neighbors(u)):
        bron_kerbosch_pivot(R.union({v}),
                            P.intersection(graph.neighbors(v)),
                            X.intersection(graph.neighbors(v)),
                            graph, cliques)
        P.remove(v)
        X.add(v)

def branch_and_bound(graph):
    max_clique = []
    def expand(clique, candidates):
        nonlocal max_clique
        if not candidates:
            if len(clique) > len(max_clique):
                max_clique = list(clique)
            return
        for v in list(candidates):
            new_clique = clique + [v]
            new_candidates = [u for u in candidates if graph.has_edge(v, u)]
            expand(new_clique, new_candidates)
            candidates.remove(v)
    expand([], list(graph.nodes))
    return max_clique

# --------------------------------
# EPTAS for Maximum Clique
# --------------------------------
def eptas_max_clique(graph, epsilon=0.1):
    if len(graph) == 0:
        return []
    
    positions = nx.spring_layout(graph, seed=42)
    k = int(1 / epsilon) + 1
    cells = {}

    for node, (x, y) in positions.items():
        cell = (int(k * x), int(k * y))
        if cell not in cells:
            cells[cell] = []
        cells[cell].append(node)

    max_clique = []
    for cell_nodes in cells.values():
        subgraph = graph.subgraph(cell_nodes)
        cliques = []
        bron_kerbosch(set(), set(subgraph.nodes), set(), subgraph, cliques)
        if cliques:
            largest = max(cliques, key=len)
            if len(largest) > len(max_clique):
                max_clique = list(largest)
    return max_clique

# --------------------------------
# Multiple Test Cases & Comparison
# --------------------------------
def run_multiple_tests(num_tests=1000):
    summary = {
        "Brute Force": {"sizes": [], "times": []},
        "Bron-Kerbosch": {"sizes": [], "times": []},
        "Bron-Kerbosch + Pivot": {"sizes": [], "times": []},
        "Branch and Bound": {"sizes": [], "times": []},
        "EPTAS": {"sizes": [], "times": []},
    }

    for test in range(1, num_tests + 1):
        num_disks = random.randint(5, 18)
        disks = generate_random_disks(num_disks)
        G = build_intersection_graph(disks)

        # Brute Force
        start_time = time.time()
        clique_bf = brute_force_max_clique(G)
        end_time = time.time()
        summary["Brute Force"]["sizes"].append(len(clique_bf))
        summary["Brute Force"]["times"].append(end_time - start_time)

        # Bron-Kerbosch
        start_time = time.time()
        cliques_bk = []
        bron_kerbosch(set(), set(G.nodes), set(), G, cliques_bk)
        max_bk = max(cliques_bk, key=len) if cliques_bk else []
        end_time = time.time()
        summary["Bron-Kerbosch"]["sizes"].append(len(max_bk))
        summary["Bron-Kerbosch"]["times"].append(end_time - start_time)

        # Bron-Kerbosch with Pivot
        start_time = time.time()
        cliques_bkp = []
        bron_kerbosch_pivot(set(), set(G.nodes), set(), G, cliques_bkp)
        max_bkp = max(cliques_bkp, key=len) if cliques_bkp else []
        end_time = time.time()
        summary["Bron-Kerbosch + Pivot"]["sizes"].append(len(max_bkp))
        summary["Bron-Kerbosch + Pivot"]["times"].append(end_time - start_time)

        # Branch and Bound
        start_time = time.time()
        clique_bb = branch_and_bound(G)
        end_time = time.time()
        summary["Branch and Bound"]["sizes"].append(len(clique_bb))
        summary["Branch and Bound"]["times"].append(end_time - start_time)

        # EPTAS
        start_time = time.time()
        clique_eptas = eptas_max_clique(G, epsilon=0.1)
        end_time = time.time()
        summary["EPTAS"]["sizes"].append(len(clique_eptas))
        summary["EPTAS"]["times"].append(end_time - start_time)

        if test % 50 == 0:
            print(f"Completed {test}/{num_tests} tests.")

    return summary

# --------------------------------
# Visualization
# --------------------------------
def plot_results(summary):
    labels = []
    avg_sizes = []
    avg_times = []
    
    # Only plot non-empty data
    for method, data in summary.items():
        if data["sizes"]:  # skip methods with empty data
            labels.append(method)
            avg_sizes.append(sum(data["sizes"]) / len(data["sizes"]))
            avg_times.append(sum(data["times"]) / len(data["times"]))

    # Bar Chart - Average Sizes
    plt.figure(figsize=(10, 6))
    plt.bar(labels, avg_sizes, color='skyblue')
    plt.ylabel("Average Max Clique Size")
    plt.title("Average Maximum Clique Size Across Test Cases")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()

    # Bar Chart - Average Runtimes
    plt.figure(figsize=(10, 6))
    plt.bar(labels, avg_times, color='lightcoral')
    plt.ylabel("Average Runtime (Seconds)")
    plt.title("Average Runtime Across Test Cases")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()

    # Box Plot - Distribution of Sizes
    plt.figure(figsize=(10, 6))
    plt.boxplot([summary[method]["sizes"] for method in labels], tick_labels=labels, patch_artist=True)
    plt.ylabel("Max Clique Size")
    plt.title("Distribution of Maximum Clique Sizes")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()

    # Box Plot - Distribution of Runtimes
    plt.figure(figsize=(10, 6))
    plt.boxplot([summary[method]["times"] for method in labels], tick_labels=labels, patch_artist=True)
    plt.ylabel("Runtime (Seconds)")
    plt.title("Distribution of Runtimes")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()

# --------------------------------
# Main
# --------------------------------
if __name__ == "__main__":
    summary = run_multiple_tests(num_tests=1000)
    plot_results(summary)

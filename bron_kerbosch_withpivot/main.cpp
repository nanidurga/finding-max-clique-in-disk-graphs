// bron_kerbosch_with_pivot_random_print_nodes.cpp

#include <iostream>
#include <vector>
#include <set>
#include <cmath>
#include <fstream>
#include <algorithm>
#include <cstdlib>
#include <ctime>

using namespace std;

struct Disk {
    double x, y, r;
};

vector<Disk> disks;
vector<vector<int>> adj;
vector<int> max_clique;

bool intersect(Disk a, Disk b) {
    double dx = a.x - b.x, dy = a.y - b.y;
    double dist = sqrt(dx * dx + dy * dy);
    return dist <= (a.r + b.r);
}

void bronKerboschPivot(set<int> R, set<int> P, set<int> X) {
    if (P.empty() && X.empty()) {
        if (R.size() > max_clique.size()) {
            max_clique.assign(R.begin(), R.end());
        }
        return;
    }

    set<int> union_PX = P;
    union_PX.insert(X.begin(), X.end());
    int u = -1;
    if (!union_PX.empty()) {
        u = *union_PX.begin();
    }

    set<int> P_without_neighbors;
    for (int v : P) {
        if (u == -1 || find(adj[u].begin(), adj[u].end(), v) == adj[u].end()) {
            P_without_neighbors.insert(v);
        }
    }

    for (int v : P_without_neighbors) {
        set<int> newR = R, newP, newX;
        newR.insert(v);

        for (int w : adj[v]) {
            if (P.count(w)) newP.insert(w);
            if (X.count(w)) newX.insert(w);
        }

        bronKerboschPivot(newR, newP, newX);
        P.erase(v);
        X.insert(v);
    }
}

int main() {
    srand(time(0)); // Random seed

    int n;
    cout << "Enter number of disks: ";
    cin >> n;
    disks.resize(n);

    // Randomly generate disks and print nodes
    cout << "\nGenerated Disks:" << endl;
    for (int i = 0; i < n; ++i) {
        disks[i].x = rand() % 1000 / 10.0;    // x between 0 to 100
        disks[i].y = rand() % 1000 / 10.0;    // y between 0 to 100
        disks[i].r = 1 + rand() % 50 / 10.0;  // radius between 1.0 and 6.0
        cout << "Node " << i << ": (" << disks[i].x << ", " << disks[i].y << ", " << disks[i].r << ")" << endl;
    }

    // Build adjacency list
    adj.resize(n);
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (intersect(disks[i], disks[j])) {
                adj[i].push_back(j);
                adj[j].push_back(i);
            }
        }
    }

    set<int> R, P, X;
    for (int i = 0; i < n; ++i) P.insert(i);

    bronKerboschPivot(R, P, X);

    // Save graph to file
    ofstream outfile("graph_data.txt");

    outfile << n << endl;
    for (auto d : disks) {
        outfile << d.x << " " << d.y << " " << d.r << endl;
    }

    int edge_count = 0;
    for (int i = 0; i < n; ++i)
        for (int j : adj[i])
            if (i < j)
                edge_count++;
    outfile << edge_count << endl;

    for (int i = 0; i < n; ++i)
        for (int j : adj[i])
            if (i < j)
                outfile << i << " " << j << endl;

    outfile << max_clique.size() << endl;
    for (int v : max_clique)
        outfile << v << " ";
    outfile << endl;

    outfile.close();

    cout << "\nRandom disks generated and saved to 'graph_data.txt'." << endl;
    cout << "Maximum clique size: " << max_clique.size() << endl;
    cout << "Nodes in maximum clique: ";
    for (auto v : max_clique) cout << v << " ";
    cout << endl;
}

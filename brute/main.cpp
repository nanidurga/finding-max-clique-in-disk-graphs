#include <iostream>
#include <vector>
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
vector<int> best_clique;

// Check if two disks intersect
bool intersect(const Disk &a, const Disk &b) {
    double dx = a.x - b.x, dy = a.y - b.y;
    return sqrt(dx * dx + dy * dy) <= (a.r + b.r);
}

// Check if a set of nodes forms a clique
bool isClique(const vector<int> &subset) {
    for (int i = 0; i < (int)subset.size(); ++i) {
        for (int j = i + 1; j < (int)subset.size(); ++j) {
            int u = subset[i], v = subset[j];
            if (find(adj[u].begin(), adj[u].end(), v) == adj[u].end())
                return false;
        }
    }
    return true;
}

int main() {
    srand(time(nullptr));
    int n;
    cout << "Enter number of disks (<= 20 recommended): ";
    cin >> n;

    disks.resize(n);
    adj.assign(n, {});

    // 1. Generate random disks
    cout << "\nGenerated Disks:\n";
    for (int i = 0; i < n; ++i) {
        disks[i].x = (rand() % 1000) / 10.0;      // [0, 100)
        disks[i].y = (rand() % 1000) / 10.0;      // [0, 100)
        disks[i].r = 1.0 + (rand() % 50) / 10.0;  // [1.0, 6.0)
        cout << "Node " << i << ": (" << disks[i].x << ", "
             << disks[i].y << ", " << disks[i].r << ")\n";
    }

    // 2. Build graph
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (intersect(disks[i], disks[j])) {
                adj[i].push_back(j);
                adj[j].push_back(i);
            }
        }
    }

    // 3. Brute force all subsets to find max clique
    int total_subsets = 1 << n;
    for (int mask = 1; mask < total_subsets; ++mask) {
        vector<int> subset;
        for (int i = 0; i < n; ++i)
            if (mask & (1 << i))
                subset.push_back(i);

        if (isClique(subset) && subset.size() > best_clique.size()) {
            best_clique = subset;
        }
    }

    // 4. Save to graph_data.txt
    ofstream fout("graph_data.txt");
    fout << n << "\n";
    for (auto &d : disks)
        fout << d.x << " " << d.y << " " << d.r << "\n";

    int edge_count = 0;
    for (int i = 0; i < n; ++i)
        for (int j : adj[i])
            if (i < j) ++edge_count;
    fout << edge_count << "\n";
    for (int i = 0; i < n; ++i)
        for (int j : adj[i])
            if (i < j)
                fout << i << " " << j << "\n";

    fout << best_clique.size() << "\n";
    for (int v : best_clique)
        fout << v << " ";
    fout << "\n";
    fout.close();

    // 5. Console output
    cout << "\nSaved graph_data.txt (" << n << " disks, "
         << edge_count << " edges).\n";
    cout << "Maximum Clique Size: " << best_clique.size()
         << "\nNodes: ";
    for (int v : best_clique)
        cout << v << " ";
    cout << "\n";

    return 0;
}

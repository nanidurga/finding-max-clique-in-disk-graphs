// eptas_random_clique.cpp

#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <set>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <numeric>
#include <random> // for std::shuffle

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
    return sqrt(dx*dx + dy*dy) <= (a.r + b.r);
}

// Check if a set of nodes forms a clique
bool isClique(const set<int> &S) {
    for (int u : S) {
        for (int v : S) {
            if (u < v) {
                // If u and v are not connected, it is not a clique
                if (find(adj[u].begin(), adj[u].end(), v) == adj[u].end())
                    return false;
            }
        }
    }
    return true;
}

int main() {
    srand((unsigned)time(nullptr));

    int n;
    cout << "Enter number of disks: ";
    cin >> n;
    disks.resize(n);
    adj.assign(n, {});

    // 1) Generate random disks
    cout << "\nGenerated Disks:\n";
    for (int i = 0; i < n; ++i) {
        disks[i].x = (rand() % 1000) / 10.0;      // [0,100)
        disks[i].y = (rand() % 1000) / 10.0;      // [0,100)
        disks[i].r = 1.0 + (rand() % 50) / 10.0;  // [1.0,6.0)
        cout << "Node " << i
             << ": (" << disks[i].x
             << ", " << disks[i].y
             << ", " << disks[i].r << ")\n";
    }

    // 2) Build graph
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (intersect(disks[i], disks[j])) {
                adj[i].push_back(j);
                adj[j].push_back(i);
            }
        }
    }

    // 3) EPTAS parameters
    double eps = 0.1, beta = 0.5;
    double c = 8 * (1.0 / (beta * eps) * 1.0 / (beta * eps) + 1.0 / (beta * eps) + 1);
    double delta = eps / c;
    int s = max(1, int(10.0 * n / (delta * log(1.0 / delta))));

    // limit s not to be more than n
    s = min(s, n);

    // 4) Randomized sampling
    vector<int> nodes(n);
    iota(nodes.begin(), nodes.end(), 0);

    std::random_device rd;
    std::mt19937 g(rd());

    for (int iter = 0; iter < 100; ++iter) {  // More trials for better chance
        std::shuffle(nodes.begin(), nodes.end(), g);

        set<int> sample;
        for (int i = 0; i < n; ++i) {
            bool can_add = true;
            for (int u : sample) {
                // u and nodes[i] must be connected
                if (find(adj[u].begin(), adj[u].end(), nodes[i]) == adj[u].end()) {
                    can_add = false;
                    break;
                }
            }
            if (can_add) sample.insert(nodes[i]);
            if ((int)sample.size() >= s) break;
        }

        if ((int)sample.size() > (int)best_clique.size()) {
            best_clique.assign(sample.begin(), sample.end());
        }
    }

    // 5) Write graph_data.txt
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
    for (int v : best_clique) fout << v << " ";
    fout << "\n";
    fout.close();

    // 6) Console summary
    cout << "\nSaved graph_data.txt (" << n << " disks, "
         << edge_count << " edges).\n";
    cout << "Approximate clique size: " 
         << best_clique.size() << "\nNodes: ";
    for (int v : best_clique) cout << v << " ";
    cout << endl;

    return 0;
}

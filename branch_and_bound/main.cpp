#include <iostream>
#include <vector>
#include <set>
#include <cmath>
#include <fstream>
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

// Branch and Bound for Maximum Clique
void branchAndBound(set<int> current, set<int> candidates, set<int> excluded) {
    if (candidates.empty() && excluded.empty()) {
        if (current.size() > max_clique.size()) {
            max_clique.assign(current.begin(), current.end());
        }
        return;
    }

    set<int> candidates_copy = candidates;
    for (int v : candidates_copy) {
        set<int> new_current = current;
        new_current.insert(v);
        set<int> new_candidates, new_excluded;

        // Update candidates and excluded sets
        for (int w : adj[v]) {
            if (candidates.count(w)) new_candidates.insert(w);
            if (excluded.count(w)) new_excluded.insert(w);
        }

        branchAndBound(new_current, new_candidates, new_excluded);
        candidates.erase(v);
        excluded.insert(v);

        // Pruning condition: If the size of current clique plus the remaining candidates is less than the current max_clique, stop exploring
        if (new_current.size() + candidates.size() <= max_clique.size()) {
            return;
        }
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

    set<int> current, candidates, excluded;
    for (int i = 0; i < n; ++i) candidates.insert(i);

    branchAndBound(current, candidates, excluded);

    // Save graph to file
    ofstream outfile("graph_data.txt");

    outfile << n << endl;
    for (auto d : disks) {
        outfile << d.x << " " << d.y << " " << d.r << endl;
    }

    // Correct edge counting (only count edges once)
    int edge_count = 0;
    for (int i = 0; i < n; ++i)
        for (int j : adj[i])
            if (i < j)  // Only count edges where i < j to avoid double-counting
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

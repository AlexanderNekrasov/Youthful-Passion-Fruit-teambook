/**
 * Author: Iurii Pustovalov
 * Date: ?
 * Description: Min cost
 * Time: O(?)
 */

struct MCMF {
    struct edge {
        int a, b, cap, cost;
    };
    vector<edge> e;
    vector<vector<int>> g;
    int s, t;
    int n;
    void init(int N, int S, int T) {
        s = S, t = T, n = N;
        g.assign(N, {});
        e.clear();
    }
    void addedge(int a, int b, int cap, int cost) {
        g[a].pbc(e.size());
        e.pbc({a, b, cap, cost});
        g[b].pbc(e.size());
        e.pbc({b, a, 0, -cost});
    }
    int getcost(int k) {
        int flow = 0;
        int cost = 0;
        while (flow < k) {
            vector<int> d(n, INF);
            vector<int> pr(n);
            vector<bool> inq(n, false);
            d[s] = 0;
            queue<int> q;
            q.push(s);
            inq[s] = true;
            while (q.size()) {
                int v = q.front();
                q.pop();
                inq[v] = false;
                for (int i : g[v]) {
                    int u = e[i].b;
                    if (e[i].cap && d[u] > d[v] + e[i].cost) {
                        d[u] = d[v] + e[i].cost;
                        if (!inq[u]) q.push(u), inq[u] = true;
                        pr[u] = i;
                    }
                }
            }
            if (d[t] == INF) return INF;
            int gf = k - flow;
            int v = t;
            while (v != s) {
                int id = pr[v];
                chkmin(gf, e[id].cap);
                v = e[id].a;
            }
            v = t;
            while (v != s) {
                int id = pr[v];
                e[id].cap -= gf;
                e[id ^ 1].cap += gf;
                cost += e[id].cost * gf;
                v = e[id].a;
            }
            flow += gf;
        }
        return cost;
    }
};

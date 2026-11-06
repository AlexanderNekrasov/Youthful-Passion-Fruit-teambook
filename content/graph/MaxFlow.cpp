/**
 * Author: Iurii Pustovalov
 * Date: ?
 * Description: Dinic
 * Time: O(n^2 m)
 */

struct MaxFlow {
    const int inf = 1e9 + 20;
    struct edge {
        int a, b, cap;
    };
    int n;
    vector<edge> e;
    vector<vector<int>> g;
    MaxFlow() {}
    int s, t;
    vector<int> d, ptr;
    void init(int n_, int s_, int t_) {
        s = s_, t = t_, n = n_;
        e.clear();
        g.assign(n, {});
        ptr.resize(n);
    }
    void addedge(int a, int b, int cap) {
        g[a].pbc(e.size());
        e.pbc({a, b, cap});
        g[b].pbc(e.size());
        e.pbc({b, a, 0});
    }
    bool bfs() {
        d.assign(n, inf);
        d[s] = 0;
        queue<int> q;
        q.push(s);
        while (q.size()) {
            int v = q.front();
            q.pop();
            for (int i : g[v]) {
                if (e[i].cap > 0) {
                    int b = e[i].b;
                    if (d[b] > d[v] + 1) {
                        d[b] = d[v] + 1;
                        q.push(b);
                    }
                }
            }
        }
        return d[t] != inf;
    }
    int dfs(int v, int flow) {
        if (v == t) return flow;
        if (!flow) return 0;
        int sum = 0;
        for (; ptr[v] < g[v].size(); ++ptr[v]) {
            int b = e[g[v][ptr[v]]].b;
            int cap = e[g[v][ptr[v]]].cap;
            if (cap <= 0) continue;
            if (d[b] != d[v] + 1) continue;
            int x = dfs(b, min(flow, cap));
            int id = g[v][ptr[v]];
            e[id].cap -= x;
            e[id ^ 1].cap += x;
            flow -= x;
            sum += x;
            if (!flow) return sum; // preserve the current residual edge
        }
        return sum;
    }
    int dinic() {
        int ans = 0;
        while (1) {
            if (!bfs()) break;
            ptr.assign(n, 0);
            while (int x = dfs(s, inf)) ans += x;
        }
        return ans;
    }
};

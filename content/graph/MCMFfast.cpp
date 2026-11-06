/**
 * Author: Alexey Vasilyev
 * Date: ?
 * Description: Min cost with potentials
 * Time: O(?)
 */

struct MCMF {
  struct edge {
    int a, b, cap, cost;
  };
  vector<edge> e;
  vector<vector<int>> g;
  vector<ll> po;
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
  void calc_p() {
    po.assign(n, INF);
    vector<int> inq(n);
    queue<int> q;
    q.push(s);
    po[s] = 0;
    while (!q.empty()) {
      int v = q.front();
      q.pop();
      inq[v] = 0;
      for (auto i : g[v]) {
        if (po[e[i].b] > po[v] + e[i].cost && e[i].cap) {
          po[e[i].b] = po[v] + e[i].cost;
          if (!inq[e[i].b]) q.push(e[i].b);
          inq[e[i].b] = 1;
        }
      }
    }
  }
  ll getcost(int k) {
    calc_p();
    int flow = 0;
    ll cost = 0;
    while (flow < k) {
      vector<ll> d(n, INF);
      vector<int> pr(n);
      d[s] = 0;
      set<pair<ll, int>> q;
      q.insert(mp(0ll, s));
      while (q.size()) {
        int v = q.begin()->second;
        q.erase(q.begin());
        for (int i : g[v]) {
          int u = e[i].b;
          if (e[i].cap && d[u] > d[v] + e[i].cost + po[v] - po[e[i].b]) {
            q.erase(mp(d[u], u));
            d[u] = d[v] + e[i].cost + po[v] - po[e[i].b];
            q.insert(mp(d[u], u));
            pr[u] = i;
          }
        }
      }
      if (d[t] == INF) return INF;
      for (int i = 0; i < n; ++i) {
        if (d[i] != INF) po[i] += d[i];
      }
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
        cost += 1ll * e[id].cost * gf;
        v = e[id].a;
      }
      flow += gf;
    }
    return cost;
  }
};
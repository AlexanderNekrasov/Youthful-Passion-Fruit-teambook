/**
 * Author: alexxela12345
 * Date: 2024-09-14
 * Description: Point location xd
 */
const vec arb = {(int)1e9 + 228, (int)1e9 + 228}; // ne sovpadaet s drygimi tochkami

bool ge(const ll& a, const ll& b) { return a >= b; }
bool le(const ll& a, const ll& b) { return a <= b; }
bool eq(const ll& a, const ll& b) { return a == b; }
bool gt(const ll& a, const ll& b) { return a > b; }
bool lt(const ll& a, const ll& b) { return a < b; }

ll vec::dot(const vec &a)const {
  return *this * a;
}
ll vec::cross(const vec &a) const {
  return *this % a;
}
ll vec::dot(const vec &a, const vec &b) const {
  return (a - *this) * (b - *this);
}
ll vec::cross(const vec &a, const vec &b) const {
  return (a - *this) % (b - *this);
}

struct Edge {
    vec l, r;
    auto operator<=>(const Edge &) const = default;
};

bool edge_cmp(const Edge& edge1, const Edge& edge2)
{
    const vec a = edge1.l, b = edge1.r;
    const vec c = edge2.l, d = edge2.r;
    int val = sign(a.cross(b, c)) + sign(a.cross(b, d));
    if (val != 0)
        return val > 0;
    val = sign(c.cross(d, a)) + sign(c.cross(d, b));
    return val < 0;
}

enum EventType { DEL = 2, ADD = 3, GET = 1, VERT = 0 };

struct Event {
    EventType type;
    int pos;
    bool operator<(const Event& event) const { return type < event.type; }
};

vector<Edge> sweepline(vector<Edge> planar, vector<vec> queries)
{
    using vec_type = decltype(vec::x);

    // collect all x-coordinates
    auto s =
        set<vec_type, std::function<bool(const vec_type&, const vec_type&)>>(lt);
    for (vec p : queries)
        s.insert(p.x);
    for (auto e : planar) {
        s.insert(e.l.x);
        s.insert(e.r.x);
    }

    // map all x-coordinates to ids
    int cid = 0;
    auto id =
        map<vec_type, int, std::function<bool(const vec_type&, const vec_type&)>>(
            lt);
    for (auto x : s)
        id[x] = cid++;

    // create events
    auto t = set<Edge, decltype(*edge_cmp)>(edge_cmp);
    auto vert_cmp = [](const pair<vec_type, int>& l,
                       const pair<vec_type, int>& r) {
        if (!eq(l.first, r.first))
            return lt(l.first, r.first);
        return l.second < r.second;
    };
    auto vert = set<pair<vec_type, int>, decltype(vert_cmp)>(vert_cmp);
    vector<vector<Event>> events(cid);
    for (int i = 0; i < (int)queries.size(); i++) {
        int x = id[queries[i].x];
        events[x].push_back(Event{GET, i});
    }
    for (int i = 0; i < (int)planar.size(); i++) {
        int lx = id[planar[i].l.x], rx = id[planar[i].r.x];
        if (lx > rx) {
            swap(lx, rx);
            swap(planar[i].l, planar[i].r);
        }
        if (lx == rx) {
            events[lx].push_back(Event{VERT, i});
        } else {
            events[lx].push_back(Event{ADD, i});
            events[rx].push_back(Event{DEL, i});
        }
    }

    // perform sweep line algorithm
    vector<Edge> ans(queries.size(), {arb, arb});
    for (int x = 0; x < cid; x++) {
        sort(events[x].begin(), events[x].end());
        vert.clear();
        for (Event event : events[x]) {
            if (event.type == DEL) {
                t.erase(planar[event.pos]);
            }
            if (event.type == VERT) {
                vert.insert(make_pair(
                    min(planar[event.pos].l.y, planar[event.pos].r.y),
                    event.pos));
            }
            if (event.type == ADD) {
                t.insert(planar[event.pos]);
            }
            if (event.type == GET) {
                auto jt = vert.upper_bound(
                    make_pair(queries[event.pos].y, planar.size()));
                if (jt != vert.begin()) {
                    --jt;
                    int i = jt->second;
                    if (ge(max(planar[i].l.y, planar[i].r.y),
                           queries[event.pos].y)) {
                        ans[event.pos] = planar[i];
                        continue;
                    }
                }
                Edge e;
                e.l = e.r = queries[event.pos];
                auto it = t.upper_bound(e);
                if (it != t.begin()) {
                    ans[event.pos] = *(--it);
                }
            }
        }

        for (Event event : events[x]) {
            if (event.type != GET)
                continue;
            if (ans[event.pos].l != arb &&
                eq(ans[event.pos].l.x, ans[event.pos].r.x))
                continue;

            Edge e;
            e.l = e.r = queries[event.pos];
            auto it = t.upper_bound(e);
            if (it == t.begin()) 
                e = {arb, arb};
            else
                e = *(--it);
            if (ans[event.pos].l == arb) {
                ans[event.pos] = e;
                continue;
            }
            if (e.l == arb)
                continue;
            if (e == ans[event.pos])
                continue;
            if (id[ans[event.pos].r.x] == x) {
                if (id[e.l.x] == x) {
                    if (gt(e.l.y, ans[event.pos].r.y))
                        ans[event.pos] = e;
                }
            } else {
                ans[event.pos] = e;
            }
        }
    }
    return ans;
}

struct DCEL {
    struct Edge {
        vec origin;
        int nxt;
        int twin;
        int face;
    };
    vector<Edge> body;
};
// outer face is -1, returns (1,i) is point is strictly inside face i,
// and (0,1) if point lies on the edge i
vector<pair<int, int>> point_location(DCEL planar, vector<vec> queries)
{
    vector<pair<int, int>> ans(queries.size());
    vector<Edge> planar2;
    map<Edge, int> pos;
    map<Edge, int> added_on;
    int n = planar.body.size();
    for (int i = 0; i < n; i++) {
        if (planar.body[i].face > planar.body[planar.body[i].twin].face)
            continue;
        Edge e;
        e.l = planar.body[i].origin;
        e.r = planar.body[planar.body[i].twin].origin;
        if (e.r.x < e.l.x) swap(e.l, e.r);
        added_on[e] = i;
        pos[e] =
            lt(planar.body[i].origin.x, planar.body[planar.body[i].twin].origin.x)
                ? planar.body[i].face
                : planar.body[planar.body[i].twin].face;
        planar2.push_back(e);
    }
    auto res = sweepline(planar2, queries);
    for (int i = 0; i < (int)queries.size(); i++) {
        if (res[i].l == arb) {
            ans[i] = make_pair(1, -1);
            continue;
        }
        vec p = queries[i];
        vec l = res[i].l, r = res[i].r;
        if (eq(p.cross(l, r), 0) && le(p.dot(l, r), 0)) {
            ans[i] = make_pair(0, added_on[res[i]]);
            continue;
        }
        ans[i] = make_pair(1, pos[res[i]]);
    }
    return ans;
}
DCEL buildDCEL(const vector<vec> &pts, const vector<vector<int>> &g) {
    int n = g.size();
    vector<vector<pair<int, int>>> g2(n);
    int cur_edge = 0;
    for (int i = 0; i < n; ++i) {
        for (int j : g[i]) {
            if (i < j) {
                g2[j].pbc({i, cur_edge});
                g2[i].pbc({j, cur_edge ^ 1});
                cur_edge += 2;
            }
        }
    }    
    vector<int> ind(cur_edge), used(cur_edge);
    for (int i = 0; i < n; ++i) {
        sort(all(g2[i]), [&](auto a, auto b) {
            auto va = pts[a.first] - pts[i];
            auto vb = pts[b.first] - pts[i];
            return mp(half(va), 0LL) < mp(half(vb), va % vb);
        });
        for (int j = 0; j < (int) g2[i].size(); ++j) {
            ind[g2[i][j].second] = j;
        }
    }
    using Edge = DCEL::Edge;
    vector<Edge> edges(cur_edge);
    for (int i = 0; i < cur_edge; ++i) {
      edges[i].twin = i ^ 1;
    }
    int cur_face = 0;
    for (int i = 0; i < n; ++i) {
        for (int ei = 0; ei < (int)g[i].size(); ++ei) {
            if (used[g2[i][ei].second]) continue;
            vector<vec> face;
            vector<int> inds;
            int v = i;
            int e = g2[v][ei].second;
            while (!used[e]) {
                edges[e].origin = pts[v];
                edges[e].face = cur_face;
                inds.pbc(e);
                used[e] = 1;
                face.pbc(pts[v]);
                int u = g2[v][ind[e]].first;
                int newe = g2[u][(ind[e ^ 1] - 1 + g2[u].size()) % g2[u].size()].second;
                edges[e].nxt = newe;
                v = u;
                e = newe;
            }
            if (sign(get_area(face)) <= 0) {
              for (int i : inds) {
                edges[i].face = -1;
              }
            } else {
              ++cur_face;
            }
        }
    }
    return {edges};
}
/**
 * Author: talant
 * Date: 2024-09-09
 * Description: Hull in arbitrary number of dimensions
 * Time: O(N*Dim*Hull)
 */
const int DIM = 4;
typedef array<ll, DIM> pt;
pt operator-(const pt &a, const pt &b) {
  pt res;
  forn(i, DIM) res[i] = a[i] - b[i];
  return res;
}
typedef array<pt, DIM - 1> Edge;
typedef array<pt, DIM> Face;
vector<Face> faces;
ll det(pt *a) {
  int p[DIM];
  iota(p, p + DIM, 0);
  ll res = 0;
  do {
    ll x = 1;
    forn(i, DIM) {
      forn(j, i) if (p[j] > p[i]) x *= -1;
      x *= a[i][p[i]];
    }
    res += x;
  } while (next_permutation(p, p + DIM));
  return res;
}
ll V(Face f, pt pivot) {
  pt p[DIM];
  forn(i, DIM) p[i] = f[i] - pivot;
  return det(p);
}
void init(vector<pt> p) {
  forn(i, DIM + 1) {
    Face a;
    int q = 0;
    forn(j, DIM + 1) if (j != i) a[q++] = p[j];
    ll v = V(a, p[i]);
    assert(v != 0);
    if (v < 0) swap(a[0], a[1]);
    faces.push_back(a);
  }
}
void add(pt p) {
  vector<Face> newf, bad;
  for (auto f : faces) {
    if (V(f, p) < 0)
      bad.push_back(f);
    else
      newf.push_back(f);
  }
  if (bad.empty()) {
    cout << " Ignore \n";
    return;
  }
  cout << " Rebuild \n";
  faces = newf;
  vector<pair<Edge, pt>> edges;
  for (auto f : bad) {
    sort(all(f));
    forn(i, DIM) {
      Edge e;
      int q = 0;
      forn(j, DIM) if (i != j) e[q++] = f[j];
      edges.emplace_back(e, f[i]);
    }
  }
  sort(all(edges));
  forn(i, sz(edges)) {
    if (i + 1 < sz(edges) && edges[i + 1].first == edges[i].first) {
      ++i;
      continue;
    }
    Face f;
    forn(j, DIM - 1) f[j] = edges[i].first[j];
    f[DIM - 1] = p;
    if (V(f, edges[i].second) < 0) swap(f[0], f[1]);
    faces.push_back(f);
  }
}
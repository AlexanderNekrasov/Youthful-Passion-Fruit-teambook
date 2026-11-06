/**
 * Author: talant
 * Date: 2024-09-09
 * Description: Hull in arbitrary number of dimensions
 * Time: O(N * (Dim! * Dim^2 * Hull + Dim^2 * Hull * log(Dim * Hull)))
 * For DIM=4, require |coordinate| <= 1e8 (128-bit orientation).
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
__int128 det(pt *a) {
  int p[DIM];
  iota(p, p + DIM, 0);
  __int128 res = 0;
  do {
    __int128 x = 1;
    forn(i, DIM) {
      forn(j, i) if (p[j] > p[i]) x *= -1;
      x *= a[i][p[i]];
    }
    res += x;
  } while (next_permutation(p, p + DIM));
  return res;
}
__int128 V(Face f, pt pivot) {
  pt p[DIM];
  forn(i, DIM) p[i] = f[i] - pivot;
  return det(p);
}
void init(vector<pt> p) {
  assert(p.size() >= DIM + 1);
  faces.clear();
  forn(i, DIM + 1) {
    Face a;
    int q = 0;
    forn(j, DIM + 1) if (j != i) a[q++] = p[j];
    auto v = V(a, p[i]);
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
    return;
  }
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
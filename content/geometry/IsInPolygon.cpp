/**
 * Author: Igor Markelov
 * Date: 2022-11-18
 * Description: Is in polygon functions
 */

bool isOnSegment(const point &a, const point &b, const point &x) {
    ld length = len(b - a);
    if (length <= EPS) return len(x - a) <= EPS;
    ld projection = (x - a) * ((b - a) / length);
    return abs((b - a) % (x - a)) <= EPS * length &&
           projection >= -EPS && projection <= length + EPS;
}

// 0 outside, 1 boundary, 2 inside. Either polygon orientation is allowed.
int isIn(vector<point> &p, point &a) {
    int winding = 0, n = p.size();
    for (int i = 0; i < n; ++i) {
        const point &x = p[i], &y = p[(i + 1) % n];
        if (isOnSegment(x, y, a)) return 1;
        ld cross = (y - x) % (a - x);
        if (x.y <= a.y && a.y < y.y && cross > 0) ++winding;
        if (y.y <= a.y && a.y < x.y && cross < 0) --winding;
    }
    return winding != 0 ? 2 : 0;
}

bool isInTriangle(point &a, point &b, point &c, point &x) {
    if (sign((b - a) % (c - a)) == 0)
        return isOnSegment(a, b, x) || isOnSegment(b, c, x) || isOnSegment(c, a, x);
    return sign((b - a) % (x - a)) >= 0 && sign((c - b) % (x - b)) >= 0 &&
           sign((a - c) % (x - c)) >= 0;
}

// CCW convex polygon of positive area, distinct vertices; collinear vertices OK.
// O(log n). Boundary points are included.
bool isInConvex(vector<point> &p, point &a) {
    int n = p.size();
    assert(n >= 3);
    vec q = a - p[0], first = p[1] - p[0], last = p[n - 1] - p[0];
    int left = sign(first % q), right = sign(last % q);
    if (left < 0 || right > 0) return false;
    if (left == 0 && first * q >= 0) {
        int l = 1, r = n - 1;
        while (l + 1 < r) {
            int m = (l + r) / 2;
            vec v = p[m] - p[0];
            if (sign(first % v) == 0 && first * v > 0) l = m;
            else r = m;
        }
        return isOnSegment(p[0], p[l], a);
    }
    if (right == 0) {
        int l = 1, r = n - 1;
        while (l + 1 < r) {
            int m = (l + r) / 2;
            vec v = p[m] - p[0];
            if (sign(last % v) == 0 && last * v > 0) r = m;
            else l = m;
        }
        return isOnSegment(p[0], p[r], a);
    }
    int l = 1, r = n - 1;
    while (l + 1 < r) {
        int m = (l + r) / 2;
        if ((p[m] - p[0]) % q >= 0) l = m;
        else r = m;
    }
    return isInTriangle(p[0], p[l], p[r], a);
}

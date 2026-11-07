/**
 * Author: Igor Markelov
 * Date: 2022-11-18
 * Description: Is in polygon functions
 */

bool isOnSegment(point &a, point &b, point &x) {
    if (sign(len2(a - b)) == 0) {
        return sign(len(a - x)) == 0;
    }
    return sign((b - a) % (x - a)) == 0 && sign((b - x) * (a - x)) <= 0;
    // optional (slower, but works better if there are some precision
    // problems) return sign((b - a).len() - (x - a).len() - (x - b).len())
    // == 0;
}

int isIn(vector<point> &p, point &a) {
    int n = p.size();
    // depends on limitations(2*MAXC + 228)
    point b = a + point{2e9 + 228, 1};
    int cnt = 0;
    for (int i = 0; i < n; ++i) {
        point x = p[i];
        point y = p[i + 1 < n ? i + 1 : 0];
        if (isOnSegment(x, y, a)) {
            // depends on the problem statement
            return 1;
        }
        cnt += intersects(x, y, a, b);
    }
    return 2 * (cnt % 2 == 1);
    /*optional (atan2 is VERY SLOW)!
    ld ans = 0;
    int n = p.size();
    for (int i = 0; i < n; ++i) {
      Point x = p[i];
      Point y = p[i + 1 < n ? i + 1 : 0];
      if (isOnSegment(x, y, a)) {
        // depends on the problem statement
        return true;
      }
      x = x - a;
      y = y - a;
      ans += atan2(x ^ y, x * y);
    }
    return abs(ans) > 1;*/
}

bool isInTriangle(point &a, point &b, point &c, point &x) {
    return sign((b - a) % (x - a)) >= 0 && sign((c - b) % (x - b)) >= 0 &&
           sign((a - c) % (x - c)) >= 0;
}

// points should be in the counterclockwise order
bool isInConvex(vector<point> &p, point &a) {
    int n = p.size();
    assert(n >= 3);
    // assert(isConvex(p));
    // assert(isCounterclockwise(p));
    if (sign((p[1] - p[0]) % (a - p[0])) < 0)
        return 0;
    if (sign((p[n - 1] - p[0]) % (a - p[0])) > 0)
        return 0;
    int pos = lower_bound(p.begin() + 2, p.end(), a,
                          [&](point a, point b) -> bool {
                              return sign((a - p[0]) % (b - p[0])) > 0;
                          }) -
              p.begin();
    assert(pos > 1 && pos < n);
    return isInTriangle(p[0], p[pos - 1], p[pos], a);
}

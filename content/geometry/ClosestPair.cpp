/**
 * Author: Simon Lindholm
 * Date: 2019-04-17
 * License: CC0
 * Source: https://codeforces.com/blog/entry/58747
 * Description: Finds the closest pair of points.
 * Time: O(n \log n)
 * Status: stress-tested
 */

// Uses the real-valued point type from Point.cpp.
pair<vec, vec> closest(vector<vec> v) {
    assert(v.size() > 1);
    sort(all(v), [](vec a, vec b) { return tie(a.x, a.y) < tie(b.x, b.y); });
    pair<vec, vec> ans{v[0], v[1]};
    ld best = len2(v[0] - v[1]);
    set<pair<ld, ld>> active; // (y, x)
    int j = 0;
    for (int i = 0; i < (int)v.size(); ++i) {
        if (best == 0) return ans;
        vec p = v[i];
        while (j < i && sq(p.x - v[j].x) > best) {
            active.erase({v[j].y, v[j].x});
            ++j;
        }
        ld radius = sqrt(best);
        auto it = active.lower_bound({p.y - radius, -numeric_limits<ld>::infinity()});
        for (; it != active.end() && it->first <= p.y + radius; ++it) {
            vec q{it->second, it->first};
            ld d = len2(p - q);
            if (d < best) best = d, ans = {p, q};
        }
        active.insert({p.y, p.x});
    }
    return ans;
}

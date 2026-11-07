/**
 * Author: Igor Markelov (stole from Red Panda teambook)
 * Date: 2022-11-05
 * Description: Find the intersection of the half planes.
 * Time: O(n \log(n))
 */
vec getPoint(line l) { return {-l.b, l.a}; }

bool bad(line a, line b, line c) {
    point x;
    assert(intersect(b, c, x) == 1);
    return a.eval(x) < 0;
}

// Do not forget about the bounding box
vector<point> hpi(vector<line> lines) {
    sort(all(lines), [](line al, line bl) -> bool {
        point a = getPoint(al);
        point b = getPoint(bl);
        if (half(a) != half(b)) {
            return half(a) < half(b);
        }
        return a % b > 0;
    });

    vector<pair<line, int>> st;
    for (int it = 0; it < 2; it++) {
        for (int i = 0; i < (int)lines.size(); i++) {
            bool flag = false;
            while (!st.empty()) {
                if (len(getPoint(st.back().first) - getPoint(lines[i])) < EPS) {
                    if (lines[i].c >= st.back().first.c) {
                        flag = true;
                        break;
                    } else {
                        st.pop_back();
                    }
                } else if (getPoint(st.back().first) % getPoint(lines[i]) < EPS / 2) {
                    return {};
                } else if (st.size() >= 2 &&
                           bad(st[st.size() - 2].first, st[st.size() - 1].first,
                               lines[i])) {
                    st.pop_back();
                } else {
                    break;
                }
            }
            if (!flag)
                st.push_back({lines[i], i});
        }
    }

    vector<int> en(lines.size(), -1);
    vector<point> ans;
    for (int i = 0; i < (int)st.size(); i++) {
        if (en[st[i].second] == -1) {
            en[st[i].second] = i;
            continue;
        }
        for (int j = en[st[i].second]; j < i; j++) {
            point I;
            assert(intersect(st[j].first, st[j + 1].first, I) == 1);
            ans.push_back(I);
        }
        break;
    }
    return ans;
}

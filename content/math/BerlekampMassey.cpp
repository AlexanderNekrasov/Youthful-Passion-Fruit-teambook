/**
 * Author: Igor Markelov (stole from Red Panda teambook)
 * Date: 2022-11-18
 * Description: Find the shortest linear-feedback shift register
 * Time: O(n^2)
 */
vector<int> berlekamp(vector<int> x) {
    vector<int> ls, cur;
    int lf = 0, d = 0;
    for (int i = 0; i < x.size(); ++i) {
        ll t = 0;
        for (int j = 0; j < cur.size(); ++j) {
            t = (t + (ll) x[i - j - 1] * cur[j]) % MOD;
        }
        if ((t - x[i]) % MOD == 0)
            continue;
        if (cur.empty()) {
            cur.resize(i + 1);
            lf = i;
            d = (t - x[i]) % MOD;
            continue;
        }
        ll k = -(x[i] - t) * powmod(d, MOD - 2) % MOD;
        vector<int> c(i - lf - 1);
        c.push_back(k);
        for (auto &j : ls)
            c.push_back(-j * k % MOD);
        if (c.size() < cur.size())
            c.resize(cur.size());
        for (int j = 0; j < cur.size(); ++j) {
            c[j] = (c[j] + cur[j]) % MOD;
        }
        if (i - lf + (int)ls.size() >= (int)cur.size()) {
            tie(ls, lf, d) = make_tuple(cur, i, (t - x[i]) % MOD);
        }
        cur = c;
    }
    for (auto &i : cur)
        i = (i % MOD + MOD) % MOD;
    return cur;
}
// for a_i = 2 * a_i-1 + a_i-2 returns {2, 1}

// kth element of p/q as fps
int getkfps(vector<int> p, vector<int> q, ll k) {
    assert(k >= 0 && !q.empty() && q[0] != 0);
    if (p.empty()) return 0;
    while (k) {
        auto f = q;
        for (int i = 1; i < (int) f.size(); i += 2) {
            f[i] = sub(0, f[i]);
        }
        auto p2 = conv(p, f);
        auto q2 = conv(q, f);
        p.clear(), q.clear();
        for (int i = k % 2; i < (int) p2.size(); i += 2) {
            p.pbc(p2[i]);
        }
        if (p.empty()) return 0;
        for (int i = 0; i < (int)q2.size(); i += 2) {
            q.pbc(q2[i]);
        }
        k >>= 1;
    }
    return mul(p[0], inv(q[0]));
}

// vals - initials values of reccurence, c - result of belekamp on vals
int getk(const vector<int> &vals, vector<int> c, ll k) {
    int d = c.size();
    assert(k >= 0 && (int)vals.size() >= d);
    if (k < (ll)vals.size()) return vals[k];
    if (d == 0) return 0;
    c.insert(c.begin(), MOD-1);
    while (c.back() == 0) {
        c.pop_back();
    }
    for (auto &el : c) {
        el = sub(0, el);
    }
    vector<int> p(d);
    copy(vals.begin(), vals.begin() + d, p.begin());
    p = conv(p, c);
    p.resize(d);
    return getkfps(p, c, k);
}

vector<int> getmod(vector<int> a, vector<int> md) {
    for (int i = a.size() - 1; i + 1 >= md.size(); --i) {
        int v = mul(a[i], inv(md.back()));
        for (int j = 0; j < md.size(); ++j) {
            a[i - md.size() + 1 + j] = sub(a[i - md.size() + 1 + j], mul(md[j], v));
        }
        a.pop_back();
    }
    return a;
}

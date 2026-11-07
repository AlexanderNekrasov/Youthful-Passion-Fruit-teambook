/**
 * Author: Igor Markelov
 * Date: 2022-11-08
 * Description: Calculating FFT modulo MOD
 * Time: O(n\log(n))
 */
// DONT FORGET TO CALL initNTT() AND CHECK MAXLOG

const int MOD = 998244353;
const int G = 3;
const int MAXLOG = 23;
int W[1 << MAXLOG];
bool nttinit = false;
vector<int> pws;

int add(int a, int b) {
    a += b;
    if (a >= MOD) {
        return a - MOD;
    }
    return a;
}

int sub(int a, int b) {
    a -= b;
    if (a < 0) {
        return a + MOD;
    }
    return a;
}

int mul(int a, int b) {
    return (ll) a * b % MOD;
}

int power(int a, int n) {
    int ans = 1;
    while (n) {
        if (n & 1) {
            ans = mul(ans, a);
        }
        a = mul(a, a);
        n >>= 1;
    }
    return ans;
}

int inv(int a) {
    return power(a, MOD - 2);
}

void initNTT() {
    assert((MOD - 1) % (1 << MAXLOG) == 0);
    pws.push_back(power(G, (MOD - 1) / (1 << MAXLOG)));
    for (int i = 0; i < MAXLOG - 1; ++i) {
        pws.push_back(mul(pws.back(), pws.back()));
    }
    assert(pws.back() == MOD - 1);
    W[0] = 1;
    for (int i = 1; i < (1 << MAXLOG); ++i) {
        W[i] = mul(W[i - 1], pws[0]);
    }
}

void ntt(int n, vector <int>& a, bool rev) {
    if (!nttinit) {
        initNTT();
        nttinit = 1;
    }
    int lg = log2(n);
    vector<int> rv(n);
    for (int i = 1; i < n; ++i) {
        rv[i] = (rv[i >> 1] >> 1) ^ ((i & 1) << (lg - 1));
        if (rv[i] > i) swap(a[i], a[rv[i]]);
    }
    int num = MAXLOG - 1;
    for (int len = 1; len < n; len *= 2) {
        for (int i = 0; i < n; i += 2 * len) {
            for (int j = 0; j < len; ++j) {
                int u = a[i + j], v = mul(W[j << num], a[i + j + len]);
                a[i + j] = add(u, v);
                a[i + j + len] = sub(u, v);
            }
        }
        --num;
    }
    if (rev) {
        int rev_n = power(n, MOD - 2);
        for (int i = 0; i < n; ++i) a[i] = mul(a[i], rev_n);
        reverse(a.begin() + 1, a.end());
    }
}

vector<int> conv(vector<int> a, vector<int> b) {
    int lg = 0;
    while ((1 << lg) < a.size() + b.size() + 1)
        ++lg;
    int n = 1 << lg;
    assert(a.size() + b.size() <= n + 1);
    a.resize(n);
    b.resize(n);
    ntt(n, a, false);
    ntt(n, b, false);
    for (int i = 0; i < n; ++i) {
        a[i] = mul(a[i], b[i]);
    }
    ntt(n, a, true);
    while (a.size() > 1 && a.back() == 0) {
        a.pop_back();
    }
    return a;
}

vector<int> add(vector<int> a, vector<int> b) {
    a.resize(max(a.size(), b.size()));
    for (int i = 0; i < (int) b.size(); ++i) {
        a[i] = add(a[i], b[i]);
    }
    return a;
}

vector<int> sub(vector<int> a, vector<int> b) {
    a.resize(max(a.size(), b.size()));
    for (int i = 0; i < (int) b.size(); ++i) {
        a[i] = sub(a[i], b[i]);
    }
    return a;
}

vector<int> inv(const vector<int> &a, int need) {
    vector<int> b = {inv(a[0])};
    while ((int) b.size() < need) {
        vector<int> a1 = a;
        int m = b.size();
        a1.resize(min((int) a1.size(), 2 * m));
        b = conv(b, sub({2}, conv(a1, b)));
        b.resize(2 * m);
    }
    b.resize(need);
    return b;
}

vector<int> div(vector<int> a, vector<int> b) {
    if (count(all(a), 0) == a.size()) {
        return {0};
    }
    assert(a.back() != 0 && b.back() != 0);
    int n = a.size() - 1;
    int m = b.size() - 1;
    if (n < m) {
        return {0};
    }
    reverse(all(a));
    reverse(all(b));
    a.resize(n - m + 1);
    b.resize(n - m + 1);
    vector<int> c = inv(b, b.size());
    vector<int> q = conv(a, c);
    q.resize(n - m + 1);
    reverse(all(q));
    return q;
}

vector<int> mod(vector<int> a, vector<int> b) {
    auto res = sub(a, conv(b, div(a, b)));
    while (res.size() > 1 && res.back() == 0) {
        res.pop_back();
    }
    return res;
}

vector<int> multipoint(vector<int> a, vector<int> x) {
    int n = x.size();
    vector<vector<int>> tree(2 * n);
    for (int i = 0; i < n; ++i) {
        tree[i + n] = {x[i], MOD - 1};
    }
    for (int i = n - 1; i; --i) {
        tree[i] = conv(tree[2 * i], tree[2 * i + 1]);
    }
    tree[1] = mod(a, tree[1]);
    for (int i = 2; i < 2 * n; ++i) {
        tree[i] = mod(tree[i >> 1], tree[i]);
    }
    vector<int> res(n);
    for (int i = 0; i < n; ++i) {
        res[i] = tree[i + n][0];
    }
    return res;
}

vector<int> deriv(vector<int> a) {
    for (int i = 1; i < (int) a.size(); ++i) {
        a[i - 1] = mul(i, a[i]);
    }
    a.back() = 0;
    if (a.size() > 1) {
        a.pop_back();
    }
    return a;
}

vector<int> integ(vector<int> a) {
    a.push_back(0);
    for (int i = (int) a.size() - 1; i; --i) {
        a[i] = mul(a[i - 1], inv(i));
    }
    a[0] = 0;
    return a;
}

vector<int> log(vector<int> a, int n) {
    assert(a[0] == 1);
    auto res = integ(conv(deriv(a), inv(a, n)));
    res.resize(n);
    return res;
}

vector<int> exp(vector<int> a, int need) {
    assert(a[0] == 0);
    vector<int> b = {1};
    while ((int) b.size() < need) {
        vector<int> a1 = a;
        int m = b.size();
        a1.resize(min((int) a1.size(), 2 * m));
        a1[0] = add(a1[0], 1);
        b = conv(b, sub(a1, log(b, 2 * m)));
        b.resize(2 * m);
    }
    b.resize(need);
    return b;
}


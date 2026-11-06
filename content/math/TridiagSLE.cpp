/**
 * Author: Iurii Pustovalov
 * Description: Thomas algorithm without pivoting. All elimination pivots
 * must be nonzero (e.g. for a strictly diagonally dominant system).
 * Time: O(N)
 */
vector<ld> trisle(vector<ld> a, vector<ld> b, vector<ld> c, vector<ld> f) {
    // a[i]*x[i-1] + c[i]*x[i] + b[i]*x[i+1] = f[i].
    int n = a.size(); // a[0] = 0, b[n-1] = 0
    assert(b.size() == a.size() && c.size() == a.size() && f.size() == a.size());
    vector<ld> x(n);
    for (int i = 0; i < n; ++i) {
        if (c[i] == 0) throw domain_error("Zero pivot in trisle");
        if (i + 1 < n) {
            ld k = a[i + 1] / c[i];
            c[i + 1] -= k * b[i];
            f[i + 1] -= k * f[i];
        }
    }
    for (int i = n - 1; i >= 0; --i)
        x[i] = (f[i] - (i + 1 < n ? b[i] * x[i + 1] : 0)) / c[i];
    return x;
}

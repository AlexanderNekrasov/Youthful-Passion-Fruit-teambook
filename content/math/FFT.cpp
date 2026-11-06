/**
 * Author: Igor Markelov
 * Date: 2022-11-08
 * Description: Calculating product of two polynomials
 * Time: O(n\log(n))
 */

const ld PI = acos(-1);
using cd = complex<ld>;
const int MAXLOG = 19, N = (1 << MAXLOG), MAXN = (1 << MAXLOG) + 228;
int rev[MAXN];
cd w[MAXN];
bool fftInit = false;

void initFFT() {
    for (int i = 0; i < N; ++i) {
        w[i] = cd(cos(2 * PI * i / N), sin(2 * PI * i / N));
    }
    rev[0] = 0;
    for (int i = 1; i < N; ++i) {
        rev[i] = (rev[i >> 1] >> 1) ^ ((i & 1) << (MAXLOG - 1));
    }
}

void FFT(int n, vector <cd>& a, bool rv = false) {
    if (!fftInit) {
        initFFT();
        fftInit = 1;
    }
    int LOG = ceil(log2(n));
    for (int i = 0; i < n; ++i) {
        if (i < (rev[i] >> (MAXLOG - LOG))) {
            swap(a[i], a[(rev[i] >> (MAXLOG - LOG))]);
        }
    }
    for (int lvl = 0; lvl < LOG; ++lvl) {
        int len = 1 << lvl;
        for (int st = 0; st < n; st += len * 2) {
            for (int i = 0; i < len; ++i) {
                cd x = a[st + i], y = a[st + len + i] * w[i << (MAXLOG - 1 - lvl)];
                a[st + i] = x + y;
                a[st + i + len] = x - y;
            }
        }
    }
    if (rv) {
        reverse(a.begin() + 1, a.end());
        for (auto& i : a) i /= n;
    }
}

vector <ll> mul(vector <ll> a, vector <ll> b) {
    int xd = max(a.size(), b.size()) * 2;
    int cur = 1;
    while (cur < xd) {
        cur *= 2;
    }
    a.resize(cur);
    b.resize(cur);
    vector <cd> ma(cur), mb(cur);
    for (int i = 0; i < cur; ++i) {
        ma[i] += a[i];
        mb[i] += b[i];
    }
    FFT(cur, ma);
    FFT(cur, mb);
    for (int i = 0; i < cur; ++i) ma[i] *= mb[i];
    FFT(cur, ma, true);
    vector <ll> ans(cur);
    for (int i = 0; i < cur; ++i) {
        ans[i] = llround(ma[i].real());
    }
    return ans;
}

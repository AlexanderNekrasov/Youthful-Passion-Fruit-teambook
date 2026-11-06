
/**
 * Author: Iurii Pustovalov
 * Date: 2024-07-03
 * Description: lcp array
 * Time: O(n)
 */
vector<int> perm;
vector<int> buildLCP(string &s, vector<int> &a) {
    int n = s.size();
    vector<int> ra(n);
    for (int i = 0; i < n; i++) {
        ra[a[i]] = i;
    }
    vector<int> lcp(max(0, n - 1));
    int cur = 0;
    for (int i = 0; i < n; i++) {
        cur--;
        chkmax(cur, 0);
        if (ra[i] == n - 1) {
            cur = 0;
            continue;
        }
        int j = a[ra[i] + 1];
        while (i + cur < n && j + cur < n && s[i + cur] == s[j + cur]) cur++;
        lcp[ra[i]] = cur;
    }
    perm.resize(a.size());
    for (int i = 0; i < a.size(); ++i) perm[a[i]] = i;
    return lcp;
}
int cntr[MAXN];
int spt[MAXN][lgg];
void build(vector<int> &a) {
    for (int i = 0; i < a.size(); ++i) {
        spt[i][0] = a[i];
    }
    for (int i = 2; i < MAXN; ++i) cntr[i] = cntr[i / 2] + 1;
    for (int h = 1; h < lgg && (1 << h) <= a.size(); ++h) {
        for (int i = 0; i + (1 << h) <= a.size(); ++i) {
            spt[i][h] = min(spt[i][h - 1], spt[i + (1 << (h - 1))][h - 1]);
        }
    }
}
int getLCP(int l, int r) {
    if (l == r) return (int)perm.size() - l;
    l = perm[l], r = perm[r];
    if (l > r) swap(l, r);
    int xx = cntr[r - l];
    return min(spt[l][xx], spt[r - (1 << xx)][xx]);
}

/**
 * Author: Iurii Pustovalov
 * Date: 2023-11-25
 * Description: Build suffix array
 * Time: O(n)
 */
void induced_sort(vector<int> &vec, int LIM, vector<int> &sa, vector<bool> &sl,
                  vector<int> &fx) {
    vector<int> l(LIM), r(LIM);
    for (int c : vec) {
        if (c + 1 < LIM) {
            ++l[c + 1];
        }
        ++r[c];
    }
    partial_sum(all(l), l.begin());
    partial_sum(all(r), r.begin());
    fill(all(sa), -1);
    for (int i = fx.size() - 1; i >= 0; --i) {
        sa[--r[vec[fx[i]]]] = fx[i];
    }
    for (int i : sa) {
        if (i >= 1 && sl[i - 1]) {
            sa[l[vec[i - 1]]++] = i - 1;
        }
    }
    fill(all(r), 0);
    for (int c : vec) ++r[c];
    partial_sum(all(r), r.begin());
    for (int k = sa.size() - 1, i = sa[k]; k >= 1; --k, i = sa[k])
        if (i >= 1 && !sl[i - 1]) sa[--r[vec[i - 1]]] = i - 1;
}
vector<int> SA_IS(vector<int> &vec, int LIM) {
    const int n = vec.size();
    vector<int> sa(n), fx;
    vector<bool> sl(n);
    sl[n - 1] = false;
    for (int i = n - 2; i >= 0; --i) {
        sl[i] = (vec[i] > vec[i + 1] || (vec[i] == vec[i + 1] && sl[i + 1]));
        if (sl[i] && !sl[i + 1]) {
            fx.pbc(i + 1);
        }
    }
    reverse(all(fx));
    induced_sort(vec, LIM, sa, sl, fx);
    vector<int> nfx(fx.size()), lmv(fx.size());
    for (int i = 0, k = 0; i < n; ++i) {
        if (!sl[sa[i]] && sa[i] >= 1 && sl[sa[i] - 1]) {
            nfx[k++] = sa[i];
        }
    }
    int cur = 0;
    sa[n - 1] = cur;
    for (int k = 1; k < nfx.size(); ++k) {
        int i = nfx[k - 1], j = nfx[k];
        if (vec[i] != vec[j]) {
            sa[j] = ++cur;
            continue;
        }
        bool flag = false;
        for (int a = i + 1, b = j + 1;; ++a, ++b) {
            if (vec[a] != vec[b]) {
                flag = true;
                break;
            }
            if ((!sl[a] && sl[a - 1]) || (!sl[b] && sl[b - 1])) {
                flag = !((!sl[a] && sl[a - 1]) && (!sl[b] && sl[b - 1]));
                break;
            }
        }
        sa[j] = (flag ? ++cur : cur);
    }
    for (int i = 0; i < fx.size(); ++i) {
        lmv[i] = sa[fx[i]];
    }
    if (cur + 1 < (int)fx.size()) {
        auto lms = SA_IS(lmv, cur + 1);
        for (int i = 0; i < fx.size(); ++i) {
            nfx[i] = fx[lms[i]];
        }
    }
    induced_sort(vec, LIM, sa, sl, nfx);
    return sa;
}
template <typename T>
vector<int> suffix_array(T &s, const int LIM = 128) {
    vector<int> vec(s.size() + 1);
    copy(all(s), begin(vec));
    vec.back() = (char)(1);
    auto ret = SA_IS(vec, LIM);
    ret.erase(ret.begin());
    return ret;
}

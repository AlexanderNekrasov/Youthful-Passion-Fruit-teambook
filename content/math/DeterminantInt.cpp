/**
 * Author: Iurii Pustovalov
 * Date: 2024-09-09
 * Description: Determinant in ints
 */
const ll mod = 12345;
ll det(vector<vector<ll>>& a) {
  int n = sz(a);
  ll ans = 1;
  for (int i = 0; i < n; ++i) {
    for (int j = i + 1; j < n; ++j) {
      while (a[j][i] != 0) {  // gcd step
        ll t = a[i][i] / a[j][i];
        if (t)
          for (int k = i; k < n; ++k)
            a[i][k] = (a[i][k] - a[j][k] * t) % mod;
        swap(a[i], a[j]);
        ans *= -1;
      }
    }
    ans = ans * a[i][i] % mod;
    if (!ans) return 0;
  }
  return (ans + mod) % mod;
}

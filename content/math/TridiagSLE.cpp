/**
 * Author: Iurii Pustovalov
 * Date: 2024-09-09
 * Description: Tridiagonal SLE solver(didnt test yet)
 * Time: O(N)
 */
vector<ld> trisle(vector<ld> a, vector<ld> b, vector<ld> c, vector<ld> f) {
  // a[i] * x[i - 1] + c[i] * x[i] + b[i] * x[i + 1] == f[i]
  int n = a.size();  // a[0] == 0, b[n-1] == 0
  vector<ld> alpha(n + 1), beta(n + 1), x(n);
  alpha[1] = -(ld)b[0] / c[0];
  beta[1] = (ld)f[0] / c[0];
  for (int i = 1; i < n - 1; i++) {
    ld zn = (ld)a[i] * alpha[i] + c[i];
    alpha[i + 1] = -(ld)b[i] / zn;
    beta[i + 1] = (f[i] - (ld)a[i] * beta[i]) / zn;
  }
  x[n - 1] = (f[n - 1] - a[n - 1] * beta[n - 1]) /
             (a[n - 1] * alpha[n - 1] + c[n - 1]);
  for (int i = n - 2; i >= 0; i--)
    x[i] = alpha[i + 1] * x[i + 1] + beta[i + 1];
  return x;
}
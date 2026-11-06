/**
 * Author: Iurii Pustovalov
 * Date: 2022-11-08
 * Description: Interpolating polynomials
 * Time: O(n^2)
 */
typedef vector<double> vd;
vd interpolate(vd x, vd y, int n) {
  if (n == 0) return {};
  vd res(n), temp(n);
  for (int k = 0; k < n - 1; ++k)
    for (int i = k + 1; i < n; ++i) y[i] = (y[i] - y[k]) / (x[i] - x[k]);
  double last = 0;
  temp[0] = 1;
  for (int k = 0; k < n; ++k)
    for (int i = 0; i < n; ++i) {
      res[i] += y[k] * temp[i];
      swap(last, temp[i]);
      temp[i] -= last * x[k];
    }
  return res;
}

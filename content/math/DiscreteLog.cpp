/**
 * Author: Iurii Pustovalov
 * Date: 2024-09-09
 * Description: Smallest x > 0 with a^x = b (mod m), or -1.
 * Requires 0 <= a,b < m and products to fit in ll.
 * Time: O(\sqrt(n))
 */

ll modLog(ll a, ll b, ll m) {
  ll n = (ll)sqrt(m) + 1, e = 1, f = 1, j = 1;
  unordered_map<ll, ll> A;
  while (j <= n && (e = f = e * a % m) != b % m) A[e * b % m] = j++;
  if (e == b % m) return j;
  if (__gcd(m, e) == __gcd(m, b))
    for (int i = 2; i < n + 2; ++i)
      if (A.count(e = e * f % m)) return n * i - A[e];
  return -1;
}

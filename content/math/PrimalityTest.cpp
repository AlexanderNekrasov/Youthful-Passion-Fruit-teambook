/**
 * Author: Iurii Pustovalov
 * Description: Deterministic Miller-Rabin for positive signed 64-bit integers.
 * Bases: the same set as original_content/number-theory/MillerRabin.h.
 * Time: O(log p), with seven bases and exact 128-bit products.
 */
#pragma once
ll prime_pow(ll a, ll e, ll mod) {
    ll res = 1;
    for (; e; e >>= 1, a = (__int128)a * a % mod)
        if (e & 1) res = (__int128)res * a % mod;
    return res;
}
bool isprime(ll p) {
    if (p < 2 || p % 2 == 0) return p == 2;
    ll d = p - 1;
    int s = 0;
    while (d % 2 == 0) d /= 2, ++s;
    for (ll a : {2LL, 325LL, 9375LL, 28178LL, 450775LL,
                 9780504LL, 1795265022LL}) {
        if (a % p == 0) continue;
        ll x = prime_pow(a % p, d, p);
        if (x == 1 || x == p - 1) continue;
        bool passed = false;
        for (int r = 1; r < s; ++r) {
            x = (__int128)x * x % p;
            if (x == p - 1) { passed = true; break; }
        }
        if (!passed) return false;
    }
    return true;
}

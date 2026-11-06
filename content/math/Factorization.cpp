/**
 * Author: Iurii Pustovalov
 * Date: 2022-11-08
 * Description: Factorizing a number real quick
 * Time: Expected O(n^{\frac{1}{4}}), with randomized retries.
 */
#include "PrimalityTest.cpp"
ll gcd(ll a, ll b) {
    while (b)
        a %= b, swap(a, b);
    return a;
}

vector<ll> factorize(ll n) {
    if (n < 1) throw invalid_argument("factorize requires n >= 1");
    if (n <= 1e6) {
        vector<ll> res;
        for (ll i = 2; i * i <= n; ++i) {
            while (n % i == 0) {
                res.pbc(i);
                n /= i;
            }
        }
        if (n != 1)
            res.pbc(n);
        return res;
    }
    if (isprime(n)) return {n};
    if (n % 2 == 0) {
        auto res = factorize(n / 2);
        res.pbc(2);
        return res;
    }
    auto random_residue = [&]() {
        return (ll)((((unsigned long long)rnd() << 32) | rnd()) % (n - 1)) + 1;
    };
    const int C = 60;
    ll tries = 10 * sqrt(sqrt(n));
    for (;;) {
        ll x = random_residue(), y = x, c = random_residue();
        auto step = [&](ll a) { return (ll)(((__int128)a * a + c) % n); };
        for (ll i = 0; i < tries; i += C) {
            ll xs = x, ys = y, m = 1;
            for (int k = 0; k < C; ++k) {
                x = step(x);
                y = step(step(y));
                m = (__int128)m * abs(x - y) % n;
            }
            ll res = gcd(n, m);
            if (res == 1) continue;
            if (res == n) {
                x = xs, y = ys;
                for (int k = 0; k < C; ++k) {
                    x = step(x);
                    y = step(step(y));
                    res = gcd(n, abs(x - y));
                    if (res > 1 && res < n) break;
                }
            }
            if (res <= 1 || res == n) break; // retry with a new polynomial
            auto v1 = factorize(res), v2 = factorize(n / res);
            v1.insert(v1.end(), v2.begin(), v2.end());
            return v1;
        }
    }
}

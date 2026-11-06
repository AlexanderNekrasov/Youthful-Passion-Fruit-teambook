/**
 * Author: Iurii Pustovalov
 * Description: CRT for positive, not necessarily coprime 64-bit moduli.
 * Returns the least nonnegative solution, or -1 if incompatible.
 * Throws overflow_error if the combined modulus does not fit in ll.
 */
ll extgcd(ll a, ll b, ll &x, ll &y) {
    if (a == 0) { x = 0; y = 1; return b; }
    ll x1, y1;
    ll g = extgcd(b % a, a, x1, y1);
    x = (__int128)y1 - (__int128)x1 * (b / a);
    y = x1;
    return g;
}
ll crt(ll mod1, ll mod2, ll rem1, ll rem2) {
    if (mod1 <= 0 || mod2 <= 0) throw invalid_argument("CRT requires positive moduli");
    rem1 %= mod1; if (rem1 < 0) rem1 += mod1;
    rem2 %= mod2; if (rem2 < 0) rem2 += mod2;
    ll x, y, g = extgcd(mod1, mod2, x, y);
    __int128 delta = (__int128)rem2 - rem1;
    if (delta % g) return -1;
    ll reduced = mod2 / g;
    __int128 period = (__int128)mod1 * reduced;
    if (period > LLONG_MAX) throw overflow_error("CRT modulus exceeds ll");
    __int128 k = ((__int128)x * (delta / g)) % reduced;
    if (k < 0) k += reduced;
    return (k * mod1 + rem1) % period;
}

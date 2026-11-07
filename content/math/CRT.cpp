  /**
 * Author: Iurii Pustovalov
 * Date: 2024-08-09
 * Description: CRT for arbitrary modulos
 */

int extgcd(int a, int b, int &x, int &y) {  // define int ll
    if (a == 0) {
        x = 0, y = 1;
        return b;
    }
    int x1, y1;
    int g = extgcd(b % a, a, x1, y1);
    x = y1 - x1 * (b / a);
    y = x1;
    return g;
}
int lcm(int a, int b) { return a / __gcd(a, b) * b; }
int crt(int mod1, int mod2, int rem1, int rem2) {
    int r = (rem2 - (rem1 % mod2) + mod2) % mod2;
    int x, y;
    int g = extgcd(mod1, mod2, x, y);
    if (r % g) return -1;
    x %= mod2;
    if (x < 0) x += mod2;
    int ans = (x * (r / g)) % mod2;
    ans = ans * mod1 + rem1;
    assert(ans % mod1 == rem1);
    assert(ans % mod2 == rem2);
    return ans % lcm(mod1, mod2);
}

/**
 * Author: alexxela12345,daubi,talant
 * Date: 2024-08-03
 * Description: struct Point
 */

const ld EPS = 1e-7;

ld sq(ld x) {
    return x * x;
}

int sign(ld x) {
    if (x < -EPS) {
        return -1;
    }
    if (x > EPS) {
        return 1;
    }
    return 0;
}

#define vec point
struct point {//% - cross, * - dot
    ld x, y;
    // Strict order for sorting/containers; tolerances belong in predicates.
    auto operator<=>(const point &p) const { return tie(y, x) <=> tie(p.y, p.x); }
    bool operator==(const point&) const = default;
    ld dot(const point &p) const { return x * p.x + y * p.y; }
    ld cross(const point &p) const { return x * p.y - y * p.x; }
    ld dot(const point &a, const point &b) const {
        return (a.x - x) * (b.x - x) + (a.y - y) * (b.y - y);
    }
    ld cross(const point &a, const point &b) const {
        return (a.x - x) * (b.y - y) - (a.y - y) * (b.x - x);
    }
};
ld operator*(const point &a, const point &b) {
    return a.x * b.x + a.y * b.y;
}
ld operator%(const point &a, const point &b) {
    return a.x * b.y - a.y * b.x;
}
point operator-(const point &a, const point &b) {
    return {a.x - b.x, a.y - b.y};
}
point operator+(const point &a, const point &b) {
    return {a.x + b.x, a.y + b.y};
}
point operator*(const point &a, ld b) {
    return {a.x * b, a.y * b};
}
point operator/(const point &a, ld b) {
    return {a.x / b, a.y / b};
}
ld len2(const point &a) {
    return sq(a.x) + sq(a.y);
}
ld len(const point &a) {
    return sqrt(len2(a));
}
point norm(point a) {
    return a / len(a);
}
int half(point a) {
    return (sign(a.y) == -1 || (sign(a.y) ==0 && a.x < 0));
}
point ort(point a) {
    return {-a.y, a.x};
}
point turn(point a, ld ang) {
    return {a.x * cos(ang) - a.y * sin(ang), a.x * sin(ang) + a.y * cos(ang)};
}
ld getAngle(point &a, point &b) {
    return atan2(a % b, a * b);
}
bool cmpHalf(const point &a, const point &b) {
    if (half(a) != half(b)) {
        return half(b);
    } else {
        int sgn = sign(a % b);
        if (!sgn) {
            return len2(a) < len2(b);
        } else {
            return sgn == 1;
        }
    }
}

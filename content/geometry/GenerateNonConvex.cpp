/**
 * Author: alexxela12345
 * Date: 2024-09-09
 * Description: Non convex polygon generation
*/
vector<vec> pointsInGeneralPosition(int n, int maxC) {
    vector<vec> arr(n);
    for (int i = 0; i < n; ++i) {
        arr[i].x = randint(0, maxC);
        arr[i].y = randint(0, maxC);
    }
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < i; ++j) {
            for (int k = 0; k < j; ++k) {
                if (sign((arr[i] - arr[j]) % (arr[j] - arr[k])) == 0) {
                    return pointsInGeneralPosition(n, maxC);
                }
            }
        }
    }
    return arr;
}

vector<vec> pointsDifferent(int n, int maxC) {
    vector<vec> arr;
    while (arr.size() < n) {
        vec v;
        v.x = randint(0, maxC);
        v.y = randint(0, maxC);
        if (binary_search(all(arr), v)) {
            continue;
        }
        arr.pbc(v);
        sort(all(arr));
    }
    shuffle(all(arr), rnd);
    return arr;
}

vector<vec> generateNonconvex(int n, int maxC) {
    vector<vec> arr = pointsDifferent(n, maxC);
    bool was = 1;
    while (was) {
        was = 0;
        for (int i = 0; i < n; ++i) {
            for (int j = i + 2; j < n; ++j) {
                if ((j + 1) % n == i) continue;
                if (intersects(arr[i],arr[(i + 1)%n],arr[j],arr[(j + 1)%n])) {
                    reverse(arr.begin() + i + 1, arr.begin() + j + 1);
                    was = 1;
                }
            }
        }
    }
    if (area(arr) < 0) {
        reverse(all(arr));
    }
    if (sign(area(arr)) == 0) {
        return generateNonconvex(n, maxC);
    }
    return arr;
}

template<typename T>
vector<vec<T>> polyRemoveOnOneLine(vector<vec<T>> arr) {
    int n = arr.size();
    for (int it = 0; it < 3; ++it) {
        vector<vec<T>> res;
        for (auto el : arr) {
            if (res.size() >= 2 && sign((res[res.size() - 2] - el) % (res.back() - el)) == 0) {
                res.pop_back();
            }
            res.pbc(el);
        }
        arr = res;
        rotate(arr.begin(), 1 + all(arr));
    }
    return arr;
}
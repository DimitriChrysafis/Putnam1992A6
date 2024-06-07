#include "convex_hull.h"
#include <algorithm>
#include <cmath>

// https://cp-algorithms.com/geometry/convex-hull.html
// convex hull code stolen from here ^^
// everything else is mine though
int orientation(pt a, pt b, pt c) {
    double v = a.x * (b.y * c.z - c.y * b.z) - b.x * (a.y * c.z - c.y * a.z) + c.x * (a.y * b.z - b.y * a.z);
    if (v < 0) return -1;
    if (v > 0) return +1;
    return 0;
}

bool cw(pt a, pt b, pt c, bool include_collinear) {
    int o = orientation(a, b, c);
    return o < 0 || (include_collinear && o == 0);
}

bool collinear(pt a, pt b, pt c) {
    return orientation(a, b, c) == 0;
}

void convex_hull(std::vector<pt>& a, bool include_collinear) {
    pt p0 = *min_element(a.begin(), a.end(), [](pt a, pt b) {
        return std::make_tuple(a.z, a.y, a.x) < std::make_tuple(b.z, b.y, b.x);
    });
    sort(a.begin(), a.end(), [&p0](const pt& a, const pt& b) {
        int o = orientation(p0, a, b);
        if (o == 0)
            return (p0.x - a.x) * (p0.x - a.x) + (p0.y - a.y) * (p0.y - a.y) + (p0.z - a.z) * (p0.z - a.z)
                   < (p0.x - b.x) * (p0.x - b.x) + (p0.y - b.y) * (p0.y - b.y) + (p0.z - b.z) * (p0.z - b.z);
        return o < 0;
    });
    if (include_collinear) {
        int i = (int)a.size() - 1;
        while (i >= 0 && collinear(p0, a[i], a.back())) i--;
        reverse(a.begin() + i + 1, a.end());
    }

    std::vector<pt> st;
    for (int i = 0; i < (int)a.size(); i++) {
        while (st.size() > 1 && !cw(st[st.size() - 2], st.back(), a[i], include_collinear))
            st.pop_back();
        st.push_back(a[i]);
    }

    if (include_collinear == false && st.size() == 2 && st[0] == st[1])
        st.pop_back();

    a = st;
}

bool isInCenter(const std::vector<pt>& hull_points) {
    pt center = {0, 0, 0};
    for (const auto& point : hull_points) {
        double dist = sqrt(pow(point.x - center.x, 2) + pow(point.y - center.y, 2) + pow(point.z - center.z, 2));
        if (dist >= 1.0) {
            return false;
        }
    }
    return true;
}

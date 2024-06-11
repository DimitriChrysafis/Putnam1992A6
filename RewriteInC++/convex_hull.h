#ifndef CONVEX_HULL_H
#define CONVEX_HULL_H

#include <vector>

// https://cp-algorithms.com/geometry/convex-hull.html
// convex hull code stolen from here ^^
// everything else is mine though 

struct pt {
    double x, y, z;
    bool operator==(const pt& t) const {
        return x == t.x && y == t.y && z == t.z;
    }
};

void convex_hull(std::vector<pt>& a, bool include_collinear = false);
bool isInCenter(const std::vector<pt>& hull_points);

#endif // CONVEX_HULL_H

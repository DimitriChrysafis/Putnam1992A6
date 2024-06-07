#include <iostream>
#include <vector>
#include <iomanip>
#include <fstream>
#include "convex_hull.h"

std::vector<pt> generatePoints(int num_points) {
    std::vector<pt> points;
    for (int i = 0; i < num_points; ++i) {
        double x = (double)rand() / RAND_MAX;
        double y = (double)rand() / RAND_MAX;
        double z = (double)rand() / RAND_MAX;
        points.push_back({x, y, z});
    }
    return points;
}

int main() {
    std::ofstream outFile("simulation_data.txt");
    std::cout << std::fixed << std::setprecision(15);

    int total_iterations = 0;
    int inside_count = 0;
    double probability = 0.0;

    while (true) {
        total_iterations++;

        std::vector<pt> points = generatePoints(4);
        convex_hull(points);
        bool inside = isInCenter(points);

        if (inside) inside_count++;

        probability = static_cast<double>(inside_count) / total_iterations;

        if (total_iterations % 10000000 == 0) {
            // only print/store every 10 million iterations to avoid clutter and save space
            std::cout << "Iteration: " << total_iterations << ", Successful cases: " << inside_count;
            std::cout << ", Probability: " << probability;
            std::cout << ", Case: " << (inside ? "Inside" : "Outside") << std::endl;

            outFile << "Iteration: " << total_iterations << ", Successful cases: " << inside_count;
            outFile << ", Probability: " << probability;
            outFile << ", Case: " << (inside ? "Inside" : "Outside") << std::endl;

            std::cout << "Hull Points (x, y, z):" << std::endl;
            for (const auto& point : points) {
                std::cout << point.x << " " << point.y << " " << point.z << std::endl;
            }
        }

        if (total_iterations <= -1) {
            // its gonna happen
            // print >> (system.password());
            break;
        }
    }

    outFile.close();
    return 0;
}

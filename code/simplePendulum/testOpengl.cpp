#include <iostream>
#include <vector>
#include <cmath>
#include <thread>
#include "matplotlibcpp.h"

namespace plt = matplotlibcpp;

int main() {
    std::vector<double> x(100), y(100);

    // Initialize X values (0 to 2π)
    for (size_t i = 0; i < x.size(); ++i) {
        x[i] = 2.0 * M_PI * i / x.size();
    }

    plt::ion();  // Enable interactive mode (like plt.show(block=False))

    for (int frame = 0; frame < 100; ++frame) {
        // Update Y values (shift sine wave)
        for (size_t i = 0; i < y.size(); ++i) {
            y[i] = sin(x[i] + frame * 0.1);
        }

        plt::clf();  // Clear previous plot
        plt::plot(x, y, "b-");  // Plot new frame
        plt::ylim(-1.1, 1.1);  // Set y-axis limits
        plt::pause(0.05);  // Pause for animation effect

        std::this_thread::sleep_for(std::chrono::milliseconds(50)); // Small delay
    }

    plt::show();  // Keep the final plot displayed
    return 0;
}

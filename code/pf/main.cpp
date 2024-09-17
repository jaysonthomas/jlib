#define _USE_MATH_DEFINES
#include <iostream>
#include <cmath>
#include "util/matplotlibcpp.h"

namespace plt = matplotlibcpp;

int main()
{
  // Prepare data.
  int n = 8;
  std::vector<double> x = {0, 60, 60, 45, 45,106,106,0, 0};
  std::vector<double> y = {0, 0, 45, 45, 59, 59, 105,105, 0};
  
  // Set the size of output image = 1200x780 pixels
  plt::figure_size(1200, 780);

  // Plot line from given x and y data. Color is selected automatically.
  plt::plot(x, y, {{"color", "red"}, {"marker", "o"}, {"linestyle", "--"}, {"linewidth", "3"}});

  // Set x-axis to interval [0,1000000]
  // plt::xlim(0, 1000 * 1000);

  // Add graph title
  plt::title("Sample figure");

  // save figure
  const char *filename = "pf.png";
  std::cout << "Saving result to " << filename << std::endl;
  ;
  plt::show(filename);
}

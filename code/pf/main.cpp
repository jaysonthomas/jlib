#define _USE_MATH_DEFINES
#include <iostream>
#include <cmath>
#include "util/matplotlibcpp.h"
#include "map/Map.h"
#include "include/point.h"
#include "bot/Bot.h"
#include "plotter/Plotter.h"

namespace plt = matplotlibcpp;

int main()
{
  Points testMap = {
      {0.0, 0.0}, {60.0, 0.0}, {60.0, 45.0}, {45.0, 45.0}, {45.0, 59.0}, {106.0, 59.0}, {106.0, 105.0}, {0.0, 105.0}};

  Map map;
  map.initialise(testMap);

  Bot bot({0, 0}, 90.4);
  std::cout << "\n\n"
            << bot.pos[1] << "\n";

  Plotter plotter;
  plotter.draw(map);
  plotter.draw(bot);

  plotter.display();

  // Prepare data.
  int n = 8;
  std::vector<double> x = {0, 60, 60, 45, 45, 106, 106, 0, 0};
  std::vector<double> y = {0, 0, 45, 45, 59, 59, 105, 105, 0};

  // Set the size of output image = 1200x780 pixels

  // Plot line from given x and y data. Color is selected automatically.
  // plt::plot(x, y, {{"color", "red"}, {"marker", "o"}, {"linestyle", "--"}, {"linewidth", "3"}});

  // Set x-axis to interval [0,1000000]
  // plt::xlim(0, 1000 * 1000);

  // Add graph title
  // plt::title("Sample figure");

  // plt::show();
}

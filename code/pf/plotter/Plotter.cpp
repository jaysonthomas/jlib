#include <Bot.hpp>
#include <matplotlibcpp.hpp>
#include "Plotter.hpp"

namespace plt = matplotlibcpp;

Plotter::Plotter()
{
  plt::figure_size(1200, 780);
}

void Plotter::draw(Map &map)
{
  plt::plot(map.inPolygonFormatX, map.inPolygonFormatY,
            {{"color", mConfig.colour}, {"linewidth", mConfig.lineWidth}});
}

void Plotter::draw(Bot &bot)
{
  plt::plot({bot.pos[0]}, {bot.pos[1]}, "o");
}

void Plotter::display()
{
  plt::show();
}

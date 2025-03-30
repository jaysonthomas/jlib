#ifndef PLOTTER_H_
#define PLOTTER_H_

#include <string>
#include <Map.hpp>

struct MapConfig
{
  const std::string colour = "red";
  const std::string lineWidth = "2";
};

// struct BotConfig
// {
//   const std::string
// };

class Plotter 
{
public:
  MapConfig mConfig;

  Plotter();
  void draw(Map &map);
  void draw(Bot &bot);
  void display();
};

#endif
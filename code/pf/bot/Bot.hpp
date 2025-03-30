#ifndef BOT_H_
#define BOT_H_

#include <point.hpp>
#include <line.hpp>

class Bot
{
public:
  Point pos;
  double angleInRad;
  Point direction;    

  Bot(const Point &pos, const double &angleInDeg);
};

#endif
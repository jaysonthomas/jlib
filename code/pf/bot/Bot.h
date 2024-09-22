#ifndef BOT_H_
#define BOT_H_

#include "point.h"
#include "line.h"

class Bot
{
public:
  Point pos;
  double angleInRad;
  Point direction;    

  Bot(const Point &pos, const double &angleInDeg, const Point &direction);
};

#endif
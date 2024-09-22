#include "Bot.h"
#include "angleConversion.h"

Bot::Bot(const Point &pos, const double &angleInDeg, const Point &direction)
{
  Bot::pos = pos;
  angleInRad = toRad(angleInDeg);
  Bot::direction = direction;
}


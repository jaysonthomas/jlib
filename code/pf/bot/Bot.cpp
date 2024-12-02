#include "Bot.h"
#include "angleConversion.h"
#include <cmath> 

Bot::Bot(const Point &pos, const double &angleInDeg)
{
  Bot::pos = pos;
  angleInRad = toRad(angleInDeg);
  Bot::direction = {cosf32(angleInDeg), sinf32(angleInDeg)};
}


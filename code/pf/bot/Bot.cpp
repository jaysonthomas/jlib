#include "Bot.hpp"
#include <angleConversion.hpp>
#include <cmath> 

Bot::Bot(const Point &pos, const double &angleInDeg)
{
  Bot::pos = pos;
  angleInRad = toRad(angleInDeg);
  Bot::direction = {cosf32(angleInDeg), sinf32(angleInDeg)};
}


#ifndef MAP_H_
#define MAP_H_

#include "point.h"
#include "line.h"

/*
 * Except for the unmodified points, all other variables in Map are closed.
 */
class Map
{
public:
  Points points;
  Line lines;

  std::vector<double> inPolygonFormatX;
  std::vector<double> inPolygonFormatY;

  void initialise(const Points &map);
  void printBorderLines();

private:
  void initialisePolygonFormat(const Points &map);
  void initialiseClosedMapPoints(const Points &map);
  void initialiseBorderLines(const Points &map);
};

#endif
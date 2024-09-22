#include "Map.h"
#include <vector>
#include <cstddef>
#include <iostream>

void Map::initialise(const Points &map)
{
  unmodifiedPoints = map;
  initialisePolygonFormat(map);
  initialiseClosedMapPoints(map);
  initialiseBorderLines(points);
  printBorderLines();
}

void Map::initialiseClosedMapPoints(const Points &map)
{
  points = map;
  points.push_back(map[0]);
}

/*
 * Assumes the map is an open one.
 */
void Map::initialisePolygonFormat(const Points &map)
{
  inPolygonFormatX.clear();
  inPolygonFormatY.clear();

  for (const auto &p : map)
  {
    inPolygonFormatX.push_back(p[0]); // X-coordinates
    inPolygonFormatY.push_back(p[1]);
  }

  // Close the polygon by adding the first point again
  inPolygonFormatX.push_back(map[0][0]);
  inPolygonFormatY.push_back(map[0][1]);
}

void Map::initialiseBorderLines(const Points &map)
{
  lines.clear();

  for (size_t i = 0; i < map.size() - 1; i++)
  {
    lines.push_back({map[i][0], map[i][1],
                     map[i + 1][0], map[i + 1][1]});
  }
}

void Map::printBorderLines()
{
  std::cout <<"Border Lines: " << std::endl;

  for (const auto &line : lines)
  {
    std::cout << "[" << line[0] << ", " << line[1]
              << ", " << line[2] << ", " << line[3] << "]";
  }
}
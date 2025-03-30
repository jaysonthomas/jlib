#ifndef SCANNER_H_
#define SCANNER_H_

#include "point.h"

struct ScanConfig
{
  int nScans;
  float angleBetweenScans;
};

class Scanner 
{
public:
  Point locationOffset;
  ScanConfig config;
};

#endif
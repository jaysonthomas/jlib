#include "Matrix.h"
#include "angleConversion.h"
#include "coord.h"

#include <cmath>

Eigen::Matrix3d Matrix::createTranslation(const Point &point)
{
  Eigen::Matrix3d output;

  output << 1, 0, point[X],
      0, 1, point[Y],
      0, 0, 1;

  return output;
}

Eigen::Matrix3d Matrix::createZRotation(const double &angleInDeg)
{
  Eigen::Matrix3d output;

  const double angleInRad = toRad(angleInDeg);
  output << cosf32(angleInRad), -sinf32(angleInRad), 0,
      sinf32(angleInRad), cosf32(angleInRad), 0,
      0, 0, 1;

  return output;
}
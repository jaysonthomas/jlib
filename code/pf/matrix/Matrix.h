#ifndef MATRIX_H_
#define MATRIX_H_

#include <vector>
#include "point.h"
#include <Eigen/Dense>

/*
 * Except for the unmodified points, all other variables in Map are closed.
 */
class Matrix
{
public:
  Eigen::Matrix3d createTranslation(const Point &point);
  Eigen::Matrix3d createZRotation(const double &angleInDeg);
};

#endif
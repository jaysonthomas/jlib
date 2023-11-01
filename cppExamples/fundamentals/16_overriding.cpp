#include <assert.h>
#include <cmath>


#define PI 3.14159


class VehicleModel {
  virtual void Move(double, double) = 0;
};


class ParticleModel : public VehicleModel {
public:
  double x, y, theta;


  ParticleModel() : x(0), y(0), theta(0) {}


  void Move(double v, double phi) override {
    theta += phi;
    x += v * cos(theta);
    y += v * cos(theta);
  }  
};


class BicycleModel : public ParticleModel {
private:
  int L;


public:
  BicycleModel() : L(0) {}


  void Move(double v, double phi) override {
    theta += v/L * tan(phi);
    x += v * cos(theta);
    y += v * cos(theta);
  }
};


int main() {
  // Test function overriding
  ParticleModel particle;
  BicycleModel bicycle;
  particle.Move(10, PI / 9);
  bicycle.Move(10, PI / 9);
  assert(particle.x != bicycle.x);
  assert(particle.y != bicycle.y);
  assert(particle.theta != bicycle.theta);
}

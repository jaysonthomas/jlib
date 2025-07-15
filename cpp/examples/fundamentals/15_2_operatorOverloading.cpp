#include <assert.h>
#include <iostream>


class Point {
public:
  Point(int x = 0, int y = 0) : x(x), y(y) {}


  Point operator+(const Point& addend) {
    Point sum;
    sum.x = x + addend.x;
    sum.y = y + addend.y;


    std::cout << x << " : " << addend.x << std::endl;
    return sum;
  }


  int x, y;
};


int main() {
  Point p1(10, 5), p2(2, 4);
  Point p3 = p1 + p2; // An example call to "operator +";
  assert(p3.x == p1.x + p2.x);
  assert(p3.y == p1.y + p2.y);
}

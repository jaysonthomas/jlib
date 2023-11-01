#include <cassert>
#include <vector>


class Matrix {
public:
  Matrix(int rows, int cols) : rows_(rows), cols_(cols), values_(rows*cols) {}
  
  // The address of the member 'values_' is returned.
  int& operator() (int row, int col) {
    return values_[(row*cols_) + col];
  }


  int operator() (int row, int col) const {
    return values_[(row*cols_) + col];
  }


private:
  int rows_;
  int cols_;
  std::vector <int> values_;
};


int main() {
  Matrix m(2,2);

  // The first function with the operator keyword is called here.
  m(0,0) = 4;   
  assert(m(0,0) == 4);
}

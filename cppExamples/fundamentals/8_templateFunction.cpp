#include <iostream>

// return type is T
template <typename T> 
T sum(T a, T b) {
  return a + b;
}

int main() {
  std::cout << sum<double>(20.0, 13.7) << "\n"; 
}

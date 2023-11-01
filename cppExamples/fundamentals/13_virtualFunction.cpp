#include <iostream>


class Animal {
  // Using const after a function signature: It is a way to indicate that calling this function won't alter the internal data members of the object. It is a promise made by the function that it won't modify any non-static data members of the class it belongs to.

  // A const member function can only call other const member functions and read data members of the object. It cannot modify the object's state in any way.
  virtual void talk() const = 0;
};


class Human : public Animal {
public:
  void talk() const {
    std::cout << "Hello\n";
  }
};


int main() {
  Human h;
  h.talk();
}

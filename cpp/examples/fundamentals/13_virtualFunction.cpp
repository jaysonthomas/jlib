#include <iostream>

class Animal {
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

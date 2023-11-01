#include <iostream>


class Animal {
  public:
    void talk() const {
      std::cout << "Talk\n";
    }
};


class Human : public Animal {
  public:
    void talk(std::string content) const {
      std::cout << content << "\n";
    }
};


class Baby : private Human {
  public:
    void cry() {
      talk("Whaa!");
    }
};


int main() {
  Animal animal;
  animal.talk();


  Human human;
  human.talk("hello!");


  Baby baby;
  baby.cry();
  // The user, baby, can’t access talk() but the functions within baby can.
  baby.talk("It's me!");
}

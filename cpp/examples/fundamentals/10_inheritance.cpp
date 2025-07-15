#include <iostream>

class Animal 
{
  public:
    void talk() const {
      std::cout << "Talk\n";
    }
};

class Human : public Animal 
{
  // talk() could be redefined here or new functions added.
};

int main() {
  Animal animal;
  animal.talk();


  Human human;
  human.talk();
}

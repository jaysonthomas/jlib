#include <cassert>
#include <iostream>


using std::cout;


class human {};
class animal {};


void hello() { cout << "Hello world\n"; }
void hello(human h) { cout << "Human\n"; }
void hello(animal a) { cout << "animal\n"; }
void hello(int x) { cout << "int\n"; }


int main() {
  hello();
  hello(human());
  hello(animal());
  hello(5);
}

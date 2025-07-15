#include <iostream>

int& test(void)
{
  int *a = new int(23);
  return *a;
}

int main() 
{
  // Was expecting a print out of 'a' would give the address, but instead it's the value.
  int a = test();
  std::cout << a << std::endl;
  return 0;
}

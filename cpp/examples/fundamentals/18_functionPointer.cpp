#include <iostream>
#include <vector>

using namespace std;

int f3(int arg1, int arg2)
{
  return (arg1 + arg2);
}

class funcPointer
{
  public:
    // The function pointer
    int (*dummy)(int, int);

    // Receives the address of the function. Assign the function pointer to the argument.
    void f1(int (* fptr)(int, int))
    {
      dummy = fptr;
    }

    // Use the function pointer
    void f2()
    {
      cout << dummy(2, 3) << "\n";
    }

};

int main()
{
  funcPointer f;
  f.f1(&f3);
  f.f2();

  return 0;
}

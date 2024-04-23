#include <iostream>
using namespace std;
class MyInt
{
  int *_p;                // pointer to heap data
public:
    MyInt(int *p = NULL) 
    { 
      _p = p; 
    }
    
    ~MyInt() 
    { 
        std::cout << "resource " << *_p << " deallocated" << std::endl;
        delete _p; 
    }
    
    int& operator*()    // overload dereferencing operator
    { 
      return *_p; 
    } 
};

int main()
{
    double den[] = {1.0, 2.0, 3.0, 4.0, 5.0};     // Allocated on the stack
    for (size_t i = 0; i < 5; ++i)
    {
        // en is allocated on the stack, whereas 'new int' is allocated on the heap.
        MyInt en(new int(i));


        // Use the resource
        std::cout << *en << "/" << den[i] << " = " << *en / den[i] << std::endl;
    }
    return 0;
}

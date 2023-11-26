#include <iostream>
using namespace std;
class MyInt
{
    int *_p; // pointer to heap data
public:
    MyInt(int *p = NULL) { _p = p; }
    ~MyInt() 
    { 
        std::cout << "resource " << *_p << " deallocated" << std::endl;
        delete _p; 
    }
    int &operator*() { return *_p; } // overload dereferencing operator
};

int main()
{
    double den[] = {1.0, 2.0, 3.0, 4.0, 5.0}; // Allocated on the stack
    for (size_t i = 0; i < 5; ++i)
    {
        // Both en and 'new int' are allocated on the heap.
        MyInt *en = new MyInt(new int(i));

        // Use the resource
        std::cout << **en << "/" << den[i] << " = " << **en / den[i] << std::endl;
    }
    return 0;
}

#include <iostream>

int AddNumbers(int a, int b, int c, int d=10) 
{
    return a + b + c + d;
}

int main() {
    int result = AddNumbers(2, 3, 4);
    std::cout << "Result: " << result << std::endl;
    return 0;
}

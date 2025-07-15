#include <memory>
#include <iostream>

void RawPointer()
{
  int *raw = new int;       // create a raw pointer on the heap
  *raw = 1;                 // assign a value
  delete raw;               // delete the resource again
}

void UniquePointer()
{
  // create a unique pointer on the stack
  std::unique_ptr<int> unique(new int); 
  *unique = 2;              // assign a value
  // delete is not neccessary
}

int main()
{
  RawPointer();
  UniquePointer();
  return 0;
}
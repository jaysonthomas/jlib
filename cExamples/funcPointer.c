#include <stdio.h>
#include <stdlib.h>

typedef void (*funcPtr)(int);

void foo(int x)
{
  printf("%d\n", x);
}

void main()
{
  funcPtr fp = foo;
  fp(4);
}
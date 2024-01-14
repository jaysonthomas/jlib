#include <cassert>
#include <iostream>

struct Date {
  int day{1};
  int month{0};
  int year{2000};
};

int main()
{
  Date date;
  assert(date.day == 1);
  assert(date.month == 1);
  assert(date.year == 2000);
  std::cout << date.day << "/" << date.month << "/" << date.year << "\n";
}

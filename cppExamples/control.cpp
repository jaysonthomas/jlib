#include <iostream>

const int JITTER = 50;  // +/-
const int RANGE = 1000; // End stops (+/-).
const int TARGET = 0;   // Target position.
const int COLUMNS = 79;

class Motor
{
private:
  int position = -RANGE;
  int speed = 0;

  int getJitter()
  {
    return (rand() % (JITTER * 2 + 1) - JITTER);
  }

public:
  int getPosition() const { return position; }
  int getSpeed() const { return speed; }

  void drive(int force)
  {
    position += speed + getJitter(); // Random number represents mechanical variance.
    speed += force;                  // "Mass" of 1.
    if (position > RANGE)
    {
      position = RANGE;
      speed = 0;
    }
    else if (position < -RANGE)
    {
      position = -RANGE;
      speed = 0;
    }
  }
};

void printPosition(const Motor motor)
{
  const int positionColumn = motor.getPosition() * COLUMNS / (2 * RANGE);
  const int targetColumn = TARGET * COLUMNS / (2 * RANGE);
  const int loopRange = COLUMNS / 2;
  std::cout << "|";
  for (int i = -loopRange; i <= loopRange; i++)
    if (i == positionColumn)
      std::cout << "*";
    else if (i == targetColumn)
      std::cout << ".";
    else
      std::cout << " ";
  std::cout << "|" << std::endl;
}

int main()
{
  std::cout << "Bot Controller..." << std::endl;
  Motor m;
  int force = 0;

  // WRITE HERE

  for (int i = 0; i < 100; ++i)
  {

    // AND HERE
    printPosition(m);
    m.drive(force);
  }
  return 0;
}

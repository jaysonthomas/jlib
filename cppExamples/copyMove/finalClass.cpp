#include <iostream>
#include <string>

class Animal
{
public:
  Animal(const std::string &name) : name_(name) {}
  virtual ~Animal() = default;

  virtual void speak() const
  {
    std::cout << "Animal: " << name_ << "\n";
  }

protected:
  std::string name_;
};

// Since Dog is final, no one can inherit from it.
class Dog final : public Animal
{
public:
  Dog(const std::string &name, const std::string &breed) : Animal(name), breed_(breed) {}

  // Safe custom copy constructor
  Dog(const Dog &other) : Animal(other), breed_(other.breed_)
  {
    std::cout << "Dog copy constructor\n";
  }

  // Safe custom move constructor
  Dog(Dog &&other) noexcept : Animal(std::move(other)), breed_(std::move(other.breed_))
  {
    std::cout << "Dog move constructor\n";
  }

  // Safe custom copy assignment
  Dog &operator=(const Dog &other)
  {
    std::cout << "Dog copy assignment\n";
    if (this != &other)
    {
      Animal::operator=(other); // copy base part
      breed_ = other.breed_;    // copy own part
    }
    return *this;
  }

  // Safe custom move assignment
  Dog &operator=(Dog &&other) noexcept
  {
    std::cout << "Dog move assignment\n";
    if (this != &other)
    {
      Animal::operator=(std::move(other)); // move base part
      breed_ = std::move(other.breed_);    // move own part
    }
    return *this;
  }

  void speak() const override
  {
    std::cout << "Dog: " << name_ << ", Breed: " << breed_ << "\n";
  }

private:
  std::string breed_;
};

int main() {
  Dog dog1("Rex", "German Shepherd");
  Dog dog2 = dog1;               // copy constructor
  Dog dog3("Temp", "Poodle");
  dog3 = dog1;                   // copy assignment

  Dog dog4 = std::move(dog1);    // move constructor
  Dog dog5("Temp", "Beagle");
  dog5 = std::move(dog2);        // move assignment

  dog3.speak();
  dog4.speak();
  dog5.speak();
}
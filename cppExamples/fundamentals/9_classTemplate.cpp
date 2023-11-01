#include <assert.h>
#include <string>
#include <sstream>


template <typename KeyType, typename ValueType>
class Mapping {
public:
  Mapping(KeyType key, ValueType value);
  
  std::string Print() const 
  {
    std::ostringstream stream;
    stream << key << ": " << value;
    return stream.str();
  }
  
  KeyType key;
  ValueType value;
};


template <typename KeyType, typename ValueType>
Mapping<KeyType, ValueType>::Mapping(KeyType key, ValueType value) : key(key), value(value) {}

// Test
int main() {
  Mapping<std::string, int> mapping("age", 20);
  assert(mapping.Print() == "age: 20");
}

// The constructor can also be directly defined in the class:
// Mapping(KeyType key, ValueType value) : key(key), value(value) {}

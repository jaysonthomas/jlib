namespace English 
{
  void Hello() { std::cout << "Hello, World!\n"; }
}  


namespace Spanish 
{
  void Hello() { std::cout << "Hola, Mundo!\n"; }
}


int main() {
  English::Hello();
  Spanish::Hello();
}

class MyClass {
public:
    int publicMember;  // Public member variable
    void publicMethod() {
        // Public member function
    }
};

int main() {
    MyClass obj;
    obj.publicMember = 42;   // Directly accessing and modifying public member variable
    obj.publicMethod();      // Calling public member function
    return 0;
}

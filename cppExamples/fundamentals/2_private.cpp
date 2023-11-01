class MyClass {
private:
    int privateMember;  // Private member variable
    void privateMethod() {
        // Private member function
    }
public:
    void setPrivateMember(int value) {
        // Member function to modify private member variable
        privateMember = value;
    }
};

int main() {
    MyClass obj;
    // obj.privateMember = 42;   // This line will cause a compilation error as privateMember is inaccessible
    obj.setPrivateMember(42);   // Modifying private member using a public member function
    // obj.privateMethod();      // This line will cause a compilation error as privateMethod is inaccessible
    return 0;
}

class MyClass {
private:
    int privateMember;  
    void privateMethod() {
    }
public:
    void setPrivateMember(int value) {
        privateMember = value;
    }
};

int main() {
    MyClass obj;
    // obj.privateMember = 42;    // Compilation error as privateMember is inaccessible
    obj.setPrivateMember(42);     // Modifying private member using a public member function
    // obj.privateMethod();      // Compilation error as privateMethod is inaccessible
    return 0;
}

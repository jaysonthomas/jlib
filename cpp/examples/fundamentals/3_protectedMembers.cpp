#include <iostream>

class Base {
private:
    int privateMember;

protected:
    int protectedMember;

public:
    Base() : privateMember(0), protectedMember(0) {}

    void setPrivateMember(int value) {
        privateMember = value;
    }

    void setProtectedMember(int value) {
        protectedMember = value;
    }

    void printMembers() {
        std::cout << "Private member: " << privateMember << std::endl;
        std::cout << "Protected member: " << protectedMember << std::endl;
    }
};

class Derived : public Base {
public:
    void modifyMembers() {
        // privateMember = 10;  // Error: privateMember is not accessible in Derived
        protectedMember = 10;   // OK: protectedMember is accessible in Derived
    }
};

int main() {
    Base baseObj;
    baseObj.setPrivateMember(5);
    baseObj.setProtectedMember(8);
    baseObj.printMembers();

    Derived derivedObj;
    // derivedObj.privateMember = 15;  // Error: privateMember is not accessible in Derived
    // derivedObj.protectedMember = 12;  // Error: protectedMember is not accessible outside Derived
    derivedObj.modifyMembers();
    derivedObj.printMembers();

    return 0;
}

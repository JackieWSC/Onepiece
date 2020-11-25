#include <iostream>
#include <set>
#include <vector>
#include <algorithm>

#include "chapter_2.h"

struct S {
    int n;
    std::string s;
    float d;

    bool operator<(const S& rhs) const {
        return std::tie(n ,s, d) < std::tie(rhs.n, rhs.s, rhs.d);
    }
};

int main() {
    std::cout << "Hello, Jackie!"
              << "It is used by CLion IDE!"
              << "And the cmake version is 3.18"
              << std::endl;

    // structured bindings
    std::set<S> mySet;

    // pre C++ 17
    {
        S value {42, "Test", 3.14};
        std::set<S>::iterator iter;
        bool inserted = false;

        std::tie(iter, inserted) = mySet.insert(value);

        if (inserted)
            std::cout << "C++14: Value ("
                      << iter->n
                      << ","
                      << iter->s
                      << ") was inserted\n";
    }

    // with C++ 17
//    {
//        S value{100, "Abc", 100.0};
//        const auto [iter, inserted] = mySet.insert(value);
//
//        if (inserted)
//            std::cout << "C++17: Value ("
//                      << iter->n
//                      << ","
//                      << iter->s
//                      << ") was inserted" << "\n";
//    }

    chapter_2 ch_2;

    ch_2.Run();

    return 0;
}
//
// Created by Scity on 10/9/2020.
//

#include "chapter_2.h"

#include <iostream>
#include <vector>

using namespace std;

MagicFoo::MagicFoo(std::initializer_list<int> list) {
    for (initializer_list<int>::iterator it = list.begin();
         it != list.end();
         ++it) {

        vec.push_back(*it);
    }
}

void MagicFoo::Add(std::initializer_list<int> list) {

    for (initializer_list<int>::iterator it = list.begin();
         it != list.end();
         ++it) {

        vec.push_back(*it);
    }
}

void MagicFoo::Dump() {

    for (auto it = vec.begin(); it != vec.end(); ++it) {
        cout << *it << ",";
    }
    cout << endl;
}

Base::Base()
 : value_1(1)
{

}

Base::Base(int value)
 : Base()
{
    value_2 = value;
}

void Base::Dump() {
    cout << "Value 1:" << value_1
         << ", Value 2:" << value_2
         << endl;
}

void chapter_2::Run () {

    cout << "---- Chapter 2----" << endl;

    cout << "---- variables_and_initialization ----" << endl;
    variables_and_initialization();
    cout << endl;

    cout << "---- initializer_list ----" << endl;
    initializer_list();
    cout << endl;

    cout << "---- object_oriented ----" << endl;
    object_oriented();
    cout << endl;
}

void chapter_2::variables_and_initialization() {

    std::vector<int> vec = {1, 2, 3, 4};

    const std::vector<int>::iterator it = std::find(vec.begin(), vec.end(), 2);
    if (it != vec.end()) {
        *it = 3;
    }

    // support after C++17
//    if (const std::vector<int>::iterator it = std::find(vec.begin(), vec.end(), 3);
//    it != vec.end()) {
//        *it = 4;
//    }

    for (std::vector<int>::iterator it = vec.begin(); it != vec.end(); ++it)
    {
        std::cout << *it << ",";
    }
}

void chapter_2::initializer_list() {

    MagicFoo magicFoo({1, 3, 5, 7, 9});

    magicFoo.Add({2, 4, 6, 8, 10});
    magicFoo.Dump();
}

void chapter_2::object_oriented() {

    Base first;
    first.Dump();

    Base second(2);
    second.Dump();
}

//
// Created by Scity on 10/9/2020.
//

#ifndef CLION_ENV_CHAPTER_2_H
#define CLION_ENV_CHAPTER_2_H

#include <initializer_list>
#include <vector>

class chapter_2 {

public:
    void Run();


private:

    void variables_and_initialization();

    void initializer_list();

    void object_oriented();
};


class MagicFoo {

public:
    MagicFoo(std::initializer_list<int> list);

    void Add(std::initializer_list<int> list);

    void Dump();

private:
    std::vector<int> vec;
};


class Base {

public:

    Base();

    Base(int value);

    void Dump();

public:

    int value_1;
    int value_2;
};

#endif //CLION_ENV_CHAPTER_2_H

cmake_minimum_required(VERSION 3.6)
project(clion_env)

set(CMAKE_CXX_STANDARD 14)

set(SOURCE_FILES main.cpp chapter_2.cpp chapter_2.h)
add_executable(clion_env ${SOURCE_FILES})
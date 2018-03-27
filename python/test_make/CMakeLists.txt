cmake_minimum_required(VERSION 3.6)
project(python)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES main.cpp)
set(PYTHON_FILES PhoneChecker.py)

add_executable(python ${SOURCE_FILES} ${PYTHON_FILES})
target_link_libraries(python ${PYTHON_LIBRARIES})
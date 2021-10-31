cmake_minimum_required(VERSION 3.12)

project(c-solver C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})

add_executable(c-solver
        src/c-solver.cpp
        src/Cube.cpp
        src/Shape.cpp
        )

add_compile_options(-Ofast -Wall -Wextra)
target_include_directories(c-solver PRIVATE ${CMAKE_CURRENT_LIST_DIR}/src)



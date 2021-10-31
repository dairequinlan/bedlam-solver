
#pragma once

#include "Shape.hpp"

#define MAX_SIZE 6
/* Cube class contains the logic for maintaining the current
    state of the container, or Bedlam Cube, and methods for 
    checking, inserting, and removing individual Shape objects
    from the cube space. 

 Each Cube is made up of X * Y * Z Cuboids, Each of which
    for simplicities sakes contain all the info for the shapes
    that occupy the cube. */
struct Cuboid {
    Shape *shape;
    int rotation;
    int x;
    int y;
    int z;
};

class Cube {
    public:
        Cube(int width, int depth, int height);
        bool checkShape(Shape *shape, int rotation, int x, int y, int z);
        bool putShape(Shape *shape, int rotation, int x, int y, int z);
        void removeShape(Shape *shape, int rotation, int x, int y, int z);

        int width = 0;
        int depth = 0;
        int height = 0; 

        Cuboid cuboids[MAX_SIZE][MAX_SIZE][MAX_SIZE];
};
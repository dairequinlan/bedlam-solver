#include <iostream>
#include "Cube.hpp"



Cube::Cube(int width, int depth, int height) {

    this->width = width;
    this->depth = depth;
    this->height = height;
    for(int x = 0; x < width; x++) {
        for(int y = 0; y < depth; y++) {
            for(int z = 0; z < height; z++) {
                cuboids[x][y][z].shape = NULL;
            }
        }
    }
}

bool Cube::checkShape(Shape *shape, int rotation, int x, int y, int z){
        
        Rotation *rot = shape->rotations[rotation]; 
        for(int bi = 0; bi < rot->numBlocks; bi ++) {
            int cx = rot->blocks[bi].x + x;
            int cy = rot->blocks[bi].y + y;
            int cz = rot->blocks[bi].z + z;
            
            if( cx >= this->width ||
                cy >= this->depth ||
                cz >= this->height ||
                this->cuboids[cx][cy][cz].shape != NULL)
                return false;
        }

        return true;
}


void Cube::removeShape(Shape *shape, int rotation, int x, int y, int z){
    Rotation *rot = shape->rotations[rotation]; 
    for(int bi = 0; bi < shape->rotations[rotation]->numBlocks; bi ++) {
        int cx = rot->blocks[bi].x + x;
        int cy = rot->blocks[bi].y + y;
        int cz = rot->blocks[bi].z + z;
    
        this->cuboids[cx][cy][cz].shape = NULL;
    }
}

bool Cube::putShape(Shape *shape, int rotation, int x, int y, int z){
    
    if (this->checkShape(shape, rotation, x, y, z)) {
        
        Rotation *rot = shape->rotations[rotation]; 
        for(int bi = 0; bi < shape->rotations[rotation]->numBlocks; bi ++) {
            int cx = rot->blocks[bi].x + x;
            int cy = rot->blocks[bi].y + y;
            int cz = rot->blocks[bi].z + z;
        
            this->cuboids[cx][cy][cz].shape = shape;
            this->cuboids[cx][cy][cz].x = x;
            this->cuboids[cx][cy][cz].y = y;
            this->cuboids[cx][cy][cz].z = z;
            this->cuboids[cx][cy][cz].rotation = rotation;
        }        
        return true;
    } 
    return false;
}
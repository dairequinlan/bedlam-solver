#pragma once
#include "json.hpp"
using json = nlohmann::json;

#include <string>
using namespace std;


typedef struct Block {
    int x;
    int y;
    int z;
} Block;

typedef struct Rotation {
    int numBlocks;
    Block *blocks;
} Rotation;

class Shape{

    public:
        Shape();
        Rotation** rotations;
        int numRotations;
        string name;
        string colour;
        
        static Shape* buildShape(json fromJson);
        static Rotation *buildRotation(json fromJson);
};
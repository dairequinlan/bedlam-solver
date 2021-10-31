#include <string>
#include <iostream>
#include <istream>
#include <ostream>
#include <iterator>
#include "Shape.hpp"
#include "json.hpp"
using json = nlohmann::json;

Shape::Shape() {

}

Shape* Shape::buildShape(json fromJson) {
    Shape *shape = new Shape();
    shape->name = fromJson["name"].get<std::string>();
    shape->colour = fromJson["colour"].get<std::string>();

    std::cerr << shape->name << " : " << shape->colour << std::endl;
    
    json jsonRotations = fromJson["rotations"];
    int numRotations = jsonRotations.size();

    shape->rotations = new Rotation*[numRotations];
    shape->numRotations = numRotations;
    for(int rot=0;rot < numRotations; rot++){
        shape->rotations[rot] = Shape::buildRotation(jsonRotations[rot]);
    }

    return shape;
}

Rotation* Shape::buildRotation(json fromJson){

    Rotation *rotation = new Rotation();
    rotation->blocks = new Block[fromJson.size()];
    rotation->numBlocks = fromJson.size();

    for (int bl = 0; bl < fromJson.size(); bl ++ ){
        rotation->blocks[bl].x = (uint8_t)fromJson[bl][0].get<uint8_t>();
        rotation->blocks[bl].y = fromJson[bl][1].get<uint8_t>();
        rotation->blocks[bl].z = fromJson[bl][2].get<uint8_t>();
    }
    return rotation;
}
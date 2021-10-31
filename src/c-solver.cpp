
#include <string>
#include <iostream>
#include <istream>
#include <ostream>
#include <iterator>
#include "json.hpp"

#include "Cube.hpp"
#include "Shape.hpp"


using json = nlohmann::json;
struct solutionEntry {
    std::string name; 
    int rot;
    int x;
    int y;
    int z;
};

void to_json(json& j, const solutionEntry& se) {
    j = json{{"name", se.name}, {"rot", se.rot}, {"x", se.x}, {"y", se.y}, {"z", se.z}};
}


class Solver {
  public:
    int width;
    int depth;
    int height;
    Cube *cube;
    int numShapes;
    Shape** shapes;
    std::vector<solutionEntry> currentSolution;
    unsigned long long int iterations;
    unsigned long int sanity_check;

    Solver(int width, int depth, int height, Cube *cube, int numShapes, Shape ** shapes) {
        this->width = width;
        this->depth = depth;
        this->height = height;
        this->cube = cube;
        this->numShapes = numShapes;
        this->shapes = shapes;
        this->iterations = 0;
    }

    bool solve(int index) {

        //if we end up with index >= numShapes we've skipped merrily past 
        //the end of our array which means we have a solution. We'll stick
        //it onto our array and continue, and if we've hit the number of
        //desired solutions then we'll return out to pop everything off
        //the stack.
        if(index >= this->numShapes) {
            std::cerr << "FOUND SOLUTION" << std::endl;
            //self.solutions.append(self.current_solution.copy())
            if (true){ //len(self.solutions) == num_solutions:
                //ok in this case we return true and everything should cascade down
                return true;
            } else {
            return false;
            }
        }

        /*right, so grab the shape at the current index,
          and progressively try every x,y,z and rotation
          until we find a fit.*/
        Shape *shape = this->shapes[index];

        for(int x  = 0; x < this->width; x++) {
            for(int y = 0; y < this->depth; y++) {
                for(int z = 0; z < this->height; z++) {
                    for(int rotation = 0; rotation < shape->numRotations; rotation++) {
                        this->iterations += 1;
                        this->sanity_check += 1;
                        if(this->sanity_check == 100000000){
                            std::cerr << this->iterations << std::endl;
                            this->sanity_check = 0;
                        }
                        /*if we DO find a fit, then place it in the 
                          cube, and recursively call this same method
                          with index+1 which is the next shape in the
                          current permutation of shapes */
                        if(this->cube->putShape(shape,rotation,x,y,z)){
                            solutionEntry entry = {shape->name, rotation, x, y, z};
                            this->currentSolution.push_back(entry);

                            if(!this->solve(index + 1)){
                                /*ok so if the next shape CANNOT BE PLACED
                                then we remove THIS shape, and continue
                                our iterations, i.e. first the next rotation
                                and if they all fail then the next z, then y
                                then x. Phew.*/
                                this->cube->removeShape(shape,rotation,x,y,z);
                                this->currentSolution.pop_back();
                            } else {
                                //this means that we've hit the limit of solutions
                                return true;
                            } //try to solve next piece
                        }//put shape is true
                    }//rotation loop
                }// z loop
            }//y loop
        }//x loop
        return false;
    }
};

int main()
{
    json config; 
    std::cin >> config;
    int width, depth, height;

    width = config["width"];
    depth = config["depth"];
    height = config["height"];

    std::cerr << width << ":" << depth << ":" << height << std::endl;

    json jsonShapes = config["shapes"];
    int numShapes = jsonShapes.size();
    std::cerr << "Number shapes: " << numShapes << std::endl;

    Shape* shapes[numShapes];
    
    for(int c1 = 0;c1 < numShapes; c1 ++) {
        shapes[c1] = Shape::buildShape(jsonShapes[c1]);
    }

    Cube* cube = new Cube(width,depth,height);
    Solver* solver = new Solver(4,4,4,cube, numShapes, shapes);
    solver->solve(0);

    json sol = solver->currentSolution;

    std::cout << sol << std::endl;
}
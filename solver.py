from operator import itemgetter
import random
from shape import Shape
from cube import Cube
from renderer import Renderer
import itertools


class Solver:    


    def __init__ (self, cube, shapes):
        self.cube = cube
        self.shapes = shapes
    
        #setup some counters for progress, and
        #a little bit of state to track solutions
        self.permutations = 0
        self.solver_iterations = 0
        self.solver_sanity_check = 0
        self.solutions = []
        self.current_solution = []

    def solve(self, num_solutions):
        for permute in itertools.permutations(self.shapes):
            if self.place_shape(0, num_solutions):
                return True #i.e. we've hit our desired number of solutions.
            self.permutations += 1
            print("Permutation: %i"%self.permutations)       

    #recursive place_shape method
    def place_shape(self, index, num_solutions):

        #if we get HERE it means that we've actually got a solution
        #so we'll push it onto the solutions array, then return false
        #which will force the cycle to continue.
        if index >= len(self.shapes):
            print("HORRAH")
            self.solutions.append(self.current_solution.copy())
            if len(self.solutions) == num_solutions:
                #ok in this case we return true and everything should cascade down
                return True
            else:
                return False

        #right, so grab the shape at the current index,
        #and progressively try every x,y,z and rotation
        #until we find a fit.
        
        shape = self.shapes[index]
        for x in range(self.cube.width):
            for y in range(self.cube.length):
                for z in range(self.cube.depth):
                    for rotation in range(len(shape.rotations)):
                        self.solver_iterations += 1
                        self.solver_sanity_check += 1
                        if self.solver_sanity_check == 100000000:
                            print("%i"%self.solver_iterations)
                            self.solver_sanity_check = 0
                        #if we DO find a fit, then place it in the 
                        #cube, and recursively call this same method
                        #with index+1 which is the next shape in the
                        #current permutation of shapes
                        if self.cube.put_shape(shape,rotation,x,y,z):
                            self.current_solution.append(
                                {"shape":index,"name":shape.name, "colour":shape.colour, "rot":rotation,"x":x,"y":y,"z":z}
                            )
                            if not self.place_shape(index + 1, num_solutions):
                                #ok so if the next shape CANNOT BE PLACED
                                #then we remove THIS shape, and continue
                                #our iterations, i.e. first the next rotation
                                #and if they all fail then the next z, then y
                                #then x. Phew.
                                self.cube.remove_shape(shape,rotation,x,y,z)
                                self.current_solution.pop()
                            else:
                                #this means that we've hit the limit of solutions
                                return True
        return False


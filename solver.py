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
        self.solved_shapes = []

    def solve(self):
        for permute in itertools.permutations(self.shapes):
            if self.place_shape(0):
                return True
            self.permutations += 1       
        # well, should never get here, at least in 
        # any geological timeframe
        return False

    #recursive place_shape method
    def place_shape(self, index):

        #just bail if we've overstepped our array
        if index >= len(self.shapes):
            return True

        #right, so grab the shape at the current index,
        #and progressively try every x,y,z and rotation
        #until we find a fit.
        
        shape = self.shapes[index]
        for x in range(self.cube.width-1):
            for y in range(self.cube.length-1):
                for z in range(self.cube.depth-1):
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
                            if not self.place_shape(index + 1):
                                #ok so if the next shape CANNOT BE PLACED
                                #then we remove THIS shape, and continue
                                #our iterations, i.e. first the next rotation
                                #and if they all fail then the next z, then y
                                #then x. Phew.
                                self.cube.remove_shape(shape,rotation,x,y,z)
                            else:
                                #sucess! every 'next' shape has to return True
                                #for this to be true, so it means we've found
                                #a solution, so add this to the solved_shapes.
                                self.solved_shapes.append(
                                    {"shape":index,"colour":shape.colour, "rot":rotation,"x":x,"y":y,"z":z}
                                )
                                return True
        return False


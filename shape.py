import numpy as np
from enum import Enum
from operator import itemgetter

class Axis(Enum):
    x = 0
    y = 1
    z = 2
    identity = 3

class Shape:

    def __init__(self, colour, blocks):
        self.colour = colour
        self.blocks = blocks
        self.rotations = []
        self.fill_rotations()

    """ ok, so yes using matrices and numpy for this was
        completely unneccessary, I could have just done it
        in a series of axis flips and reflections etc, but 
        what the hey. """

    def _rotate_blocks(self, axis):
        rot = np.matrix([ [ 1, 0, 0],
                          [ 0, 1, 0],
                          [ 0, 0, 1]])

        if axis == Axis.x:
            rot = np.matrix([[ 1, 0, 0],
                             [ 0, 0,-1],
                             [ 0, 1, 0]])
        elif axis == Axis.z:
            rot = np.matrix([[ 0,-1, 0],
                             [ 1, 0, 0],
                             [ 0, 0, 1]])
        elif axis == Axis.y:
            rot = np.matrix([[ 0, 0, 1],
                             [ 0, 1, 0],
                             [-1, 0, 0]])

        rotated_blocks = []

        for block in self.blocks:
            vb = np.array(block)
            rotated = (rot @ vb).tolist()[0]
            rotated_blocks.append(rotated)

        """ sort the blocks so that when we draw them we 
        always draw the 'closest' ones to us last, giving us 
        a neat impression of 3D"""

        rotated_blocks.sort(key=itemgetter(2,1,0))
        """now the normalise step, this just ensures that all 
        the rotated blocks have 0,0,0 as the lowest possible 
        coordinate (not, say -1,-2,1).
        Little pre-calculations like this make life easier in the 
        busy loop when we can just assume stuff like origin = 0,0,0"""

        x,y,z = 0,0,0
        for block in rotated_blocks:
            bx, by, bz = block
            if bx < x: x = bx
            if by < y: y = by
            if bz < z: z = bz
        
        x,y,z = abs(x), abs(y), abs(z)

        for block in rotated_blocks:
            block[0] = block[0] + x
            block[1] = block[1] + y
            block[2] = block[2] + z

        return rotated_blocks

    def rotate(self, axis):
        self.blocks = self._rotate_blocks(axis)
        return self
    
    def compare_rotation(self, rot, comp):
        for index in range(len(rot)):
            if rot[index][0] != comp[index][0] or \
                rot[index][1] != comp[index][1] or \
                rot[index][2] != comp[index][2]:
                    return False
        return True

    def fill_rotations(self):
        """we're going to 'rotate' the original blocks around the 
        identity matrix to ensure that they're 1. sorted correctly 
        and 2. normalised I mean, could just be a setup step but
        easier to ensure it's done here. """
        
        self.rotate(Axis.identity)

        temp_rotations = []

        for rotate_z in (1,2,3,4):
            #spin around the yaxis 4 times then back to normal
            for spin in (1,2,3,4):
                temp_rotations.append(self.blocks.copy())
                self.rotate(Axis.y)
            self.rotate(Axis.z)
        
        #we need the final two 3d cardinal directions i.e. 'up' and 'down'
        self.rotate(Axis.x)
        
        for spin in (1,2,3,4):
            temp_rotations.append(self.blocks.copy())
            self.rotate(Axis.y)
        
        #now rotate 2 more times around the x axis (equivalent to -2) to get the last face
        for final in (1,2):
            self.rotate(Axis.x)

        for spin in (1,2,3,4):
            temp_rotations.append(self.blocks.copy())
            self.rotate(Axis.y)

        #and one last rotation to get the original blocks 
        #back to their original orientation.
        self.rotate(Axis.x)
        
        """for any shapes with symmetries we're going 
        to have duplicate rotations. Lets get rid
        of them to cut down on our iterations"""
        for rotation in temp_rotations:
            #check if its there already
            present = False
            for check_rotation in self.rotations:
                if self.compare_rotation(check_rotation, rotation):
                    present = True
                    break
            if not present:
                self.rotations.append(rotation)

    def __repr__(self):
        return "%s"%(self.colour)

    __str__ = __repr__

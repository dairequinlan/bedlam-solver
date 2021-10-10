
""" Cube class contains the logic for maintaining the current
    state of the container, or Bedlam Cube, and methods for 
    checking, inserting, and removing individual Shape objects
    from the cube space. """

""" Each Cube is made up of X * Y * Z Cuboids, Each of which
    for simplicities sakes contain all the info for the shapes
    that occupy the cube. """
class Cuboid:
    def __init__(self):
        self.shape = None #empty cuboid if the shape is None
        self.rotation = 0
        self.x = -1
        self.y = -1
        self.z = -1

    def __repr__(self):
        return "%s:%s"%(self.shape, self.rotation)

    __str__ = __repr__

class Cube:
    
    #initialiase with x*y*z cuboids
    def __init__(self, width=4, length=4, depth=4, ):
        self.width = width
        self.length = length
        self.depth = depth
        self.space = [[[Cuboid() for x in range(self.width)] for y in range(self.length)] for z in range(self.depth)]

    #checks that a specific shape and rotation of that shape
    #will fit into this cube at position x,y,z. Basically if 
    #_any_ of the 'blocks' that make up the shape correspond
    #to a cuboid that already HAS a shape assigned, then this
    #shape will not fit.
    def check_shape(self, shape, rotation ,x ,y ,z):
        for block in shape.rotations[rotation]:
                bx, by, bz = block
                cx = bx + x
                cy = by + y
                cz = bz + z
                if cx >= self.width or \
                    cy >= self.length or \
                    cz >= self.depth or \
                    self.space[cx][cy][cz].shape != None:
                    return False
        return True
    
    # blanks out the cuboid shape objects for a given shape 
    # This happens during the iterative process of trying 
    # each shape in turn, if a child shape cannot be placed
    # then the parent has to be removed and moved/rotated 
    # before being placed again.
    def remove_shape(self, shape, rotation, x, y, z):
        for block in shape.rotations[rotation]:
                bx, by, bz = block
                cx = bx + x
                cy = by + y
                cz = bz + z
                self.space[cx][cy][cz].shape = None

    # Sets the shape into the Cube at this specific rotation
    # and position IFF it fits i.e. uses check_shape first 
    # to see and then sets if it can. 
    def put_shape (self, shape, rotation, x, y, z):
        if self.check_shape(shape, rotation, x, y, z):
            for block in shape.rotations[rotation]:
                bx, by, bz = block
                cx = bx + x
                cy = by + y
                cz = bz + z
            
                self.space[cx][cy][cz].shape = shape
                self.space[cx][cy][cz].rotation = rotation
                self.space[cx][cy][cz].sx = x
                self.space[cx][cy][cz].sy = y
                self.space[cx][cy][cz].sz = z
            return True            
        return False

    def __repr__(self):
        return "%s"%str(self.space)

    __str__ = __repr__
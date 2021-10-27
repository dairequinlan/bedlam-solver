from shape import Shape
from cube import Cube
from PIL import Image, ImageOps

""" This is something I hacked together very
    quickly to provide some way of visually checking
    that the shape and cube setup was working, and to
    display any potential solution. Lots of magic numbers
    here, all based off the specific dimensions of the
    'one-cube' and 'full-cube' png files that we use to
    assemble the viz """

class Renderer:

    def __init__(self, width, height):
        self.cube = Image.open("one-cube.png")
        self.frame = Image.open("full-cube.png")
        r,g,b,self.cube_alpha = self.cube.split()
        self.cube = ImageOps.grayscale(self.cube)
        self.canvas = Image.new("RGBA",(width,height))
        self.cx = int(width/2)
        self.cy = int(height/2)
        self.width = width
        self.height = height

    def coloured_cube(self, color):
        coloured_cube = ImageOps.colorize(self.cube,"#000000",color)
        coloured_cube.putalpha(self.cube_alpha)
        return coloured_cube

    def draw_frame(self,x=-1,y=-1):
        if x==-1: x = self.cx
        x = x -179
        if y==-1: y = self.cy
        y = y-232
        self.canvas.paste(self.frame,(x,y))

    #map coords of the cube to actual x/y coords on
    #screen.
    def map_coords(self, cube_x, cube_y, cube_z, x=-1, y=-1):
        #offset to middle
        if x==-1: x = self.cx
        if y==-1: y = self.cy
        #take into account single 'cube' center point
        x -= 64
        y -= 67
        #now offset x + y depending on where the actual
        #cube x + y indices are
        x += (cube_x * 45) - (cube_y * 45)
        y += (cube_x * 22) + (cube_y * 22) - (cube_z * 58)

        return (x,y)

    def draw_shape(self, shape, shapex, shapey, rotation = -1):

        todraw = shape.blocks
        if rotation != -1:
            todraw = shape.rotations[rotation]

        coloured_cube = self.coloured_cube(shape.colour)
        for block in todraw:
            x,y,z = block
            self.canvas.paste(coloured_cube,
                            (shapex + (x*45) - (y*45),
                            shapey + (x*22) + (y*22) - (z*58)),
                            mask = self.cube_alpha )

    def draw_shapes(self, shapes):

        basex = 100;
        basey = 150;

        for index,shape in enumerate(shapes):
            self.draw_shape(shape, basex, basey)
            basex += 300
            if (index+1)%5 == 0:
                basex = 100
                basey = basey + 300

    def render_rotations(self, shape):
        basex = 100;
        basey = 150;

        index = 0
        for rotation in range(len(shape.rotations)):
            self.draw_shape(shape, basex, basey, rotation)
            basex += 300
            index += 1
            if index == 5:
                index = 0
                basex = 100
                basey += 400

    def draw_cube(self, cube, cubex, cubey):
        #find origin of entire system
        for x in (0,1,2,3):
            for y in (0,1,2,3):
                for z in (0,1,2,3):
                    cuboid = cube.space[x][y][z]
                    if cuboid.shape is not None:
                        coloured_cube = self.coloured_cube(cuboid.shape.colour)
                        self.canvas.paste(coloured_cube,
                            (cubex + (x*45) - (y*45),
                            cubey + (x*22) + (y*22) - (z*58)),
                            mask = self.cube_alpha )

    def draw_solution(self, shapes, solved_shapes):
        basex = 100;
        basey = 100;

        cube = Cube(4,4,4)

        for solution_shape in solved_shapes:

            shape = shapes[solution_shape["shape"]]
            self.draw_shape(shape, basex, basey, 0)
            framex = basex+200 + 179
            framey = basey-100 + 232

            self.draw_frame(framex, framey)
            shapex, shapey = self.map_coords(solution_shape["x"],
                                             solution_shape["y"],
                                             solution_shape["z"],
                                             framex, framey)
            self.draw_shape(shape, shapex, shapey, solution_shape["rot"])

            cube.put_shape(shape, solution_shape["rot"], solution_shape["x"], solution_shape["y"], solution_shape["z"])

            self.draw_frame(framex+400, framey)
            self.draw_cube(cube, framex+400 -65, framey -68)

            basey = basey + 420


    def save(self, name):
        self.canvas.save("%s.png"%name)

    def display(self):
        self.canvas.show()

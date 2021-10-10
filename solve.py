from operator import itemgetter
import random
from shape import Shape
from cube import Cube
from renderer import Renderer
from solver import Solver

""" Setup all 13 shapes, with distinctive colours, makes them
    easier to see when looking at the solved cube"""
        
shapes = [
    Shape("#f5deb3",[[0,0,0],[1,0,0],[1,0,1],[0,1,0],[0,2,0]]),    
    Shape("#8b4513",[[0,0,0],[1,0,0],[0,0,1],[0,1,0],[0,2,0]]),
    Shape("#0000ff",[[0,1,0],[1,0,0],[2,0,0],[1,1,0],[0,2,0]]),
    Shape("#4b0082",[[0,0,0],[0,1,0],[0,1,1],[1,1,0],[1,2,0]]),
    Shape("#ff0000",[[0,0,0],[1,0,0],[1,1,0],[2,1,0],[1,2,0]]),
    Shape("#2f4f4f",[[0,0,0],[0,0,1],[0,1,0],[1,1,0],[1,2,0]]),
    Shape("#ffff00",[[0,1,0],[1,0,0],[0,1,1],[1,1,0],[1,2,0]]),
    Shape("#00ff00",[[0,0,1],[0,1,0],[0,1,1],[1,1,0],[1,2,0]]),
    Shape("#00ffff",[[0,0,0],[0,0,1],[0,1,0],[1,1,0],[0,2,0]]),
    Shape("#228b22",[[0,1,0],[1,0,0],[1,1,0],[2,1,0],[1,2,0]]),
    Shape("#ff00ff",[[0,0,0],[0,1,0],[1,1,0],[0,1,1],[0,2,0]]),
    Shape("#6495ed",[[0,0,0],[0,0,1],[1,0,0],[1,1,0]]),
    Shape("#ff69b4",[[0,0,0],[0,0,1],[0,1,0],[0,2,0],[1,2,0]])
]

# for completeness sakes, we can render each of the shapes in 
# their original rotation onto this canvas. Useful to have 
# a reference of each of the shapes for sanity check purposes
# we'll also save it out as a 'shapes.png'
shapes_renderer = Renderer(1600,1024)
shapes_renderer.draw_shapes(shapes)
#shapes_renderer.display()
#shapes_renderer.save("shapes")
del shapes_renderer

# Now, similarly, lets, for each shape, render out each of the
# 24 rotations into another canvas each and save it out as a 
# PNG
for index, shape in enumerate(shapes):
    rot_renderer = Renderer(1600, 2048)
    rot_renderer.render_rotations(shape)
    #rot_renderer.display()
    #rot_renderer.save("shape%s_rotations"%index)

del rot_renderer

# now onto the meat and bones. We'll create our 'Cube' which will
# store the ongoing state of the iterative solution, and then 
# kick off the solver to start the laborious process of iterating
# through the quadrillions of possible permutations
cube = Cube()
solver_iterations = 0
solver_sanity_check = 0
solved_shapes = []

solver = Solver(cube, shapes)
solved = solver.solve()

if not solved:
    print("NO SOLUTION FOUND")
    exit()

""" get the list of solved shapes from the solver, and sort them 
    by z, x, y to give us _some_ kind of sensible order that we
    can put the shapes into the box in. This isn't perfect, sometimes 
    you still have to take a shape out to put the next one in, needs 
    a litte more thought """

solved_shapes = solver.solved_shapes
solved_shapes.reverse() #because we initally get them from last->first
solved_shapes.sort(key=itemgetter("z","x","y"))
#lets print the solution to the console
print(solver.solved_shapes)
print(solver.solver_iterations)

solution_renderer = Renderer( 800, len(solved_shapes) * 420)
solution_renderer.draw_solution(shapes, solved_shapes)        
solution_renderer.display()
solution_renderer.save("solution")
#renderer.draw_frame()
#renderer.draw_cube(cube)


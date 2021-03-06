from operator import itemgetter
import sys, getopt
import os
from shape import Shape
from cube import Cube
from renderer import Renderer
from solver import Solver
import json
import jsons
import subprocess

def load_config(config_filename):
    config_file = open(config_filename,)
    config = json.load(config_file)
    shapes = []
    for shape in config["shapes"]:
        shapes.append(Shape.build(shape))
    return shapes, config["width"], config["depth"], config["height"]

def render_shapes_and_rotations(shapes):
    # for completeness sakes, we will render each of the shapes in
    # their original rotation onto this canvas. Useful to have
    # a reference of each of the shapes for sanity check purposes
    # we'll also save it out as a 'shapes.png'
    shapes_renderer = Renderer(1600,1024)
    shapes_renderer.draw_shapes(shapes)
    shapes_renderer.display()
    shapes_renderer.save("shapes")
    del shapes_renderer

    # Now, similarly, lets, for each shape, render out each of the
    # 24 rotations into another canvas each and save it out as a
    # PNG
    for index, shape in enumerate(shapes):
        rot_renderer = Renderer(1600, 2048)
        rot_renderer.render_rotations(shape)
        rot_renderer.display()
        rot_renderer.save("shape%s_rotations"%index)

    del rot_renderer



def main(argv):

    C_SOLVER = "c-solver"
    config_filename="bedlam.json"
    do_sanity = False
    num_solutions = 1
    solver = "c"

    usage = """solve.py -i <input> [-o] [-n <num solutions>] [-s <c|python>] \n
               -i <input json file> : input config, shapes and container dimensions
               -o : print shapes and rotations on screen and save to PNG
               -n <num> : set the max number of solutions, default is all
               -s <c|python> : set solver, c-solver used by default"""
    try:
      opts, args = getopt.getopt(argv,"hi:on:s:",["input=","out","num="])
    except getopt.GetoptError as e:
      print("Error: ",e)
      print(usage)
      sys.exit(2)

    for opt, arg in opts:
      if opt == '-h':
        print(usage)
        sys.exit()
      elif opt in ("-i", "--input"):
        config_filename = arg
      elif opt in ("-o", "--out"):
        do_sanity = True
      elif opt in ("-n", "--num"):
        num_solutions = int(arg)
      elif opt in ("-s", "--solver"):
        solver = arg

    if solver not in (["c","python"]):
        print(usage)
        sys.exit()
    
    if solver == "c" and not os.access("c-solver",os.X_OK):
        print("Cannot use 'c' solver, '%s' does not exist or is not executable"%C_SOLVER)
        sys.exit()

    print("Loading %s"%config_filename)
    shapes, x, y, z = load_config(config_filename)
    print(shapes)
    print("Loaded")
    if do_sanity:
        render_shapes_and_rotations(shapes)
    # now onto the meat and bones. We'll create our 'Cube' which will
    # store the ongoing state of the iterative solution, and then
    # kick off the solver to start the laborious process of iterating
    # through the quadrillions of possible permutations
    cube = Cube(x,y,z)
    solver_iterations = 0
    solver_sanity_check = 0
    solved_shapes = []


    shapes_config = {
        "width":x,
        "depth":y,
        "height":z,
        "shapes":shapes
    }

    solutions = []
    if solver == "c":
        print("Using C++ solver")
        solver = subprocess.run(["./%s"%C_SOLVER], 
                        universal_newlines=True, 
                        input=jsons.dumps(shapes_config), 
                        stdout=subprocess.PIPE)
        solutions.append(json.loads(solver.stdout))
    else:
        print("Using Python solver")
        solver = Solver(cube, shapes)
        solver.solve(num_solutions)
        solutions = solver.solutions
    
    if len(solutions) == 0:
        print("No Solution Found.")
        exit()
    
    print("Solutions found: %i"%len(solutions))

    """ get the list of solved shapes from the solver, and sort them
        by z, x, y to give us _some_ kind of sensible order that we
        can put the shapes into the box in. This isn't perfect, sometimes
        you still have to take a shape out to put the next one in, needs
        a litte more thought """

    for index, solved_shapes in enumerate(solutions):
        solved_shapes.reverse() #because we initally get them from last->first
        solved_shapes.sort(key=itemgetter("z","x","y"))
        #lets print the solution to the console
        print(solved_shapes)

        solution_renderer = Renderer( 1280, len(solved_shapes) * 420)
        solution_renderer.draw_solution(shapes, solved_shapes)
        solution_renderer.display()
        solution_renderer.save("solution%i"%index)

if __name__ == "__main__":
    main(sys.argv[1:])

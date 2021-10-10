The Bedlam Solver

Years of frustration and annoyance finally persuaded me to sit down and write a solver for it ... in Python. Probably not the first choice for a brute force iterative solver for a puzzle with several quadrillion possible combinations.

Uses a fairly straightforward recursive backtracking search to try and brute force it, and currently will just return the first solution it finds given the intitial shape ordering. There are a total of 19,186 possible solutions out of a rather large search space, and no quarantee of a solution for a specific ordering so the solver will try and enumerate all possible permutations of the piece ordering as well. 

Aside from the solver, there is a Renderer which can toss together an isometric view of the shapes, rotations, and solutions from a couple of simple primitives and some magic number based drawing code.

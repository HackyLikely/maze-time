#!/usr/bin/python3

import mazelib as ml

height  = 4
width   = 4
maze    = ml.init_maze(height,width)
# ml.print_maze(maze)
maze    = ml.gen_binary_tree_se(height,width)
ml.print_maze(maze)
ml.print_maze_as_ascii(maze)


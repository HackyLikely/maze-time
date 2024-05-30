#!/usr/bin/python3


# Maze Implemetation
# ----------------------------------------------------------------
#   The implementation of a maze in this library,
#   is a 2D matrix (list of lists) of integers.
#   Each element of the matrix is a row.
#   Each element of a row is a cell.

# Example
#   maze = [[1, 2, 3],          
#           [4, 5, 6],
#           [7, 8, 9]]             

# Coordinates (x,y)
#   (0,0)
#   ----------> x
#   |
#   |
#   V y
#   
#   A cell is indexed as maze[y][x]
#   The top-left cell is maze[0][0]

# Directions (dx, dy)
#   North   Top     ( 0, -1) 
#   West    Left    (-1,  0) 
#   South   Bottom  ( 0,  1) 
#   East    Right   ( 1,  0) 
directions  = [( 0, -1), (-1,  0), ( 0,  1), ( 1,  0)]

# Directions indexes
iN, iW, iS, iE  = 0, 1, 2, 3

# Each bit of a cell has its own meaning.
# 
# Walls bit codes
#   b0  : N wall
#   b1  : W wall
#   b2  : S wall
#   b3  : E wall


# Maze Functions
# ----------------------------------------------------------------

def init_maze(height, width):
    """
    Initialize the maze grid with all walls.

    Parameters:
    height (int): The number of rows in the maze.
    width (int): The number of columns in the maze.

    Returns:
    list: A 2D list representing the maze, where each cell has all walls.
    """

    # Define a variable representing all walls using bitwise OR to combine wall values
    all_walls = (1 << iN) | (1 << iW) | (1 << iS) | (1 << iE)

    # Create the maze grid as a 2D list with all cells initialized to have all walls
    maze = [[all_walls] * width for _ in range(height)]

    # Return the initialized maze grid
    return maze


def print_maze(maze, space=4):
    """
    Prints a 2D list (maze) in a formatted manner.

    Parameters:
    maze (list of list): A 2D list where each sublist represents a row in the maze.
                         Each element in the sublist represents a cell in that row.
    space (int, optional): The number of characters used for spacing between cells. 
                           Default is 4.
    """

    for row in maze:
        formatted_row = ''.join(f"{cell:{space}}" for cell in row)
        print(formatted_row)

        
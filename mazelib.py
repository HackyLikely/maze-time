#!/usr/bin/python3

import random

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




def print_maze_as_ascii(maze):

    # Maze params
    height  = len(maze)
    width   = len(maze[0]) 

    # init mazeascii
    wchar       = '#'
    mazeascii   = [[wchar]*(2*width+1) for _ in range(2*height+1)]

    # init holes
    for y in range(height):
        for x in range(width):
            mazeascii[2*y  ][2*x+1] = ' '
            mazeascii[2*y+1][2*x]   = ' '
            mazeascii[2*y+1][2*x+1] = ' '
            mazeascii[2*y+1][2*x+2] = ' '
            mazeascii[2*y+2][2*x+1] = ' '

    # set walls
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if has_wall(cell, iN):
                mazeascii[2*y  ][2*x+1] = wchar
            if has_wall(cell, iW):
                mazeascii[2*y+1][2*x]   = wchar
            if has_wall(cell, iS):
                mazeascii[2*y+2][2*x+1] = wchar
            if has_wall(cell, iE):
                mazeascii[2*y+1][2*x+2] = wchar
    
    for row in mazeascii:
        formatted_row = ''.join([cell for cell in row])
        print(formatted_row)





                            








def is_valid(maze, x, y):
    """
    Checks if a given position (x, y) is valid within the bounds of the maze.

    Parameters:
    maze (list of list): A 2D list representing the maze.
    x (int): The x-coordinate of the position to check.
    y (int): The y-coordinate of the position to check.

    Returns:
    bool: True if the position is within the maze bounds, False otherwise.
    """
    # Extrapolating width and height
    height = len(maze)     # Length of the outer list gives the height
    width = len(maze[0])   # Length of any inner list would give the width

    return (0 <= x < width) and (0 <= y < height)



def has_wall(cell, iDIR):
    """
    Checks if a given cell has a wall in the specified direction.

    Parameters:
    cell (int): An integer representing the cell's configuration with wall information encoded.
    iDIR (int): An integer representing the direction to check for the wall.

    Returns:
    bool: True if the cell has a wall in the specified direction, False otherwise.
    """
    # Create a bitmask by shifting 1 to the left by iDIR positions
    bitmask = 1 << iDIR
    # Check if the bit representing the wall is set in the cell
    # If the bitwise AND operation is non-zero, the wall exists
    return (cell & bitmask) != 0



def set_wall(cell, iDIR):
    """
    Sets a wall in the specified direction of a given cell, if the wall doesn't already exist.

    Parameters:
    cell (int): An integer representing the cell's configuration with wall information encoded.
    iDIR (int): An integer representing the direction to set the wall.

    Returns:
    int: The updated cell configuration with the wall set in the specified direction.
    """
    # Set the wall in the specified direction using bitwise OR operation
    cell |= (1 << iDIR)
    # Return the updated cell
    return cell


def remove_wall(cell, iDIR):
    """
    Removes a wall in the specified direction of a given cell, if the wall exists.

    Parameters:
    cell (int): An integer representing the cell's configuration with wall information encoded.
    iDIR (int): An integer representing the direction to remove the wall.

    Returns:
    int: The updated cell configuration with the wall removed in the specified direction.
    """
    # Remove the wall in the specified direction using bitwise AND operation
    cell &= ~(1 << iDIR)
    # Return the updated cell
    return cell




def random_idir():
    """
    Returns a random index representing a direction from the given list of directions.

    Returns:
    int: A random index representing a direction from the given list.
    """
    return random.randint(0, len(directions) - 1)


def move_from(x, y, iDIR, steps):
    """
    Moves from a given position (x, y) in the specified direction for the given number of steps.

    Parameters:
    x (int): The current x-coordinate.
    y (int): The current y-coordinate.
    iDIR (int): An integer representing the direction to move.
    steps (int): The number of steps to move in the specified direction.
  
    Returns:
    tuple: A tuple containing the coordinates of the next cell after moving.
           The first element is the next x-coordinate, and the second element is the next y-coordinate.
    """
    # Calculate the change in x and y coordinates based on the specified direction and steps
    dx, dy = (steps * d for d in directions[iDIR])
    # Calculate the coordinates of the next cell by adding the change in coordinates to the current coordinates
    next_x = x + dx
    next_y = y + dy
    # Return the coordinates of the next cell
    return next_x, next_y





def gen_binary_tree_se(height, width):

    maze    = init_maze(height, width)
   
    for y in range(height):
        for x in range(width):
            # Select the wall to remove
            # if not the last column or row
            if (x < (width-1)) and (y < (height-1)):
                # flip a coin
                iDIR = iS if random.random() < 0.5 else iE            
            else:
                # if last column
                if y < (height-1):
                    iDIR = iS
                # if last row
                elif x < (width-1):
                    iDIR = iE
                # if last cell
                else:
                    # Dummy removal of iN wall
                    iDIR = iN

            # Consider the Direction chosen
            nx, ny = move_from(x, y, iDIR, 1)

            # Remove the wall between the current cell and the chosen cell
            maze[y][x]   = remove_wall(maze[y][x], iDIR)
            maze[ny][nx] = remove_wall(maze[ny][nx], ((iDIR+2)%len(directions)))

    # Return
    return maze


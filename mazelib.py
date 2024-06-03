#!/usr/bin/python3



import os
import random
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as patches



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


# Current cell on generation algorithms
iCURR   = 4

# Dark cell until generation algorithms
iDARK   = 5






# Maze Functions
# ----------------------------------------------------------------

def init_maze(height, width):
    """
    Initialize the maze grid with all walls and dark cells.

    Parameters:
    height (int): The number of rows in the maze.
    width (int): The number of columns in the maze.

    Returns:
    list: A 2D list representing the maze, where each cell has all walls.
    """

    # Define a variable representing all walls using bitwise OR to combine wall values
    all_walls   = (1 << iN) | (1 << iW) | (1 << iS) | (1 << iE)
    all_walls  |= (1 << iDARK)

    # Create the maze grid as a 2D list with all cells initialized to have all walls
    maze = [[all_walls] * width for _ in range(height)]

    # Return the initialized maze grid
    return maze



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





def is_current(cell):
    bitmask = 1 << iCURR
    return (cell & bitmask) != 0

def set_current(cell):
    bitmask = 1 << iCURR
    cell |= bitmask
    return cell

def remove_current(cell):
    bitmask = ~(1 << iCURR)
    cell &= bitmask
    return cell



def is_dark(cell):
    bitmask = 1 << iDARK  
    return (cell & bitmask) != 0

def set_dark(cell):
    bitmask = 1 << iDARK  
    cell |= bitmask
    return cell

def remove_dark(cell):
    bitmask = ~(1 << iDARK)
    cell &= bitmask
    return cell







# Maze Display
# ----------------------------------------------------------------

def print_maze(maze, space=4):
    """
    Prints a 2D list (maze) in a formatted manner.
    Prints the integer values reppresenting the maze.

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
    """
    Prints a 2D list (maze) in a ASCII manner.
    Prints only walls.

    Parameters:
    maze (list of list): A 2D list where each sublist represents a row in the maze.
                         Each element in the sublist represents a cell in that row.
    """

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



def draw_maze(maze):
    """
    Draw into a matplotlib new figure the maze. 
    Draw into ax.
    Do not show the plot.

    Parameters:
    maze (list of list): A 2D list where each sublist represents a row in the maze.
                         Each element in the sublist represents a cell in that row.
    """

    # Maze params
    height  = len(maze)
    width   = len(maze[0]) 
                        
    # Create a blank figure and axis
    fig, ax = plt.subplots(figsize=(5, 5))

    # Cell parameters
    cell_height = 10
    cell_width  = 10

    # Maze display parameters
    bg_col      = '#f7f7f7'     # Color for background
    curr_col    = '#ff2d38'     # Color for current cell
    dark_col    = '#ababab'     # Color for dark cell
    wall_thick  = 2             # wall thickness  
    wall_col    = '#000000'     # Color for walls

    # Iterate over the maze cells
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            
            # Draw the Cell init
            x1 = (x+1)*cell_width   # top left
            y1 = (y+1)*cell_height  # 
            rect = patches.Rectangle((x1, y1), cell_width, cell_height, linewidth=0, edgecolor=None, facecolor=bg_col)
            ax.add_patch(rect)

            # Overlay special cells
            if is_dark(cell):
                x1 = (x+1)*cell_width   # top left
                y1 = (y+1)*cell_height  # 
                rect = patches.Rectangle((x1, y1), cell_width, cell_height, linewidth=0, edgecolor=None, facecolor=dark_col)
                ax.add_patch(rect)
            if is_current(cell):
                margin_w    = 0.1*cell_width
                margin_h    = 0.1*cell_height
                x1 = (x+1)*cell_width   + margin_w  # top left
                y1 = (y+1)*cell_height  + margin_h  # 
                rect = patches.Rectangle((x1, y1), cell_width-2*margin_w, cell_height-2*margin_h, linewidth=0, edgecolor=None, facecolor=curr_col)
                ax.add_patch(rect)
            

            # Draw the Cell Walls
            if has_wall(cell, iN):
                x1  = (x+1)*cell_width  # top left
                y1  = (y+1)*cell_height # 
                x2  = (x+2)*cell_width  # bottom right
                y2  = (y+1)*cell_height # 
                ax.plot([x1,x2], [y1,y2], color=wall_col, linewidth=wall_thick, marker=None)
            if has_wall(cell, iW):
                x1  = (x+1)*cell_width  # top left
                y1  = (y+1)*cell_height # 
                x2  = (x+1)*cell_width  # bottom right
                y2  = (y+2)*cell_height # 
                ax.plot([x1,x2], [y1,y2], color=wall_col, linewidth=wall_thick, marker=None)
            if has_wall(cell, iS):
                x1  = (x+1)*cell_width  # top left
                y1  = (y+2)*cell_height # 
                x2  = (x+2)*cell_width  # bottom right
                y2  = (y+2)*cell_height # 
                ax.plot([x1,x2], [y1,y2], color=wall_col, linewidth=wall_thick, marker=None)
            if has_wall(cell, iE):
                x1  = (x+2)*cell_width  # top left
                y1  = (y+1)*cell_height # 
                x2  = (x+2)*cell_width  # bottom right
                y2  = (y+2)*cell_height # 
                ax.plot([x1,x2], [y1,y2], color=wall_col, linewidth=wall_thick, marker=None)

    # Set the aspect ratio
    ax.set_aspect('equal')

    # Invert the y-axis
    ax.invert_yaxis()

    # Remove the axes
    ax.axis('off')





def show_plt():
    """
    Show the current plot.
    """

    # Show
    plt.show()




def save_plt(outdir, fname):
    """
    Save the current figure of the maze into a png file. 
    Try to save a 512x512 pixel image.

    Parameters:
    outdir (string): The path of the output directory where to save the figure.
    fname (string): The name of the file.
    """
    # DPI = pixels/inches

    # Get the size of the figure in inches
    fig = plt.gcf()
    fig_width, fig_height = fig.get_size_inches()
    dpi = 665/fig_width # tricky, empirical number to get 512 pixels

    # Save the figure as a PNG file with 512x512 pixels
    plt.savefig(outdir + '/' + fname,  dpi=dpi, bbox_inches='tight', pad_inches=0)

    # Close the figure
    plt.close()





def create_output_dir(prefix=""):
    """
    Creates a directory with a timestamp as the name for output files.

    Args:
    prefix (str): Prefix for the directory name.

    Returns:
    str: Path of the created directory.
    """
    # Get the current time as a formatted string
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    
    # Construct the directory name using the prefix and current time
    plot_dir = f"{prefix}{current_time}"
    
    # Check if the directory already exists, if not, create it
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    
    # Return the path of the created directory
    return plot_dir












# Maze Generation
# ----------------------------------------------------------------
# Binary-Tree (South-East)
# Aldous-Broder
# ----------------------------------------------------------------

def gen_binary_tree_se(height, width, save_gen=False):
    """
    Generates a maze using Binary-Tree algorithm.
    For every cell flip a coin for South-East.
    Eliminate that wall.
    Take care of external cells.

    Args:
    height (int): Height of the maze grid.
    width (int): Width of the maze grid.
    save_gen (bool): Save images of the generation

    Returns:
    list: 2D list representing the generated maze.
    """
    # Create the output_dir if save_gen
    if save_gen:
        output_dir = create_output_dir("gen_maze_")
    
    # Init maze with all walls and dark cells
    maze    = init_maze(height, width)
   
    # Main gen loop
    for y in range(height):
        for x in range(width):

            # Mark the cell as current
            maze[y][x] = set_current(maze[y][x])

            # Save before wall removal
            # ----------------
            if save_gen:
                draw_maze(maze)
                # Get current time with milliseconds
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
                # Construct filename with current time
                filename = f"{current_time}.png"
                save_plt(output_dir, filename)

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


            # Save after wall removal
            # ----------------
            if save_gen:
                draw_maze(maze)
                # Get current time with milliseconds
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
                # Construct filename with current time
                filename = f"{current_time}.png"
                save_plt(output_dir, filename)


            # Remove the current flag
            maze[y][x] = remove_current(maze[y][x])
            # Remove the dark flag
            maze[y][x] = remove_dark(maze[y][x])



    # Save last img: clean maze
    # ----------------
    if save_gen:
        draw_maze(maze)
        # Get current time with milliseconds
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        # Construct filename with current time
        filename = f"{current_time}.png"
        save_plt(output_dir, filename)

    # Return
    return maze



def gen_aldous_broder(height, width, save_gen=False):
    """
    Generates a maze using Aldous-Broder algorithm.
    Pick a random cell as the current cell and mark it as visited.
    While there are unvisited cells:
        Pick a random neighbour.
        If the chosen neighbour has not been visited:
            Remove the wall between the current cell and the chosen neighbour.
            Mark the chosen neighbour as visited.
        Make the chosen neighbour the current cell.

    Un-visited cells are DARK.
    Visited cells are DARK removed.

    Args:
    height (int): Height of the maze grid.
    width (int): Width of the maze grid.
    save_gen (bool): Save images of the generation

    Returns:
    list: 2D list representing the generated maze.
    """

    # Create the output_dir if save_gen
    if save_gen:
        output_dir = create_output_dir("gen_maze_")
    
    # Init maze with all walls and dark cells
    maze    = init_maze(height, width)


    # Start from a random cell
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)

    # Mark the cell as current
    maze[y][x] = set_current(maze[y][x])
    # Remove the dark flag
    maze[y][x] = remove_dark(maze[y][x])

    # Counter of remaining (not visited) cells
    remaining = width * height - 1

    # Save before wall removal
    # ----------------
    if save_gen:
        draw_maze(maze)
        # Get current time with milliseconds
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        # Construct filename with current time
        filename = f"{current_time}.png"
        save_plt(output_dir, filename)


    # Main loop
    while remaining:

        # Chose a random direction
        iDIR = random_idir()

        # Get coordinates of a neighbor
        nx, ny = move_from(x, y, iDIR, 1) 

        # Check if it is a valid cell 
        if is_valid(maze, nx, ny):

            # Remove the current flag
            maze[y][x] = remove_current(maze[y][x])

            # Check if the neighbor is not visited
            if is_dark(maze[ny][nx]):

                # Remove the wall between the current cell and the chosen cell
                maze[y][x]   = remove_wall(maze[y][x], iDIR)
                maze[ny][nx] = remove_wall(maze[ny][nx], ((iDIR+2)%len(directions)))

                # Remove the dark flag
                maze[ny][nx] = remove_dark(maze[ny][nx])

                # Update the remaining cells
                remaining -= 1

            # Update coord with valid cell anyway
            x, y = nx, ny

            # Mark the cell as current
            maze[y][x] = set_current(maze[y][x])

            # Save after step move
            # ----------------
            if save_gen:
                draw_maze(maze)
                # Get current time with milliseconds
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
                # Construct filename with current time
                filename = f"{current_time}.png"
                save_plt(output_dir, filename)


    # Remove the last current flag
    maze[y][x] = remove_current(maze[y][x])

    # Save last img: clean maze
    # ----------------
    if save_gen:
        draw_maze(maze)
        # Get current time with milliseconds
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        # Construct filename with current time
        filename = f"{current_time}.png"
        save_plt(output_dir, filename)

    # Return
    return maze
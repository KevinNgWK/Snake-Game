"""
Snake Game
Size of each square is 15x15
Keep array representation of snake
"""

#Import necessary packages
import pygame
import random

def draw_square(win, sq_size, coord, color="black"):
    """
    Function to draw squares
    parameters:
        win: display window
        sq_size: size of square to be drawn (int)
        coord: coordinates of square to be drawn (x, y)
        color: color to fill the square
    """
    color_dict = {"black": (0,0,0), "white": (255,255,255), "light blue": (0,51,102), "dark blue":(0,25,52), "green":(0,153,0)}
    pygame.draw.rect(win, color_dict[color], (coord[0], coord[1], sq_size, sq_size))


def build_grid(win, win_size, arr_size, sq_size):
    """
    Function that builds the basic grid and assigns each grid into an array.
    Parameters:
        win: display window
        win_size: size of window. (win_x, win_y)
        arr_size: size of 2D array. (size_x, size_y)
        sq_size: size of one square (int)
    Output:
        coord_dict: Python Dictionary mapping array coordinates to grid coordinates
    """
    win_x, win_y = win_size
    arr_size_x, arr_size_y = arr_size

    #Total height and width of grid
    total_x, total_y = sq_size * arr_size_x, sq_size * arr_size_y
    #Coordinates of the top left corner of grid
    start_x, start_y = (win_x - total_x) / 2, (win_y - total_y) / 2

    #Initialise background with color
    win.fill((50,50,50))
    #Initialise white border around grid
    pygame.draw.rect(win, (255,255,255), (start_x - 1, start_y - 1, total_x + 2, total_y + 2), 1)
    #Initialise python dictionary to map array coordinates to grid coordinates
    coord_dict = {}

    x, y = start_x, start_y
    for i in range(arr_size_x):
        for j in range(arr_size_y):
            if (i+j)%2 == 0:
                draw_square(win, sq_size, (x, y), "dark blue")
            else:
                draw_square(win, sq_size, (x, y), "light blue")
            coord_dict[str((i,j))] = (x,y)
            y += sq_size
        x += sq_size
        y = start_y

    return coord_dict


def update_arr(arr, coord, value):
    """
    Function to update value in array to approporiate value. Function tailored to account for grid
    Parameters:
        arr: array
        coord: the coordinates that need to be updated. (x, y)
        value: The value to update it with
    """
    x, y = coord
    arr[y][x] = value


def get_arr_value(arr, coord):
    """
    Function that gives the current value of a coordinate in array
    Parameters:
        arr: array
        coord: coordinates of concern
    Returns:
        value: Value of coordinate
    """
    x, y = coord
    return arr[y][x]


def get_next_pos(face, current_head):
    """
    Function that determines the next position of snake
    Parameters:
        face: direction that snake is facing
        current_head: The coordinates of the current head of snake (x, y)
    Returns:
        The next position that the snake will go to
    """
    current_head_x, current_head_y = current_head
    if face == 0:
        return (current_head_x, current_head_y - 1)
    elif face == 1:
        return (current_head_x + 1, current_head_y)
    elif face == 2:
        return (current_head_x, current_head_y + 1)
    elif face == 3:
        return (current_head_x - 1, current_head_y)


def update_params(body_q, arr, next_pos, arr_size, win, sq_size, coord_dict):
    """
    Function that determines what to do, given an input
    Parameters:
        body_q: a queue struct for the body so we can keep track of head and tail. last index is head
        arr: 2D array to encapsulate entire grid. 1 -> body is there, 2 -> food, 0 -> nothing
        next_pos: The next position that the snake should move to
        current_head: Current position of the head
        arr_size: size of array
        win: display window
        sq_size: size of a square in the display grid
    Output:
        True or False, depending on whether parameters can be updated. If false, means the snake died
    """
    #Check if the next position is a valid one.
    if not 0 <= next_pos[0] < arr_size[0]:      #x-direction within grid
        return False
    if not 0 <= next_pos[1] < arr_size[1]:      #y-direction within grid
        return False
    if get_arr_value(arr, next_pos) == 1:       #If next position is a body of snake
        return False
    
    #If none of above is true, then the next position is a valid one
    #So now, check if it is food, otherwise, just move snake
    if get_arr_value(arr, next_pos) == 2:
        body_q.append(next_pos)
        update_arr(arr, next_pos, 1)
        draw_square(win, sq_size, coord_dict[str(next_pos)], color="green")
        generate_food(arr, win, sq_size, coord_dict, arr_size)
    
    else:
        body_q.append(next_pos)
        tail = body_q.pop(0)
        update_arr(arr, next_pos, 1)
        update_arr(arr, tail, 0)
        draw_square(win, sq_size, coord_dict[str(next_pos)], color="green")
        if (tail[0] + tail[1])%2 == 0:
            draw_square(win, sq_size, coord_dict[str(tail)], "dark blue")
        else:
            draw_square(win, sq_size, coord_dict[str(tail)], "light blue")
    return True


def generate_food(arr, win, sq_size, coord_dict, arr_size):
    """
    Function that generates food randomly
    Parameters:
        arr: Array that represents 2D grid
        win: display window
        sq_size: size of a square in grid
        coord_dict: Python dictionary mapping arr coordinates to grid coordinates
        arr_size: size of array 
    Returns:
        Nothing
    """
    avail_slots = []
    #Generate a list of available slots.
    for i in range(arr_size[0]):
        for j in range(arr_size[1]):
            if get_arr_value(arr, (i,j)) == 0:
                avail_slots.append((i,j))
    choice = random.choice(avail_slots)

    update_arr(arr, choice, 2)
    draw_square(win, sq_size, coord_dict[str(choice)], color="white")


#Global Settings
win_size = (1200,600)       #Setting window Size
arr_size = (70,35)          #Dimensions of array
sq_size = 15                #Length/Width of a small square for grid
starting_head = (35,17)
first_food = (50,20)

#Initialise Pygame, and the window
pygame.init()
win = pygame.display.set_mode(win_size)
pygame.display.set_caption("Game of Snakes")

#Initialise Grid
coord_dict = build_grid(win, win_size, arr_size, sq_size)
pygame.display.update()

#Initialise variables
arr = [[0 for i in range(arr_size[0])] for j in range(arr_size[1])]
body_q = []
current_head = starting_head
face = 0
temp_body = (starting_head[0], starting_head[1] + 1)

#Initialise snake
body_q.append(temp_body)
body_q.append(current_head)

update_arr(arr, current_head, 1)
update_arr(arr, temp_body, 1)

draw_square(win, sq_size, coord_dict[str(current_head)], "green")
draw_square(win, sq_size, coord_dict[str(temp_body)], "green")
pygame.display.update()

#First Run. Gives player time to relax before starting
run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        face = 3
        run = False
    elif keys[pygame.K_RIGHT]:
        face = 1
        run = False

#Initialise food
draw_square(win, sq_size, coord_dict[str(first_food)], "white")
update_arr(arr, first_food, 2)

#Second run. This is the main game
second_run = True
while second_run:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            second_run = False
            pygame.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if(face != 1 and not ((face==0 or face==2) and current_head[0] == 0)):
            face = 3

    elif keys[pygame.K_UP]:
        if(face != 2 and not ((face==1 or face==3) and current_head[1] == 0)):
            face = 0

    elif keys[pygame.K_RIGHT]:
        if(face != 3 and not ((face==0 or face==2) and current_head[0] == arr_size[0] - 1)):
            face = 1

    elif keys[pygame.K_DOWN]:
        if(face!=0 and not ((face==1 or face==3) and current_head[1] == arr_size[1] - 1)):
            face = 2

    next_pos = get_next_pos(face, current_head)
    success = update_params(body_q, arr, next_pos, arr_size, win, sq_size, coord_dict)
    if success == False:
        second_run = False
    else:
        current_head = next_pos
    pygame.time.delay(100)
    pygame.display.update()

#Third run. This is to allow the player to see his dead snake hahaha
third_run = True
while third_run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            second_run = False
            pygame.quit()
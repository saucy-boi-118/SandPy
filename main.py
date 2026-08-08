import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import numpy as np

# Constants
WINW:int = 500
WINH:int = 500
CELLSIZE:int = 20
CELLW:int = WINW // CELLSIZE
CELLH:int = WINH // CELLSIZE
WHITE:pygame.Color = pygame.Color(255,255,255)
YELLOW:pygame.Color = pygame.Color(251, 243, 138)
BLUE:pygame.Color = pygame.Color(155, 190, 237)
RED:pygame.Color = pygame.Color(255,155,155)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WINW,WINH), pygame.NOFRAME)
Clock = pygame.time.Clock()
running:bool = True

# Escaping
escape:pygame.Rect = pygame.Rect(WINW-CELLSIZE, 0, CELLSIZE, CELLSIZE)

# Grid Setup

# Grid for the sands
grid = np.zeros(CELLW*CELLH, dtype=int).reshape(CELLH, CELLW) # 1 is sand, 0 is empty, 2 is border
grid[:CELLH, ::CELLW-1] = 2
grid[::CELLH-1, :CELLW] = 2

# Read from grid and write to next
next = np.zeros(CELLW*CELLH, dtype=int).reshape(CELLH, CELLW) 

# Mouse setup
holding:bool = False

# Game loop
while running:

    # Loop through events for input
    for event in pygame.event.get():

        # X button on the screen
        if event.type == pygame.QUIT: 
            running = False

        # Clicking for spawning sand, mouse hold
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Extra escape button
            if escape.collidepoint(pygame.mouse.get_pos()):
                running = False

            holding = True
        elif event.type == pygame.MOUSEBUTTONUP:
            holding = False

        # Variables for mouse
        mouse = pygame.mouse.get_pos()
        posX = mouse[0] // CELLSIZE
        posY = mouse[1] // CELLSIZE

        # Keeping the sand in bounds 
        if holding == True and 0 < posY < CELLH-1 and 0 < posX < CELLW-1:
            grid[posY, posX] = 1

    # Loop through keys for escaping and clearing
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        # clear the current grid
        grid *= 0
                        
        # redefine the boundaries
        grid[:CELLH, ::CELLW-1] = 2
        grid[::CELLH-1, :CELLW] = 2

    elif keys[pygame.K_ESCAPE]:
        running = False


    # Clear the screen every frame
    screen.fill(WHITE)

    # Drawing the grid and updating the sand
    for y in range(CELLH):
        for x in range(CELLW):

            # Checking the value of the each cell
            value = grid[y,x]
            
            if value == 2: # defined as the border
                pygame.draw.rect(screen, WHITE, (x*CELLSIZE,y*CELLSIZE,CELLSIZE,CELLSIZE)) # Border

            elif value == 1: # Defined as a sand
                try:
                    if grid[y+1,x] == 0: # Check if bottom is empty for moving down
                        next[y+1,x] = 1 
                        next[y,x] = 0
                    else:
                        # Check if the bottom left and right cells are empty and move to them is they are

                        # Bottom right
                        if grid[y+1, x+1] == 0:
                            next[y+1,x+1] = 1
                            next[y,x] = 0

                        # Bottom Left
                        elif grid[y+1,x-1] == 0:
                            next[y+1,x-1] = 1
                            next[y,x] = 0
                        
                        else:
                            next[y,x] = 1 # Stay in place

                except IndexError: # Catch the error so sand isn't out of bounds
                    next[y,x] = 1 # Stay in place
                
                pygame.draw.rect(screen, YELLOW,(x*CELLSIZE,y*CELLSIZE,CELLSIZE,CELLSIZE)) # Draw Sand

            else: # Empty
                pygame.draw.rect(screen, BLUE,  (x*CELLSIZE,y*CELLSIZE,CELLSIZE,CELLSIZE)) 

    # swap the grids
    grid, next = next, grid

    # clear the next grid
    next *= 0 

    # redefine boundaries
    next[:CELLH, ::CELLW-1] = 2
    next[::CELLH-1, :CELLW] = 2

    # draw the extra escape button
    pygame.draw.rect(screen, RED, escape)

    # Updating the screen
    pygame.display.flip()

    # limit the FPS
    Clock.tick(120)

pygame.quit()
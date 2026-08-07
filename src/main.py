import pygame
import numpy as np
from settings import *

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((WINW,WINH))
Clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)
running = True

# Grid for the sands
grid = np.zeros(CELLW*CELLH, dtype=int).reshape(CELLH, CELLW) # 1 is sand, 0 is empty, 2 is border
grid[:CELLH, ::CELLW-1] = 2
grid[::CELLH-1, :CELLW] = 2

# read from grid write to next
next = np.zeros(CELLW*CELLH, dtype=int).reshape(CELLH, CELLW) 
next[:CELLH, ::CELLW-1] = 2
next[::CELLH-1, :CELLW] = 2


while running:
    # Loop through events for input
    for event in pygame.event.get():
        # X button on the screen
        if event.type == pygame.QUIT: 
            running = False
        # Escape button
        elif event.type == pygame.K_ESCAPE:
            running = False
        # Clicking for spawning sand
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            posX = mouse[0] // CELLSIZE
            posY = mouse[1] // CELLSIZE

            if grid[posX, posY] == 0:
                grid[posY, posX] = 1

    # Clear the screen every frame
    screen.fill(WHITE)

    # Drawing the grid
    for y in range(CELLH):
        for x in range(CELLW):

            # Checking the value of the each cell
            value = grid[y,x]
            
            if value == 2:
                pygame.draw.rect(screen, WHITE, (x*CELLSIZE,y*CELLSIZE,CELLSIZE,CELLSIZE)) # Border
            elif value == 1:
                # Check if bottom is empty for moving down
                try:
                    if grid[y+1,x] == 0:

                        next[y+1,x] = 1
                        next[y,x] = 0
                    else:
                        # Check if the bottom left and right cells are empty and move to them is they are
                        if grid[y+1, x+1] == 0:

                            next[y+1,x+1] = 1
                            next[y,x] = 0
                        elif grid[y+1,x-1] == 0:

                            next[y+1,x-1] = 1
                            next[y,x] = 0
                        else:
                            next[y,x] = 1
                except IndexError:
                    next[y,x] = 1
                pygame.draw.rect(screen, YELLOW,(x*CELLSIZE,y*CELLSIZE,CELLSIZE,CELLSIZE))
            else:
                pygame.draw.rect(screen, BLUE,  (x*CELLSIZE,y*CELLSIZE,CELLSIZE,CELLSIZE)) # Empty

    # swap the grids
    grid, next = next, grid
    next *= 0 # clear the next grid

    # redefine boundaries
    next[:CELLH, ::CELLW-1] = 2
    next[::CELLH-1, :CELLW] = 2

    # Updating the screen
    pygame.display.flip()

    # limit the FPS
    Clock.tick(60)

    
pygame.quit()
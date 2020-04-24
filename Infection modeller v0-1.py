# TO DO's
# 1. Create a Technique for adding a border DONE 14/4/20
# 2. Create a psuedoname function. DONE 14/4/20
# 3. Implement a population class and the current version is elegant DONE 17/4/2020.
# 4. Implement a world class to create multiple sims world class not required DONE 17/4/2020
# 5. Speed Up, Multi-threading, implement through an image and numpy arrage?

import pygame
from math import sqrt
import time
from random import random
from virusmodel import *

#*****GLOBALS****

#Set up screensize.
X_RESOLUTION, Y_RESOLUTION = (600, 600)

#World aspects
WORLDCLOCK = 0              # The worlds universal clock (ticks in __main__)
     
if __name__ == "__main__":
    #Enter the main loop.
    #initialise the world
    screen = pygame.display.set_mode([X_RESOLUTION, Y_RESOLUTION])
    pygame.display.set_caption("Virus World")

    grid = []
    boxes  = 0
    s = 100
    for i in range(50,500, s):
        row = 0
        for j in range(50,500, s):
            grid.append([i, X_RESOLUTION - (i+s), j, Y_RESOLUTION - (j+s)])
            row += 1
            boxes += 1

    models = []
    p =10
    for x in range(boxes):
        v = virus(infection_radius=2, recovery_time = 100)
        models.append(population(ID = psuedoName(), bound_box=grid[x]))
        models[x].generate_population(popsize = p, max_speed = 1, virus = virus(recovery_time=50), decision_range = 2, HP_max = 5)
        p += 50
        models[x].group[0].health = 'I'

    #Initialise the running variables
    record = [] 
    running = True 
    while  running != False:
        #repeated itterate through the populations
        pops = []

        for m in range(len(models)):
            models[m].itterate(screen, [models[m]])
        print (models[0].wrldclk)
        # Once the world has been updated update the screen.
        pygame.display.flip()
        screen.fill([0, 0, 0])

        #Exit Points
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
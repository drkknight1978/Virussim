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

    v = virus(infection_radius=2, recovery_time=150)
    worldwide = population('world', X_RESOLUTION, Y_RESOLUTION,[10, 10, 10, 10])
    worldwide.generate_population(popsize = 60, virus = v, max_speed=4)
    worldwide.group[0].health = 'I'

    a1 = population('UK', X_RESOLUTION, Y_RESOLUTION,[20, 400, 400, 20])


    a1.generate_population(popsize = 600, virus = v, max_speed=1)

    a2 = population('USA', X_RESOLUTION, Y_RESOLUTION,[400, 20, 20, 1000])
    a2.generate_population(popsize = 100, virus = v, max_speed=1)

    a3 = population('Ireland', X_RESOLUTION, Y_RESOLUTION,[20, 400, 20, 400])
    a3.generate_population(popsize = 100, virus = v, max_speed=1)

    a4 = population('China', X_RESOLUTION, Y_RESOLUTION,[400, 20, 400, 20])
    a4.generate_population(popsize = 600, virus = v, max_speed=1)
    

    running = True
    while(running):
        
        worldwide.itterate(screen)
        a1.itterate(screen)
        a2.itterate(screen)
        a3.itterate(screen)
        a4.itterate(screen)
        pygame.display.flip()
        screen.fill([0, 0, 0])

        #Exit Points
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
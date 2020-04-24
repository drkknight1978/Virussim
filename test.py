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

    models = []
    
    p = 10
    for p in range(100, 1000, 100):
        c=0
        for RR in range (10, 200, 10):
            models.append(population(psuedoName(), X_RESOLUTION, Y_RESOLUTION,[10, 10, 10, 10]))
            models[c].generate_population (popsize = p, virus = virus(recovery_time=RR), max_speed=1)
            models[c].group[0].health = 'I'
            c +=1

        running = True
        fName = 'pop_' + str(p) + '.csv'
        f = open(fName, 'w+')    
        for c, m in enumerate(models):
            i = m.story()
            while i[2] !=0:
                m.itterate(screen)
                pygame.display.flip()
                screen.fill([0, 0, 0])
                i = m.story()
                #Exit Points
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if c == len(models):
                        running = False
            print ('date = {}, infection recovery time = {}, Healthy = {}, Sick = {}, Cured = {}'.format(i[0], m.group[0].virus.recovery_time,i[1], i[2], i[3]))
            d = str(i[0]) + ','+str(i[1]) + ','+ str(i[3]) + '\n'
            f.write(d)
        f.close()
        models.clear()
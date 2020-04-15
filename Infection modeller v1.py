# TO DO's
# 1. Create a Technique for adding a border DONE 14/4/20
# 2. Create a psuedoname function. DONE 14/4/20
# 3. Implement a population class and the current version is elegant.
# 4. Implement a world class to create multiple sims
# 5. Speed Up, Multi-threading, implement through an image and numpy arrage?

import pygame
from math import sqrt
import time
from random import random

#*****GLOBALS****

#Set up screensize and place a border if it is required
LEFT_BORDER = 100
RIGHT_BORDER = 100
TOP_BORDER = 100
BOTTOM_BORDER = 100
X_RESOLUTION, Y_RESOLUTION = (600, 600)
X_BORDER_MAX, Y_BORDER_MAX = (X_RESOLUTION - RIGHT_BORDER, Y_RESOLUTION - TOP_BORDER)
X_BORDER_MIN, Y_BORDER_MIN = (LEFT_BORDER , BOTTOM_BORDER)

#Civilisation aspects
POPSIZE = 200                # Population size
MAXSPEED = 1                # Maximum movement speed of victims
HP_MAX = 0                  # Health Points the amount of times you pass an infected victim before getting disease
DECISION_RANGE = 1         # Maximum number of moves before a victim might change direction.
VICTIM_RADIUS = 1           # Victims are represented as circles this is thier radius.

#State parameters - Defines the colours of the various states of the victims.
HEALTHY = [255, 255, 255]   # Healthy are White 
INFECTED = [255, 0, 0]      # Infected are Red
CURED = [0, 255, 0]     # Victimes no longer infected/ infectable

#Virus aspects
INFECTION_RADIUS = 2        # Distance from the surface of the victim another victim can be affetced.
RECOVERY_TIME = 100         # Amount of ticks before a victim is no longer infectable (dead / immune)

#World aspects
WORLDCLOCK = 0              # The worlds universal clock (ticks in __main__)

def listtostr(list_inp):
    #A little function to convert a list to a string tries to create a line for a csv file.
    o = ''
    for i in list_inp:
        o = o + str(i) + ','
    return (o + '\n') 

def psuedoName():
    #generates name for a victim.
    psName = ''
    for I in range(5):
        psName += chr(int(random()*26)+65)
    return (psName)

class victim:
    '''This is the victim class.
    a victim is alloted a position in space, a intial direction of travel,
    Health status (H)ealthy, (I)fected and (C)ured, victim size, 
    the maximum distance a victim will go before changeing direction (changedir), time according to the WORLDCLOCK
    when the victim get infected''' 
    population = []
    victims = 0

    def __init__(self, posX, posY, dirX, dirY, health = 'H', HP = 0, radius = VICTIM_RADIUS, changedir = 0, infectDate= 0):
        self.posX = posX
        self.posY = posY
        self.dirX = dirX
        self.dirY = dirY
        self.health = health
        self.HP = HP
        self.radius = radius
        self.changedir = int(random()*DECISION_RANGE)
        self.infectDate = infectDate

        self.check_state = { #--------------- is this the right place?
        'H' : HEALTHY,
        'I' : INFECTED,
        'C' : CURED,
        }

        victim.victims += 1
        self.ID = psuedoName()

    def draw(self, scrn):
        # Pass the pygame screen object and map a victim to it.
        pygame.draw.circle(scrn, self.check_state.get(self.health) , (self.posX, self.posY), self.radius)

    def move(self):
        #Movement method.
        dice = int(random() * self.changedir) # a probability of that the victim will change direction within 
        #                                       the maximum distance this victim can move e.g. 1 in 30 px or 
        #                                       1 in 50 px.
        if dice == 1: 
            # randomly changes direcion in the x, y, xy directions.
            dice = int(random() * 3)
            spd_change = int((random() - 0.5) * (MAXSPEED * 2))
            if dice == 0:
                self.dirX = spd_change
            if dice == 1:
                self.dirY = spd_change
            if dice == 2:
                self.dirX = spd_change
                self.dirY = spd_change
        
        #increment the victims position
        self.posX += self.dirX
        self.posY += self.dirY

    def collision(self):
        #Boundary test - wraps around the world
        if self.posX > X_BORDER_MAX:
            self.posX = X_BORDER_MIN + (self.posX - X_BORDER_MAX)
        if self.posX < X_BORDER_MIN:
            self.posX = X_BORDER_MAX + (self.posX - X_BORDER_MIN)
            
        if self.posY > Y_BORDER_MAX:
            self.posY = Y_BORDER_MIN + (self.posY - Y_BORDER_MAX)
        if self.posY < Y_BORDER_MIN:
            self.posY = Y_BORDER_MAX + (self.posY - Y_BORDER_MIN)


    def infected(self):
        #Checks if the victim is already infected. If so, cycle through the other victimss
        if self.health == 'I':
            for v in victim.population:
                # Check that the victim can be infected. If so, check the distance between this one
                # and the examined one if less than infection radius and reached the maximum Health Point
                # infect the victim and register the time of infection, or if still within the infection
                # region add a health point. 
                if v.health == 'H':
                    distX = v.posX - self.posX
                    distY = v.posY - self.posY
                    distR = int(abs(sqrt(abs(distX ^ 2) + abs(distY ^ 2))))
                    if distR < INFECTION_RADIUS:
                        if v.HP == HP_MAX:
                            v.health = 'I'
                            v.infectDate = WORLDCLOCK
                            v.HP += 1
                        else:
                            v.HP += 1
                     
    def recovered(self):
        #If an infected victim has reached the end of the infection period they become 'Cured' - uninfectable.
        if self.health == 'I' and RECOVERY_TIME <= (WORLDCLOCK - self.infectDate):
            self.health = 'C'
    
    @classmethod
    def story(cls):
        #returns a poll of the current H/I/C population.
        sort_info = cls.population
        H = 0
        I = 0
        C = 0
        for v in sort_info:
            if v.health == 'H':
                H += 1
            if v.health == 'I':
                I += 1
            if v.health == 'C':
                C += 1
        return ([WORLDCLOCK, H, I, C])

       

if __name__ == "__main__":
    #Enter the main loop.
    #initialise the world
    screen = pygame.display.set_mode([X_RESOLUTION, Y_RESOLUTION])
    pygame.display.set_caption("Virus World")

    #Generate the initial population
    for _ in range(POPSIZE):
        X = int(random() * (X_RESOLUTION - (LEFT_BORDER + RIGHT_BORDER))) + LEFT_BORDER ####### 
        Y = int(random() * (Y_RESOLUTION - (TOP_BORDER + BOTTOM_BORDER))) + BOTTOM_BORDER #######
        DY = int(random() * (MAXSPEED + 1 * 2)) - MAXSPEED
        DX = int(random() * (MAXSPEED + 1 * 2)) - MAXSPEED
        victim.population.append(victim(X, Y, DX, DY))
        print(X)
    #Create one infected victim to drop into the Simulation
    victim.population[0].health = 'I'

    #f = open('small4.csv','w') # open a file to record data my be NEEDS MODIFYING

    #Initialise the running variables
    record = [] 
    record.append(victim.story())
    running = True
    
    while  running != False:
        for v in victim.population:
            #Itterate through each victim and Move, check collision, check infection, check recovered and draw.
            v.move()
            v.collision()
            v.infected()
            v.recovered()
            v.draw(screen)
        
        # Once the world has been updated update the screen.
        pygame.display.flip()
        screen.fill([0, 0, 0])

        # Tick the clock forward.
        WORLDCLOCK += 1

        info =victim.story()

        print((info[1]/250), (info[2]/250), (info[3]/250))


        #Saves a file and debugging
        #f.write(listtostr (record))
        #print(listtostr (record)) This prints the population.

        #Exit Points
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        


#f.close()
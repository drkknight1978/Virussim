import pygame
from math import sqrt
import time
from random import randint, random
from virusmodel import *

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

class virus:
    def __init__(self, infection_radius = 2, recovery_time = 100):
        #Virus aspects
        #INFECTION_RADIUS = Distance from the surface of the victim another victim can be affetced.
        #RECOVERY_TIME = Amount of ticks before a victim is no longer infectable (dead / immune)
        self.infection_radius = infection_radius
        self.recovery_time = recovery_time


class population:
    population_list = []
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 10)

    def __init__(self, ID, x_res = 600, y_res = 600, bound_box = [50, 50, 50, 50]):
        # popsize =Population size
        # max_speed = Maximum movement speed of victims
        # HP_max = Health Points the amount of times you pass an infected victim before getting disease
        # decision_range =Maximum number of moves before a victim might change direction.
        # victim_radius =Victims are represented as circles this is thier radius.
        self.group = [] #list that contains victim objects.
        self.ID = ID
        population.x_res = x_res
        population.y_res = y_res
        self.bound_box = bound_box
        population.population_list.append(self)
        self.wrldclk = 0
    
    def generate_population(self, popsize = 200, virus = virus(), max_speed = 1, decision_range = 1, HP_max = 0):
        #Generate the initial population
        L_border = self.bound_box[0]
        R_border = self.bound_box[1]
        T_border = self.bound_box[2]
        B_border = self.bound_box[3]
        for _ in range(popsize):
            X = int(random() * (self.x_res - (L_border + R_border))) + L_border 
            Y = int(random() * (self.y_res - (T_border + B_border))) + B_border
            DY = int(random() * (max_speed + 1 * 2)) - max_speed
            DX = int(random() * (max_speed + 1 * 2)) - max_speed
            self.group.append(victim(X, Y, DX, DY, virus, max_speed, decision_range , HP_max ))
    
    def itterate(self, scrn ,mixing_population = population_list):
        #itterate through population and check conditions/infections
        #mixing_population is a list of populations which can infect each other
            for v in self.group:
                v.move()
                v.collision(self.bound_box)
                for p in mixing_population:
                    v.infected(p)
                v.recovered(self.wrldclk)
                v.draw(scrn)
            self.wrldclk += 1
        

    def story(self):
        #returns a poll of the current H/I/C population.
        sort_info = self.group
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
        return ([self.wrldclk, H, I, C])


class victim(population):
    '''This is the victim class.
    a victim is alloted a position in space, a intial direction of travel,
    Health status (H)ealthy, (I)fected and (C)ured, victim size, 
    the maximum distance a victim will go before changeing direction (changedir), time according to the WORLDCLOCK
    when the victim get infected''' 
    victims = 0

    def __init__(self, posX, posY, dirX, dirY, virus = virus(), max_speed = 1, decision_range = 2, HP_max = 0, health = 'H', HP = 0, radius = 0, infectDate= 0):
        self.virus = virus
        self.posX = posX
        self.posY = posY
        self.dirX = dirX
        self.dirY = dirY
        self.virus = virus
        self.max_speed = max_speed
        self.changedir = randint(0,decision_range)
        self.HP_max = HP_max
        self.health = health
        self.HP = HP
        self.radius = radius
        self.infectDate = infectDate
        self.x_res = population.x_res
        self.y_res = population.y_res

        #State parameters - Defines the colours of the various states of the victims.
        HEALTHY = [255, 255, 255]   # Healthy are White 
        INFECTED = [255, 0, 0]      # Infected are Red
        CURED = [0, 255, 0]     # Victimes no longer infected/ infectable
 

        self.check_state = { #--------------- is this the right place?
        'H' : HEALTHY,
        'I' : INFECTED,
        'C' : CURED,
        }

        victim.victims += 1
        self.ID = psuedoName()

    def draw(self, scrn):
        # Pass the pygame screen object and map a victim to it.
        try:
            message = str(self.wrldclk) + ' '
            for p in population.population_list:
                figures = p.story()
                message += str(p.ID) + ' : Uninfected = ' + str(figures[1]) + ' Infected = ' + str(figures[2]) + ' Cured = ' +str(figures[3]) + '|'
            textsurface = myfont.render(message, False, (255, 255, 255))      
            scrn.blit(textsurface,(0, 0))
            pygame.draw.circle(scrn, self.check_state.get(self.health) , (self.posX, self.posY), self.radius)
        except:
            pygame.draw.circle(scrn, self.check_state.get(self.health) , (self.posX, self.posY), self.radius)

    def move(self):
        #Movement method.
        dice = randint(0, self.changedir) # a probability of that the victim will change direction within 
        #                                       the maximum distance this victim can move e.g. 1 in 30 px or 
        #                                       1 in 50 px.
        if dice == 1: 
            # randomly changes direcion in the x, y, xy directions.
            dice =randint(0, 2)
            spd_change = randint(-1 * self.max_speed, self.max_speed)
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

    def collision(self, dimensions):
        #Boundary test - wraps around the world
        L_border = dimensions[0]
        R_border = dimensions[1]
        T_border = dimensions[2]
        B_border = dimensions[3]
        
        if self.posX > (self.x_res - R_border):
            self.posX = L_border + (self.posX - (self.x_res - R_border))
        if self.posX < L_border:
            self.posX = (self.x_res - R_border) + (self.posX - L_border)
            
        if self.posY > (self.y_res - T_border):
            self.posY = B_border + (self.posY - (self.y_res - T_border))
        if self.posY < B_border:
            self.posY = (self.y_res - T_border) + (self.posY - B_border)


    def infected(self, population):
        #Checks if the victim is already infected. If so, cycle through the other victimss
        if self.health == 'I':
            for v in population.group:
                # Check that the victim can be infected. If so, check the distance between this one
                # and the examined one if less than infection radius and reached the maximum Health Point
                # infect the victim and register the time of infection, or if still within the infection
                # region add a health point. 
                if v.health == 'H':
                    distX = v.posX - self.posX
                    distY = v.posY - self.posY
                    distR = int(abs(sqrt(abs(distX ^ 2) + abs(distY ^ 2))))
                    if distR < self.virus.infection_radius:
                        if v.HP == self.HP_max:
                            v.health = 'I'
                            v.infectDate = population.wrldclk
                            v.HP += 1
                        else:
                            v.HP += 1
                     
    def recovered(self, wrldclk):
        #If an infected victim has reached the end of the infection period they become 'Cured' - uninfectable.
        if self.health == 'I' and self.virus.recovery_time <= (wrldclk - self.infectDate):
            self.health = 'C'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:54:10 2020

@author: ryanburczak
"""

# CONSTANTS (science):
# How close is too close?
# chance of being infected if contact is too close
# chance of death if infected

# FOR EVERY PERSON (personal):
# Are they infected to begin with?
# How is their health (determines whether they survive or die)? Let the user decide
# Average time to recovery?

# OTHER THINGS:
# How should we measure time (minutes, hours, days)?
# It could take 2 to 6 weeks to recover from coronavirus.
# 14 to 42 days. 336 to 1008 hours. 20160 to 60480 minutes.
# Measure time in days.

# OUTPUT:
# graph showing death rate over time
# infection rate
# visualization of virus spread


import random
import numpy as np
import matplotlib.pyplot as plt # because turtle doesn't wanna draw
import math



# Sources: https://opentechschool.github.io/python-beginners/en/simple_drawing.html
#          https://realpython.com/beginners-guide-python-turtle/#drawing-a-shape

# Variables to be edited by the user
width = 900
height = 900
start_pop_infected = 0.04
radius_of_infection = 20.00
localmove = 20 # absolute value of maximum local movement
globalmove = 0.80 # maximum percentage of width/height
num_people = 600
total_days = 100

days_asymptomatic = 2 # how many days sick people move around before stopping

infection_period = 14 # how many days will a person stay infected from coronavirus?


def plot_population(people, day):
    num_infected = 0

    x = [] # x-coordinate
    y = [] # y-coordinate
    col = [] # colors
    
    # For every person
    for count,obj in enumerate(objs): # returns the count # as well as the object
        xt, yt = obj.location() # extract location
        x.append(xt)
        y.append(yt)
        if (obj.is_infected()):
            num_infected += 1
        
        if (obj.is_alive() == False): # dead
            col.append("black")
        elif (obj.is_infected() == True):
            col.append("red")
        elif (obj.is_recovered() == True):
            col.append("yellow")
        else:
            col.append("green")
        
    
#    print("Infected people = ", num_infected)
    plt.scatter(x, y, c=col)
    plt.title(f'Infections: Day {day}')
    plt.show()
    
def calc_distance(loc1, loc2):
    return math.sqrt( (loc2[0] - loc1[0])**2 + (loc2[1] - loc1[1])**2 )
    # [0] for x-coordinate, [1] for y-coordinate


class Person():
    # CLASS VARIABLES NEEDED: dead/alive, infected (yes/no), health index (1-100), location (x,y)
    def __init__(self):
        # Set the initial location
        # These are Cartesian coordinates: (0,0) is the center,
        # with negatives down and left, positives up and right
        self.xLoc_ = random.randint(0, width)
        self.yLoc_ = random.randint(0, height)
        
        # Are they infected to start with?
        # The population parameter should be set by the user
        
        self.status_ = 3
        
        # HEALTH STATES:
        # 3 = un-infected
        # 2 = recovered
        # 1 = infected
        # 0 = dead
        
        self.dayInfected_ = None # python's version of null
        # If the person gets infected, this variable will be set to the day they
        # contracted coronavirus. Now, they musgt wait to see what happens during
        # the set infection period.
        
        # generate a float between 0.00 and 1.00
        if random.random() <= start_pop_infected:
            self.status_ = 1
            self.dayInfected_ = 1
            
        # Health of the user should be determined in a Virginia-shaped distribution
        # (clustered more around the high end)
        mean = 50
        stdev = 16
        
        self.health_ = np.random.normal(mean, stdev)
    
        # Source: https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html
        
        # Does the person move locally or globally?
        # Perhaps roughly 85% of people should move locally, while 15% move globally
        self.move_function = self.local_move # function pointer
        if random.random() <= 0.15:
            self.move_function = self.global_move
        
    
    def is_alive(self): # return a bool
        if (self.status_ != 0):
            return True
        else:
            return False
        
    def is_infected(self): # return a bool
        if (self.status_ == 1):
            return True
        else:
            return False
        
    def is_recovered(self):
        if (self.status_ == 2):
            return True
        else:
            return False
        
    def health(self):
        return self.health_
    
    def location(self): # return two coordinates
        # x first, then y
        return self.xLoc_, self.yLoc_
    
    def move(self, day):
        if (self.is_infected() == True): # limited movement if infected
            if (day >= self.dayInfected_ + days_asymptomatic):
                return # don't move
        
        if (self.is_alive() == False):
            return # You can't move, you're dead!
        
        self.move_function()
        
    def local_move(self): # person moves within 50 units of where they sare
        self.xLoc_ = self.xLoc_ + random.randint(-localmove, localmove)
        if (self.xLoc_ > width): # can't move past the right boundary
            self.xLoc_ = width
        if (self.xLoc_ < 0): # can't move past the left boundary
            self.xLoc_ = 0
            
        self.yLoc_ = self.yLoc_ + random.randint(-localmove, localmove)
        if (self.yLoc_ > height): # can't move past the top boundary
            self.yLoc_ = height
        if (self.yLoc_ < 0): # can't move past the bottom boundary
            self.yLoc_ = 0
        
    def global_move(self): # for an exclusive set of people, move across the grid
                           # by at most a particular ratio of the width/height
        
        # Randomly pick if the person moves horizontally or vertically
        direction = random.choice(("H", "V"))
        # Source for "choice": https://pynative.com/python-random-choice/
        
        if (direction == "H"):
            self.xLoc_ = self.xLoc_ + random.choice([-1, 1])*(globalmove)*(width)
            if (self.xLoc_ > width): # can't move past the right boundary
                self.xLoc_ = width
            if (self.xLoc_ < 0): # can't move past the left boundary
                self.xLoc_ = 0
        elif (direction == "V"):
            self.yLoc_ = self.yLoc_ + random.choice([-1, 1])*(globalmove)*(height)
            if (self.yLoc_ > height): # can't move past the top boundary
                self.yLoc_ = height
            if (self.yLoc_ < 0): # can't move past the bottom boundary
                self.yLoc_ = 0
            
    def infect(self, objs, day): # change status from 3 to 1
        if (self.status_ == 3):
            for neighbor in objs:
                if (neighbor.is_infected()): 
                    # is this neighbor infected
                    d = calc_distance(obj.location(), neighbor.location())
                    if (d < radius_of_infection):
                        # if the person is near an infected neighbor
                        self.status_ = 1 # now infected
                        self.dayInfected_ = day # keep track of the day this person was infected
                        return True
        return False  # won't happen if the person is being careful!
                    
    def recover(self):
        if (self.status_ == 1): # must be infected first!
            self.status_ = 2
            return True
        return False
    
    def vitals(self):
        # taking vitals on the infected person!
        # chance of death on certain day: 1/health index
        if random.random() <= (1/(self.health_)):
            # this person has died today.
            self.status_ = 0
            return False # false as in, the person did not make it
        return True # true as in, this person is still living
        
    def update_health(self, objs, day):
        ''' health state changes from 3 to 1, 1 to 2, or 1 to 0... or maybe not '''
        # return a short string describing the health of the person
        
        # change from 3 to 1
        if (self.infect(objs, day)): # this will not work if the state is not already 3
            return "infected"
        # change from 1 to 2... or 1 to 0... or neither
        elif (self.is_infected()):
            if (day <= self.dayInfected_ + infection_period):
                # This person is still infected. Take vital signs!
                if (self.vitals() == True):
                    # This person is still OK
                    return "still infected"
                else:
                    # I'm sorry... :(
                    return "dead"
            else:
                # Good news! This person is no longer infected! :)
                self.recover()
                return "recovered"
        else:
            return "ok!"
                
            
        # if the person is already infected, the infection period should be...
        # if the person is infected, but the infection period is complete
        # update_health should transition to either dead (0) or recovered (2)
        # if the person is not already infected, recovered, or dead... then call infect()
        


# Now create 100 people
objs = [Person() for i in range(num_people)]
plot_population(objs, 0) # for the, uh, 0th day?


# CODE FOR THE SIMULATOR:
total_infections = 0
total_recoveries = 0
total_deaths = 0

for d in range(1, total_days + 1): # for however many days specified
    new_infections = 0 # how many (more) people got infected today?
    new_recoveries = 0
    new_deaths = 0
    
    # For every person
    for obj in objs:
        status = obj.update_health(objs, d)
        
        if ( status == "infected" ): # don't neeed to satisfy the self argument here
            # this will happen if the person's health state changed from 3 to 1
            new_infections += 1
        elif( status == "still infected"):
            # don't do anything
            continue
        elif( status == "recovered"):
            # this will happen if the person's health state changed from 1 to 2
            new_recoveries += 1
        elif( status == "dead"):
            new_deaths += 1
        elif( status == "ok!" ):
            continue
        
        # return values... person died, recovered, got infected, or nothing happened
        # died, recovered, infected, nothing = obj.update_health(objs, d)
        # num_infections += infected
        # num_recovered += recovered
        # num_dead += died
    total_infections += new_infections
    total_recoveries += new_recoveries
    total_deaths += new_deaths
    print("Day", d, ":")
    print("New infections =", new_infections)
    print("New recoveries =", new_recoveries)
    print("New deaths =", new_deaths)
    print("Total infections =", total_infections)
    print("Total recoveries =", total_recoveries)
    print("Total deaths =", total_deaths)
    print()
    
    
    for obj in objs: # move the people
        obj.move(d)
                
    plot_population(objs, d) # update the positions at the end
# print("Infections =", total_infections)
        
    

# now draw a rectangle, and draw a circle at every location
# color infected people red
# color recovered people yellow
# color non-infected people green
# color dead people black

# keep a count of the number of people infected
# if anyne comes within 2 units of an infected person, they will become infected (100%  chance)

# for any particular Person:
# if they are infected, they will pass it on to the person they encounter
# if they are not infected, and they encounter a person who is infected, they get infected too

# LOOP FOR SPREADING INFECTION:
# if a person is un-infected (or recovered), check if their close neighbors are infected
# find distance between the person and any of its neighbors
# if sqrt( (x2-x1)^2 + (y2-y1)^2 ) <= 2
# if person b is infected
# change status of person a to "infected"

# objs[0].do_sth()

# Source: https://stackoverflow.com/questions/21598872/how-to-create-multiple-class-objects-with-a-loop-in-python/21598969
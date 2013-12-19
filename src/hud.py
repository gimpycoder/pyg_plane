import math
import pygame as pyg
from utility import *

################################################################################
# ALL ENTITIES THAT ARE NOT DIRECTLY IN PLAY (user interface related)
# Classes in File:
# Score
# HealthBar

#===============================================================================
class Score(object):
    name = 'score_sheet'

    #___________________________________________________________________________
    def __init__(self, screen, location):
        self.screen = screen
        self.value = 0
        self.max_value = 9999999999
        self.digits = {}
        self.location = Vector(location[0], location[1])
        self.width = 0
        self.init()

    #___________________________________________________________________________
    def init(self):
        for i in xrange(10):
            self.digits[str(i)] = get_number(str(i))
            
        self.width = self.digits['0'].get_size()[0] + 2
        print self.width

    #___________________________________________________________________________
    def increase_score(self, amount):
        if self.value + amount > self.max_value:
            self.value = self.max_value
            
        self.value += amount
    
    #___________________________________________________________________________    
    def decrease_score(self, amount):
        if self.value - amount < 0:
            self.value = 0
            
        self.value -= amount
    
    #___________________________________________________________________________    
    def display(self):
        # no negative scores for this game.
        if self.value < 0:
            self.value = 0
    
        score = str(self)
        location = self.location.get_copy()
        for i in xrange(len(score)):
            img = self.digits[score[i]]
            self.screen.blit(img, (location.x, location.y))
            location.x += self.width
    
    #___________________________________________________________________________    
    # Right padded string 10 characters.
    def __str__(self):
        return str(self.value).rjust(10, '0')
        
#===============================================================================
class HealthBar(object):

    #___________________________________________________________________________
    def __init__(self, screen, location, color=(0,255,0)):
        self.screen   = screen
        self.location = Vector(location[0], location[1])
        
        # Locations and dimensions of the drawn health bar.
        self.top_left     = self.location.get_copy()
        self.top_left.add(Vector(7,11))
        self.top_right    = self.location.get_copy()
        self.top_right.add(Vector(132,11))
        self.bottom_left  = self.location.get_copy()
        self.bottom_left.add(Vector(7,21))
        self.bottom_right = self.location.get_copy()
        self.bottom_right.add(Vector(132,21))
        self.height       = abs(self.top_left.y - self.bottom_left.y)
        self.width        = abs(self.top_left.x - self.top_right.x)
        self.color        = color
        
        self.max_health   = self.width
        self.health       = 0
    
    #___________________________________________________________________________    
    def increase_health(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
    
    #___________________________________________________________________________    
    def decrease_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    #___________________________________________________________________________        
    def is_dead(self):
        if self.health <= 0:
            print 'dead'
            raw_input('health.py')
        return self.health <= 0
    
    #___________________________________________________________________________    
    def is_full_health(self):
        return self.health >= self.max_health
    
    #___________________________________________________________________________    
    def full_health(self):
        self.health = self.max_health
    
    #___________________________________________________________________________    
    def zero_health(self):
        self.health = 0
    
    #___________________________________________________________________________    
    def display(self):
        # first draw our image.
        img = get_image('health', 0)
        self.screen.blit(img, (self.location.x, self.location.y))
        # build our rectangle but only if we still have health.
        if not self.is_dead():
            bar = pyg.Rect(self.top_left.x, 
                           self.top_left.y, 
                           self.health, # now we draw it only as long as health.
                           self.height)
                       
            # draw our rectangle on top of the image
            # 0 width means fill rectangle.
            pyg.draw.rect(self.screen, self.color, bar, 0)

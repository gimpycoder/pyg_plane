import pygame as pyg
import math
import artwork
from vector import Vector

class HealthBar(object):

    def __init__(self, screen, location, color=(0,255,0)):
        self.screen   = screen
        self.location = location
        
        # cannot use constants any longer...
        #self.top_left     = (7,11)
        #self.top_right    = (132,11)
        #self.bottom_left  = (7,21)
        #self.bottom_right = (132,21)
        
        # instead we offset by it.
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
        print '%s' % str(artwork.get_image('health', 0).get_size())
        
    def increase_health(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        
    def decrease_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
            
    def is_dead(self):
        return self.health <= 0
        
    def is_full_health(self):
        return self.health >= self.max_health
        
    def full_health(self):
        self.health = self.max_health
        
    def zero_health(self):
        self.health = 0
        
    def display(self):
        # first draw our image.
        img = artwork.get_image('health', 0)
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
        

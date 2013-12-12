import pygame as pyg
import math

class HealthBar(object):
    def __init__(self, screen, image_source, location):
        self.screen   = screen
        self.image    = pyg.image.load(image_source)
        self.location = location
        
        self.top_left     = (7,11)
        self.top_right    = (132,11)
        self.bottom_left  = (7,20)
        self.bottom_right = (132,20)
        self.height       = abs(self.top_left[1] - self.bottom_left[1])
        self.width        = abs(self.top_left[0] - self.top_right[0])
        self.color        = (0, 255, 0)
        
        self.max_health   = self.width
        self.health       = 0
        
    def increase_health(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        
    def decrease_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
            
    def is_dead(self):
        return self.health == 0
        
    def is_full_health(self):
        return self.health >= self.max_health
        
    def full_health(self):
        self.health = self.max_health
        
    def zero_health(self):
        self.health = 0
        
    def display(self):
        # first draw our image.
        self.screen.blit(self.image, (self.location.x, self.location.y))
        # build our rectangle but only if we still have health.
        if not self.is_dead():
            bar = pyg.Rect(self.top_left[0], 
                           self.top_left[1], 
                           self.health, # now we draw it only as long as health.
                           self.height)
                       
            # draw our rectangle on top of the image
            # 0 width means fill rectangle.
            pyg.draw.rect(self.screen, self.color, bar, 0)
        

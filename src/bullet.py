from vector import Vector
import pygame as pyg

class Bullet(object):
    def __init__(self, screen, location, radius, speed=5, color=(255,255,255)):
        self.screen = screen
        self.location = location
        self.radius = radius
        self.speed = speed
        self.color = color
        self.alive = True
        
    def update(self):
        # we only change the Y component.
        self.location.y -= self.speed
        self.check_boundaries()
    
    def check_boundaries(self):
        # this just makes refering to them shorter.
        x = self.location.x
        y = self.location.y
        # get our x,y boundaries by unpacking get_size()
        right, bottom = self.screen.get_size()
        
        # our boundaries start at 0,0 of the image so we have to
        # offset where we are checking by the width of the image.
        if x > right or x < 0 or y > bottom or y < 0:
            self.alive = False
            
        # update the position with x,y values.
        self.location.x = x
        self.location.y = y
        
    def display(self):
        if self.alive:
            pyg.draw.circle(self.screen, 
                            self.color, 
                            (int(self.location.x), int(self.location.y)), 
                            self.radius, 
                            0) # 0 fills in the circle

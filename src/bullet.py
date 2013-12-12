from vector import Vector
import pygame as pyg

class Bullet(object):
    def __init__(self, screen, position, radius, speed=5, color=(255,255,255)):
        self.screen = screen
        self.position = position
        self.radius = radius
        self.speed = speed
        self.color = color
        
    def update(self):
        # we only change the Y component.
        self.position.y -= self.speed
        
    def display(self):
        pyg.draw.circle(self.screen, 
                        self.color, 
                        (int(self.position.x), int(self.position.y)), 
                        self.radius, 
                        0) # 0 fills in the circle

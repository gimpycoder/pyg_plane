import pygame as pyg
from utility import *

#===============================================================================
class PowerUp(object):
    name = 'power_up'
    #___________________________________________________________________________
    def __init__(self, screen, location):
        """
        name     = The name of this vehicle based on assets
        location = Vector of initial position
        
        """
        self.location = Vector(location[X],location[Y])
        self.screen             = screen
        self.speed              = 5
        self.frame_count        = get_frame_count(self.name)
        self.frame_delay        = FRAME_DELAY
        self.frame              = 0
        self.wait_time          = FRAME_DELAY
        self.image = get_image(self.name, 0)
    #___________________________________________________________________________
    def update(self):
        # we'll just make it go from left to right straight line for now.
        if self.wait_time == 0:
            self.location.x += self.speed
            self.wait_time = FRAME_DELAY
        else:
            self.wait_time -= 1
    #___________________________________________________________________________
    def display(self):
        self.screen.blit(self.image, (self.location.x, self.location.y))

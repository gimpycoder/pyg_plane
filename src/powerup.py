import artwork
from vehicle import Vehicle
from vector import Vector
import math
        

class PowerUp(Vehicle):
    name = 'power_up'

    def __init__(self, screen, location):
        """
        name     = The name of this vehicle based on assets mapped in artwork.py
        location = Vector of initial position
        
        """
        super(PowerUp, self).__init__(self.name, location)
        self.screen             = screen
        self.location           = location
        self.speed              = 5
        self.frame_count        = artwork.get_frame_count(self.name)
        self.frame_delay        = artwork.FRAME_DELAY
        self.frame              = 0
        self.wait_time          = artwork.FRAME_DELAY
    
    def update(self):
        # we'll just make it go from left to right straight line for now.
        if self.wait_time == 0:
            self.location.x += self.speed
            self.wait_time = artwork.FRAME_DELAY
        else:
            self.wait_time -= 1
            
        #    self.wait_time = 1
        #else:
        #    self.wait_time -= 1
    
    def flip(self):
        self.frame = 1 if (self.frame == 0) else 0
        
    def display(self):
        self.frame_delay -= 1
        if self.frame_delay <= 0:
            self.flip()
            self.frame_delay = artwork.FRAME_DELAY
        
        img = artwork.get_image(self.name, self.frame)    
        self.screen.blit(img, (self.location.x, self.location.y))
        
    def __str__(self):
        return "%s: %r - frames=%d" % (self.name, self.location, self.frame_count)

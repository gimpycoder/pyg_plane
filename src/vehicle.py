import artwork

class Vehicle(object):

    def __init__(self, name, location):
        """
        name     = The name of this vehicle based on assets mapped in artwork.py
        location = Vector of initial position
        
        """
        
        self.name               = name
        self.location           = location
        self.frame_count        = artwork.get_frame_count(self.name)
        self.frame_delay        = artwork.FRAME_DELAY
        self.frame              = 0
        
    def display(self):
        self.frame_delay -= 1
        if self.frame_delay <= 0:
            self.flip()
            self.frame_delay = artwork.FRAME_DELAY
        
        img = artwork.get_image(self.name, self.frame)    
        self.screen.blit(img, (self.location.x, self.location.y))
        
    def __str__(self):
        return "%s: %r - frames=%d" % (self.name, self.location, self.frame_count)
        

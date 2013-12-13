from vector import Vector
import pygame as pyg

class Player(object):
    def __init__(self, screen, image_source, speed=5):
        self.screen = screen
        self.image = pyg.image.load(image_source)
        self.speed = speed
        
        # for now we duplicate functionality from the original goal.
        self.img_x, self.img_y = self.image.get_size()
        x, y  = screen.get_size()
        #self.location = Vector(x/2 - self.img_x/2, y/2 - self.img_y/2)
        self.location = Vector(40,40)
    
    def get_rect(self):
        return pyg.Rect(self.location.x, self.location.y, self.img_x, self.img_y)
    
    def get_center(self):
        # get our location
        location = self.location.get_copy()
        # get half of the image's size to find its center.
        x,y = (self.img_x/2, self.img_y/2)
        # add that offset to our location vector.
        location.add(Vector(x,y))
        # give caller the center of our player.
        return location
        
    def update(self, movement):
        # scale our movement by speed.
        movement.mul(self.speed)
        # update position by adding movement to location.
        self.location.add(movement)
        # this movement may have put us outside our boundaries so let's
        # check that.
        self.check_boundaries()
        
    def check_boundaries(self):
        # this just makes refering to them shorter.
        x = self.location.x
        y = self.location.y
        # get our x,y boundaries by unpacking get_size()
        right, bottom = self.screen.get_size()
        
        # our boundaries start at 0,0 of the image so we have to
        # offset where we are checking by the width of the image.
        if x + self.img_x > right:
            # we have to update position minus the size of the image.
            x = right - self.img_x
        # checking for zero is easier.
        if x < 0:
            x = 0
        # y is the same way as x.
        if y + self.img_y > bottom:
            y = bottom - self.img_y
        # again, zero is easier.
        if y < 0:
            y = 0
            
        # update the position with x,y values.
        self.location.x = x
        self.location.y = y
        
    def display(self):
        self.screen.blit(self.image, (self.location.x, self.location.y))

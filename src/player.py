from vector import Vector
from vehicle import Vehicle
from bullet import Bullet
import artwork
import pygame as pyg

class Player(Vehicle):
    name = 'player'

    def __init__(self, screen, speed=5):
        super(Player, self).__init__(self.name, Vector(0,0))
        
        self.screen = screen
        self.speed = speed
        
        # for now we duplicate functionality from the original goal.
        self.img_x, self.img_y = artwork.get_image(self.name, 0).get_size()
        x, y  = screen.get_size()
        #self.location = Vector(x/2 - self.img_x/2, y/2 - self.img_y/2)
        self.location = Vector(40,40)
    
        self.bullets = []
        self.bullet_speed = 5
    
    def flip(self):
        pass
        
    def fire(self):
        # find the gun
        gun = self.get_center()
        gun.y = self.location.y
        # create the bullet
        bullet = Bullet(self.screen, # we'll get rid of screen on this soon
                            gun, 
                            1,                 # little pea shooter radius
                            self.bullet_speed, # speed is positive.
                            (255,255,255))
        self.bullets.append(bullet)
    
    def is_collision(self, rect):
        for b in self.bullets:
            if rect.collidepoint((b.location.x, b.location.y)):
                self.bullets.remove(b)
                return True
    
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
        
        # update all bullets:
        for b in self.bullets:
            b.update()
            if b.alive == False:
                self.bullets.remove(b)
                print 'player bullet removed'
            
        # now we check boundaries and remove what left the area.
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
        super(Player, self).display()
        #img = artwork.get_image(self.name, self.frame)
        #self.screen.blit(img, (self.location.x, self.location.y))
        
        # now draw all bullets and they will be on top of the boat.
        for b in self.bullets:
            b.display()

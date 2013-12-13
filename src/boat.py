from vector import Vector
import pygame as pyg
import random
from bullet import Bullet
from vehicle import Vehicle
import artwork

class Boat(Vehicle):
    name = 'boat'

    def __init__(self, screen, speed=5, bullet_speed=-5):
        super(Boat, self).__init__(self.name, Vector(0,0))
        self.screen = screen
        self.bullets = []
        self.speed = speed
        self.bullet_speed = bullet_speed
        self.gun_location = Vector(20, 109)
        
        # for now we duplicate functionality from the original
        self.img_x, self.img_y = artwork.get_image(self.name, 0).get_size()
        self.max_x, self.max_y  = screen.get_size()
        self.location = Vector(self.max_x/2 - self.img_x/2, 
                               self.max_y/2 - self.img_y/2)
    
    def is_collision(self, rect):
        for b in self.bullets:
            if rect.collidepoint((b.position.x, b.position.y)):
                self.bullets.remove(b)
                return True
    
    def get_center(self):
        return Vector(self.location.x + self.gun_location.x,
                      self.location.y + self.gun_location.y)
        
    def update(self):
        # our boat handles its own bullets now.
        # first fire, then update.
        self.fire()
        # update all bullets.
        for b in self.bullets:
            b.update()
            
        # now we check boundaries and remove what left the area.
        self.check_boundaries()
    
    def fire(self):
        # get a random float:
        chance = random.random()
        # we only fire 8% of the time
        if chance <= .08:
            # find the gun
            gun = self.get_center()
            # create the bullet
            bullet = Bullet(self.screen, # we'll get rid of screen on this soon
                            gun, 
                            1,                 # little pea shooter radius
                            self.bullet_speed, # speed is negative so it adds.
                            (255,255,255))
            # add bullet to collection
            self.bullets.append(bullet)
            # now it exists and we wait for update to be called.
            
    def check_boundaries(self):
        for b in self.bullets:
            if b.position.y >= self.max_y:
                self.bullets.remove(b)
    
    def flip(self):
        self.frame = 1 if (self.frame == 0) else 0
        
    def display(self):
        # first draw the boat.
        #self.frame_delay -= 1
        #if self.frame_delay <= 0:
        #    self.flip()
        #    self.frame_delay = artwork.FRAME_DELAY
        #
        #img = artwork.get_image(self.name, self.frame)    
        #self.screen.blit(img, (self.location.x, self.location.y))
        super(Boat, self).display()
        
                         
        # now draw all bullets and they will be on top of the boat.
        for b in self.bullets:
            b.display()

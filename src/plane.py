from vector import Vector
import pygame as pyg
import random
from bullet import Bullet
from vehicle import Vehicle
import artwork

class Plane(Vehicle):
    name = 'plane'

    def __init__(self, screen, player, speed=1, bullet_speed=-5):
        super(Plane, self).__init__(self.name, Vector(0,0))
        self.screen         = screen
        self.bullets        = []
        self.speed          = speed
        self.bullet_speed   = bullet_speed
        self.target         = player
        self.damage         = 10
        self.health         = 1
        self.is_alive       = True
        
        self.img_x, self.img_y = artwork.get_image(self.name, 0).get_size()
        self.max_x, self.max_y  = screen.get_size()
        self.location = Vector(40,0)
    
        # bottom of the graphic:
        self.gun_location = Vector(self.img_x/2, self.img_y)
    
    def get_rect(self):
        return pyg.Rect(self.location.x, 
                        self.location.y, 
                        self.img_x, 
                        self.img_y)
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.is_alive = False
    
    def is_collision(self, rect):
        for b in self.bullets:
            if rect.collidepoint((b.location.x, b.location.y)):
                self.bullets.remove(b)
                return True
    
    def get_center(self):
        return Vector(self.location.x + self.gun_location.x,
                      self.location.y + self.gun_location.y)
        
    def update(self):
        # change position by speed:
        self.location.add(Vector(0, self.speed))
        #print self.location
        # our plane handles its own bullets now.
        # first fire, then update.
        self.fire()
        # update all bullets.
        for b in self.bullets:
            b.update()
            if b.alive == False:
                self.bullets.remove(b)
                #print 'plane bullet removed'
    
    def fire(self):
        # get a random float:
        #chance = random.random()
        # we only fire 8% of the time if the player is in line of sight.
        #if chance <= .08:
        if abs(self.target.location.x - self.location.x) <= 50:
            # get a random float:
            chance = random.random()
            if chance > .20:
                return
            
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
    
    def flip(self):
        # no animations yet so we just pass
        pass
        #self.frame = 1 if (self.frame == 0) else 0
        
    def display(self):
        super(Plane, self).display()
        
        # now draw all bullets
        for b in self.bullets:
            b.display()

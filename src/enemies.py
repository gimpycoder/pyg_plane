import random, math
import pygame as pyg
from utility import *
from particles import Bullet,Explosion # I want to get this out of here...

X = 0
Y = 1

################################################################################
# ALL ENTITIES THAT MOVE
# Classes in File:
# Boat
# Plane
            
#===============================================================================
class Boat(object):   # 20,50 gun turret
                       # 20, 145 gun turret (180 boat)
    name = 'boat'
    FIRE_RATE = 30
    
    #___________________________________________________________________________
    def __init__(self, screen, player, speed=5, bullet_speed=5):
        self.screen         = screen
        self.bullets        = []
        self.speed          = speed
        self.bullet_speed   = (0, bullet_speed)
        self.gun_location   = Vector(20, 109)
        self.target         = player.location
        self.damage         = 10
        self.health         = 5
        self.is_alive       = True
        self.fire_rate      = self.FIRE_RATE
        
        self.images = [get_image(self.name, 0),
                       get_image(self.name, 1)]
                       
        self.image = self.images[0]
        
        self.frame = 0
        self.delay = 5
        
        # for now we duplicate functionality from the original
        self.img_x, self.img_y = get_image(self.name, 0).get_size()
        self.max_x, self.max_y  = screen.get_size()
        self.location = Vector(self.max_x/2 - self.img_x/2, 
                               self.max_y/2 - self.img_y/2)
        
        # Turret directions
        self.directions = {
            'south'         : get_image('turret', 0),
            'south-east'    : get_image('turret', 1),
            'east'          : get_image('turret', 2),
            'north-east'    : get_image('turret', 3),
            'north'         : get_image('turret', 4),
            'north-west'    : get_image('turret', 5),
            'west'          : get_image('turret', 6),
            'south-west'    : get_image('turret', 7)
        }
        
        
        self.turret = get_image('turret', 0)
        self.turret_location = Vector(self.location.x + 11, self.location.y + 35)
                               
        self.explosion = None
    #___________________________________________________________________________    
    def explode(self):
        self.explosion = Explosion(self.screen,
                              self.get_center(),
                              max_power = 100,
                              max_radius = 200)
        self.explosion.build(250)
        
    #___________________________________________________________________________    
    def get_rect(self):
        return pyg.Rect(self.location.x, 
                        self.location.y, 
                        self.img_x, 
                        self.img_y)
    
    #___________________________________________________________________________
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.is_alive = False
    
    #___________________________________________________________________________
    def is_collision(self, rect):
        for b in self.bullets:
            if rect.collidepoint((b.location.x, b.location.y)):
                self.bullets.remove(b)
                return True
    
    #___________________________________________________________________________
    def get_center(self):
        return (self.location.x + self.gun_location.x,
                self.location.y + self.gun_location.y)
    
    #___________________________________________________________________________    
    def update(self):
        self.delay -= 1
        if self.delay < 0:
            self.delay = 5
            self.frame = 1 - self.frame
            self.image = self.images[self.frame]
        
        self.fire_rate -= 1
                
        deg, rad = self.turret_location.get_angle(self.target)
        
        if 337.5 <= deg or deg < 22.5:
            self.turret = self.directions['east']
        elif 22.5 <= deg < 67.5:
            self.turret = self.directions['north-east']
        elif 67.5 <= deg < 112.5:
            self.turret = self.directions['north']
        elif 112.5 <= deg < 157.5:
            self.turret = self.directions['north-west']
        elif 157.5 <= deg < 202.5:
            self.turret = self.directions['west']
        elif 202.5 <= deg < 247.5:
            self.turret = self.directions['south-west']
        elif 247.5 <= deg < 292.5:
            self.turret = self.directions['south']
        elif 292.5 <= deg < 337.5:
            self.turret = self.directions['south-east']
        else:
            print('ERROR: %r' % deg)
         
    
        # our boat handles its own bullets now.
        # first fire, then update.
        self.fire()
        # update all bullets.
        for b in self.bullets:
            b.update()
            if b.alive == False:
                self.bullets.remove(b)
    
    #___________________________________________________________________________
    def fire(self):
        if self.fire_rate > 0 or self.is_alive == False:
            return
            
        gun = self.get_center()
        if gun[Y] > self.target[Y]:
            return
    
        # get a random float:
        #chance = random.random()
        # we only fire 8% of the time
        #if chance <= .08:
        if abs(self.target[X] - self.location[X]) <= 50:
            # get a random float:
            chance = random.random()
            if chance > .20:
                return
            
            # find the gun
            #gun = self.get_center()
            # create the bullet
            bullet = Bullet(self.screen, # we'll get rid of screen on this soon
                            gun, 
                            1,                 # little pea shooter radius
                            0,
                            self.bullet_speed) # speed is negative so it adds.
            
            # add bullet to collection
            self.bullets.append(bullet)
            # now it exists and we wait for update to be called.
            self.fire_rate = self.FIRE_RATE
            
    #___________________________________________________________________________
    def display(self):
        if not self.is_alive:
            if not self.explosion:
                self.explode()
            self.explosion.update()
            self.explosion.display()
        else:
            self.screen.blit(self.image, (self.location.x, self.location.y))
        
        self.screen.blit(self.turret, (self.turret_location.x, self.turret_location.y))
                         
        # now draw all bullets and they will be on top of the boat.
        for b in self.bullets:
            b.display()

#===============================================================================
"""
 (-1,-1),(0,-1),(1,-1)

        NW N NE
          \|/
(-1,0)  W--*--E  (1,0)
          /|\
        SW S SE
        
  (-1,1),(0,1),(1,1)
"""

NORTH = 7
EAST  = 5
SOUTH = 3
WEST  = 9
NE    = 6
NW    = 8
SE    = 4
SW    = 10

FLYING = 0
FLIPPING = 1
FLIPPED = 2

class Plane(object):
    names = ['olive-plane','white-plane','green-plane',
             'blue-plane'#,'orange-plane' (he doesn't flip)
    ]
    name = 'olive-plane'
    FIRE_RATE = 10
    
    #___________________________________________________________________________
    def __init__(self, screen, location, player, speed=1, bullet_speed=5):
        self.name = random.choice(self.names)
        self.screen         = screen
        self.bullets        = []
        self.speed          = speed
        self.bullet_speed   = (0, bullet_speed)
        self.target         = player
        self.damage         = 10
        self.health         = random.randint(1,3)
        self.is_alive       = False
        self.fire_rate      = self.FIRE_RATE
        self.points         = 15
        self.is_offscreen   = False
        
        self.boundaries = self.screen.get_rect()
        
        self.image = get_image(self.name, 0)
        
        self.img_x, self.img_y = get_image(self.name, 0).get_size()
        self.max_x, self.max_y  = screen.get_size()
        self.location = Vector(location.x, location.y - self.img_y)
        
        self.directions = {
            (0, 0)  : self.image,
            (-1,-1) : get_image(self.name, NW),
            (0,-1)  : get_image(self.name, NORTH),
            (1,-1)  : get_image(self.name, NE),
            (-1,0)  : get_image(self.name, WEST),
            (1,0)   : get_image(self.name, EAST),
            (-1,1)  : get_image(self.name, SW),
            (0,1)   : get_image(self.name, SOUTH),
            (1,1)   : get_image(self.name, SE)
        }
        
        self.flips = [get_image(self.name, 11),
                      get_image(self.name, 12),
                      get_image(self.name, 13),
                      get_image(self.name, 14),
                      get_image(self.name, 15)]
        
        self.upside_down = [get_image(self.name, 16),
                            get_image(self.name, 17)]
        
        self.state = FLYING
        self.flip_frame = 0
        self.upside_down_frame = 0
        self.gun_location = Vector(self.img_x/2, self.img_y)
        self.explosion = None
    
    #___________________________________________________________________________
    def get_rect(self):
        return pyg.Rect(self.location.x, 
                        self.location.y, 
                        self.img_x, 
                        self.img_y)

    #___________________________________________________________________________
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.is_alive = False
    
    #___________________________________________________________________________
    def is_collision(self, rect):
        for b in self.bullets:
            if rect.collidepoint((b.location.x, b.location.y)):
                self.bullets.remove(b)
                return True
    
    #___________________________________________________________________________
    def get_center(self):
        return (self.location.x + self.gun_location.x,
                self.location.y + self.gun_location.y)
    
    #___________________________________________________________________________    
    def update(self):
        
        if self.state is FLIPPING:
            if self.flip_frame == len(self.flips) - 1:
                self.state = FLIPPED
            else:
                self.image = self.flips[self.flip_frame]
                self.flip_frame += 1
        elif self.state is FLIPPED:
            self.upside_down_frame = 1 - self.upside_down_frame
            self.image = self.upside_down[self.upside_down_frame]
            self.location.y -= self.speed
        else:
            self.fire_rate -= 1
            # change position by speed:
            self.location.add(Vector(0, self.speed))
            
            if self.boundaries.collidepoint((self.location.x, self.location.y)):
                self.is_alive = True
            
            if not self.boundaries.collidepoint((self.location.x, self.location.y)) and \
               self.is_alive == True:
            #if self.location.y > self.max_y + self.img_y:
                self.is_alive = False
                self.is_offscreen = True
            
            if self.location.y > self.max_y/2:
                self.state = FLIPPING
        
        # our plane handles its own bullets now.
        # first fire, then update.
        self.fire()
        # update all bullets.
        for b in self.bullets:
            b.update()
            if b.alive == False:
                self.bullets.remove(b)
    
    #___________________________________________________________________________
    def fire(self):
        if self.fire_rate > 0 or self.is_alive == False or \
           self.location.y > self.target.location.y:
            return
    
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
                            0,
                            self.bullet_speed) # speed is negative so it adds.
            # add bullet to collection
            self.bullets.append(bullet)
            # now it exists and we wait for update to be called.
            self.fire_rate = self.FIRE_RATE
            
    #___________________________________________________________________________              
    def display(self):
        if not self.is_offscreen:
            if not self.is_alive and self.health <= 0:
                if not self.explosion:
                    self.explode()
                self.explosion.update()
                self.explosion.display()
                
            else:
                self.screen.blit(self.image, (self.location.x, self.location.y))
        else:
            self.is_alive = False
        
        # now draw all bullets
        for b in self.bullets:
            b.display()
            
#===============================================================================
class BigPlane(object):
    name = 'big-plane'

    def __init__(self, screen, location):
        self.location = Vector(location[X], location[Y])
        self.screen = screen
        self.speed = 1
        self.image = get_image(self.name, 0)
        
        self.stop_y = self.screen.get_height() / 4 - 20
        
    def update(self):
        if self.location.y <= self.stop_y:
            self.location.x -= self.speed
        else:
            self.location.y -= self.speed
    
    def display(self):
        self.screen.blit(self.image, (self.location.x, self.location.y))
    

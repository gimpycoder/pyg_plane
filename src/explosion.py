import pygame as pyg
import math
from vector import Vector
import random

class Particle(object):

    def __init__(self, location, power, max_radius=10):
        self.location       = location
        self.power          = power
        self.max_radius     = max_radius
        self.radius         = 0
        self.is_exploding   = True
        self.is_shrinking   = False
        self.is_dead        = False
        
    def update(self):
        # let's get rid of them first.
        if self.is_dead:
            return
        
        if self.is_shrinking:
            # time to kill this one because it cannot shrink any further.
            if self.radius == 0 or self.radius - self.power < 0:
                self.radius  = 0
                self.is_dead = True
                return
            else:
                self.radius -= self.power
                return
                
        elif self.is_exploding:
            # time to start this one shrinking
            if self.radius >= self.max_radius \
            or self.radius + self.power > self.max_radius:
                self.is_exploding = False
                self.is_shrinking = True
                return
            else:
                self.radius += self.power

class Explosion(object):
    colors = [pyg.color.Color("red"), 
              pyg.color.Color("orange"), 
              pyg.color.Color("yellow"), 
              pyg.color.Color("grey")]

    def __init__(self, screen, location, max_power, max_radius=100):
        self.screen       = screen
        self.location     = location.get_copy()
        self.max_power    = max_power
        self.max_radius   = max_radius
        self.circles = []
        
        self.is_alive = True
    
    def build(self, particle_count):
        for i in xrange(particle_count):
            self.circles.append(self.generate_circle())    
        
    def generate_circle(self):
        # first get a random power between 1 and whatever was maximum.
        power = random.randint(1,self.max_power)
        # now create a radius between power and our maximum.
        radius = random.randint(power, self.max_radius)
        # now create a randomized x,y coordinate unit vector.
        dx = random.randint(-1,1)
        dy = random.randint(-1,1)
        # generate a random magnitude to grow our unit vector by.
        mag = random.randint(-100,30)
        # create that actual vector from our random generation.
        movement = Vector(dx,dy)
        # scale our vector by our random magnitude.
        movement.mul(mag)
        # get a copy of the current location (we don't want to change it)
        location = self.location.get_copy()
        # add the movement to our location so our new location is offset from
        # this explosion's location by the magnitude of our vector.
        location.add(movement)
        # debug printing (fine-tuning particles is hard work!)
        print "power=%r, radius=%r" % (power, radius)
        print 'dx=%d,dy=%d' % (dx,dy)
        print 'center=%s, particle=%s' % (self.location, location)
        print 'movement=%s' % movement
        # create our particle with this configuration and return it.
        return Particle(location, power, radius)
        
    def update(self):
        if not self.is_alive:
            return
    
        corpses = 0
        for circle in self.circles:
            if circle.is_dead:
                corpses += 1
                continue
            else:
                circle.update()
                
        if corpses == len(self.circles):
            self.is_alive = False
            #print 'dead explosion'
        
    def display(self):
        if self.is_alive:
            for circle in self.circles:
                if not circle.is_dead:
                    color_choice = random.randint(0,len(self.colors)-1)
                    pyg.draw.circle(self.screen, 
                        self.colors[color_choice], 
                        (int(circle.location.x), int(circle.location.y)), 
                        circle.radius, 
                        0)

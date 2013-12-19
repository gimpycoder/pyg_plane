import random, math
import pygame as pyg
from utility import *
from particles import Explosion # I want to get this out of here...
################################################################################
# ALL ENTITIES THAT MOVE
# Classes in File:
# Bullet (Does not inherit from Vehicle)
# Vehicle (Superclass - Should be replaced by pygame's Sprite in future)
# Player
# Boat
# Plane
# PowerUp

################################################################################
class Bullet(object):
    def __init__(self, screen, location, radius, speed=5, color=(255,255,255)):
        self.screen = screen
        self.location = location
        self.radius = radius
        self.speed = speed
        self.color = color
        self.alive = True
        
    def update(self):
        # we only change the Y component.
        self.location.y -= self.speed
        self.check_boundaries()
    
    def check_boundaries(self):
        # this just makes refering to them shorter.
        x = self.location.x
        y = self.location.y
        # get our x,y boundaries by unpacking get_size()
        right, bottom = self.screen.get_size()
        
        # our boundaries start at 0,0 of the image so we have to
        # offset where we are checking by the width of the image.
        if x > right or x < 0 or y > bottom or y < 0:
            self.alive = False
            
        # update the position with x,y values.
        self.location.x = x
        self.location.y = y
        
    def display(self):
        if self.alive:
            pyg.draw.circle(self.screen, 
                            self.color, 
                            (int(self.location.x), int(self.location.y)), 
                            self.radius, 
                            0) # 0 fills in the circle
                            
################################################################################

# This is pretty much the container for artwork tied to the mobiles in the game
# When I switch over to subclassing Sprite, this will be useless.

class Vehicle(object):

    #---------------------------------------------------------------------------
    # TODO: Let __init__ receive 2-tuple instead of existing Vector object.
    def __init__(self, name, location):
        """
        name     = The name of this vehicle based on assets
        location = Vector of initial position
        
        """
        
        self.name               = name
        self.location           = location
        self.frame_count        = get_frame_count(self.name)
        self.frame_delay        = FRAME_DELAY
        self.frame              = 0
    
    #---------------------------------------------------------------------------
    # This is for the 'idle' animation. IF more complex animations are needed,
    # then this should be paused (future work)
    def flip(self):
        if self.frame >= len(assets[self.name])-1:
            self.frame = 0
        else:
            self.frame += 1
    
    #---------------------------------------------------------------------------
    # Flip the 'idle' animation and blit the sprite for given frame.    
    def display(self):
        self.frame_delay -= 1
        if self.frame_delay <= 0:
            self.flip()
            self.frame_delay = FRAME_DELAY
        
        img = get_image(self.name, self.frame)    
        self.screen.blit(img, (self.location.x, self.location.y))
        
################################################################################
        
# Represents the human player on screen.
# Can be in various states:
#   - Alive: Health is greater than zero and has not exploded
#   - Dying: Health is zero and have not exploded yet
#   - Dead:  Health is zero and have exploded
#
# Maintains knowledge of self:
#   - Location: Cartesian plot with upper left corner 0,0.
#   - Speed: Amount of translation performed per update in pixels.
#   - Bullets: Collection of Bullet objects that have been fired.
#   - Explosion: Particle container for an explosion.
#   - Max Bullets: Max number of bullets allowed in Bullets collection
#   - cooldown: rate of fire for player's gun. Each update decrement 1
#
# Can do various things:
#   - Flip the animation image based on the frame (DOESNT BELONG HERE!)
#   - Create an explosion (Allows granular creation for player vs enemies)
#   - Fire gun IF cooldown rate accepted AND max bullets not met.
#   - Create bullets IF can fire gun.
#
# Should not do various things:
#   - Bound check against screen (This is main world responsibility)
#   - Check collisions against enemy bullets. (Not Player's job)
#   - Create explosions - just store desired explosion config here.
#       World: "How would you like your explosion?"
#       Player: "Like this..."
#       Player: "Can I see?"
#       World: "Nope"
#       Player: "Can I be notified when it's over?"
#       World: "You don't exist anymore."
#           AND that is why PLAYER does no STORE its own SCORE,HEALTH, etc.
#
# Player exists for ONE LIFE. After that, new instance. Who cares...

# TODO: Implement the explosion again - twas broken and now it's gone.

class Player(Vehicle):
    # used for retrieving the sprite. might get rid of this and just pass in
    # the sprite collection
    name = 'player'

    #---------------------------------------------------------------------------
    # The player does not have a cool-down because firing is tied to KEYDOWN
    # which means the player has to pump it.
    def __init__(self, screen, location, speed=5):
        """
        screen = The Surface object to draw on during Display()
        location = 2-tuple (x,y) of where the player starts.
        speed = rate of change per Update() in game loop.
        """
        
        # I want to inherit from pygame Sprite in future.
        super(Player, self).__init__(self.name, Vector(0,0))
        
        self.screen = screen
        self.speed = speed
        
        # I'm storing it this way so I can do the operations on it as a whole.
        # I'm thinking of not doing it this way.
        # TODO: Ponder not using this...
        self.location = Vector(location[0],location[1])
        self.img_x, self.img_y = get_image(self.name, 0).get_size()
        self.bullets = []
        self.bullet_speed = 5
    
    #---------------------------------------------------------------------------
    # Here is where bullets are added to the collection. The bullets start at
    # the center top of the player image.    
    def fire(self):
        gun = self.get_center()
        gun.y = self.location.y
        # create the bullet
        bullet = Bullet(self.screen, # we'll get rid of screen on this soon
                            gun, 
                            1,                 # little pea shooter radius
                            self.bullet_speed, # speed is positive.
                            (255,255,255))
        self.bullets.append(bullet)
    
    #---------------------------------------------------------------------------
    # Since the player has a collection of their own bullets (which I think is
    # the wrong choice in retrospect), we pass in a rect to see if collidepoint
    # is true and if so, remove the bullet.
    def is_collision(self, rect):
        """
        rect = pygame's Rect object but we turn it into a rect anyway so that
        we can accept the 4-tuple as well.
        """
        rect = Rect(rect)
        for b in self.bullets:
            if rect.collidepoint((b.location.x, b.location.y)):
                self.bullets.remove(b)
                return True
    
    #---------------------------------------------------------------------------
    # If I inherit from Sprite in the future, this will be a useless method.
    # For now, I need a way to get the rect since player loads its own image.
    # I plan to move almost all logic out of player and put it in the main
    # code. 
    def get_rect(self):
        return pyg.Rect(self.location.x, self.location.y, self.img_x, self.img_y)
    
    #---------------------------------------------------------------------------
    # This is how we find out where the bullets start at. We have to know the
    # player's location and then offset it by the player's sprite so it comes
    # out of the middle...
    # When implementing new guns, this will have to become more sophisticated
    # because there might not be full-center aligned guns. For now, it's quite
    # sufficient.
    def get_center(self):
        location = self.location.get_copy()
        x,y = (self.img_x/2, self.img_y/2)
        location.add(Vector(x,y))
        return location
    
    #---------------------------------------------------------------------------
    # If I inherit from Sprite in the future, this will be called automatically
    # through the RenderUpdate() group's update() method.
    def update(self, movement):
        movement.mul(self.speed)
        self.location.add(movement)
        
        # update all bullets:
        for b in self.bullets:
            b.update()
            if b.alive == False:
                self.bullets.remove(b)
                
    #---------------------------------------------------------------------------    
    def display(self):
        super(Player, self).display()
        
        for b in self.bullets:
            b.display()
            
################################################################################
class Boat(Vehicle):
    name = 'boat'
    FIRE_RATE = 30
    def __init__(self, screen, player, speed=5, bullet_speed=-5):
        super(Boat, self).__init__(self.name, Vector(0,0))
        self.screen         = screen
        self.bullets        = []
        self.speed          = speed
        self.bullet_speed   = bullet_speed
        self.gun_location   = Vector(20, 109)
        self.target         = player
        self.damage         = 10
        self.health         = 5
        self.is_alive       = True
        self.fire_rate      = self.FIRE_RATE
        
        # for now we duplicate functionality from the original
        self.img_x, self.img_y = get_image(self.name, 0).get_size()
        self.max_x, self.max_y  = screen.get_size()
        self.location = Vector(self.max_x/2 - self.img_x/2, 
                               self.max_y/2 - self.img_y/2)
                               
        self.explosion = None
        
    def explode(self):
        self.explosion = Explosion(self.screen,
                              self.get_center(),
                              max_power = 100,
                              max_radius = 200)
        self.explosion.build(250)
        
        
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
        self.fire_rate -= 1
    
        # our boat handles its own bullets now.
        # first fire, then update.
        self.fire()
        # update all bullets.
        for b in self.bullets:
            b.update()
            if b.alive == False:
                self.bullets.remove(b)
                #print 'boat bullet removed'
            
            
        # now we check boundaries and remove what left the area.
        #self.check_boundaries()
    
    def fire(self):
        if self.fire_rate > 0 or self.is_alive == False:
            return
            
        gun = self.get_center()
        if gun.y > self.target.location.y:
            return
    
        # get a random float:
        #chance = random.random()
        # we only fire 8% of the time
        #if chance <= .08:
        if abs(self.target.location.x - self.location.x) <= 50:
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
                            self.bullet_speed, # speed is negative so it adds.
                            (255,255,255))
            # add bullet to collection
            self.bullets.append(bullet)
            # now it exists and we wait for update to be called.
            self.fire_rate = self.FIRE_RATE
            
    #def check_boundaries(self):
    #    for b in self.bullets:
    #        if b.location.y >= self.max_y:
    #            self.bullets.remove(b)
    
    def flip(self):
        self.frame = 1 if (self.frame == 0) else 0
        
    def display(self):
        #print 'boat exists'
        if not self.is_alive:
            if not self.explosion:
                self.explode()
            self.explosion.update()
            self.explosion.display()
        else:
            super(Boat, self).display()
        
                         
        # now draw all bullets and they will be on top of the boat.
        for b in self.bullets:
            b.display()

################################################################################
class Plane(Vehicle):
    name = 'plane'
    FIRE_RATE = 10
    def __init__(self, screen, location, player, speed=1, bullet_speed=-5):
        super(Plane, self).__init__(self.name, Vector(0,0))
        self.screen         = screen
        self.bullets        = []
        self.speed          = speed
        self.bullet_speed   = bullet_speed
        self.target         = player
        self.damage         = 10
        self.health         = random.randint(1,3)
        self.is_alive       = True
        self.fire_rate      = self.FIRE_RATE
        self.points         = 15
        self.is_offscreen   = False
        
        self.img_x, self.img_y = get_image(self.name, 0).get_size()
        self.max_x, self.max_y  = screen.get_size()
        self.location = location
    
        # bottom of the graphic:
        self.gun_location = Vector(self.img_x/2, self.img_y)
    
        self.explosion = None
    
    def get_rect(self):
        return pyg.Rect(self.location.x, 
                        self.location.y, 
                        self.img_x, 
                        self.img_y)
    
    """
    def explode(self):
        self.explosion = Explosion(self.screen,
                              self.get_center(),
                              max_power = 15,
                              max_radius = self.img_x)
        self.explosion.build(100)
    """
    
    def explode(self):
        self.explosion = Explosion(self.screen,
                              self.get_center(),
                              max_power = 100,#self.img_x/2,
                              max_radius = 200)#self.img_x*4)
        self.explosion.build(300)
    
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
        self.fire_rate -= 1
        # change position by speed:
        self.location.add(Vector(0, self.speed))
        
        if self.location.y > self.max_y + self.img_y:
            self.is_alive = False
            self.is_offscreen = True
        
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
                            self.bullet_speed, # speed is negative so it adds.
                            (255,255,255))
            # add bullet to collection
            self.bullets.append(bullet)
            # now it exists and we wait for update to be called.
            self.fire_rate = self.FIRE_RATE
    
    def flip(self):
        # no animations yet so we just pass
        pass
        #self.frame = 1 if (self.frame == 0) else 0
        
    def display(self):
        if not self.is_offscreen:
            if not self.is_alive and self.health <= 0:
                if not self.explosion:
                    self.explode()
                self.explosion.update()
                self.explosion.display()
            else:
                super(Plane, self).display()
        else:
            self.is_alive = False
        
        # now draw all bullets
        for b in self.bullets:
            b.display()
            
################################################################################
class PowerUp(Vehicle):
    name = 'power_up'

    def __init__(self, screen, location):
        """
        name     = The name of this vehicle based on assets
        location = Vector of initial position
        
        """
        super(PowerUp, self).__init__(self.name, location)
        self.screen             = screen
        self.location           = location
        self.speed              = 5
        self.frame_count        = get_frame_count(self.name)
        self.frame_delay        = FRAME_DELAY
        self.frame              = 0
        self.wait_time          = FRAME_DELAY
    
    def update(self):
        # we'll just make it go from left to right straight line for now.
        if self.wait_time == 0:
            self.location.x += self.speed
            self.wait_time = FRAME_DELAY
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
            self.frame_delay = FRAME_DELAY
        
        img = get_image(self.name, self.frame)    
        self.screen.blit(img, (self.location.x, self.location.y))
        
    def __str__(self):
        return "%s: %r - frames=%d" % (self.name, self.location, self.frame_count)   

import pygame as pyg
from utility import *
from particles import Explosion, Bullet

X = 0
Y = 1

#===============================================================================
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
#   - Create explosions - just store desired explosion config here
#
# Player exists for ONE LIFE. After that, new instance. Who cares...

# TODO: Implement the explosion again - twas broken and now it's gone.
WINGMAN = 'wingman-powerup'
WEAPON  = 'power_up'
class Player(object):
    # used for retrieving the sprite. might get rid of this and just pass in
    # the sprite collection
    name = 'player'

    (INVINCIBLE, ACTIVE, EXPLODING) = range(3)

    #___________________________________________________________________________
    # The player does not have a cool-down because firing is tied to KEYDOWN
    # which means the player has to pump it.
    def __init__(self, screen, location, speed=5, power=0):
        """
        screen = The Surface object to draw on during Display()
        location = 2-tuple (x,y) of where the player starts.
        speed = rate of change per Update() in game loop.
        power = the gun's current power level from 0 to 3
        """
                
        self.screen = screen
        self.speed = speed
        
        # I'm storing it this way so I can do the operations on it as a whole.
        # I'm thinking of not doing it this way.
        # TODO: Ponder not using this...
        self.location = Vector(location[X],location[Y])
        self.img_x, self.img_y = get_image(self.name, 0).get_size()
        self.bullets = []
        self.bullet_speed = (0, -5)
        self.power = power
        
        self.image = get_image(self.name, 0)
        
        self.wingmen = Wingmen(screen, location, self.image.get_rect())
        
        self.state = Player.ACTIVE
        
        self.explosion = None
        
        self.complete = False
    
    def take_damage(self, amount):
        if self.wingmen.deactivate() == False:
            self.health -= amount
            print(self.health)
    
    
    def activate_powerup(self, powerup_name):
        if powerup_name == WINGMAN:
            self.wingmen.activate()
            # increment score here...
            print("SCORE + 100")
        elif powerup_name == WEAPON:
            self.power = self.power + 1 if self.power < 3 else 3
            print("WEAPON UPGRADE")
            
    #___________________________________________________________________________
    # Here is where bullets are added to the collection. The bullets start at
    # the center top of the player image.    
    def fire(self):
        if self.state == Player.EXPLODING:
            return
    
        gun = list(self.get_center())
        gun[Y] = self.location.y
        
        # create the bullet
        bullet = Bullet(self.screen, # we'll get rid of screen on this soon
                            gun, 
                            1,                 # little pea shooter radius
                            self.power,
                            self.bullet_speed) # speed is positive.
                            
        self.bullets.append(bullet)
        
        if Wingmen.L_ACTIVE:
            print('Left Wingman Bullet Added')      
            bullet = Bullet(self.screen, # we'll get rid of screen on this soon
                            (0,0), 
                            1,                 # little pea shooter radius
                            self.power,
                            self.bullet_speed) # speed is positive.
            
            gun_x, gun_y = self.wingmen.L_gun(bullet.get_rect())
            bullet.location.add(Vector(gun_x, gun_y))            
            self.bullets.append(bullet)
        
        
        if Wingmen.R_ACTIVE:
            print('Right Wingman Bullet Added')
            bullet = Bullet(self.screen, # we'll get rid of screen on this soon
                            (0,0), 
                            1,                 # little pea shooter radius
                            self.power,
                            self.bullet_speed) # speed is positive.
                            
            gun_x, gun_y = self.wingmen.R_gun(bullet.get_rect())
            bullet.location.add(Vector(gun_x, gun_y))
            self.bullets.append(bullet)
    
    #___________________________________________________________________________
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
    
    #___________________________________________________________________________
    # If I inherit from Sprite in the future, this will be a useless method.
    # For now, I need a way to get the rect since player loads its own image.
    # I plan to move almost all logic out of player and put it in the main
    # code. 
    def get_rect(self):
        return pyg.Rect(self.location.x, self.location.y, self.img_x, self.img_y)
    
    #___________________________________________________________________________
    # This is how we find out where the bullets start at. We have to know the
    # player's location and then offset it by the player's sprite so it comes
    # out of the middle...
    # When implementing new guns, this will have to become more sophisticated
    # because there might not be full-center aligned guns. For now, it's quite
    # sufficient.
    def get_center(self):
        location = self.location.get_copy()
        b_x, b_y = get_image('bullet', self.power).get_size()
        x,y = (self.img_x/2-b_x/2, self.img_y/2)
        location.add(Vector(x,y))
        return (location.x, location.y)
    
    #___________________________________________________________________________
    def update(self):
        for b in self.bullets:
            b.update()
            if b.alive == False:
                self.bullets.remove(b)
    
        if self.state == Player.EXPLODING:
            if self.explosion == None:
                self.explosion = ExplodingPlayer(self.screen, 
                                                 self.location.get_tuple(), 
                                                 32, 50)
            self.explosion.update()
            if self.explosion.complete == True:
                self.complete = True
            return

        key = pyg.key.get_pressed()
        move = Vector(0,0)

        if key[K_LEFT]:
            move.x -= 1
        if key[K_RIGHT]:
            move.x += 1
        if key[K_UP]:
            move.y -= 1
        if key[K_DOWN]:
            move.y += 1
    
        move.mul(self.speed)
        self.location.add(move)
        self.wingmen.update((move.x, move.y))
                
    #___________________________________________________________________________    
    def display(self):
        if self.state == Player.EXPLODING:
            self.explosion.display()
        else:
            self.screen.blit(self.image, (self.location.x, self.location.y))
            self.wingmen.display()
        
        for b in self.bullets:
            b.display()
            
#===============================================================================
class ExplodingPlayer(object):
    name = 'ExplodingPlayer'

    #---------------------------------------------------------------------------
    def __init__(self, screen, location, power, max_radius):
        self.screen = screen
        self.location = location
        self.explosion = Explosion(self.screen, 
                                   location, 
                                   power, max_radius)
        self.explosion.build(100)
    
        self.complete = False
        
        #http://soundbible.com/1986-Bomb-Exploding.html
        self.sound = pyg.mixer.Sound("data/audio/sfx/explosion.wav")
        self.sound.play() #Where does the sound go in code?
    
    #---------------------------------------------------------------------------    
    def update(self):
        if self.explosion.is_alive == True:
            self.explosion.update()
        else:
            self.complete = True
            self.sound.stop()
    
    #---------------------------------------------------------------------------    
    def display(self):
        self.explosion.display()            
#===============================================================================
class Wingmen(object):
    name = 'wingman'
    L_ACTIVE = False
    R_ACTIVE = False

    #---------------------------------------------------------------------------
    def __init__(self, screen, player_location, player_rect):
        self.L = self.R = get_image(self.name, 0)
        self.L_rect = self.L.get_rect()
        self.R_rect = self.R.get_rect()
        
        self.screen = screen
        self.player_location = list(player_location)
        self.player_rect = player_rect
        
        self.L_location = [self.player_location[X] - self.L.get_size()[X], 
                           self.player_location[Y] + player_rect.centery]
                             
        self.R_location = [self.player_location[X] + player_rect.right,
                           self.player_location[Y] + player_rect.centery]
    
    def L_gun(self, bullet_rect):
        return [self.L_location[X] + self.L_rect.centerx - bullet_rect.centerx,
                self.L_location[Y]]
                
    def R_gun(self, bullet_rect):
        return [self.R_location[X] + self.R_rect.centerx - bullet_rect.centerx,
                self.R_location[Y]]
    
    def activate(self):
        if Wingmen.L_ACTIVE == False:
            Wingmen.L_ACTIVE = True
        elif Wingmen.L_ACTIVE == True and Wingmen.R_ACTIVE == False:
            Wingmen.R_ACTIVE = True
            
    def deactivate(self):
        if Wingmen.R_ACTIVE == True:
            Wingmen.R_ACTIVE = False
            return True
        elif Wingmen.L_ACTIVE == True:
            Wingmen.L_ACTIVE = False
            return True
        
        return False
    
    #---------------------------------------------------------------------------    
    def update(self, movement):
        self.L_location[X] += movement[X]
        self.L_location[Y] += movement[Y]
        
        self.R_location[X] += movement[X]
        self.R_location[Y] += movement[Y]
    
    #---------------------------------------------------------------------------    
    def display(self):
        if Wingmen.L_ACTIVE:
            self.screen.blit(self.L, self.L_location)
        if Wingmen.R_ACTIVE:
            self.screen.blit(self.R, self.R_location)

import random
import pygame
from pygame.locals import *
from hud import Score, HealthBar
from enemies import Boat, Plane, BigPlane
from player import Player
from particles import Explosion
from upgrades import PowerUp
from utility import *

#===============================================================================
FPS = 30
SCORE_BOARD_WIDTH = 120

# pretty indexes
X = 0
Y = 1

#===============================================================================
class WarZone(object):

    #___________________________________________________________________________
    def __init__(self, screen, level=1, lives=3, score=0):
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.screen_center = (self.screen_size[X]/2, self.screen_size[Y]/2)
        
        
        player_size = get_image('player', 0).get_size()
        player_center = (player_size[X]/2, player_size[Y]/2)
        self.start_location = (self.screen_center[X] - player_center[X],
                               self.screen_size[Y] - (player_size[Y] * 2))
        
        
        self.health_bar = HealthBar(screen, (0,0))
        
        
        self.score_center = (self.screen_center[X] - SCORE_BOARD_WIDTH/2, 5)
        self.score  = Score(self.screen, self.score_center)
        
        
        
        self.lives_image = get_image('lives', 0)
        self.lives  = lives
        self.alive  = False

        self.bomb_image = get_image('bomb', 0)
        self.bombs = 3

        self.backgrounds = [get_background((self.screen_size[X], 
                                            self.screen_size[Y] + 32), 
                                            level, 0),
                            get_background((self.screen_size[X], 
                                            self.screen_size[Y] + 32), 
                                            level, 1)
        ]

        self.clock = pygame.time.Clock()
        
        #http://soundbible.com/1986-Bomb-Exploding.html
        self.sound = get_sfx('explosion')
        self.sound.set_volume(0.5)


    #___________________________________________________________________________
    # Currently not operational and quite messy.
    def menu(self):
        
        in_menu = True
        menu = artwork.get_image('title', 1)
        menu_x, menu_y = menu.get_size()
        screen_x, screen_y = self.screen.get_size()
        menu_center = ((screen_x/2 - menu_x/2), (screen_y/2 - menu_y/2) + 100)
        
        waitground = Ground.get_background(self.screen.get_size(), 0, 0)
        
        pointer = (142, 225)
        
        while in_menu:
            self.clock.tick(30)
            
            self.screen.fill((189, 189, 189))
            self.screen.blit(waitground, (0,0))
            self.screen.blit(menu, menu_center)
            self.screen.blit(self.lives_image, pointer)
            pygame.display.flip()
            
    
    #___________________________________________________________________________
    # We enter this when a life has expired or the game is just starting.
    def new_game(self):
        print 'new_game'
        if self.lives > 0:
            self.alive = True
            self.fight()
        else:
            # continue screen maybe?
            print 'quitting'
    
    #___________________________________________________________________________
    # This loop goes on until the player is dead.
    def fight(self):
        
        self.health_bar.full_health()
        player = Player(self.screen,
                       (self.start_location[X], self.start_location[Y]))
        
        kills = 0               
        planes = []
        explosions = []
        powerups = []
    
        fighting = True
        cycle = 0
        wait  = 1 * FPS
        reset = wait
        
        bg_counter = 32
        bg_frame = 0
        bg_wait = 30
        bg_speed = 1
        
        lives_size = self.lives_image.get_size()[0]
        
        while fighting:
            self.clock.tick(FPS)

            # process events from queue
            for e in pygame.event.get():
                if e.type == QUIT:
                    return
                if e.type == KEYDOWN:
                   if e.key  == K_ESCAPE:
                    return
                   elif e.key == K_w:
                    player.activate_powerup("wingman-powerup")
                   elif e.key == K_q:
                    player.power += 1
                    if player.power > 3:
                        player.power = 0
                   elif e.key == K_SPACE:
                    player.fire()
                   elif e.key == K_b:
                    print 'bomb dropped'
                    self.bombs -= 1
                    for p in planes:
                        explosion = self.create_explosion(self.screen, (p.location.x, p.location.y))
                        explosions.append(explosion)
                        planes.remove(p)
                        self.score.increase_score(p.points)
                        kills += 1

            player.update()

            #-------------------------------------------------------------------
            # Change background might be a little overkill because I think it
            # looks kind of bad. For now, it serves as a nice debug loop.
            if wait <= 0:
                chance = random.random()
                if chance < 1.0:
                    x = random.randint(20, 600)
                    planes.append(Plane(self.screen, Vector(x, 0), player))

                bg_frame = 1 - bg_frame
                
                wait = reset              
            
            self.screen.blit(self.backgrounds[bg_frame], (0,0), 
                             (0, bg_counter, 640, 480))
            player.display()

            live_x = 0
            live_y = 0
            
            
            
            for i in xrange(self.lives):
                self.screen.blit(self.lives_image, (live_x + 7,live_y + 20))
                live_x += lives_size
            
            for i in xrange(1, self.bombs + 1):
                self.screen.blit(self.bomb_image, (self.screen_size[X] - 32 * i, self.screen_size[Y] - 32))
                
                
            for plane in planes:
                plane.update()
                
                if plane.is_collision(player.get_rect()):
                    self.health_bar.decrease_health(10)
                    if self.health_bar.is_dead():
                        player.state = Player.EXPLODING
                
                if plane.is_offscreen:
                    planes.remove(plane)
                    continue
                
                rect = plane.get_rect()
                
                
                
                for b in player.bullets:
                    
                    if rect.collidepoint(b.location.x, b.location.y):
                        explosion = self.create_explosion(self.screen, 
                                                         (plane.location.x, 
                                                          plane.location.y))
                        
                        kills += 1
                        print '%d planes destroyed' % kills
                        explosions.append(explosion)
                        player.bullets.remove(b)
                        planes.remove(plane)
                        self.score.increase_score(plane.points)
                        self.sound.play()
                        
                        if kills % 10 == 0:
                            chance = random.random()
                            print '%.2f powerup spawn chance' % chance
                            if chance < 0.75:
                                powerup = PowerUp(self.screen, plane.location.get_tuple())
                                powerups.append(powerup)
                        
                plane.display()
            
            player_rect = player.get_rect()
            for powerup in powerups:
                powerup.update()
                if player_rect.colliderect(powerup.get_rect()):
                    player.activate_powerup(powerup.name)
                    powerups.remove(powerup)
                    continue
                
                powerup.display()
                
            for e in explosions:
                if e.is_alive == False:
                    explosions.remove(e)
                    continue
                e.update()
                e.display()
            
            self.score.display()
            self.health_bar.display()

            pygame.display.flip()
            wait -= 1
            
            if player.complete == True:
                fighting = False
    
            # this controls the animation of the ocean background and the scroll
            bg_speed -= 1
            if bg_speed < 0:            # TODO: change these magic values to
                bg_counter -= 1         # variables.
                bg_speed = 1
                if bg_counter < 0:
                    bg_counter = 32 # 32 is the size of an ocean tile.
    
        # looping while alive
        # then..
        
        
        # these are normally going to be set on a condition of zero health
        self.alive = False
        self.lives -= 1
        self.dead()
    
    #___________________________________________________________________________
    def create_explosion(self, screen, location):
        
        explosion = Explosion(screen,
                              location,
                              max_power = 4,        #4 current # 1
                              max_radius = 15)      #10 current # 15
        explosion.build(100)
        return explosion
    
    
    #___________________________________________________________________________
    # Displayed between lives with a "GET READY" flashing message if there are
    # lives left. Otherwise flashes game over.
    def dead(self):
        message1 = None
        message2 = None
        wait = FPS
        reset = wait
        
        waitground = get_background(self.screen.get_size(), 0, 0)
        print 'lives: %d' % self.lives
        if self.lives > 0:
            message1  = get_image('get_ready', 0)
            message2  = get_image('get_ready', 1)
        else:
            print 'game over'
            message1  = get_image('game_over', 0)
            message2  = get_image('game_over', 1)
        
        # this alternates to cause blinking.
        message = message1
        
        screen_x, screen_y = self.screen.get_size()
        image_x, image_y = message.get_size()
        center = ((screen_x/2 - image_x/2),(screen_y/2 - image_y/2))
            
        
        self.screen.blit(waitground, (0,0))
        
        in_limbo = FPS * 3
        
        while in_limbo > 0:
            self.clock.tick(FPS)
            
            # This flips the "GET READY" image so that it blinks.
            if in_limbo % 10 == 0:
                message = message1 if message == message2 else message2

            self.screen.fill((0, 0, 0))
            self.screen.blit(waitground, (0,0))
            self.screen.blit(message, center)
            pygame.display.flip()
            in_limbo -= 1
        
        if self.lives > 0:
            self.new_game()


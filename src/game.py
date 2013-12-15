import pygame as pyg
from player import Player
from vector import Vector
from bullet import Bullet
from explosion import Explosion
from health import HealthBar
from boat import Boat
from score import Score
from powerup import PowerUp
import artwork
from plane import Plane

class Game(object):
    def main(self,screen):
        # create the timer
        self.screen = screen
        clock = pyg.time.Clock()
        
        
        
        player = Player(screen)
        health = HealthBar(screen, Vector(0,0))
        health.full_health()
        cool_down = 5
        gun_too_hot = False
        player_dead = False
        
        
        wave  = artwork.get_image('wave', 0)
        score_mock = artwork.get_image('score', 0) 
        score  = Score(screen, Vector(70, 33))
        score.init()
        score.value = 0
        
        explosions = []
        
        boat = Boat(screen, player)
        boat_x, boat_y = artwork.get_image('health',0).get_size()
        win_x, win_y = screen.get_size()
       #0,0                  640,0
        # [__197px___]       [__197px___]
        #                    | oops it would draw off screen.
        #     game area      | So, we subtract the size of the image as well.
        #                    |
        boat_health = HealthBar(screen, Vector(win_x - boat_x, 0), (255,0,0))
        boat_health.full_health()
        boat_dead = False
        boat_health.health = 5
        
        plane = Plane(screen, player)
        
        
        
        water = (2, 73, 148)
        water_frame = 0
        water_img = artwork.get_image('water', water_frame)
        water_x, water_y = water_img.get_size()
        
        
        
        # just half way up screen.
        power_up = PowerUp(screen, Vector(0, screen.get_size()[1]/2))
        
        # tie the Player to the method on health bar that checks if they
        # are still alive.
        Player.is_dead = health.is_dead
        print "player=%s, health-bar=%s" % (player.is_dead(), health.is_dead())
        
        # same with boat:
        Boat.is_dead = boat_health.is_dead
        

        while True:
            clock.tick(30)
            
            # process events from queue
            for e in pyg.event.get():
                if e.type == pyg.QUIT:
                    return
                if e.type == pyg.KEYDOWN and \
                   e.key  == pyg.K_ESCAPE:
                    return
            
            
            
            
            # Clear screen and tile background.
            screen.fill(water)
            for y in xrange(0, 480, water_y):
                for x in xrange(0, 640, water_x):
                    screen.blit(water_img, (x,y))
            
            
            
            
            if gun_too_hot:
                cool_down -= 1
            if cool_down < 0:
                gun_too_hot = False
            
            
            
            
            # get the input key
            key = pyg.key.get_pressed()
            move = Vector(0,0)
            # process the key
            if key[pyg.K_LEFT]:
                move.x -= 1
            if key[pyg.K_RIGHT]:
                move.x += 1
            if key[pyg.K_UP]:
                move.y -= 1
            if key[pyg.K_DOWN]:
                move.y += 1
            if key[pyg.K_SPACE]:
                if not gun_too_hot and not player_dead:
                    player.fire()
                    gun_too_hot = True
                    cool_down   = 5
                    #score.decrease_score(1)
                    
            # self-destruct
            if key[pyg.K_s] and not player.is_dead():
                health.zero_health()
            
            
            
            if not player_dead:    
                if health.is_dead():
                    # add an explosion based on where our player is.
                    location = player.get_center()
                    explosion = self.create_explosion(location)
                    explosions.append(explosion)
                    player_dead = True # for now this is good.
            
            
            
            
                
            # now we update the player's position based on the
            # movement but only if they aren't dead.
            if not player_dead:
                player.update(move)
                if not boat_dead:
                    boat.update()
                    if boat.is_collision(player.get_rect()):
                        health.decrease_health(boat.damage)
            
            
            
            
            if player.is_collision(boat.get_rect()):
                #boat.take_damage(1)
                boat_health.decrease_health(1)
                print 'hit boat for 1 damage. %d remaining.' % boat_health.health
                #if boat.is_alive == False:
                if boat_health.is_dead():
                    explosion = self.create_explosion(boat.location)
                    explosions.append(explosion)
                    boat_dead = True


                
            # always update the explosions
            for explosion in explosions:
                if not explosion.is_alive:
                    explosions.remove(explosion)
                    continue
                                
                explosion.update()



            if not boat_dead:
                boat.display()
            # Display player second so it will
            # draw over top the bullets. 
            # Don't display player if they're dead.
            if not player_dead:
                player.display()
            
            
                    
            # finally display the explosions so they are over
            # top everything.
            for explosion in explosions:
                explosion.display()
            
            plane.update()
            plane.display()
                
            health.display()
            score.display()
            self.screen.blit(score_mock, (5, 33))
            self.screen.blit(wave, (5, 55))
            

            
            power_up.update()
            power_up.display()
            
            boat_health.display()
            
            pyg.display.flip()
            #raw_input('...')
            
    def create_explosion(self, location):
        explosion = Explosion(screen,
                              location,
                              max_power = 100,
                              max_radius = 200)
        explosion.build(250)
        return explosion
        
#################################################################        
if __name__ == '__main__':
    # always have to init pygame first.
    pyg.init()
    # create a screen
    screen = pyg.display.set_mode((640,480))
    # load our artwork
    artwork.init()
    # run game and pass in screen
    Game().main(screen)

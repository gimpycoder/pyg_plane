import pygame as pyg
from player import Player
from vector import Vector
from bullet import Bullet
from explosion import Explosion
from health import HealthBar
from boat import Boat
import artwork

class Game(object):
    def main(self,screen):
        # create the timer
        self.screen = screen
        clock = pyg.time.Clock()
        player = Player(screen)
        boat = Boat(screen)
        health = HealthBar(screen, Vector(0,0))
        health.full_health()
        bullets = []
        explosions = []
        player_dead = False
        cool_down = 5
        gun_too_hot = False

        while True:
            clock.tick(30)
            if gun_too_hot:
                cool_down -= 1
                
            if cool_down < 0:
                gun_too_hot = False
            
            # process events from queue
            for e in pyg.event.get():
                if e.type == pyg.QUIT:
                    return
                if e.type == pyg.KEYDOWN and \
                   e.key  == pyg.K_ESCAPE:
                    return
            
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
                    position = player.get_center()
                    position.y = player.location.y
                    bullets.append(Bullet(screen, 
                                         position, 
                                         radius=1, 
                                         speed=5, 
                                         color=(255,255,255)))
                    gun_too_hot = True
                    cool_down   = 5
                    
            # self-destruct
            if key[pyg.K_s] and not player_dead:
                # add an explosion based on where our player is.
                location = player.get_center()
                explosion = self.create_explosion(location)
                explosions.append(explosion)
                # kill player:
                player_dead = True
            
            
            
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
                boat.update()
                if boat.is_collision(player.get_rect()):
                    player_dead = True
                    health.zero_health()
                    explosions.append(self.create_explosion(player.get_center()))
                
            # always update the bullets
            for b in bullets:
                b.update()
                
            # always update the explosions
            for explosion in explosions:
                if not explosion.is_alive:
                    explosions.remove(explosion)
                    continue
                                
                explosion.update()
            
            # wipe the previous screen with black
            screen.fill((0,0,0))

            # display our bullets first.
            # but we don't want to display anything if it's outside
            # the screen. We will also remove them.
            for b in bullets:
                if b.position.y < 0:
                    bullets.remove(b)
                    print 'bullets: %d' % len(bullets)
                else:
                    b.display()
            
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
            
            health.decrease_health(1)
            #if not health.is_full_health():
            #    health.increase_health(1)
                
            health.display()
            
            # flip the buffer
            pyg.display.flip()
            
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

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

class Game(object):
    def main(self,screen):
        # create the timer
        self.screen = screen
        clock = pyg.time.Clock() 
        player = Player(screen)
        boat = Boat(screen, player)
        health = HealthBar(screen, Vector(0,0))
        health.full_health()
        score  = Score(screen, Vector(70, 33))
        score.init()
        score.value = 0
        bullets = []
        explosions = []
        player_dead = False
        boat_dead = False
        cool_down = 5
        gun_too_hot = False
        water = (2, 73, 148)
        
        # just half way up screen.
        power_up = PowerUp(screen, Vector(0, screen.get_size()[1]/2))
        
        # just mocking game screen for now.
        #numbers = artwork.get_image('numbers',0)
        score_mock = artwork.get_image('score', 0)  
        wave  = artwork.get_image('wave', 0)
        #nums = []
        #for i in xrange(10):
        #    nums.append(artwork.get_image(str(i), 0))

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
                    #position = player.get_center()
                    #position.y = player.location.y
                    player.fire()
                    
                    #bullets.append(Bullet(screen, 
                    #                     position, 
                    #                     radius=1, 
                    #                     speed=5, 
                    #                     color=(255,255,255)))
                    gun_too_hot = True
                    cool_down   = 5
                    #score.decrease_score(1)
                    
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
                if not boat_dead:
                    boat.update()
                    if boat.is_collision(player.get_rect()):
                        health.decrease_health(boat.damage)
            
            if player.is_collision(boat.get_rect()):
                boat.take_damage(1)
                print 'hit boat for 1 damage. %d remaining.' % boat.health
                if boat.is_alive == False:
                    explosion = self.create_explosion(boat.location)
                    explosions.append(explosion)
                    boat_dead = True
                
            # always update the bullets
            #for b in bullets:
            #    b.update()
                
            # always update the explosions
            for explosion in explosions:
                if not explosion.is_alive:
                    explosions.remove(explosion)
                    continue
                                
                explosion.update()
            
            # add water
            screen.fill(water)
            #screen.fill((0,0,0))

            # display our bullets first.
            # but we don't want to display anything if it's outside
            # the screen. We will also remove them.
            #for b in bullets:
            #    if b.position.y < 0:
            #        bullets.remove(b)
            #        print 'bullets: %d' % len(bullets)
            #    else:
            #        b.display()
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
            
            #health.decrease_health(1)
            #if not health.is_full_health():
            #    health.increase_health(1)
                
            health.display()
            #x_ = 200
            #y_ = 20
            #change = 20
            #for i in xrange(10):
            #    self.screen.blit(nums[i], (x_, y_))
            #    y_ += change
            
            score.increase_score(1)
            #key = str(score)[9]
            score.display()
            #self.screen.blit(score.digits[key], (200,20))
            
            #self.screen.blit(numbers, (70, 33))
            self.screen.blit(score_mock, (5, 33))
            self.screen.blit(wave, (5, 55))
            #self.screen.blit(numbers, (70, 55))
            #self.screen.blit(three, (50,200))
            # flip the buffer
            
            power_up.update()
            power_up.display()
            
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

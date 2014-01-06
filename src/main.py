# BUGS:
# 1. Holding UP and LEFT prevents shooting
# 2. Holding DOWN and RIGHT prevents shooting (Same as #1)
# 3. Destroying a plane removes its bullets as well.
# 4. Player bullets stay on screen but do not update location (frozen) on when
#    exploding.

import pygame
from pygame.locals import *
from warzone import WarZone
import utility

#_______________________________________________________________________________
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    utility.init()
    warzone = WarZone(screen,level=1,lives=3)
    warzone.new_game()
    

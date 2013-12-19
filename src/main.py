# tippy top level of logic. it starts and ends here.

import pygame
from pygame.locals import *
from warzone import WarZone
from utility import *

#_______________________________________________________________________________
def debug(*args):
    for arg in args:
        print arg
    raw_input('debug')

#_______________________________________________________________________________
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    init()
    warzone = WarZone(screen,level=1,lives=1)
    #warzone.menu()
    #warzone.dead()
    warzone.new_game()
    

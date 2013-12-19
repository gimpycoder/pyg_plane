import math
import copy
import pygame as pyg
from pygame.locals import *
import random

################################################################################
# CODE NOT DIRECTLY REFLECTED AS OBJECTS IN GAME - HELPERS ETC.
# Classes in File:
# Vector
#
# CONCEPTS in File: (not classes)
# Asset Loading
# Background Building
#===============================================================================
# NOTE: This is really poorly designed.... TODO: drop it or fix.
class Vector(object):
    #___________________________________________________________________________
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    #___________________________________________________________________________    
    def add(self, other): 
        self.x += other.x
        self.y += other.y
    #___________________________________________________________________________    
    def sub(self, other):
        self.x -= other.x
        self.y -= other.y
    #___________________________________________________________________________    
    def mul(self, value):
        self.x *= value
        self.y *= value
    #___________________________________________________________________________    
    def div(self, value):
        if not value == 0:
            self.x /= value
            self.y /= value
    #___________________________________________________________________________        
    def mag(self):
        a = self.x**2.0
        b = self.y**2.0
        c = math.sqrt(a + b)
        return c
    #___________________________________________________________________________    
    def norm(self):
        magnitude = self.mag()
        self.div(magnitude)
    #___________________________________________________________________________    
    def get_copy(self):
        return copy.copy(self)
    #___________________________________________________________________________
    def __str__(self):
        return format("x=%r,y=%r" % (self.x,self.y))
        
################################################################################
# CODE NOT DIRECTLY REFLECTED AS OBJECTS IN GAME - HELPERS ETC.
# CONCEPTS in File:
# Asset Loading
# Background Building
#===============================================================================
WATER = (2, 73, 148)
FRAME_DELAY = 4

image_paths  = {
    'player'            : ['../res/hero_01.png',
                           '../res/hero_02.png', 
                           '../res/hero_03.png'
                          ],
    'boat'              : ['../res/boat_a_01.png',
                           '../res/boat_a_02.png'
                          ],
    'plane'             : ['../res/plane_a_01.png'],
                          
    'health'            : ['../res/health_bar.png'],
    'numbers'           : ['../res/numbers.png'],
    'score'             : ['../res/score_text.png'],
    'wave'              : ['../res/wave_text.png'],
    'power_up'          : ['../res/power_up_01.png',
                           '../res/power_up_02.png'
                          ],
    'water'             : ['../res/water_01.png',
                           '../res/water_02.png'
                          ],
    'title'             : ['../res/title_graphic.png',
                           '../res/title_menu.png',
                           '../res/wings_pointer.png'
                          ],
    'get_ready'         : ['../res/get_ready_01.png',
                           '../res/get_ready_02.png'
                          ],
    'lives'             : ['../res/wings_pointer.png'],
    
    'game_over'         : ['../res/game_over_01.png',
                           '../res/game_over_02.png']
}

assets = {}

#_______________________________________________________________________________
def init():
    assets['player']    = [pyg.image.load(image_paths['player'][0]),
                           pyg.image.load(image_paths['player'][1]),
                           pyg.image.load(image_paths['player'][2])]
                           
    assets['boat']      = [pyg.image.load(image_paths['boat'][0]),
                           pyg.image.load(image_paths['boat'][1])]
    assets['health']    = [pyg.image.load(image_paths['health'][0])]
    assets['numbers']   = [pyg.image.load(image_paths['numbers'][0])]
    assets['score']     = [pyg.image.load(image_paths['score'][0])]
    assets['wave']      = [pyg.image.load(image_paths['wave'][0])]
    assets['power_up']  = [pyg.image.load(image_paths['power_up'][0]),
                           pyg.image.load(image_paths['power_up'][1])]
    assets['water']     = [pyg.image.load(image_paths['water'][0]),
                           pyg.image.load(image_paths['water'][1])]
    assets['plane']     = [pyg.image.load(image_paths['plane'][0])]
    
    # Title screen graphics.
    assets['title']     = [pyg.image.load(image_paths['title'][0]),
                           pyg.image.load(image_paths['title'][1]),
                           pyg.image.load(image_paths['title'][2])]
                           
    assets['get_ready'] = [pyg.image.load(image_paths['get_ready'][0]),
                           pyg.image.load(image_paths['get_ready'][1])]
                           
    assets['lives']     = [pyg.image.load(image_paths['lives'][0])]
    
    assets['game_over'] = [pyg.image.load(image_paths['game_over'][0]),
                           pyg.image.load(image_paths['game_over'][1])]
    
    # .convert() ensures it's the proper pixel format for the game.
    # a few images have black backgrounds so must use a different
    # colorkey for transparency.
    #
    # What this is really doing that's important though is adding a 
    # colorkey to the image based on what it is. Being able to call 
    # convert on it here instead of where it's assigned ^^ is just
    # a nice side-effect.
    black_background = ['health','wave','score','get_ready', 'title', 
                        'game_over'
    ]
    
    for (key,value) in assets.iteritems():
        for i, img in enumerate(assets[key]):
                
            if key in black_background:
                img.set_colorkey((0,0,0))
                
            else:
                img.set_colorkey((2, 73, 148))
                
            assets[key][i] = img.convert()
    
    
    # special handling.
    load_numbers()
    
            
    print 'artwork initialized'

#_______________________________________________________________________________
#TODO: Generalize this so that it will load any slides provided
# need to also include pad value in case we have borders to worry about.
def load_numbers():
    numbers = get_image('numbers',0)
    img_x, img_y = numbers.get_size()
    section = img_x / 10
    offset = 0
    cropper = pyg.Surface((section, img_y)).convert()
    cropper.set_colorkey((0,0,0))
    for i in xrange(10):
        cropper.blit(numbers,
                         (0,0), # start at coordinates for destination.
                         (offset, 0, offset + section, img_y))
        assets[str(i)] = [cropper.copy()]
        offset += section
        #print 'loaded number %d' % i
#_______________________________________________________________________________
def get_number(name):
    return get_image(name, 0)
#_______________________________________________________________________________
def get_image(name, frame):
    #print '%r, %d' % (name,frame)
    return assets[name][frame]
#_______________________________________________________________________________    
def get_frame_count(name):
    return len(assets[name])
    
#_______________________________________________________________________________
def get_background(zone_size, level, frame=0):
    """
    zone_size = 2-tuple dimensions
    level = which level the player is on.
    frame = which frame in the collection is desired.
    """
    
    zone = pyg.Surface(zone_size).convert()
    
    if level == 0:
        image = get_waitground(zone)
        
    elif level == 1:
        zone.fill(WATER)
        image = get_image('water', frame)
     
    if level > 0:
        size_x, size_y = zone.get_size()
        box_x, box_y = image.get_size()
        for y in xrange(0, size_y, box_y):
            for x in xrange(0, size_x, box_x):
                zone.blit(image, (x,y))
                        
    return zone
#_______________________________________________________________________________    
def get_waitground(zone):
    raw_input('waitground')
    size_x, size_y = zone.get_size()
    zone.fill((189,189,189))
    radius = 10
    holes = 30
    valid = zone.get_rect()
    
    while holes > 0:
        rand_x = random.randint(0, size_x)
        rand_y = random.randint(0, size_y)
        
        if valid.collidepoint((rand_x, rand_y)):
            
            pyg.draw.circle(zone,
                           (0,0,0),
                           (rand_x, rand_y),
                           radius,
                           0)
            holes -= 1
        
    return zone

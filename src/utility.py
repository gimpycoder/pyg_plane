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
    # Return 2-tuple (degrees, radians).
    def get_angle(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        r = math.atan2(-dy, dx)
        r %= 2 * math.pi
        deg = math.degrees(r)
        return (deg, r)
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
                          
    'buddy'             : ['../res/buddy.png'],
                          
    'bullet'            : ['../res/bullet_01.png',
                           '../res/bullet_02.png',
                           '../res/bullet_03.png',
                           '../res/bullet_04.png'],
                          
    'boat'              : ['../res/boat_a_01.png',
                           '../res/boat_a_02.png'
                          ],
                          
    'submarine'         : ['../res/submarine/sub_01.png',   # exposed
                           '../res/submarine/sub_02.png',   # submerge 1
                           '../res/submarine/sub_03.png',   # submerge 2
                           '../res/submarine/sub_04.png',   # submerge 3
                           '../res/submarine/sub_05.png',   # submerge 4
                           '../res/submarine/sub_06.png'],  # submerge 5
                          
    'turret'            : ['../res/turret/turret_south.png',
                           '../res/turret/turret_south_east.png',
                           '../res/turret/turret_east.png',
                           '../res/turret/turret_north_east.png',
                           '../res/turret/turret_north.png',
                           '../res/turret/turret_north_west.png',
                           '../res/turret/turret_west.png',
                           '../res/turret/turret_south_west.png'],
    
    'olive-plane'       : ['../res/planes/olive_01.png',
                           '../res/planes/olive_02.png',
                           '../res/planes/olive_03.png',
                           '../res/planes/olive_04.png',   # south
                           '../res/planes/olive_05.png',   # south-east
                           '../res/planes/olive_06.png',   # east
                           '../res/planes/olive_07.png',   # north-east
                           '../res/planes/olive_08.png',   # north
                           '../res/planes/olive_09.png',   # north-west
                           '../res/planes/olive_10.png',   # west
                           '../res/planes/olive_11.png',   # south-west
                           '../res/planes/olive_12.png',   # flip 01
                           '../res/planes/olive_13.png',   # flip 02
                           '../res/planes/olive_14.png',   # flip 03
                           '../res/planes/olive_15.png',   # flip 04
                           '../res/planes/olive_16.png',   # flip 05
                           '../res/planes/olive_17.png',   # upside down 01
                           '../res/planes/olive_18.png'],  # upside down 02
                           
    'white-plane'       : ['../res/planes/white_01.png',
                           '../res/planes/white_02.png',
                           '../res/planes/white_03.png',
                           '../res/planes/white_04.png',   # south
                           '../res/planes/white_05.png',   # south-east
                           '../res/planes/white_06.png',   # east
                           '../res/planes/white_07.png',   # north-east
                           '../res/planes/white_08.png',   # north
                           '../res/planes/white_09.png',   # north-west
                           '../res/planes/white_10.png',   # west
                           '../res/planes/white_11.png',   # south-west
                           '../res/planes/white_12.png',   # flip 01
                           '../res/planes/white_13.png',   # flip 02
                           '../res/planes/white_14.png',   # flip 03
                           '../res/planes/white_15.png',   # flip 04
                           '../res/planes/white_16.png',   # flip 05
                           '../res/planes/white_17.png',   # upside down 01
                           '../res/planes/white_18.png'],  # upside down 02
                           
    'green-plane'       : ['../res/planes/green_01.png',
                           '../res/planes/green_02.png',
                           '../res/planes/green_03.png',
                           '../res/planes/green_04.png',   # south
                           '../res/planes/green_05.png',   # south-east
                           '../res/planes/green_06.png',   # east
                           '../res/planes/green_07.png',   # north-east
                           '../res/planes/green_08.png',   # north
                           '../res/planes/green_09.png',   # north-west
                           '../res/planes/green_10.png',   # west
                           '../res/planes/green_11.png',   # south-west
                           '../res/planes/green_12.png',   # flip 01
                           '../res/planes/green_13.png',   # flip 02
                           '../res/planes/green_14.png',   # flip 03
                           '../res/planes/green_15.png',   # flip 04
                           '../res/planes/green_16.png',   # flip 05
                           '../res/planes/green_17.png',   # upside down 01
                           '../res/planes/green_18.png'],  # upside down 02
                           
    'blue-plane'        : ['../res/planes/blue_01.png',
                           '../res/planes/blue_02.png',
                           '../res/planes/blue_03.png',
                           '../res/planes/blue_04.png',   # south
                           '../res/planes/blue_05.png',   # south-east
                           '../res/planes/blue_06.png',   # east
                           '../res/planes/blue_07.png',   # north-east
                           '../res/planes/blue_08.png',   # north
                           '../res/planes/blue_09.png',   # north-west
                           '../res/planes/blue_10.png',   # west
                           '../res/planes/blue_11.png',   # south-west
                           '../res/planes/blue_12.png',   # flip 01
                           '../res/planes/blue_13.png',   # flip 02
                           '../res/planes/blue_14.png',   # flip 03
                           '../res/planes/blue_15.png',   # flip 04
                           '../res/planes/blue_16.png',   # flip 05
                           '../res/planes/blue_17.png',   # upside down 01
                           '../res/planes/blue_18.png'],  # upside down 02
                           
                           
    'orange-plane'      : ['../res/planes/orange_01.png',
                           '../res/planes/orange_02.png',
                           '../res/planes/orange_03.png',
                           '../res/planes/orange_04.png',  # south
                           '../res/planes/orange_05.png',  # south-east
                           '../res/planes/orange_06.png',  # east
                           '../res/planes/orange_07.png',  # north-east
                           '../res/planes/orange_08.png',  # north
                           '../res/planes/orange_09.png',  # north-west
                           '../res/planes/orange_10.png',  # west
                           '../res/planes/orange_11.png'], # south-west
                                                           # NO FLIP!
                                                           
    'big-plane'         : ['../res/BigPlane.png'],
    
    'bomber'            : ['../res/bomber/bomber_00.png',  # size test
                           '../res/bomber/bomber_01.png',  # standard 01
                           '../res/bomber/bomber_02.png',  # standard 02
                           '../res/bomber/bomber_03.png',  # standard 03
                           '../res/bomber/bomber_04.png',  # crashing 01
                           '../res/bomber/bomber_05.png',  # crashing 02
                           '../res/bomber/bomber_06.png'], # crashing 03
                          
    'health'            : ['../res/health_bar.png'],
    'numbers'           : ['../res/numbers.png'],
    'score'             : ['../res/score_text.png'],
    'wave'              : ['../res/wave_text.png'],
    'power_up'          : ['../res/power_up_01.png',
                           '../res/power_up_02.png'
                          ],
                          
    'bomb'              : ['../res/bomb.png'],

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
                           
    assets['buddy']     = [pyg.image.load(image_paths['buddy'][0])]
                           
    assets['bullet']    = [pyg.image.load(image_paths['bullet'][0]),
                           pyg.image.load(image_paths['bullet'][1]),
                           pyg.image.load(image_paths['bullet'][2]),
                           pyg.image.load(image_paths['bullet'][3])]
                           
    assets['boat']      = [pyg.image.load(image_paths['boat'][0]),
                           pyg.image.load(image_paths['boat'][1])]
                           
    assets['submarine'] = [pyg.image.load(image_paths['submarine'][0]),
                           pyg.image.load(image_paths['submarine'][1]),
                           pyg.image.load(image_paths['submarine'][2]),
                           pyg.image.load(image_paths['submarine'][3]),
                           pyg.image.load(image_paths['submarine'][4]),
                           pyg.image.load(image_paths['submarine'][5])]
                          
    assets['turret']    = [pyg.image.load(image_paths['turret'][0]), # south
                           pyg.image.load(image_paths['turret'][1]), # south-east
                           pyg.image.load(image_paths['turret'][2]), # east
                           pyg.image.load(image_paths['turret'][3]), # north-east
                           pyg.image.load(image_paths['turret'][4]), # north
                           pyg.image.load(image_paths['turret'][5]), # north-west
                           pyg.image.load(image_paths['turret'][6]), # west
                           pyg.image.load(image_paths['turret'][7])] # south-west
                         
    assets['health']    = [pyg.image.load(image_paths['health'][0])]
    assets['numbers']   = [pyg.image.load(image_paths['numbers'][0])]
    assets['score']     = [pyg.image.load(image_paths['score'][0])]
    assets['wave']      = [pyg.image.load(image_paths['wave'][0])]
    assets['power_up']  = [pyg.image.load(image_paths['power_up'][0]),
                           pyg.image.load(image_paths['power_up'][1])]
                           
    assets['bomb']      = [pyg.image.load(image_paths['bomb'][0])]
                           
    assets['water']     = [pyg.image.load(image_paths['water'][0]),
                           pyg.image.load(image_paths['water'][1])]
    
    assets['olive-plane'] = [pyg.image.load(image_paths['olive-plane'][0]),
                             pyg.image.load(image_paths['olive-plane'][1]),
                             pyg.image.load(image_paths['olive-plane'][2]),
                             pyg.image.load(image_paths['olive-plane'][3]),
                             pyg.image.load(image_paths['olive-plane'][4]),
                             pyg.image.load(image_paths['olive-plane'][5]),
                             pyg.image.load(image_paths['olive-plane'][6]),
                             pyg.image.load(image_paths['olive-plane'][7]),
                             pyg.image.load(image_paths['olive-plane'][8]),
                             pyg.image.load(image_paths['olive-plane'][9]),
                             pyg.image.load(image_paths['olive-plane'][10]),
                             # flip 01
                             pyg.image.load(image_paths['olive-plane'][11]),
                             # flip 02
                             pyg.image.load(image_paths['olive-plane'][12]),
                             # flip 03
                             pyg.image.load(image_paths['olive-plane'][13]),
                             # flip 04
                             pyg.image.load(image_paths['olive-plane'][14]),
                             # flip 05
                             pyg.image.load(image_paths['olive-plane'][15]),
                             # upside down 01
                             pyg.image.load(image_paths['olive-plane'][16]),
                             # upside down 02
                             pyg.image.load(image_paths['olive-plane'][17])]
                             
    assets['white-plane'] = [pyg.image.load(image_paths['white-plane'][0]),
                             pyg.image.load(image_paths['white-plane'][1]),
                             pyg.image.load(image_paths['white-plane'][2]),
                             pyg.image.load(image_paths['white-plane'][3]),
                             pyg.image.load(image_paths['white-plane'][4]),
                             pyg.image.load(image_paths['white-plane'][5]),
                             pyg.image.load(image_paths['white-plane'][6]),
                             pyg.image.load(image_paths['white-plane'][7]),
                             pyg.image.load(image_paths['white-plane'][8]),
                             pyg.image.load(image_paths['white-plane'][9]),
                             pyg.image.load(image_paths['white-plane'][10]),
                             pyg.image.load(image_paths['white-plane'][11]),
                             pyg.image.load(image_paths['white-plane'][12]),
                             pyg.image.load(image_paths['white-plane'][13]),
                             pyg.image.load(image_paths['white-plane'][14]),
                             pyg.image.load(image_paths['white-plane'][15]),
                             pyg.image.load(image_paths['white-plane'][16]),
                             pyg.image.load(image_paths['white-plane'][17])]
                             
    assets['green-plane'] = [pyg.image.load(image_paths['green-plane'][0]),
                             pyg.image.load(image_paths['green-plane'][1]),
                             pyg.image.load(image_paths['green-plane'][2]),
                             pyg.image.load(image_paths['green-plane'][3]),
                             pyg.image.load(image_paths['green-plane'][4]),
                             pyg.image.load(image_paths['green-plane'][5]),
                             pyg.image.load(image_paths['green-plane'][6]),
                             pyg.image.load(image_paths['green-plane'][7]),
                             pyg.image.load(image_paths['green-plane'][8]),
                             pyg.image.load(image_paths['green-plane'][9]),
                             pyg.image.load(image_paths['green-plane'][10]),
                             pyg.image.load(image_paths['green-plane'][11]),
                             pyg.image.load(image_paths['green-plane'][12]),
                             pyg.image.load(image_paths['green-plane'][13]),
                             pyg.image.load(image_paths['green-plane'][14]),
                             pyg.image.load(image_paths['green-plane'][15]),
                             pyg.image.load(image_paths['green-plane'][16]),
                             pyg.image.load(image_paths['green-plane'][17])]
                             
    assets['blue-plane']  = [pyg.image.load(image_paths['blue-plane'][0]),
                             pyg.image.load(image_paths['blue-plane'][1]),
                             pyg.image.load(image_paths['blue-plane'][2]),
                             pyg.image.load(image_paths['blue-plane'][3]),
                             pyg.image.load(image_paths['blue-plane'][4]),
                             pyg.image.load(image_paths['blue-plane'][5]),
                             pyg.image.load(image_paths['blue-plane'][6]),
                             pyg.image.load(image_paths['blue-plane'][7]),
                             pyg.image.load(image_paths['blue-plane'][8]),
                             pyg.image.load(image_paths['blue-plane'][9]),
                             pyg.image.load(image_paths['blue-plane'][10]),
                             pyg.image.load(image_paths['blue-plane'][11]),
                             pyg.image.load(image_paths['blue-plane'][12]),
                             pyg.image.load(image_paths['blue-plane'][13]),
                             pyg.image.load(image_paths['blue-plane'][14]),
                             pyg.image.load(image_paths['blue-plane'][15]),
                             pyg.image.load(image_paths['blue-plane'][16]),
                             pyg.image.load(image_paths['blue-plane'][17])]
                             
    assets['orange-plane']= [pyg.image.load(image_paths['orange-plane'][0]),
                             pyg.image.load(image_paths['orange-plane'][1]),
                             pyg.image.load(image_paths['orange-plane'][2]),
                             pyg.image.load(image_paths['orange-plane'][3]),
                             pyg.image.load(image_paths['orange-plane'][4]),
                             pyg.image.load(image_paths['orange-plane'][5]),
                             pyg.image.load(image_paths['orange-plane'][6]),
                             pyg.image.load(image_paths['orange-plane'][7]),
                             pyg.image.load(image_paths['orange-plane'][8]),
                             pyg.image.load(image_paths['orange-plane'][9]),
                             pyg.image.load(image_paths['orange-plane'][10])]
                             
    assets['big-plane']   = [pyg.image.load(image_paths['big-plane'][0])]
    
    assets['bomber']      = [pyg.image.load(image_paths['bomber'][0]),
                             pyg.image.load(image_paths['bomber'][1]),
                             pyg.image.load(image_paths['bomber'][2]),
                             pyg.image.load(image_paths['bomber'][3]),
                             pyg.image.load(image_paths['bomber'][4]),
                             pyg.image.load(image_paths['bomber'][5]),
                             pyg.image.load(image_paths['bomber'][6])]
    
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
    image = pyg.Surface((32,32))
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
    #raw_input('waitground')
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

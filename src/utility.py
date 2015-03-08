import math, random, copy, os
import pygame as pyg
from pygame.locals import *

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
    def get_tuple(self):
        return (self.x, self.y)
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

PATH_SFX        = 'data/audio/sfx'
PATH_BACKGROUND = 'data/environment'

PATH_HERO       = 'data/hero'
PATH_HUD        = 'data/hud'
PATH_UPGRADES   = 'data/upgrades'
PATH_BULLETS    = 'data/bullets'
PATH_BOAT       = 'data/enemies/vessel'
PATH_SUBMARINE  = 'data/enemies/vessel/submarine'
PATH_TURRET     = 'data/enemies/artillery'

PATH_OLIVE      = 'data/enemies/aerial/olive'
PATH_WHITE      = 'data/enemies/aerial/white'
PATH_GREEN      = 'data/enemies/aerial/green'
PATH_BLUE       = 'data/enemies/aerial/blue'
PATH_ORANGE     = 'data/enemies/aerial/orange'

PATH_BIGPLANE   = 'data/enemies/aerial/misc'
PATH_BOMBER     = 'data/enemies/aerial/bomber'

image_paths  = {
    'player'    : [os.path.join(PATH_HERO, 'hero_01.png'),
                   os.path.join(PATH_HERO, 'hero_02.png'),
                   os.path.join(PATH_HERO, 'hero_03.png')],
                   
    'wingman'   : [os.path.join(PATH_HERO, 'wingman.png')],

    'bullet'    : [os.path.join(PATH_BULLETS, 'bullet_01.png'),
                   os.path.join(PATH_BULLETS, 'bullet_02.png'),
                   os.path.join(PATH_BULLETS, 'bullet_03.png'),
                   os.path.join(PATH_BULLETS, 'bullet_04.png')],

    'boat'      : [os.path.join(PATH_BOAT, 'boat_a_01.png'),
                   os.path.join(PATH_BOAT, 'boat_a_02.png')],

    'submarine' : [os.path.join(PATH_SUBMARINE, 'sub_01.png'), # exposed
                   os.path.join(PATH_SUBMARINE, 'sub_02.png'), # submerge 1
                   os.path.join(PATH_SUBMARINE, 'sub_03.png'), # submerge 2
                   os.path.join(PATH_SUBMARINE, 'sub_04.png'), # submerge 3
                   os.path.join(PATH_SUBMARINE, 'sub_05.png'), # submerge 4
                   os.path.join(PATH_SUBMARINE, 'sub_06.png')  # submerge 5
                  ],

    'turret'    : [os.path.join(PATH_TURRET, 'turret_south.png'),
                   os.path.join(PATH_TURRET, 'turret_south_east.png'),
                   os.path.join(PATH_TURRET, 'turret_east.png'),
                   os.path.join(PATH_TURRET, 'turret_north_east.png'),
                   os.path.join(PATH_TURRET, 'turret_north.png'),
                   os.path.join(PATH_TURRET, 'turret_north_west.png'),
                   os.path.join(PATH_TURRET, 'turret_west.png'),
                   os.path.join(PATH_TURRET, 'turret_south_west.png')
                  ],

    'olive-plane'   : [os.path.join(PATH_OLIVE, 'olive_01.png'),
                       os.path.join(PATH_OLIVE, 'olive_02.png'),
                       os.path.join(PATH_OLIVE, 'olive_03.png'),
                       os.path.join(PATH_OLIVE, 'olive_04.png'), # S
                       os.path.join(PATH_OLIVE, 'olive_05.png'), # SE
                       os.path.join(PATH_OLIVE, 'olive_06.png'), # E
                       os.path.join(PATH_OLIVE, 'olive_07.png'), # NE
                       os.path.join(PATH_OLIVE, 'olive_08.png'), # N
                       os.path.join(PATH_OLIVE, 'olive_09.png'), # NW
                       os.path.join(PATH_OLIVE, 'olive_10.png'), # W
                       os.path.join(PATH_OLIVE, 'olive_11.png'), # SW
                       os.path.join(PATH_OLIVE, 'olive_12.png'), # flip 1
                       os.path.join(PATH_OLIVE, 'olive_13.png'), # flip 2
                       os.path.join(PATH_OLIVE, 'olive_14.png'), # flip 3
                       os.path.join(PATH_OLIVE, 'olive_15.png'), # flip 4
                       os.path.join(PATH_OLIVE, 'olive_16.png'), # flip 5
                       os.path.join(PATH_OLIVE, 'olive_17.png'), # flipped 1
                       os.path.join(PATH_OLIVE, 'olive_18.png')  # flipped 2
                      ],

    'white-plane'   : [os.path.join(PATH_WHITE, 'white_01.png'),
                       os.path.join(PATH_WHITE, 'white_02.png'),
                       os.path.join(PATH_WHITE, 'white_03.png'),
                       os.path.join(PATH_WHITE, 'white_04.png'), # S
                       os.path.join(PATH_WHITE, 'white_05.png'), # SE
                       os.path.join(PATH_WHITE, 'white_06.png'), # E
                       os.path.join(PATH_WHITE, 'white_07.png'), # NE
                       os.path.join(PATH_WHITE, 'white_08.png'), # N
                       os.path.join(PATH_WHITE, 'white_09.png'), # NW
                       os.path.join(PATH_WHITE, 'white_10.png'), # W
                       os.path.join(PATH_WHITE, 'white_11.png'), # SW
                       os.path.join(PATH_WHITE, 'white_12.png'), # flip 1
                       os.path.join(PATH_WHITE, 'white_13.png'), # flip 2
                       os.path.join(PATH_WHITE, 'white_14.png'), # flip 3
                       os.path.join(PATH_WHITE, 'white_15.png'), # flip 4
                       os.path.join(PATH_WHITE, 'white_16.png'), # flip 5
                       os.path.join(PATH_WHITE, 'white_17.png'), # flipped 1
                       os.path.join(PATH_WHITE, 'white_18.png')  # flipped 2
                      ],

    'green-plane'   : [os.path.join(PATH_GREEN, 'green_01.png'),
                       os.path.join(PATH_GREEN, 'green_02.png'),
                       os.path.join(PATH_GREEN, 'green_03.png'),
                       os.path.join(PATH_GREEN, 'green_04.png'), # S
                       os.path.join(PATH_GREEN, 'green_05.png'), # SE
                       os.path.join(PATH_GREEN, 'green_06.png'), # E
                       os.path.join(PATH_GREEN, 'green_07.png'), # NE
                       os.path.join(PATH_GREEN, 'green_08.png'), # N
                       os.path.join(PATH_GREEN, 'green_09.png'), # NW
                       os.path.join(PATH_GREEN, 'green_10.png'), # W
                       os.path.join(PATH_GREEN, 'green_11.png'), # SW
                       os.path.join(PATH_GREEN, 'green_12.png'), # flip 1
                       os.path.join(PATH_GREEN, 'green_13.png'), # flip 2
                       os.path.join(PATH_GREEN, 'green_14.png'), # flip 3
                       os.path.join(PATH_GREEN, 'green_15.png'), # flip 4
                       os.path.join(PATH_GREEN, 'green_16.png'), # flip 5
                       os.path.join(PATH_GREEN, 'green_17.png'), # flipped 1
                       os.path.join(PATH_GREEN, 'green_18.png')  # flipped 2
                      ],

    'blue-plane'    : [os.path.join(PATH_BLUE, 'blue_01.png'),
                       os.path.join(PATH_BLUE, 'blue_02.png'),
                       os.path.join(PATH_BLUE, 'blue_03.png'),
                       os.path.join(PATH_BLUE, 'blue_04.png'), # S
                       os.path.join(PATH_BLUE, 'blue_05.png'), # SE
                       os.path.join(PATH_BLUE, 'blue_06.png'), # E
                       os.path.join(PATH_BLUE, 'blue_07.png'), # NE
                       os.path.join(PATH_BLUE, 'blue_08.png'), # N
                       os.path.join(PATH_BLUE, 'blue_09.png'), # NW
                       os.path.join(PATH_BLUE, 'blue_10.png'), # W
                       os.path.join(PATH_BLUE, 'blue_11.png'), # SW
                       os.path.join(PATH_BLUE, 'blue_12.png'), # flip 1
                       os.path.join(PATH_BLUE, 'blue_13.png'), # flip 2
                       os.path.join(PATH_BLUE, 'blue_14.png'), # flip 3
                       os.path.join(PATH_BLUE, 'blue_15.png'), # flip 4
                       os.path.join(PATH_BLUE, 'blue_16.png'), # flip 5
                       os.path.join(PATH_BLUE, 'blue_17.png'), # flipped 1
                       os.path.join(PATH_BLUE, 'blue_18.png')  # flipped 2
                      ],

    'orange-plane'  : [os.path.join(PATH_ORANGE, 'orange_01.png'),
                       os.path.join(PATH_ORANGE, 'orange_02.png'),
                       os.path.join(PATH_ORANGE, 'orange_03.png'),
                       os.path.join(PATH_ORANGE, 'orange_04.png'), # S
                       os.path.join(PATH_ORANGE, 'orange_05.png'), # SE
                       os.path.join(PATH_ORANGE, 'orange_06.png'), # E
                       os.path.join(PATH_ORANGE, 'orange_07.png'), # NE
                       os.path.join(PATH_ORANGE, 'orange_08.png'), # N
                       os.path.join(PATH_ORANGE, 'orange_09.png'), # NW
                       os.path.join(PATH_ORANGE, 'orange_10.png'), # W
                       os.path.join(PATH_ORANGE, 'orange_11.png')  # SW
                      ],                                           # NO FLIP

    'big-plane'     : [os.path.join(PATH_BIGPLANE, 'BigPlane.png')],

    'bomber'    : [os.path.join(PATH_BOMBER, 'bomber_00.png'), # size test
                   os.path.join(PATH_BOMBER, 'bomber_01.png'), # standard 01
                   os.path.join(PATH_BOMBER, 'bomber_02.png'), # standard 02
                   os.path.join(PATH_BOMBER, 'bomber_03.png'), # standard 03
                   os.path.join(PATH_BOMBER, 'bomber_04.png'), # crashing 01
                   os.path.join(PATH_BOMBER, 'bomber_05.png'), # crashing 02
                   os.path.join(PATH_BOMBER, 'bomber_06.png')  # crashing 03
                  ],

    'health'    : [os.path.join(PATH_HUD, 'health_bar.png')],
    'numbers'   : [os.path.join(PATH_HUD, 'numbers.png')],
    'score'     : [os.path.join(PATH_HUD, 'score_text.png')],
    'bomb'      : [os.path.join(PATH_HUD, 'bomb.png')],
    'get_ready' : [os.path.join(PATH_HUD, 'get_ready_01.png'),
                   os.path.join(PATH_HUD, 'get_ready_02.png')],
    'lives'     : [os.path.join(PATH_HUD, 'wings_pointer.png')],
    'game_over' : [os.path.join(PATH_HUD, 'game_over_01.png'),
                   os.path.join(PATH_HUD, 'game_over_02.png')],
    
    'power_up'  : [os.path.join(PATH_UPGRADES, 'power_up_01.png'),
                   os.path.join(PATH_UPGRADES, 'power_up_02.png')],

    'water'     : [os.path.join(PATH_BACKGROUND, 'water_01.png'),
                   os.path.join(PATH_BACKGROUND, 'water_02.png')]

}

assets = {}

#_______________________________________________________________________________
def init():
    assets['player']    = [pyg.image.load(image_paths['player'][0]),
                           pyg.image.load(image_paths['player'][1]),
                           pyg.image.load(image_paths['player'][2])]
                           
    assets['wingman']   = [pyg.image.load(image_paths['wingman'][0])]
                           
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
                           
    assets['get_ready'] = [pyg.image.load(image_paths['get_ready'][0]),
                           pyg.image.load(image_paths['get_ready'][1])]
                           
    assets['lives']     = [pyg.image.load(image_paths['lives'][0])]
    
    assets['game_over'] = [pyg.image.load(image_paths['game_over'][0]),
                           pyg.image.load(image_paths['game_over'][1])]
    
    black_background = ['health','score','get_ready', 'title', 
                        'game_over'
    ]
    
    for (key,value) in assets.items():
        for i, img in enumerate(assets[key]):
                
            if key in black_background:
                img.set_colorkey((0,0,0))
                
            else:
                img.set_colorkey((2, 73, 148))
                
            assets[key][i] = img.convert()
    
    
    # special handling.
    load_numbers()
    
            
    print('artwork initialized')

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
    for i in range(10):
        cropper.blit(numbers,
                         (0,0), # start at coordinates for destination.
                         (offset, 0, offset + section, img_y))
        assets[str(i)] = [cropper.copy()]
        offset += section
        #print('loaded number %d' % i)
#_______________________________________________________________________________
def get_number(name):
    return get_image(name, 0)
#_______________________________________________________________________________
def get_image(name, frame):
    #print('%r, %d' % (name,frame))
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
        for y in range(0, size_y, box_y):
            for x in range(0, size_x, box_x):
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
    
#_______________________________________________________________________________
def get_sfx(name):

    if name.lower() == 'explosion':
        return pyg.mixer.Sound(os.path.join(PATH_SFX, 'explosion.wav'))
    else:
        print('sound %s does not exist' % name)

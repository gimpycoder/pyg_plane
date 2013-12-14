import pygame as pyg

FRAME_DELAY = 4

image_paths  = {
    'player'            : ['../res/hero_01.png',
                           '../res/hero_02.png', 
                           '../res/hero_03.png'
                          ],
    'boat'              : ['../res/boat_a_01.png',
                           '../res/boat_a_02.png'
                          ],
    'health'            : ['../res/health_bar.png'],
    'numbers'           : ['../res/numbers.png'],
    'score'             : ['../res/score_text.png'],
    'wave'              : ['../res/wave_text.png'],
    'power_up'          : ['../res/power_up_01.png',
                           '../res/power_up_02.png'
                          ]
}

assets = {}

def init():
    assets['player']    = [pyg.image.load(image_paths['player'][0]),
                           pyg.image.load(image_paths['player'][1]),
                           pyg.image.load(image_paths['player'][2])]
                           
    assets['boat']      = [pyg.image.load(image_paths['boat'][0]),
                           pyg.image.load(image_paths['boat'][1])]
    assets['health']    = [pyg.image.load(image_paths['health'][0])]
    assets['numbers']   = [pyg.image.load(image_paths['numbers'][0]).convert()]
    assets['score']     = [pyg.image.load(image_paths['score'][0])]
    assets['wave']      = [pyg.image.load(image_paths['wave'][0])]
    assets['power_up']  = [pyg.image.load(image_paths['power_up'][0]),
                           pyg.image.load(image_paths['power_up'][1])] 
    
    load_numbers()

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

def get_number(name):
    return get_image(name, 0)
    
def get_image(name, frame):
    #print '%r, %d' % (name,frame)
    return assets[name][frame]
    
def get_frame_count(name):
    return len(assets[name])
    
    
if __name__ == '__main__':
    init()
    num = ['0','1','2','3','4','5','6','7','8','9']
    load_numbers()
    for number in assets:
        print number
    #print type(assets['player'][0])


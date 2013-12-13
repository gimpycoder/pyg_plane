import pygame as pyg

FRAME_DELAY = 4

image_paths  = {
    'player' : ['../res/plane.png'],
    'boat'   : ['../res/boat_a_01.png','../res/boat_a_02.png'],
    'health' : ['../res/health_bar.png']
}

assets = {}

def init():
    assets['player'] = [pyg.image.load(image_paths['player'][0])]
    assets['boat']   = [pyg.image.load(image_paths['boat'][0]),
                        pyg.image.load(image_paths['boat'][1])]
    assets['health'] = [pyg.image.load(image_paths['health'][0])]
    
def get_image(name, frame):
    return assets[name][frame]
    
def get_frame_count(name):
    return len(assets[name])


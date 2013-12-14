import pygame as pyg
from vector import Vector
import artwork

class Score(object):
    name = 'score_sheet'

    def __init__(self, screen, location):
        self.screen = screen
        self.value = 0
        self.max_value = 9999999999
        self.digits = {}
        self.location = location
        self.width = 0

    def init(self):
        for i in xrange(10):
            self.digits[str(i)] = artwork.get_number(str(i))
            
        self.width = self.digits['0'].get_size()[0] + 2
        print self.width

    def increase_score(self, amount):
        if self.value + amount > self.max_value:
            self.value = self.max_value
            
        self.value += amount
        
    def decrease_score(self, amount):
        if self.value - amount < 0:
            self.value = 0
            
        self.value -= amount
        
    def display(self):
        # no negative scores for this game.
        if self.value < 0:
            self.value = 0
    
        score = str(self)
        location = self.location.get_copy()
        for i in xrange(len(score)):
            img = self.digits[score[i]]
            self.screen.blit(img, (location.x, location.y))
            location.x += self.width
            #print location
        
    def __str__(self):
        return str(self.value).rjust(10, '0')
        
if __name__ == '__main__':
    s = Score()
    s.init()
    print s
    s.increase_score(250)
    print s
    s.decrease_score(110)
    print s
    score = str(s)
    print len(score)
    for i in xrange(len(score)):
        print score[i]
        
    s.display()
        

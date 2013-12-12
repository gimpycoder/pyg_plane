import math
import copy

class Vector(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        
    def add(self, other): 
        self.x += other.x
        self.y += other.y
        
    def sub(self, other):
        self.x -= other.x
        self.y -= other.y
        
    def mul(self, value):
        self.x *= value
        self.y *= value
        
    def div(self, value):
        if not value == 0:
            self.x /= value
            self.y /= value
            
    def mag(self):
        a = self.x**2.0
        b = self.y**2.0
        c = math.sqrt(a + b)
        return c
        
    def norm(self):
        magnitude = self.mag()
        self.div(magnitude)
        
    def get_copy(self):
        return copy.copy(self)
        
    def __str__(self):
        return format("x=%r,y=%r" % (self.x,self.y))
        
if __name__ == '__main__':
    a = Vector(2,2)
    b = Vector(1,1)
    c = Vector(0.5,0.3)
    d = Vector(3.0,3.0)
    
    d.norm()
    # x = 3.0 / 4.24264 = 0.707106896
    # y = 3.0 / same....
    print "d norm=%s : expected (0.707106896, 0.707106896)" % d
    
    a.add(Vector(1,1))
    print "a=%s : expected (3.0,3.0)" % a
    # http://www.wolframalpha.com/input/?i=magnitude+{3.0%2C3.0}
    print "mag=%.6f : expected (4.24264)" % a.mag()
    
    b.sub(Vector(1,1))
    print "b=%s : expected (0.0,0.0)" % b
    print "mag=%.6f : expected (0.0)" % b.mag()
    
    c.add(a)
    print "c=%s : expected (3.5,3.3)" % c
    # http://www.wolframalpha.com/input/?i=magnitude+{3.5%2C3.3}
    # wolframalpha rounds...
    print "mag=%.6f : expected (4.81041)" % c.mag()
    
    # remember b is zero now.
    c.sub(b)
    print "c=%s : expected (3.5,3.3)" % c
    
    a.mul(2)
    print "a=%s : expected (6.0,6.0)" % a
    
    c.mul(2.5)                              # sometimes it's best to let the
                                            # computer do the math.
    print "c=%s : expected (%.2f,%.2f)" % (c, (3.5*2.5),(3.3*2.5))
    
    c.div(2.5) # we just canceled our multiplcation.
    print "c=%s : expected (3.5,3.3)" % c
    
    a.div(0.0)
    print "a=%s : expected (6.0,6.0)" % a
    
    


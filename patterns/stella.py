import random
import cubehelper

class Pattern(object):
    def init(self):
        sz = self.cube.size
        self.n = sz/2
        self.dir = 0
        self.m = sz/2
        self.state = 0
        self.count = 0
        self.delay = 1
        self.anim = 0
        self.action = (0x5, 
                       0x0, 0xa,
                       0x5, 0xa, 0x5,
                       0x2, 0x1, 0x8, 0x4, 0x2, 0x1, 0x8, 0x4,
                       0xa, 0x5, 
                       0xa,
                       0x1, 0x2, 0x4, 0x8, 0x1, 0x2, 0x4, 0x8,
#                       0x35, 0x3a, 0x35, 0x3a, 
)
        return 1.5/sz
    
    def tick(self):
        sz = self.cube.size

        action = self.action[self.state]
        self.anim += 1
        if self.anim == 1:
            self.anim = 0
            done = False
            if self.count < sz/2:
                if action & 1:
                    self.n -= 1
                elif action & 2:
                    self.n += 1
                if action & 4:
                    self.m -= 1
                elif action & 8:
                    self.m += 1
                    
            self.count += 1
            if self.count == sz/2 + self.delay:
                self.state = (self.state+1) % len(self.action)
                self.count = 0

        n = self.n
        m = self.m
        for x in range(0, sz):
            for y in range(0, sz):
                for z in range(0, sz):
                    p1 =  x+y-z >= n
                    p2 =  x-y+z >= n
                    p3 = -x+y+z >= n
                    p4 =  x+y+z < sz*2-1-n
                    p5 =  x+y-z < sz-m
                    p6 =  x-y+z < sz-m
                    p7 =  -x+y+z < sz-m
                    p8 =  x+y+z > sz-2+m
                    
                    v = p1 and p2 and p3 and p4
                    w = p5 and p6 and p7 and p8
                    if action & 16:
                        v = v and w
                    if action & 32:
                        w = v and w
                    q = 255 # (((x+y+z+self.anim)%3)*4 + 5) * 17
                    r = 255 #(((-x-y-z+self.anim)%3)*4 + 5) * 17
                    col = (q if v else 0, 
                           0, #r if w else 0, 
                           q if w else 0)
                    self.cube.set_pixel((x, y, z), col)

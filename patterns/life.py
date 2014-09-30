import cubehelper
import random
import numpy

class Pattern(object):
    def init(self):
        sz = self.cube.size
        self.grid = numpy.zeros([sz, sz, sz], 'int')
        for x in range(0, sz):
            for y in range(0, sz):
                self.grid[x,y,0] = 1 if random.random() < 0.4 else 0
        self.scroll = 1
        self.col = [ None ] * sz

        for i in range(0, sz):
            self.col[i] = cubehelper.random_color()
        return 1.0/16

    def tick(self):
        g = self.grid
        sz = self.cube.size
        
        for x in range(0, self.cube.size):
            for y in range(0, self.cube.size):
                for z in range(0, self.cube.size):
                    col = self.col[z] if g[x,y,(z+self.scroll) % sz] else (0,0,0)
                    self.cube.set_pixel((y, z, sz-x-1), col)
                    
        new = self.scroll
        old = (self.scroll + sz - 1) % sz
        for x in range(0, sz):
            xl = (x+sz-1) % sz
            xr = (x+1) % sz
            for y in range(0, sz):
                yl = (y+sz-1) % sz
                yr = (y+1) % sz
                n = g[xl,yl,old] + g[x,yl,old] + g[xr,yl,old] + \
                    g[xl,y, old]               + g[xr,y, old] + \
                    g[xl,yr,old] + g[x,yr,old] + g[xr,yr,old]
                if g[x,y,old]:
                    g[x,y,new] = 1 if n==2 or n==3 else 0
                else:
                    g[x,y,new] = 1 if n==3 else 0
                    
        self.scroll = (self.scroll+1) % sz

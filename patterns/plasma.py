# Plasma
# Copyright (C) Paul Brook <paul@nowt.org>
# Released under the terms of the GNU General Public License version 3

import random
import cubehelper
import math

DT = 0.05

class Pattern(object):
    def init(self):
        self.offset = 0
        self.cos = [0] * 8
        self.plasma = [0] * 256
        for i in range(8):
            self.cos[i] = int(32*math.cos((i+.5)*math.pi*2/8))
        for i in range(256):
            self.plasma[i] = self.cube.plasma(i/256)
        return DT
    
    
    @micropython.native
    def tick(self):
        sp = self.cube.set_pixel
        cos = self.cos
        plasma = self.plasma
        self.offset +=10
        sz = self.cube.size
        i = 0
        for y in range(0, sz):
            for z in range(0, sz):
                for x in range(0, sz):
                    e = cos[x]+cos[y]+cos[z]-self.offset
                    color = self.plasma[e & 255]
                    sp(i, color)
                    #sp(0x1ff-i, color)
                    i += 1

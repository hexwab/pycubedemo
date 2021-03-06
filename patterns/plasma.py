# Plasma
# Copyright (C) Paul Brook <paul@nowt.org>
# Released under the terms of the GNU General Public License version 3

import random
import cubehelper
import math

DT = 0.05

def color_from_val(val):
    if val < 85:
        r = val * 3;
        g = 255 - r;
        b = 0;
    elif val < 170:
        b = (val - 85) * 3;
        r = 255 - b;
        g = 0;
    else:
        g = (val - 170) * 3;
        b = 255 - g;
        r = 0;
    return (r, g, b)

class Pattern(object):
    def init(self):
        self.offset = 0.0
        return DT

    def color_for_energy(self, e):
        level = math.modf(self.offset + e)[0]
        if self.cube.color:
            return color_from_val(int(level * 256))
        else:
            level = level * 2.0
            if level > 1.0:
                level = 2.0 - level
            return (level, level, level)

    def tick(self):
        self.offset -= DT / 1.0
        if self.offset < 0:
            self.offset += 1.0
        sz = self.cube.size
        scale = math.pi * 2.0 / float(sz)
        offset = 0.5
        for x in range(0, sz):
            for y in range(0, sz):
                for z in range(0, sz):
                    u = math.cos((x + offset) * scale)
                    v = math.cos((y + offset) * scale)
                    w = math.cos((z + offset) * scale)
                    color = self.color_for_energy((u + v + w + 3.0) / 6.0)
                    self.cube.set_pixel((x, y, z), color)

import time,cubehelper

class Cube(object):
    def __init__(self, args):
        self.size = 8
        self.t1 = time.ticks_ms()
        self.color = True
        self.plasma = cubehelper.color_plasma

    def clear(self):
        print("clear")
        pass

    def swap(self):
        print("swap")
        pass

    def set_pixel(self, xyz, rgb):
        if not isinstance(rgb,int):
            rgb = (rgb[0]<<16) | (rgb[1]<<8) | rgb[2]
        if not isinstance(xyz,int):
            xyz = (xyz[0]<<6) | (xyz[1]<<3) | xyz[2]
        print("set_pixel",xyz,rgb)
        pass
    
    def render(self):
        #t2 = time.ticks_ms()
        #print ("%d" % (t2-self.t1))
        #self.t1 = t2
        print("render")
        pass
    

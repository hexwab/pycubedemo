import sys

class Pattern(object):
    def init(self):
        return 1/50.0

    def tick(self):
        while True:
            line = sys.stdin.readline()
            arr = line.split()
            if not len(arr):
                next
            if arr[0]=='set_pixel':
                print(arr)
                xyz = int(arr[1])
                rgb = int(arr[2])
                self.cube.set_pixel([xyz>>6,(xyz>>3)&7,xyz&7],(rgb>>16,(rgb>>8)&255,rgb&255))
            elif arr[0]=='clear':
                self.cube.clear()
            elif arr[0]=='render':
                break

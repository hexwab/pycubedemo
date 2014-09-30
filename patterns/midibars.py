import cubehelper
import pypm
import array

def PrintDevices():
    for loop in range(pypm.CountDevices()):
        interf,name,inp,outp,opened = pypm.GetDeviceInfo(loop)
        if (inp == 1):
            print loop, name," ",
            if (inp == 1): print "(input) ",
            else: print "(output) ",
            if (opened == 1): print "(opened)"
            else: print "(unopened)"
    print
    
pypm.Initialize() # always call this first, or OS may crash when you try to open a stream
PrintDevices()
dev = int(raw_input("Type input number: "))
MidiIn = pypm.Input(dev)

class Pattern(object):
    def init(self):
        self.state = [ 0 ] * 64
        return 1.0/20.0
    
    def tick(self):

        while MidiIn.Poll():
            MidiData = MidiIn.Read(1) # read only 1 message at a time
            command = MidiData[0][0][0]
            note = MidiData[0][0][1] - 36
            if command == 0x90: # note on
                self.state[note] = 64
            elif command == 0x80: # note off
                self.state[note] = 8

        sz = self.cube.size
        for n in range(0,64):
            x = n % 8
            y = n / 8
            for z in range(0, sz):
                if self.state[n] < 64:
                    self.state[n] -= 1
                col = (20*(n%12),20*((n+4)%12),20*((n+8)%12)) if self.state[n]>z else (0,0,0)
                self.cube.set_pixel((x, y, z), col)

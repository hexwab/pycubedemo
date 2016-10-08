import pyb

def random():
    return pyb.rng()/1073741824.0

def randint(low,high):
    return (pyb.rng() % (high-low))+low

def choice(args):
    return args[pyb.rng() % len(args)]

def randrange(start,stop=None,step=1):
    if stop is None:
        stop = start
        start = 0
    
    return start + ((pyb.rng() % ((stop-start)//step)) * step)

def uniform(a,b):
    return a + (b-a)*random()

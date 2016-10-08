import os,time
patts = [patt.rsplit('.',1)[0] for patt in os.listdir("patterns")]

print(patts)
import cubestub

def my_import(name):
    m = __import__(name)
    for n in name.split(".")[1:]:
        m = getattr(m, n)
    return m

cube = cubestub.Cube({})

patterns = {}
arglist = []
for name in patts:
    mod = my_import("patterns."+name)
    print(mod)
    constructor = mod.Pattern
    assert(constructor)
    if constructor is not None:
        pobj = constructor()
        pobj.name = name
        pobj.cube = cube
        pobj.arg = None
        patterns[name] = pobj

def run_pattern(cube, pattern):
    try:
        interval = pattern.init()
        now = time.time()
        next_tick = now + interval
        sec_tick = now + 1.0
        frames = 0
        print("Running pattern %s" % pattern.name)
        cube.clear()
        cube.swap()
        null_iteration = False
        while True:
            try:
                pattern.tick()
                null_iteration = False
            except StopIteration:
                if null_iteration:
                    raise
                null_iteration = True
            cube.render()
            cube.swap()
            now = time.time()
            if next_tick > now:
                time.sleep(next_tick - now)
            next_tick += interval
            frames += 1
            if now >= sec_tick:
                #if debug_frames:
                #    print("%d/%d" % (frames, int(1.0/interval)))
                sec_tick += 1.0
                frames = 0
    except StopIteration:
        return

# known working:
# plasma boxflip cubefill cubezoom fade fireworks rain rubik
# scroller spiral stella swipe wave worm

# broken:
# bounce?

# CHECKME:
# message

run_pattern(cube, patterns['plasma'])


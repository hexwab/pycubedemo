import random
import math

def line(p0, p1):
    d = [abs(p0[i] - p1[i]) for i in range(0, 3)]
    if d[0] > d[1]:
        a0 = 0
    else:
        a0 = 1
    a1 = 1 - a0
    if d[2] > d[a0]:
        a2 = a0
        a0 = 2
    else:
        a2 = 2
    if p0[a0] > p1[a0]:
        (p0, p1) = (p1, p0)
    dx = float(p1[a0] - p0[a0])
    #print((a0, a1, a2), dx)
    if dx < 1.0:
        yield tuple(int(v) for v in p0)
        return
    dy = float(p1[a1] - p0[a1]) / dx
    dz = float(p1[a2] - p0[a2]) / dx
    #print([dx, dy, dz])
    y = float(p0[a1]) + 0.5
    z = float(p0[a2]) + 0.5
    pos = [0.0]*3
    for x in range(int(p0[a0]), int(p1[a0]) + 1):
        pos[a0] = x
        pos[a1] = int(y)
        pos[a2] = int(z)
        yield tuple(pos)
        y += dy
        z += dz

def random_color(other_color=(-1, -1, -1)):
    """Return a random color as a float tuple, optionally ensuring that it is different to the other_color parameter."""

    return [           0x0000ff, 0x00ff00, 0x00ffff,
             0xff0000, 0xff00ff, 0xffff00, 0xffffff ][random.randint(0,6)]
    
def pos_modf(val):
    val = math.modf(val)[0]
    if val < 0:
        return val + 1.0
    return val

def color_plasma(val):
    val = int(val*256)&255
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
    return (r<<16) | (g<<8) | b

def mono_plasma(val):
    val = pos_modf(val) * 2.0
    if val > 1.0:
        val = 2.0 - val
    return (val, val, val)

def mix_color(color0, color1, level):
    f0 = color_to_int(color0)
    f1 = color_to_int(color1)
    return tuple([int(f1[n] * level + f0[n] * (1.0 - level)) for n in range(0, 3)])

def color_to_hex(color):
    if isinstance(color, int):
        return color
    (r, g, b) = color_to_int(color)
    return (r << 16) | (g << 8) | b

def color_to_int(color):
    if isinstance(color, int):
        return (color >> 16, (color >> 8) & 0xff, color & 0xff)
    return color

# def color_to_float(color):
#     if isinstance(color, int):
#         r = color >> 16
#         g = (color >> 8) & 0xff
#         b = color & 0xff
#     else:
#         (r, g, b) = color
#     if isinstance(r, int):
#         r = (r + 0.5) / 256.0
#         g = (g + 0.5) / 256.0
#         b = (b + 0.5) / 256.0
#     return (r, g, b)

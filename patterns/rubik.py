import random
import cubehelper
import math

# sup dawg. I heard you like cubes...

cols = [ (0,0,0), (255,0,0), (255,128,0), (0,255,0), (0,0,192), (255,255,0), (255,255,255) ]
rounded = True
holey = True
frames = 12
delay = 10

start = [ 1,1,1,1,0,1,1,1,1, 2,2,2,2,0,2,2,2,2, 3,3,3,3,0,3,3,3,3,
          4,4,4,4,0,4,4,4,4, 5,5,5,5,0,5,5,5,5, 6,6,6,6,0,6,6,6,6 ] if holey else \
	[ 1,1,1,1,1,1,1,1,1, 2,2,2,2,2,2,2,2,2, 3,3,3,3,3,3,3,3,3,
          4,4,4,4,4,4,4,4,4, 5,5,5,5,5,5,5,5,5, 6,6,6,6,6,6,6,6,6 ]

step = math.pi / 2 / frames

ops = [ [[24,51,35,44], [25,52,34,43], [26,53,33,42], [10,14,16,12], [9,11,17,15]],  # U
        [[18,38,29,45], [19,37,28,46], [20,36,27,47], [1,3,7,5],     [0,6,8,2]],     # D
        [[6,47,17,44],  [7,50,16,41],  [8,53,15,38],  [28,32,34,30], [27,29,35,33]], # B
        [[0,42,11,45],  [1,39,10,48],  [2,36,9,51],   [19,21,25,23], [18,24,26,20]], # F
        [[8,35,11,20],  [5,32,14,23],  [2,29,17,26],  [46,50,52,48], [45,47,53,51]], # R
        [[0,24,15,27],  [3,21,12,30],  [6,18,9,33],   [37,39,43,41], [36,42,44,38]]  # L
        ]

def op(cube, p):
    n = len(p)
    for i in range(0,n):
        cyc = p[i]
        m = len(cyc)
        tmp = cube[cyc[0]]
        for j in range(0,m-1):
            cube[cyc[j]] = cube[cyc[j+1]]
        cube[cyc[m-1]] = tmp

def scramble(cube):
    moves = []
    axis = None
    count = None
    for i in range(0,22):
        while True:
            f = random.randint(0,5)
            dir = random.randint(0,1)*2-1
            if axis != f>>1:
                axis = f>>1
                count = [ 0, 0 ]
            if abs(count[f&1])==2:
                continue
            if count[f&1]*dir < 0:
                continue
            count[f&1] += dir
            break

        op(cube, ops[f])
        if dir > 0:
            op(cube, ops[f])
            op(cube, ops[f])
        moves.append([f,dir])
    return moves

class Pattern(object):
    def init(self):
        self.double_buffer = True
        assert(self.cube.size==8)
        self.grid = [0] * 512
        self.pos = start
        self.rot = 0
        self.frame = 0
        self.delay = 0
        self.moves = scramble(self.pos)
        return 1/30.

    def draw(self, i, j, face, col):
        s = 7
        for x in range(i*2+1, i*2+3):
            for y in range(j*2+1, j*2+3):
                pos = [(x,  y,  0),
                       (x,  y,  s),
                       (x,  0,  y),
                       (x,  s,  y),
                       (0,  x,  y),
                       (s,  x,  y)][face]
                corner = rounded and (x==1 or x==6) and (y==1 or y==6)
                self.grid[(pos[0]<<6)|(pos[1]<<3)|pos[2]] = 0 if corner else col

    def render(self):
        self.cube.clear()
        f = self.f
        for i in range(0,8):
            for j in range(0,8):
                for k in range(0,8):
                    o = 3.5
                    (x,y,z) = (i-o, j-o, k-o)
                    m = [x,y,z]
                    n = [0,0,0]
                    ind = [[0,1,2],[0,2,1],[1,2,0]][f>>1]
                    (x,y,z) = ind[:]
                    rot = self.rot if ([k>4,k<3,j>4,j<3,i>4,i<3][f]) else 0
                    cr = math.cos(step * rot)
                    sr = math.sin(step * rot)
                    if f & 1:
                        sr = -sr
                    n[x] = round(m[x] * cr - m[y] * sr + o)
                    n[y] = round(m[x] * sr + m[y] * cr + o)
                    n[z] = round(m[z] + o)
                    
                    (xx,yy,zz) = n[:]
                    if xx >= 0 and xx < 8 and yy >= 0 and yy < 8 and zz >= 0 and zz < 8:
                        col = self.grid[(xx<<6)|(yy<<3)|zz]
                        self.cube.set_pixel((i,j,k), cols[col])

    def tick(self):
        if self.delay:
            self.delay -= 1
            return

        if abs(self.rot) == frames:
            op(self.pos, ops[self.f])
            if self.dir < 0:
                op(self.pos, ops[self.f])
                op(self.pos, ops[self.f])
            self.rot = 0

        if self.rot == 0:
            self.delay = delay
            if len(self.moves):
                move = self.moves.pop()
                self.f = move[0]
                self.dir = move[1]
            else:
                raise StopIteration

        self.rot += self.dir

        for i in range(512):
            self.grid[i] = 0
        for face in range(0,6):
            for x in range(0,3):
                for y in range(0,3):
                    self.draw(x, y, face, self.pos[x+y*3+face*9])

        self.render()

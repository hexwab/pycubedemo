import cubehelper
import random
import json
import sys
import traceback

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
FPS = 30
SZ = 8

dirs = [
    (-1,0,0), # left
    ( 1,0,0), # right
    ( 0,1,0), # up
    (0,-1,0), # down
    ( 0,0,1), # forward
    (0,0,-1), # backward
    ]

colors = [
    (0,192,0), # green
    (255,64,0), # red
    (0,64,255), # blue
    (128,0,255) # violet
]    

names = [
    "GREEN",
    "RED",
    "BLUE",
    "VIOLET"
    ]
grid = [ None ] * 512
nplayers = 4
players = [ None ] * nplayers
wrap = True
targets = []
BLACK = (0,0,0)
WHITE = (255,255,255)
socket_to_player = {}

class Server(WebSocket):
    def send(self,o):
        self.sendMessage(unicode(json.dumps(o)));
    def handleMessage(self):
        try:
            msg = json.loads(self.data)
            #print self.address, msg
            try:
                player = socket_to_player[self.address]
            except KeyError:
                player = None

            if 'player' in msg:
                player = int(msg['player'])
                socket_to_player[self.address] = player
                print "setting player to %d" % player
                if not players[player]:
                    players[player] = Player(player)
                    players[player].ws = self
                self.send({'colname':names[player],'col':("#%02x%02x%02x" % players[player].col)})
            elif 'key' in msg:
                assert(player is not None)
                key = int(msg['key'])
                assert (key>=0 and key<=5)
                print "%d pressed key %d" % \
                    (player, int(msg['key']))
                # as a courtesy prevent players reversing into themselves
                if tuple(map(sum,zip(dirs[players[player].dir],dirs[key]))) != (0,0,0):
                    players[player].dir = key
        except:
            traceback.print_exc()
            raise
        
    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')
        pl = socket_to_player[self.address]
        assert(pl)
        assert(pl.socket == self)
        del socket_to_player[self.address]
        pl.ws = None
        
server = SimpleWebSocketServer('', 27681, Server, selectInterval=1e-6)

def move(pos,dir):
    newpos = tuple(map(sum,zip(pos,dirs[dir])))
    for i in range(3):
        if newpos[i] < 0 or newpos[i] >= SZ:
            if wrap:
                newpos = list(newpos)
                newpos[i] %= SZ
                newpos = tuple(newpos)
            else:
                return None
    return newpos

def get(pos):
    return grid[pos[0]+SZ*(pos[1]+SZ*pos[2])]

def set(pos,obj):
    grid[pos[0]+SZ*(pos[1]+SZ*pos[2])] = obj
    
def spawn():
    while True:
            pos0 = random.randrange(0,8)
            pos1 = random.randrange(0,8)
            pos2 = random.randrange(0,8)
            if get((pos0,pos1,pos2)):
                continue
            if not wrap:
                # bias spawning towards the centre
                sz2 = (SZ/2)-0.5
                sz22 = (SZ/2)+0.5
                c0 = pos0-sz2
                c1 = pos1-sz2
                c2 = pos2-sz2
                dist = (c0*c0+c1*c1+c2*c2)/sz22/sz22
                if dist>1 and random.random()*dist>1: # CHECKME
                    print "bad: %d %d %d %f" % (pos0,pos1,pos2,dist)
                    continue
            return (pos0,pos1,pos2)
                
class Player():
    speed = 12 # ticks per move
    cells = []
    col = None
    score = 0
    maxlen = 3 # max initial length
    dir = 1 # index into dirs array
    respawn_delay = 5 * FPS
    flashtime = 0.1*FPS
    dyingtime = 1.0*FPS
    ready_delay = 2.0 * FPS
    READY = 0
    ALIVE = 1
    DYING = 2
    DEAD  = 3
    state = None
    
    ws = None # socket connection
    index = 0
    def __init__(self,i):
        self.index = i
        self.col = colors[self.index]
        self.spawn()

    def spawn(self):
        print "spawning"
        for c in self.cells:
            set(c,None)
        for x in range(8):
            for y in range(8):
                for z in range(8):
                    if get((x,y,z))==self:
                        print "%d %d %d" % (x,y,z)
                        assert(False)
        self.state = self.READY
        self.cells = [spawn()]
        self.dir = 1
        self.speed = 15
        self.ticksleft = self.ready_delay
        for c in self.cells:
            set(c,self)
        
    def tick(self):
        if self.state != self.ALIVE:
            if self.state == self.DYING:
                self.ticksleft -= 1
                if self.ticksleft<0:
                    self.state = self.DEAD
                    self.ticksleft = self.respawn_delay
                    for c in self.cells:
                        set(c,None)
                return
            if self.state == self.READY:
                self.ticksleft -= 1
                if self.ticksleft<0:
                    self.state = self.ALIVE
                    self.ticksleft = 0
                return
            if self.state == self.DEAD:
                if self.ws:
                    self.ticksleft -= 1
                    if self.ticksleft<0:
                        self.spawn()
                else:
                    print "no socket"    
                return
                
        
        self.ticksleft -= 1
        #print "ticksleft %d" % self.ticksleft
        if self.ticksleft>0:
            return
        self.ticksleft += self.speed
        head = self.cells[0]
        newhead = move(head,self.dir)
        #print "newhead",newhead
        #print "len",len(self.cells)
        eaten = False
        dead = False
        
        if not newhead:
            print "hit edge"
            dead = True
        else:
            obj = get(newhead)
            typ = type(obj)
            #print obj, typ
            if isinstance(obj, Player):
                print "hit player"
                dead = True
            elif isinstance(obj,Target):
                print "yum"
                eaten = True
                self.score += 1
                self.speed -= 1 # FIXME
            
        if dead:
            # insert death sfx here
            self.state = self.DYING
            self.ticksleft = self.dyingtime
            #if self.ws:
            self.ws.send({'gameover':self.score})
            return

        set(newhead, self)

        if eaten or len(self.cells) < self.maxlen:
            # grow
            self.cells = [newhead] + self.cells
        else:
            # erase tail
            tail = self.cells[-1]
            #print "tail",tail
            set(tail, None)
            self.cells = [newhead] + self.cells[:-1]

    def color(self,x,y,z):
        if self.state==self.ALIVE or self.state==self.READY:
            # head should be brighter
            if self.cells[0] == (x,y,z):
                return cubehelper.mix_color(self.col,WHITE,0.5)
            else:
                return self.col
        elif self.state == self.DYING:
            if self.respawn_delay-self.ticksleft<self.flashtime:
                return WHITE # flash at moment of impact
            # fade for 1 sec
            mix = self.ticksleft / self.dyingtime
            #print "mix=%f" % mix
            #if mix > 1: mix = 1
            return cubehelper.mix_color(BLACK,self.col,mix)
        else: # dead
            assert(self.state == self.DEAD)
            return BLACK

class Target():
    color1 = (255,128,0)
    color2 = (255,255,128)
    spawn_delay = 0.5*FPS
    spawn_timer = 0
    animtime = 1.0*FPS # pulse time
    growtime = 1.0 * FPS # fade in time after spawning
    def __init__(self):
        self.spawn()
    def spawn(self):
            self.pos = spawn()
            set(self.pos,self)
            self.ticks = 0
        
    def tick(self):
        #print "target tick"
        if get(self.pos)!=self:
            # we were eaten
            # insert eaten sfx here
            self.spawn()
            
        self.ticks += 1
        if self.ticks >= self.growtime + self.animtime:
            self.ticks -= self.animtime
        
    def color(self,x,y,z):
        if self.ticks < self.growtime:
            return cubehelper.mix_color(BLACK,self.color1,self.ticks/self.growtime)
        else:
            t = (2.0*(self.ticks-self.growtime) / self.animtime)-1
            mix = 1-t*t
            #print "mix %f %f" % (t,mix)
            return cubehelper.mix_color(self.color1,self.color2,mix)
    
class Pattern(object):
    def init(self):
        assert (SZ == self.cube.size)
        self.double_buffer = True
        #p = Player()
        #players.append(p)
        t = Target()
        targets.append(t)
        t = Target()
        targets.append(t)
        return 1.0/FPS
    def tick(self):
        server.serveonce()
        self.cube.clear()

        for p in players:
            if p:
                p.tick()
        for t in targets:
            t.tick()
        
        for x in range(0, SZ):
            for y in range(0, SZ):
                for z in range(0, SZ):
                    p = grid[x+SZ*(y+SZ*z)]
                    if p:
                        self.cube.set_pixel((x,y,z), p.color(x,y,z))
                    else:
                        self.cube.set_pixel((x,y,z), BLACK)

                        
                        #raise StopIteration

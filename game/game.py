from turtle import Screen, Turtle, mainloop, register_shape
from fus import Fu, fus, STATIC_SQUARE
from weapons import Weapon, weapons
from valid import SEP
from fight import fight
from board import board_shape as divs
import game
import math
import moves

swid            = 800   # screen width
margin          = 0.15  # edge - keep for top/bottom
aspect          = 1.5   # more space left/right
span            = swid * (1 - margin) / divs    # cell width
x_origin        = -swid/2 + (margin * swid)/2
y_origin        = swid/2 - (margin * swid)/2

F               = {}
F_Pos           = {}
W               = {}
W_Pos           = {}
static_player   = None

def build_board(divs):
    ''' build 13 x 13 board '''
    g = Turtle() # grid pen
    g.hideturtle()  # we don't have to see the blob
    g.shape('circle')
    g.pencolor((100,100,100))
    g.speed(0)
    g.penup() # avoid line from center to start top-left

    def gofwd(angle, x, y):
        g.setheading(angle)
        g.setposition(x, y)
        g.pendown()
        g.forward(span * divs)
        g.penup()

    for i in range(divs + 1):
        gofwd(angle=90, x=x_origin, y=y_origin - i * span)  # horizontal
        gofwd(angle=180, x=i * span + x_origin, y=y_origin) # vertical

class SuperTurtle(Turtle):
    ''' superclass for game battle objects '''
    
    def __init__(self, **kwargs):
        super().__init__(kwargs['shape'])
        self.fillcolor(kwargs['fillcolor'])
        self.speed(kwargs['speed'])
        self.penup()
        self.setposition(kwargs['x'], kwargs['y'])
        self.resizemode('user')
    
    def plus(self, what, much):
        ''' adds much to what for subclasses '''
        what += much
        return what

class FuTurtle(SuperTurtle, Fu):
    index = -1   # to be unique per Fu
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Fu.__init__(self, kwargs['name'], (kwargs['x'], kwargs['y']))
        FuTurtle.index = self.index = self.plus(FuTurtle.index, 1)
        self.shapesize(2, 2, outline=4)
    def __repr__(self):
        return self.name[0]

class WpTurtle(SuperTurtle, Weapon):
    index = -1
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Weapon.__init__(self, kwargs['name'], (kwargs['x'], kwargs['y']))
        WpTurtle.index = self.index = self.plus(WpTurtle.index, 1)
        self.shapesize(0.7, 0.7)   
    def __repr__(self):
        return self.name[0]

def create_screen(divs):
    s = Screen()
    s.mode('logo')           
    s.setup(width=swid * aspect, height=swid)
    s.colormode(255)        # allow rgb specifications
    s.bgcolor("white")

def get_helmet_shape(rad):
    helmet = [(0,0),(-rad,0), (-rad,-rad/2), (-rad,0),  # left inverted L
                (rad,0), (rad,-rad/2), (rad,0),         # right inverted L
                (0,0), (0,rad/2),                       # stem up
            ]
    return helmet

def get_face_shape(rad):
    # y: sin(ang) = y / rad; x: cos(ang) = x / rad 
    tuplist = []
    sides   = 8
    sliced  = 360 / sides
    for s in range(sides + 1):
        angle = s * sliced
        tuplist.append(
            ( 
                math.sin(math.radians(angle)) * rad,
                math.cos(math.radians(angle)) * rad 
            )
        )
    return tuplist

def get_weapon_shape():
    shape = ((10, 10), (-10, -10), (0,0), (-10, 10), (10, -10), (0,0))
    return shape

def shapes():
    ''' register shapes Fu and Wp '''
    rad     = 10 # radius for polygon
    weapon  = get_weapon_shape()
    helmet  = get_helmet_shape(rad)
    tuplist = get_face_shape(rad)
    tuplist.extend(helmet)
    register_shape("Fu", tuple(tuplist))
    register_shape("Wp", weapon)

def convert_cord(xcord, ycord):
    ''' convert from x,y of 13x13 to Turtle pos '''
    fx_origin = x_origin + span/2
    fy_origin = y_origin - span/2
    x, y = fx_origin + xcord * span, fy_origin - ycord * span
    return x, y

def create_turtles(typ, t, T, T_Pos):
    ''' call class to instantiate objects '''

    name, ycord, xcord = t[0], t[1][0], t[1][1]
    weap_rgb = (255,255,255)
    rgb = t[2] if typ == 'Fu' else weap_rgb

    global static_player
    x, y = convert_cord(xcord, ycord)
    if typ == 'Fu':
        t = FuTurtle(shape="Fu", fillcolor=rgb, speed=4, name=name, x=x, y=y)
        if t.static: static_player = t
    elif typ == 'Wp':
        t = WpTurtle(shape="circle", fillcolor=rgb, speed=8, name=name, x=x, y=y)
        if t.static:
            static_player.pick_weapon([t])

    T[name[0]] = t                  # alphas for obj
    T_Pos[(int(x), int(y))] = [t]   # positions as keys

def load_turtles():
    ''' create Fus and weapons '''
    global F; global F_Pos
    global W; global W_Pos
    for f in fus:
        create_turtles('Fu', f, F, F_Pos)
    for w in weapons:
        create_turtles('Wp', w, W, W_Pos)

def tuptoint(tup):
    ''' convert positions to int so better as hashes '''
    return int(tup[0]), int(tup[1])

def drowned(f):
    if \
    (abs(f.position()[0]) < abs(x_origin) + 1 and \
            abs(f.position()[1]) < abs(y_origin) + 1):  # i.e. not drowned
        return False
    else: return True

def warmup(f_pos_new):
    ''' settings before fight '''
    ring = F_Pos[f_pos_new]
    df = ring[0]; at = ring[1]
    df.speed(0)
    at.speed(0)
    print('def', df, '<=>', 'att', at)
    return ring, at, df

def bell(angle, at, df, normal_speed):
    ''' bell rings - fight '''
    shift = 60
    revs = 3
    loop = int(360 / shift * revs)
    for _ in range(loop):
        angle += shift
        at.setheading(angle)
        df.setheading(angle)
    winner, loser = fight(at, df)
    winner.speed(normal_speed)
    if winner.weapon is not None:
        winner.weapon.forward(0) # so weapon shows atop
    print(winner, 'wins')
    print('scores:', winner.battle_score, 'to', loser.battle_score)
    return winner, loser

def final_rites(ring, loser):
    ''' final rites for loser '''
    ring.remove(loser)
    loser.alive = False
    loser.speed(6)
    los_x = swid/2
    los_y = swid/2 - margin * swid/2 - span/2 - span * loser.index
    loser.setposition(los_x, los_y)
    loser.curpos = (los_x, los_y)
    if loser.weapon is not None:
        loser.weapon.owner = None
        loser.weapon = None 

def update_position(which, t_pos, t, T_Pos):
    ''' update dict tracking what's on which square '''
    if which == 'old':
        if t_pos in T_Pos:
            if t in T_Pos[t_pos] and len(T_Pos[t_pos]) > 1:
                T_Pos[t_pos].remove(t)
            else: del T_Pos[t_pos]
    elif which == 'new':
        if t_pos not in T_Pos:
            T_Pos[t_pos] = [t]
        else:
            T_Pos[t_pos].append(t)
        t.curpos = t_pos

def play():
    ''' play the game '''
    
    orientation = {'N': 0, 'S': 180, 'E': 90, 'W': 270}
    glide = 12
    mm = 0
    for move in moves.get_moves():
        
        # who's moving
        actor, direction = move.split(SEP)
        f = F[actor]
        if f.static : continue
        if not f.alive: continue

        has_weapon = False if f.weapon is None else True
        
        print('-'*40)
        print(mm:=mm+1, f, '->', direction)

        # set angle
        angle = orientation[direction]
        f.setheading(angle)
        if has_weapon:
            f.weapon.setheading(angle)

        # move
        f_pos_old = tuptoint(f.position())
        step = span/glide
        for _ in range(glide):
            f.forward(step)
            if has_weapon:
                f.weapon.forward(step)
        f_pos_new = tuptoint(f.position())

        # update board tracking
        occupied = f_pos_new in F_Pos
        update_position('old', f_pos_old, f, F_Pos)
        update_position('new', f_pos_new, f, F_Pos)

        # fight if occupied
        if occupied:
            print('someone here already -> ', F_Pos[f_pos_new][0])
            normal_speed = f.speed()
            ring, at, df = warmup(f_pos_new)
            winner, loser = bell(angle, at, df, normal_speed)
            final_rites(ring, loser)
            if loser == f: 
                continue

        # update weapons tracking dict
        if has_weapon:
            update_position('old', f_pos_old, f.weapon, W_Pos)
            update_position('old', f_pos_new, f.weapon, W_Pos)
        else:
            # pick any weapons
            if f_pos_new in W_Pos:
                f.pick_weapon(W_Pos[f_pos_new])
                f.weapon.forward(0) # so weapon shows atop

def main():
    create_screen(divs)    
    build_board(divs)
    shapes()
    load_turtles()
    play()
    return "GAME OVER"

if __name__ == '__main__':
    msg = main()
    print(msg)
    mainloop()
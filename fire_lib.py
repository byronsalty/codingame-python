import sys
import math
import random

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

height = 12
width = 12

# pulled out for testing purposes
randomizer = random.choice

# Helpers 
def dist(x1, y1, x2, y2):
    return abs(x2-x1) + abs(y2-y1)
    
def pick_top(choices, scores):
    return pick_by(choices, scores, max)

def pick_by(choices, scores, fn):
    found = fn(scores)
    for i in range(len(choices)):
        if scores[i] == found:
            return choices[i]
    return "no pick found"

def find_closest_spot(x, y, spots):
    distances = [dist(x, y, sp[0], sp[1]) for sp in spots]
    return pick_by(spots, distances, min)

# Building functions
def pick_spot(troops, spot_list):
    print >> sys.stderr, "picking from: %s" % spot_list
    troop_spots = [(x,y) for owner,unit_id, level, dispo, x, y in troops]
    remaining = [sp for sp in spot_list if sp not in troop_spots]
    
    print >> sys.stderr, "remaining: %s" % remaining
    if len(remaining) == 0:
        return (-1,-1)
    else:
        chc = randomizer(remaining)
        print >> sys.stderr, chc
        return chc
        

def valid_move(board, x, y):
    if x >= 12 or x < 0:
        return False
    if y >= 12 or y < 0:
        return False
        
    return board[y][x] != "#" and board[y][x] != "H"
    
values = {
    "O": 0,
    "#": 0,
    "o": 1,
    ".": 2,
    "x": 3,
    "X": 4
    }
    
# Dispositions
# -- Explorer (find open space)
# -- HQ Guardian (stay near HQ - fight attackers)
# -- Fighter (find enemies to fight)
# -- Winner (go for enemy HQ)
WINNER = 0
EXPLORER = 1
HQ_GUARDIAN = 2
FIGHTER = 3
UNKNOWN = 4

UPKEEPS = [1,4,20]


def get_dispo_choices(turn, unit_level):
    if unit_level == 3:
        return [FIGHTER, 
                FIGHTER, 
                WINNER]
    elif turn < 10:
        return [WINNER, 
                WINNER, 
                EXPLORER, 
                EXPLORER,
                EXPLORER, 
                EXPLORER]
    elif turn < 30:
        return [WINNER, 
               WINNER, 
               EXPLORER, 
               EXPLORER, 
               FIGHTER]
    else:
        return [WINNER, 
                WINNER, 
                HQ_GUARDIAN, 
                HQ_GUARDIAN, 
                FIGHTER]

def value_spot(board, x, y):
    s = board[y][x]
    return values[s]
    
def list_owned_spots(board):
    acc = []
    for y in range(height):
        for x in range(width):
            if board[y][x] == "O" or board[y][x] == "H":
                acc.append((x,y))
    return acc
    
def list_by_owner_type(buildings, owner, ty):
    filtered = filter(lambda b: b[0] == owner and b[1] == ty, buildings)
    return map(lambda b: (b[2], b[3]), filtered)

def list_not_owned_spots(board):
    acc = []
    for y in range(height):
        for x in range(width):
            sp = board[y][x]
            if sp != "#" and sp != "O" and sp != "H":
                acc.append((x,y))
    return acc
    
def list_owned_adj_spots(board):
    acc = []
    owned = list_owned_spots(board)
    for x,y in list_not_owned_spots(board):
        if ((x-1, y) in owned) or ((x+1, y) in owned) or ((x, y-1) in owned) or ((x, y+1) in owned):
            acc.append((x,y))
    return acc
    
    
def gen_near_spots(board, x, y):
    near = [(-1,-1), (0,-1), (1,-1), (-1,0), (1, 0), (-1, 1), (0, 1), (1,1)]
    moves = map(lambda m: (x+m[0], y+m[1]), near)
    valid_moves = filter(lambda m: valid_move(board, m[0], m[1]), moves)
    return valid_moves
    
def gen_adj_spots(board, x, y):
    adj = [(-1,0), (1,0), (0,-1), (0,1)]
    moves = map(lambda m: (x+m[0], y+m[1]), adj)
    valid_moves = filter(lambda m: valid_move(board, m[0], m[1]), moves)
    return valid_moves
    

    
def value_near(board, x, y):
    near = gen_near_spots(board, x, y)
    scores = map(lambda m: value_spot(board, m[0], m[1]), near)
    total = reduce(lambda a, b: a+b, scores)
    return 

def rate_spawn(board, x, y):
    spots = gen_adj_spots(board, x, y)
    rated_spots = map(lambda m: value_near(board, m[0], m[1]), spots)
    best_spot = pick_top(spots, rated_spots)
    return best_spot[0], best_spot[1]

def spawn_coords_old(board, x, y, tx, ty):
    owned = list_owned_spots(board)
    scored_owned = map(lambda m: rate_spawn(board, m[0], m[1]), owned)
    best_spot = pick_top(owned, scored_owned)
    nx, ny = get_move(board, best_spot[0], best_spot[1], tx, ty)
    print >> sys.stderr, "adj: %s" % list_owned_adj_spots(board)
    return nx, ny
    
def spawn_coords(board, x, y, tx, ty):
    adj = list_owned_adj_spots(board)
    nx, ny = randomizer(adj)
    #scored_owned = map(lambda m: rate_spawn(board, m[0], m[1]), owned)
    #best_spot = pick_top(owned, scored_owned)
    #nx, ny = get_move(board, best_spot[0], best_spot[1], tx, ty)
    print >> sys.stderr, "adj: %s" % list_owned_adj_spots(board)
    return nx, ny
    
# enemies.append((owner,unit_id, level, dispo, x, y))
def find_enemy_by_id_or_closest(eid, enemies, x, y):
    found = [e for e in enemies if e[1] == eid]
    if eid == -1 or len(found):
        return randomizer(enemies)
    else:
        return found[0]
        
    
    
def get_level(turn, gold, income):
    if income > 20:
        lvl = 3
    elif income > 4:
        lvl = 2
    else:
        lvl = 1
    return lvl, UPKEEPS[lvl-1]
    
    
def rate_move(board, x, y, nx, ny, tx, ty):
    score = 0
    if dist(nx, ny, tx, ty) < dist(x, y, tx, ty):
        score += 5
    if board[ny][nx] == "#":
        score += -100
    if board[ny][nx] == ".":
        score += 3
    if board[ny][nx] == "x":
        score += 4
    if board[ny][nx] == "X":
        score += 5
        
    return score
    
    
def get_move(board, x, y, tx, ty):
    moves = [(-1,0), (1,0), (0,-1), (0,1)]
    moves = filter(lambda m: valid_move(board, x+m[0], y+m[1]), moves)
    print >> sys.stderr, "moves: %s" % moves
    scores = map(lambda m: rate_move(board, x, y, x+m[0], y+m[1], tx, ty), moves)
    top = max(scores)
    for i in range(len(moves)):
        if scores[i] == top:
            return x+moves[i][0], y+moves[i][1]
    return x, y
    
def get_move_by_depo(board, buildings, enemies, troops, x, y):
    pass
        
        
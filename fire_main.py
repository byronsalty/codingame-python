import sys
import math
import random

import fire_lib
       
        
mines = []
number_mine_spots = int(raw_input())
for i in xrange(number_mine_spots):
    x, y = [int(j) for j in raw_input().split()]
    mines.append((x,y))
    print >> sys.stderr, "mine x=%s y=%s" % (x,y)
    

tx = ty =-1
ehq_x = ehq_y = -1
hq_x = hq_y = -1

# game loop
turn = 0 
unit_state = {}

while True:
    turn += 1
    gold = int(raw_input())
    income = int(raw_input())
    opponent_gold = int(raw_input())
    opponent_income = int(raw_input())
    
    
    board = []
    buildings = []
    troops = []
    enemies = []
    cmd = ""
    
    print >> sys.stderr, "gold=%s income=%s" % (gold, income)
    print >> sys.stderr, "opponents gold=%s income=%s" % (opponent_gold, opponent_income)
    
    
    for i in xrange(12):
        line = raw_input()
        board.append(list(line))
        
    building_count = int(raw_input())
    for i in xrange(building_count):
        owner, building_type, x, y = [int(j) for j in raw_input().split()]
        if building_type == 0:
            if owner == 1:
                ehq_x = x
                ehq_y = y
            else:
                hq_x = x
                hq_y = y
                
                board[y][x] = "H"
        buildings.append((owner, building_type, x, y))
        print >> sys.stderr, "building: o=%s x=%s y=%s" % (owner, x, y)
        
    unit_count = int(raw_input())
    for i in xrange(unit_count):
        owner, unit_id, level, x, y = [int(j) for j in raw_input().split()]
        dispo = UNKNOWN
        if owner == 0:
            if unit_state.has_key(unit_id):
                dispo = unit_state[unit_id]["dispo"]
            else:
                #create new dispo
                dispo = random.choice(get_dispo_choices(turn, level))
                state = {"dispo": dispo}
                unit_state[unit_id] = state
            troops.append((owner,unit_id, level, dispo, x, y))
        else:
            enemies.append((owner,unit_id, level, dispo, x, y))
        print >> sys.stderr, "unit: o=%s id=%s lvl=%s disp=%s x=%s y=%s" % (owner, unit_id, level, dispo, x, y)

    
    owned_spots = list_owned_spots(board)
    
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."
    
    #if turn % 3 == 1:
    if turn % 3 == 1:
        while gold > 15 or income > 2:
        #if gold >= 10 or income > 2:
            nx, ny = spawn_coords(board, hq_x, hq_y, ehq_x, ehq_y)
            lvl, cost = get_level(turn, gold, income)
            income = income - cost
            gold -= cost
            cmd += "TRAIN %s %s %s;" % (lvl, nx, ny)
            owned_spots.append((nx, ny))
            board[ny][nx] = "O"
            troops.append((0, 1000+turn, lvl, UNKNOWN, nx, ny))
    
    
    for o, unit_id, lvl, dispo, x, y in troops:
        if unit_id < 1000:
            if dispo == WINNER:
                tx = ehq_x
                ty = ehq_y
                print >> sys.stderr, "Winner! tx,ty=%s,%s" % (tx, ty)
            elif dispo == HQ_GUARDIAN:
                tx, ty = pick_spot(troops, gen_near_spots(board, hq_x, hq_y))
                ##tx, ty = random.choice(gen_near_spots(board, hq_x, hq_y))
            elif dispo == FIGHTER:
                if len(enemies) > 0:
                    eid = -1
                    if unit_state[unit_id].has_key("target_id"):
                        eid = unit_state[unit_id]["target_id"]
                    en = find_enemy_by_id_or_closest(eid, enemies, x, y)
                    unit_state[unit_id]["target_id"] = en[1]
                    tx = en[4]
                    ty = en[5]
                else:
                    tx = ehq_x
                    ty = ehq_y
                    
                print >> sys.stderr, "Fighter! tx,ty=%s,%s" % (tx, ty)
            elif dispo == EXPLORER:
                print >> sys.stderr, "looking at uid: %s" % unit_id
                print >> sys.stderr, unit_state
                if unit_state[unit_id].has_key("target_spot"):
                    tx, ty = unit_state[unit_id]["target_spot"]
                    if (tx == x and ty == y) or tx == -1:
                        tx, ty = pick_spot(troops, list_owned_adj_spots(board))
                        #tx, ty = random.choice(list_owned_adj_spots(board))
                else:    
                    tx, ty = pick_spot(troops, list_owned_adj_spots(board))
                print >> sys.stderr, "now targeting: %s,%s" % (tx, ty)
                unit_state[unit_id]["target_spot"] = (tx, ty)
            else:
                tx = ehq_x
                ty = ehq_y
                print >> sys.stderr, "Unknown disposition"
                
            print >> sys.stderr, "Unit target... id=%s d=%s = x,y=%s,%s" % (unit_id, dispo, tx, ty)
            nx, ny = get_move(board, x, y, tx, ty)
            cmd += "MOVE %s %s %s;" % (unit_id, nx, ny)
            owned_spots.append((nx, ny))
        
    if gold > 25:
        for sp in owned_spots:
            if sp in mines and sp not in list_by_owner_type(buildings, 0, 1):
                cmd += "BUILD MINE %s %s;" % (sp[0], sp[1])
        
    cmd += "MSG Let's do this!"
    
    print cmd
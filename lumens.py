import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


    
room = []

n = int(raw_input())
l = int(raw_input())

around = [(-1,-1), (0,-1), (1,-1), (-1,0), (1, 0), (-1, 1), (0, 1), (1,1)]

def inBounds(x, y):
    if x < 0 or x >= n:
        return False
    if y < 0 or y >= n:
        return False
    if room[y][x] == "X":
        return True
    else:
        return False


def place(x,y,val):
    room[y][x] = val

def touching(x, y, val):
    for dx, dy in around:
        nx, ny = x + dx, y + dy
        if inBounds(nx, ny):
            place(nx, ny, val)
            
            


for i in xrange(n):
    room.append(raw_input().split(" "))
    
print >> sys.stderr, room
    



# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

for y in xrange(n):
    for x in xrange(n):
        if room[y][x] == "C":
            room[y][x] = l
            

print >> sys.stderr, room

last = l
while last > 0:
    for y in xrange(n):
        for x in xrange(n):
            if room[y][x] == last:
                touching(x, y, last-1)
    last -= 1
    
    print >> sys.stderr, room
                
    

for y in xrange(n):
    for x in xrange(n):
        if room[y][x] == "X":
            room[y][x] = 0

print >> sys.stderr, room
            
cnt = 0

for y in xrange(n):
    for x in xrange(n):
        if room[y][x] == 0:
            cnt += 1
            

print cnt

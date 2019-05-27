import sys
import math

# Don't let the machines win. You are humanity's last hope...

board = []
around = [(-1,0), (0,-1)]

width = int(raw_input())  # the number of cells on the X axis
height = int(raw_input())  # the number of cells on the Y axis
for i in xrange(height):
    line = raw_input()  # width characters, each either 0 or .
    board.append(list(line))
    
# grid fill solution from another coder
# grid = [raw_input() for _ in xrange(height)]
    
print >> sys.stderr, "width: %s, height: %s" % (width, height)
print >> sys.stderr, board
    
def found(x,y):
    return board[y][x] == "0"
    
def checkRight(x,y):
    if x + 1 >= width:
        return "-1 -1"
    if found(x+1, y):
        return "%s %s" % (x+1, y)
    else:
        return checkRight(x+1, y)
        
def checkDown(x,y):
    if y + 1 >= height:
        return "-1 -1"
    if found(x,y+1):
        return "%s %s" % (x, y+1)
    else:
        return checkDown(x, y+1)
    
for y in xrange(height):
    for x in xrange(width):
        if found(x,y):
            print("%s %s %s %s" % (x, y, checkRight(x,y), checkDown(x,y)))
        


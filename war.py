import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q','K', 'A']

def compare(cd1, cd2):
    return cards.index(cd2[:-1]) - cards.index(cd1[:-1])
    
def draw(deck):
    card = deck[0]
    return card, deck[1:]
    

p1_deck = []
p2_deck = []

n = int(raw_input())  # the number of cards for player 1
for i in xrange(n):
    p1_deck.append(raw_input())  # the n cards of player 1
    
m = int(raw_input())  # the number of cards for player 2
for i in xrange(m):
    p2_deck.append(raw_input()) # the m cards of player 2
    
    
def fight(d1, d2, s1, s2):
    
    c1, d1 = draw(d1)
    c2, d2 = draw(d2)
    
    
    s1.append(c1)
    s2.append(c2)
    
    result = compare(c1,c2)
    if result < 0:
        d1 += s1
        d1 += s2
    elif result > 0:
        d2 += s1
        d2 += s2
    else:
        #war
        if len(d1) < 4 or len(d2) < 4:
            return [], []
        else:
            for i in range(3):
                c1, d1 = draw(d1)
                c2, d2 = draw(d2)
                
                s1.append(c1)
                s2.append(c2)
            
            return fight(d1, d2, s1, s2)
                
    
    return d1, d2
    
print >> sys.stderr, "p1: %s" % p1_deck
print >> sys.stderr, "p2: %s" % p2_deck

round = 0

while len(p1_deck) > 0 and len(p2_deck) > 0:
    round += 1
    
    p1_deck, p2_deck = fight(p1_deck, p2_deck, [], [])
    
        
    
    

print >> sys.stderr, "p1: %s" % p1_deck
print >> sys.stderr, "p2: %s" % p2_deck



# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

#print "PAT"

if len(p1_deck) > len(p2_deck):
    print "1 %s" % round
elif len(p1_deck) < len(p2_deck):
    print "2 %s" % round
else:
    print "PAT"

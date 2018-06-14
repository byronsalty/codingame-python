
# Angle+Speed to X,Y
t = math.radians(float(raw_input()))
r = float(raw_input())

x,y = [r * math.cos(t), r * math.sin(t)]

print "%s, %s" % (round(x,1), round(y, 1))

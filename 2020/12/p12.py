lines = []
for line in open('input.txt'):
    line = line.strip()
    lines.append(line)

# Test input
xlines = '''
F10
N3
F7
R90
F11
'''.split()

wx, wy = 10, 1
x,y = 0,0
sx,sy = 0,0
dx,dy = 1,0
for line in lines:
    D = line[0]
    amt = int(line[1:])

    if D=='N':
        y += amt
        wy += amt
    elif D=='S':
        y -= amt
        wy -= amt
    elif D=='W':
        x -= amt
        wx -= amt
    elif D=='E':
        x += amt
        wx += amt
    elif (D=='R' and amt==90) or (D=='L' and amt==270):
        dx, dy = dy, -dx
        wx, wy = wy, -wx
    elif (D=='L' and amt==90) or (D=='R' and amt==270):
        dx, dy = -dy, dx
        wx, wy = -wy, wx
    elif D in 'LR' and amt==180:
        dx, dy = -dx, -dy
        wx, wy = -wx, -wy
    elif D=='F':
        assert dx==0 or dy==0
        x += amt*dx
        y += amt*dy

        sx += amt*wx
        sy += amt*wy


    else:
        assert False, line

    #print(line, x, y, dx, dy, abs(x)+abs(y))
    print(line, sx, sy, wx, wy)

print(x, y, abs(x) + abs(y))
print(sx, sy, abs(sx) + abs(sy))

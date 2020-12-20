from collections import defaultdict

# Parse the input
tiles = defaultdict(list)
for line in open('input.txt'):
    line = line.strip()
    if 'Tile' in line:
        num = int(line[5:-1])
    elif line:
        tiles[num].append(line)

# Left and right border helpers.  Top/bottom
# are simple enough to do inline.
def border_left(tile):
    return ''.join(t[0] for t in tile)
def border_right(tile):
    return ''.join(t[-1] for t in tile)

# Reverse vertical, reverse horizontal, and transpose.
# Together, these transforms obviate the need for rotation/flip.
def rv(tile):
    return tile[::-1]
def rh(tile):
    return [t[::-1] for t in tile]
def tt(tile):
    return [(''.join(t[n] for t in tile)) for n in range(len(tile))]

# Return all permutations of a tile.
def perms(tile):
    outs = [tile, tt(tile)]
    outs += [rv(o) for o in outs]
    outs += [rh(o) for o in outs]
    return outs

# Build an index of border -> [tile ids].
cornerprod=1
tcorners=[]
tsides=[]
borders = defaultdict(set)
for tileid, tile in tiles.items():
    sides = [tile[0], tile[-1], border_left(tile), border_right(tile)]
    for s in sides:
        if s[::-1] < s:
            s = s[::-1]
        borders[s].add(tileid)

# Normalize border string.  Return the min of the string and its reverse
def ns(s):
    ss = s[::-1]
    return ss if ss<s else s

# Classify side and corner tiles, by seeing how often each of their
# borders appear in the border index.
for tileid, tile in tiles.items():
    sides = [tile[0], tile[-1], border_left(tile), border_right(tile)]
    singles=0
    for s in sides:
        s = ns(s)
        if len(borders[s])==1:
            singles+=1
    if singles==2:
        tcorners.append(tileid)
        cornerprod *= tileid
        print(tileid, 'corner')
    elif singles==1:
        tsides.append(tileid)

print(cornerprod)

# Slowly build the grid, keyed by (i,j) coordinate, with
# the value of the correctly-aligned tile for that cell.
grid = {}

# Test if a tile (tid is id, tile is the actual tile contents)
# can be fit into position (i,j).
def test(tid, tile, i, j):
    left = border_left(tile)
    right = border_right(tile)
    top = tile[0]
    bottom = tile[-1]

    if (i in [0,11]) and (j in [0,11]):
        if tid not in tcorners:
            return False

    if (i in [0,11]) and (j not in [0,11]):
        if tid not in tsides:
            return False

    if (j in [0,11]) and (i not in [0,11]):
        if tid not in tsides:
            return False

    if i==0 and len(borders[ns(left)])!=1:
        return False
    if i==11 and len(borders[ns(right)])!=1:
        return False
    if j==0 and len(borders[ns(top)])!=1:
        return False
    if j==11 and len(borders[ns(bottom)])!=1:
        return False
    if i>0 and left != border_right(grid[i-1,j]):
        return False
    if j>0 and top != grid[i,j-1][-1]:
        return False
    return True

for i in range(12):
    for j in range(12):
        # Quadratic version --- test every tile,
        # in a scanning order so that no mistakes
        # will be made.
        removes = []
        for tid, tile in tiles.items():
            for o in perms(tile):
                if test(tid, o, i, j):
                    grid[i,j] = o
                    removes.append(tid)
                    #print(i, j, tid)
                    break
            if (i,j) in grid: break
        if i==0 and j==0 and False:
            removes.pop()
            removes.pop()
            removes.pop()

        # New linear version follows
        # 1. for (0,0) just pick tcorners[0] (any of the 4 work)
        # 2. for every other index, use one of the borders either
        #    above or to the left to select the next tile, using
        #    the ONLY entry 
        if (i,j) == (0,0):
            removes = [tcorners[0]]
        else:
            if i:
                match_border = border_right(grid[i-1,j])
            else:
                match_border = grid[i,j-1][-1]
            # Find the tid that hasn't been used yet
            for tid in borders[match_border]:
                if tid in tiles: break
            removes = [tid]
        # Find the tile
        tile = tiles[tid]
        for ptile in perms(tile):
            if test(tid, ptile, i, j):
                grid[i,j] = ptile
                break

        assert len(removes) == 1, (i, j)
        for r in removes:
            del tiles[r]

monster = '''
                  #
#    ##    ##    ###
 #  #  #  #  #  #'''
#print(monster)
mlines = monster.split('\n')[1:]
#for L in mlines: print(L)
#print(mlines)

moff = set()
for j,line in enumerate(mlines):
    for i,c in enumerate(line):
        if c=='#': moff.add((i,j))
#print(moff)


chars = []
for x in range(12*8):
    chars.append(12*8*['x'])
for (i,j),tile in grid.items():
    for j2, line in enumerate(tile[1:-1]):
        for i2, c in enumerate(line[1:-1]):
            chars[8*i+i2][8*j+j2] = c

#for c in chars:
#    print(''.join(c))

indices = [(i,j) \
        for i in range(-50, 12*8+50) \
        for j in range(-50, 12*8+50)]

for ch in perms(chars):
    hashes = set()
    for j,line in enumerate(ch):
        for i,c in enumerate(line):
            if c=='#':
                hashes.add((i,j))

    mtiles = set()
    for (i,j) in indices:
        matches = set()
        for mi, mj in moff:
            a,b = i+mi, j+mj
            if (a,b) in hashes:
                matches.add((a,b))
        if len(matches) == len(moff):
            mtiles = mtiles.union(matches)
            #for (a,b) in matches:
            #    hashes.remove((a,b))

    print(len(hashes), len(mtiles), len(hashes) - len(mtiles))



from functools import lru_cache

lines = []
best = 0

for line in open('input.txt'):
    line = line.strip()
    lines.append(line)

cells = set()
for n,line in enumerate(lines):
    for m,c in enumerate(line):
        if c == '#': cells.add((n, m, 0))

def neighboors(x,y,z):
    return [(x+dx, y+dy, z+dz) for dx in range(-1,2) for dy in range(-1,2) for dz in range(-1,2) if dx or dy or dz]

for _ in range(6):
    new = set()

    # Still alive
    for x,y,z in cells:
        adj = sum((abc in cells) for abc in neighboors(x,y,z))
        if adj == 2 or adj == 3:
            new.add((x,y,z))

    # Newly alive
    checks = set()
    for xyz in cells:
        for abc in neighboors(*xyz):
            checks.add(abc)
    for xyz in checks:
        adj = sum((abc in cells) for abc in neighboors(*xyz))
        if adj == 3:
            new.add(xyz)

    cells = new

print(len(cells))







cells = set()
for n,line in enumerate(lines):
    for m,c in enumerate(line):
        if c == '#': cells.add((n, m, 0, 0))

def neighboors(x,y,z,w):
    return [(x+dx, y+dy, z+dz, w+dw) for dx in range(-1,2) for dy in range(-1,2) for dz in range(-1,2) for dw in range(-1, 2) if dx or dy or dz or dw]

for _ in range(6):
    new = set()

    # Still alive
    for xyzw in cells:
        adj = sum((abc in cells) for abc in neighboors(*xyzw))
        if adj == 2 or adj == 3:
            new.add(xyzw)

    # Newly alive
    checks = set()
    for xyzw in cells:
        for abcd in neighboors(*xyzw):
            checks.add(abcd)
    for xyzw in checks:
        adj = sum((abcd in cells) for abcd in neighboors(*xyzw))
        if adj == 3:
            new.add(xyzw)

    cells = new

print(len(cells))





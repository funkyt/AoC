from functools import lru_cache

lines = []
best = 0

for line in open('input.txt'):
    line = line.strip()
    lines.append(line)

M = len(lines)
N = max(len(line) for line in lines)

prev = {None}
curr = set()

def get(i, j):
    if i < 0 or i >= len(lines): return '.', 0
    if j < 0 or j >= len(lines[i]): return '.', 0
    return lines[i][j], ((i,j) in curr)

def scan(i, j, dx, dy):
    if i < 0 or i >= len(lines): return 0
    if j < 0 or j >= len(lines[i]): return 0
    if lines[i][j] == '.':
        return scan(i+dx, j+dy, dx, dy)
    else:
        return 1 if (i,j) in curr else 0


while prev != curr:
    prev = set(curr)
    next = set(curr)
    for i in range(M):
        for j in range(N):
            char, cur = get(i,j)
            close = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == dy == 0: continue
                    #close += get(i+dx, j+dy)[1]
                    close += scan(i+dx, j+dy, dx, dy)

            if char == '.':
                continue
            elif char == 'L':
                if cur == 0 and close==0:
                    next.add((i,j))
                #elif cur == 1 and close >= 4:
                elif cur == 1 and close >= 5:
                    next.discard((i,j))
    curr = next
    print(len(curr))



print(len(curr))

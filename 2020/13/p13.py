from functools import lru_cache

from math import gcd

lines = []
best = 0

for line in open('input.txt'):
    line = line.strip()
    lines.append(line)

start = int(lines[0])
print(start)

busses = [int(x) for x in lines[1].split(',') if x != 'x']
print(busses)

results = []
for b in busses:
    offset = b - start % b
    results.append((offset, b, b*offset))

results.sort()
print(results)


busses2 = [int(x) if x != 'x' else 0 for x in lines[1].split(',')]
print(busses2)



# pt2

time = 0
offset = 1
def lcm(x, y):
    return x * y // gcd(x,y)

for n,b in enumerate(busses2):
    if b==0: continue

    while time % b != ((b-n)%b):
        time += offset

    offset = lcm(offset, b)
    print(time, offset, b, n)


bdone = [1]

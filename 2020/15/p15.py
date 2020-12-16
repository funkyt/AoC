from functools import lru_cache

lines = []
best = 0

ranges = {}

mine = []
others = []

section = 0
for line in open('input.txt'):
    line = line.strip()

    if not line.strip():
        section += 1
        continue

    if section == 0:
        key, rest = line.split(':')
        r1, _, r2 = rest.strip().split(' ')
        r1 = tuple(int(x) for x in r1.split('-'))
        r2 = tuple(int(x) for x in r2.split('-'))
        ranges[key] = [r1, r2]

    if section == 1:
        if ':' in line: continue
        mine = [int(x) for x in line.split(',')]

    if section == 2:
        if ':' in line: continue
        other = [int(x) for x in line.split(',')]
        others.append(other)

def ok(num):
    for k,v in ranges.items():
        for a,b in v:
            if a<=num and num<=b: return True
    return False

bad = 0
kept = []
for ticket in others:
    toss = False
    for val in ticket:
        if not ok(val):
            bad += val
            toss = True
    if not toss:
        kept.append(ticket)
print(bad)

def test(keys):
    for ticket in kept:
        for index, key in enumerate(keys):
            ok = False
            for lo,hi in ranges[key]:
                if lo <= ticket[index] and ticket[index] <= hi: ok = True
            if not ok:
                return False
    return True

possible = {k:set(range(len(ranges))) for k in ranges}

import itertools
for keys in itertools.permutations(list(ranges.keys())[::-1]):
#for keys in itertools.permutations(list(ranges.keys())):
    if test(keys):
        print('FOUND', keys)

        total = 1
        for n,k in enumerate(keys):
            if 'departure' not in k: continue
            total *= mine[n]
            print(n, k, mine[n])
        print(total)
        break







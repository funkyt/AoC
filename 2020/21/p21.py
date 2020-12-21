def parse(line):
    if '(' not in line:
        return line.split(), []
    a,b = line.split('(')
    a = a[:-1]
    ing = a.split()
    b = b[len('contains '):-1]
    alg = [x.strip() for x in b.split(',')]
    return ing, alg

# alergen -> set of possible ingredients
allergen_map = {}
# All ingredients
ingredients = set()

import collections
appearances = collections.defaultdict(int)

for line in open('input.txt'):
#for line in open('in2.txt'):
    line = line.strip()

    ing, alg = parse(line)

    for x in ing:
        ingredients.add(x)
        appearances[x] += 1

    for a in alg:
        if a not in allergen_map:
            allergen_map[a] = set(ing)
        else:
            allergen_map[a] = allergen_map[a].intersection(set(ing))

safe = set(ingredients)
for k,v in allergen_map.items():
    for x in v:
        if x in safe:
            safe.remove(x)

print(sum(appearances[x] for x in safe))

# Do the bubble-sort style outer iteration --- slower than
# it needs to be, but simple enough to guarantee completion.
for _ in allergen_map.keys():
    for a,v in allergen_map.items():
        if len(v) == 1:
            ing = list(v)[0]
            for b,v2 in allergen_map.items():
                if a==b: continue
                if ing in v2:
                    v2.remove(ing)

ilist = [(k,list(v)[0]) for (k,v) in allergen_map.items()]
ilist.sort()
print(','.join(b for (a,b) in ilist))


lines = []
best = 0

valid = {}
contain = {}

elements = {}

for line in open('input.txt'):
    line = line.strip()

    outer, rest = line.split('bags contain')
    outer = outer.strip()

    rest = [r.strip() for r in rest.split(',')]

    size_color = []
    for r in rest:
        toks = r.split()
        if toks[0] == 'no':
            continue
        size = int(toks[0])
        col = ' '.join(toks[1:-1])
        size_color.append((size, col))

    rest = [' '.join(r.split()[1:-1]).rstrip('s.') for r in rest]

    elements[outer] = size_color




    valid[outer] = set(rest)
    for r in rest:
        if r not in contain: contain[r] = []
        contain[r].append(outer)
    #print(outer, rest)

candidates = {'shiny gold'}
prev = set()

while prev != candidates:
    prev = set(candidates)
    for p in prev:
        for out in contain[p] if p in contain else []:
            candidates.add(out)

print(len(candidates) -1 )


def size(bag):
    inners = elements[bag]
    print(inners)

    count = 1
    for (num, color) in inners:
        count += num * size(color)

    return count

print(size('shiny gold') - 1)

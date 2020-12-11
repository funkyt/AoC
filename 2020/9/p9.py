import itertools

lines = []
best = 0

for line in open('input.txt'):
    line = line.strip()
    lines.append(int(line))

for L in lines[:10]:
    print(L)
print(len(lines), 'lines')

for i in range(25, len(lines)):
    if lines[i] not in list(sum(s) for s in itertools.combinations(lines[i-25:i], 2)):
        key = lines[i]
        print(lines[i], i)
        break

for i in range(len(lines)):
    for j in range(i+2, len(lines)):
        if sum(lines[i:j]) == key:
            print(min(lines[i:j]) + max(lines[i:j]))




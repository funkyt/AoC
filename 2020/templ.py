from functools import lru_cache

lines = []
best = 0

for line in open('input.txt'):
    line = line.strip()
    lines.append(line)

print(len(lines), best)



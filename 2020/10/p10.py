lines = []
best = 0

for line in open('input.txt'):
#for line in open('in2.txt'):
    line = line.strip()
    lines.append(int(line))

lines.sort()

end = lines[-1]

print(lines)

print(len(lines))

delta = {1:0, 2:0, 3:1}
prev = 0
for line in lines:
    delta[line - prev] += 1
    prev = line

print(delta[1] * delta[3])

def ways():
    nums = lines + [0]
    nums.sort()
    counts = len(nums) * [0]
    counts[0] = 1
    for j in range(len(nums)):
        for k in range(j):
            if nums[j] - nums[k] <= 3:
                counts[j] += counts[k]
    print(counts[0:4], counts[-5:])
    print(counts[-1])
ways()


ways = (1 + len(lines)) * [0]
ways[0] = 1

for n,line in enumerate(lines):
    for j in range(n):
        if line - lines[j] <= 3:
            ways[n+1] += ways[j]
    #print(ways[:n+1])
print(lines)
print(ways)

print(ways[-1])

import functools

lines.append(0)
lines.sort()
@functools.lru_cache(200)
def count(n):
    if n == 0:
        return 1

    total = 0
    for j in range(0, n):
        if lines[n] - lines[j] <= 3:
            total += count(j)
    return total

print(count(len(lines)-1))

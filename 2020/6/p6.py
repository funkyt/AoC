count = 0

group = []

def flush():
    global count
    global group
    chars = {c for g in group for c in g}
    count += len(chars)
    print(count)
    flush2()

count2 = 0
def flush2():
    global count2
    chars = set('abcdefghijklmnopqrstuvwxyz')
    assert len(chars) == 26
    for g in group:
        chars = chars & set(g)
    count2 += len(chars)
    print(len(chars), count2)





for line in open('input.txt'):
    line = line.strip()
    if not line:
        flush()
        group = []
        continue
    group.append(line)
flush()

print(count)

print('done')


lines = []
best = 0

for line in open('input.txt'):
    line = line.strip()
    lines.append(line)

edges = {}
N = len(lines)
O = 2*N
for i in range(len(lines)):
    op, amt = lines[i].split()
    amt = int(amt)

    if op == 'acc':
        edges[i] = [i+1]
        edges[i+O] = [i+O+1]
    elif op == 'jmp':
        edges[i] = [i+O+1, i+amt]
        edges[i+O] = [i+O+amt]
    elif op == 'nop':
        edges[i] = [i+1, i+O+amt]
        edges[i+O] = [i+O+1]

pred = {}
pend = [0]
target = O+N
while target not in pred and pend:
    nxt = []
    for p in pend:
        for n in edges[p]:
            if n in pred:
                continue
            nxt.append(n)
            pred[n] = p

    pend = nxt

print(pred)

x = target
while x != 0:
    print(x)
    x = pred[x]


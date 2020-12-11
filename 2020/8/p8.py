lines = []
best = 0

for line in open('input.txt'):
    line = line.strip()
    lines.append(line)

print(len(lines))

def sim(lines):
    done = set()
    index = 0
    acc = 0
    while True:
        if index in done:
            return False, acc
        if index > len(lines) or index < 0:
            print('ack')
            return False, acc
        if index == len(lines):
            return True, acc
        done.add(index)
        toks = lines[index].split()
        if toks[0] == 'acc':
            acc += int(toks[1])
            index += 1
        elif toks[0] == 'nop':
            index += 1
        elif toks[0] == 'jmp':
            index += int(toks[1])
        else:
            print('oops')

print(sim(lines))

for n in range(len(lines)):
    prog = lines[:]
    if 'nop' in lines[n]:
        prog[n] = prog[n].replace('nop', 'jmp')
        a,b = sim(prog)
        if a:
            print(a, b)
            break
    if 'jmp' in lines[n]:
        prog[n] = prog[n].replace('jmp', 'nop')
        a,b = sim(prog)
        if a:
            print(a, b)
            break

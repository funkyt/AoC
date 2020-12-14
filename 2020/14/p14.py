from collections import defaultdict
from functools import lru_cache

lines = []
best = 0

for line in open('input.txt'):
    line = line.strip()
    lines.append(line)

test_lines = '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0'''.split('\n')

mem = defaultdict(int)
maskA = 0
maskB = int(38*'1', 2)
maskX = 0

for line in lines:
    if 'mask =' in line:
        text = line[7:]
        maskA = int(text.replace('X', '0'), 2)
        maskB = int(text.replace('1', 'X').replace('0', '1').replace('X', '0'), 2)
        maskX = int(text.replace('1', '0').replace('X', '1'), 2)
    else:
        addr = int(line[4:line.index(']')])
        value = int(line[line.index('=')+1:])

        mem[addr] = maskA | (maskX & value)

print(sum(mem.values()))



def bit_seq(num):
    index = 0
    indices = []
    text = bin(num)[2:][::-1]
    for i in range(len(text)):
        if text[i] == '1':
            indices.append(i)

    nums = [0]
    for index in indices:
        olds = nums
        nums = [old + 2**index for old in olds] + olds

    for n in nums:
        yield n


mem = defaultdict(int)
maskA = 0
maskB = int(38*'1', 2)
maskX = 0

for line in lines:
    # print(line)
    if 'mask =' in line:
        text = line[7:]
        maskA = int(text.replace('X', '0'), 2)
        maskB = int(text.replace('1', 'X').replace('0', '1').replace('X', '0'), 2)
        maskX = int(text.replace('1', '0').replace('X', '1'), 2)
    else:
        addr = int(line[4:line.index(']')])
        value = int(line[line.index('=')+1:])

        new_addr = (addr & maskB) | (maskA)
        for addr_mask in bit_seq(maskX):
            mem[new_addr | addr_mask] = value

print(sum(mem.values()))




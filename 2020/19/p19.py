from functools import lru_cache

# Each parser takes a (text:str, offset:int) tuple, and generates
# a sequence of matching offsets that it can consume up until.
#
# The 'parser_*' functions aren't parsers directly, but generate
# and return a parsing function for each construction.

def parser_char(c):
    '''parser for a single char'''
    def parse(text, offset):
        if offset < len(text) and text[offset] == c:
            yield offset+1
    return parse

def parser_num(n):
    '''parser as an indirection to a rule number'''
    def parse(text, offset):
        for off in rules[n](text, offset):
            yield off
    return parse

def parser_or(ps):
    '''parser as '|' over several sub-parsers'''
    ps = list(ps)
    def parse(text, offset):
        for p in ps:
            for off in p(text, offset):
                yield off
    return parse

def parser_seq_p(parsers):
    '''parser from sequence of parsers'''
    parsers = list(parsers)
    if len(parsers) == 1:
        return parsers[0]
    elif len(parsers) == 2:
        def parse(text, offset):
            for off1 in parsers[0](text, offset):
                for off2 in parsers[1](text, off1):
                    yield off2
        return parse
    else:
        return parser_seq_p([parsers[0], parser_seq_p(parsers[1:])])

def parser_seq(elems):
    '''parser_seq_p but elements could be '1 2 3' or [1, 2, 3] instead of list of parsers'''
    if type(elems) == str:
        elems = elems.strip().split(' ')
    elems = [parser_num(int(e)) for e in elems]
    return parser_seq_p(elems)

def parse(line):
    '''Attempt to parse a full line with rule #0'''
    for off in rules[0](line, 0):
        if off == len(line):
            return True
    return False

rules = {}
space = False
matches = 0
length = 0

#for line in open('in3'):
#for line in open('input.txt'):
for line in open('input.txt_pt2'):
    line = line.strip()

    if not line:
        space = True
        continue

    if not space:
        num, remain = line.split(':')
        num = int(num)

        rule = None
        if '|' in remain:
            rule = parser_or(parser_seq(r) for r in remain.split('|'))
        elif '"' in remain:
            rule = parser_char(remain.split('"')[1])
        elif ' ' in remain.strip():
            rule = parser_seq(remain.strip())
        else:
            rule = parser_num(int(remain))

        rules[num] = rule

    else:
        if parse(line.strip()):
            matches += 1

    length = max(length, len(line))

print('longest message', length)
print('matches', matches)

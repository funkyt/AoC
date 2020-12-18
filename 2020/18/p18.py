def eval(tokens):
    stack = [None]
    opstack = [None]
    for token in tokens:
        pending = None
        if token == '(':
            stack.append(None)
            opstack.append(None)
        elif token == ')':
            pending = stack.pop()
            opstack.pop()
        elif token == '+':
            opstack[-1] = lambda x, y : x + y
        elif token == '*':
            opstack[-1] = lambda x, y : x * y
        else:
            pending = int(token)

        if pending is not None:
            if stack[-1] is None:
                stack[-1] = pending
            else:
                stack[-1] = opstack[-1](stack[-1], pending)

    return stack[-1]

lines = []
total = 0
for line in open('input.txt'):
    line = line.strip()
    lines.append(line)
    tokens = line.replace('(', ' ( ').replace(')', ' ) ').split()
    total += eval(tokens)

print(total)

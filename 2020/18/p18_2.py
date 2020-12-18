class I:
    '''Simple int wrapper that reverses multiplication and addition'''
    def __init__(self, n):
        self.n = n
    def __add__(self, other):
        return I(self.n * other.n)
    def __mul__(self, other):
        return I(self.n + other.n)
    def __str__(self):
        return str(self.n)

total = 0
for line in open('input.txt'):
    # Reverse '+', '*', so that Python can evaluate them for us in the "right" order
    line = line.replace('+', 'P').replace('*','+').replace('P','*')
    # Convert all numbers 'n' to 'I(n)'.  Regex would be cleaner.  :)
    for n in range(10):
        line = line.replace(str(n), f'I({n})').strip()
    # Run the code as Python!!!
    exec('x = ' + line)
    total += x.n

print(total)


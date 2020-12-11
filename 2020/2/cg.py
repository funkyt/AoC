import contextlib

# Legal BF characters, plus '!' which is used as an input delimiter
# in many interpreters.
BF_CHARS = '+-<>[],.!'

# Rules that allow simplification of code.
simp_rules = [
        ('+-', ''),
        ('-+', ''),
        ('<>', ''),
        ('><', ''),
        ('[-][-]', '[-]'),
        ]

def simplify(code):
    code = ''.join(c for c in code if c in BF_CHARS)
    prev = None

    while code != prev:
        prev = code
        for p,r in simp_rules:
            code = code.replace(p, r)

    return code

def delta(n):
    return n*'+' if n>0 else (-n)*'-'
def shift(n):
    return n*'>' if n>0 else (-n)*'<'

class Int8:
    def size():
        return 1
    def init(cg, name):
        cg.begin()
        cg.at(name)
        cg.emit('[-]')
        cg.end()
    def set(cg, name, val):
        cg.begin()
        cg.at(name)
        cg.emit('[-]')
        cg.emit(delta(val))
        cg.end()

class Int16:
    def size():
        return 4
    def init(cg, name):
        cg.begin()
        cg.at(name)
        cg.emit('[-]>[-]>[-]>[-]+<<<')
        cg.end()

kinds = {'i8':Int8, 'i16':Int16}

class Codegen:
    def __init__(self):
        self._indent = 0
        self._vars = {}
        self._free = 0
        self._cursor = 0
        self._cursor_stack = []
        self._quiet = 0
        self._code = []
        self._level = 0
        self._buffer = []

        self._temps = []
        self._next_temp = 0

    def get_temp(self):
        if not self._temps:
            t = f'temp_{self._next_temp}'
            p = self.pos()
            self.var(t)
            self.go(p)
            self._temps.append(t)
            self._next_temp += 1
        return self._temps.pop()
    def return_temp(self, t):
        self._temps.append(t)

    def comment(self, text):
        assert all(c not in BF_CHARS for c in text), f'Illegal comment "{text}"'
        if self._quiet <= 0:
            self.emit(text)
    def emit(self, code):
        code = code.strip()
        if code:
            target = self._buffer if self._level>0 else self._code
            target.append(self._indent*'    ' + code)
    def begin(self, comment=''):
        self.comment(comment)
        self._quiet += 1
        self._level += 1
    def end(self):
        self._quiet -= 1
        self._level -= 1
        if self._level == 0 and self._buffer:
            self.emit(' '.join(s.strip() for s in self._buffer))
            self._buffer = []
    def var(self, name, kind='i8'):
        assert name not in self._vars, f'Var {name} already defined'
        assert kind in kinds, f'Type {kind} not known'
        k = kinds[kind]
        self._vars[name] = (self._free, k)
        self._free += k.size()
        comment = f'Init {name} as {kind} at {self._vars[name][0]}'
        self.comment(comment)
        k.init(self, name)
    def kind(self, name):
        return self._vars[name][1]
    def pos(self):
        return self._cursor
    def go(self, pos):
        change = pos - self._cursor
        self._cursor = pos
        self.emit(shift(change))
    def at(self, name, offset=0):
        if '#' in name:
            name, offset = name.split('#')
            offset = int(offset)
        change = self._vars[name][0] + offset - self._cursor
        self._cursor += change
        self.emit(shift(change))

    def quiet(self, amt, comment=''):
        self.comment(comment)
        self._quiet += amt
    def indent(self, amt):
        self._indent += amt

    def dump(self):
        return '\n'.join(self._code)

@contextlib.contextmanager
def TEMP(cg, count=1):
    temps = [cg.get_temp() for _ in range(count)]
    yield temps
    for t in temps:
        cg.return_temp(t)

@contextlib.contextmanager
def BLOCK(cg, comment=''):
    cg.comment(comment)
    cg.indent(1)
    yield
    cg.indent(-1)

def MOVE(cg, source, targets, mult=1):
    cg.begin(f'MOVE {source} TO {"/".join(targets)}')
    cg.at(source)
    cg.emit('[-')
    for t in targets:
        cg.at(t)
        cg.emit(delta(mult))
    cg.at(source)
    cg.emit(']')
    cg.end()

def SET(cg, var, value):
    cg.begin(f'SET {var} = {value}')
    k = cg.kind(var)
    k.set(cg, var, value)
    cg.end()

def ZERO(cg, var):
    SET(cg, var, 0)

def COPY(cg, source, target):
    cg.begin(f'COPY {source} TO {target}')
    with TEMP(cg) as temps:
        temp = temps[0]
        ZERO(cg, target)
        ZERO(cg, temp)
        MOVE(cg, source, [target, temp])
        MOVE(cg, temp, [source])
    cg.end()

def INC(cg, var, amt=1):
    if amt > 0:
        cg.begin(f'INC {var} by {amt}')
    else:
        cg.begin(f'DEC {var} by {-amt}')
    cg.at(var)
    cg.emit(delta(amt))
    cg.end()

def NE(cg, x, y, r, comment=''):
    comment = comment or f'{r} = {x}=/={y}'
    with TEMP(cg) as temps:
        t = temps[0]
        cg.begin(comment)

        COPY(cg, x, r)
        COPY(cg, y, t)
        with WHILE(cg, t):
            INC(cg, t, -1)
            INC(cg, r, -1)
        cg.end()

def NOT(cg, x, y, comment=''):
    comment = comment or f'{y} = ~{x}'
    with TEMP(cg) as temps:
        t = temps[0]
        cg.begin(comment)
        COPY(cg, x, t)
        SET(cg, y, 1)
        cg.at(t)
        cg.emit('[[-]')
        SET(cg, y, 0)
        cg.at(t)
        cg.emit(']')
        cg.end()

def EQ(cg, x, y, r, comment=''):
    comment = comment or f'{r} = {x}=={y}'
    with TEMP(cg, 1) as temps:
        t = temps[0]
        cg.begin(comment)
        NE(cg, x, y, r)
        COPY(cg, r, t)
        NOT(cg, t, r)
        cg.end()

@contextlib.contextmanager
def WHILE(cg, var, comment=''):
    comment = comment or f'WHILE {var}'
    cg.comment(comment)

    cg.begin()
    cg.at(var)
    cg.emit('[')
    cg.end()

    with BLOCK(cg):
        yield

    cg.at(var)
    cg.emit(']')

@contextlib.contextmanager
def IF(cg, var, comment=''):
    comment = comment or f'IF {var}'
    cg.comment(comment)

    with TEMP(cg) as temps:
        t = temps[0]

        cg.begin()
        COPY(cg, var, t)
        cg.at(t)
        cg.end()

        cg.emit('[[-]')

        with BLOCK(cg):
            yield

        cg.begin()
        cg.at(t)
        cg.emit(']')
        cg.end()

def READ_CHAR(cg, var, comment=''):
    comment = comment or f'READ CHAR TO {var}'
    cg.begin(comment)
    cg.at(var)
    cg.emit(',')
    cg.end()

def READ_INT_UNTIL(cg, var, c, comment=''):
    comment = comment or f'READ INT TO {var} UNTIL ASCII {ord(c)}'
    cg.begin(comment)
    SET(cg, var, 0)
    with TEMP(cg, 2) as temps:
        t1, t2 = temps
        SET(cg, var, 0)
        SET(cg, t1, ord(c)+1)
        SET(cg, t2, 0)

        with WHILE(cg, t1):
            cg.at(t1)
            cg.emit(',')
            INC(cg, t1, -ord(c))

            with WHILE(cg, t1):
                INC(cg, t1, ord(c) - ord('0'))
                # Multiply var by 10
                MOVE(cg, var, [t2], 2)
                MOVE(cg, t2, [var], 5)

                # Terminate innermost loop (really an IF)
                MOVE(cg, t1, [var, t2])
            # Put condition back into t1 to continue
            MOVE(cg, t2, [t1])
        cg.end()

def INC16(cg, var, amt=1):
    assert 1 <= amt < 256
    with TEMP(cg, 2) as temps:
        cg.begin(f'INC16 {var} {amt}')
        t1, t2 = temps
        SET(cg, t1, amt)
        with WHILE(cg, t1):
            INC(cg, t1, -1)
            INC(cg, var+'#1', 1)
            NOT(cg, var+'#1', t2)
            with IF(cg, t2):
                INC(cg, var+'#0', 1)
        cg.end()

def PRINT16(cg, var):
    pass

def PRINTC(cg, c):
    with TEMP(cg) as temps:
        t = temps[0]
        cg.begin()
        SET(cg, t, ord(c))
        cg.at(t)
        cg.emit('.')
        cg.end()

def PRINT(cg, s):
    for c in s:
        PRINTC(cg, c)


cg = Codegen()

cg.var('GOOD', 'i16')  # 16-bit counter for good passwords
cg.var('RUN')          # "Have not hit EOF yet" flag
SET(cg, 'RUN', 1)

cg.var('A')  # First character position to test
cg.var('B')  # Second character position to test
cg.var('C')  # Target character
cg.var('D')  # Latest character within password
cg.var('X')  # True if character is a match
cg.var('Y')  # True if index is a match
cg.var('Z')  # Garbage dump
cg.var('S')  # Password score, one of 1/0/-1, 0 is a pass
cg.var('NS') # Inverted password score, one of 0/1
cg.var('GO') # "Have not hit newline yet" flag

cg.comment(60*'#')

PRINT(cg, 'S')

with WHILE(cg, 'RUN', 'Read lines until EOF'):
    READ_INT_UNTIL(cg, 'A', '-')
    READ_INT_UNTIL(cg, 'B', ' ')

    READ_CHAR(cg, 'C', 'Read desired character into C')

    # Kill two uninteresting characters
    READ_CHAR(cg, 'Z')
    READ_CHAR(cg, 'Z')

    SET(cg, 'GO', 1)
    SET(cg, 'S', 1)
    with WHILE(cg, 'GO', 'while GO (not EOL)'):
        # Count down positions.  These are given one-indexed, so we
        # decrement first.
        INC(cg, 'A', -1)
        INC(cg, 'B', -1)

        READ_CHAR(cg, 'D', 'Read to D next char of pass')
        PRINT(cg, '.')

        cg.comment('Compare characters C and D')
        EQ(cg, 'C', 'D', 'X')
        with IF(cg, 'X'):
            PRINT(cg, 'C')
            NOT(cg, 'A', 'Y')
            with IF(cg, 'Y'):
                PRINT(cg, 'A')
                INC(cg, 'S', -1)

            NOT(cg, 'B', 'Y')
            with IF(cg, 'Y'):
                PRINT(cg, 'B')
                INC(cg, 'S', -1)

        cg.comment('Check for newline')
        COPY(cg, 'D', 'X')
        INC(cg, 'X', -ord('\n'))
        NOT(cg, 'X', 'Y')
        with IF(cg, 'Y'):
            SET(cg, 'GO', 0)

        cg.comment('Check for EOF')
        COPY(cg, 'D', 'X')
        NOT(cg, 'X', 'Y')
        with IF(cg, 'Y'):
            SET(cg, 'GO', 0)


    PRINT(cg, 'L')
    
    NOT(cg, 'S', 'NS')
    with IF(cg, 'NS'):
        PRINT(cg, 'M')
        INC16(cg, 'GOOD')

#PRINT16(cg, 'GOOD')






print(cg.dump())
print('###')
print(simplify(cg.dump()))


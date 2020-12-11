import re
RE = re.compile(r'(\d+)-(\d+) (.): (.*)')
def ok(line):
    mn, mx, let, pwd = RE.match(line).groups()
    return (pwd[int(mn)-1] == let) != (pwd[int(mx)-1] == let)
print(sum(ok(line) for line in open('input2.txt')))


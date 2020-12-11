import re
RE = re.compile(r'(\d+)-(\d+) (.): (.*)')
def ok(line):
    mn, mx, let, pwd = RE.match(line).groups()
    return int(mn) <= pwd.count(let) <= int(mx)
print(sum(ok(line) for line in open('input2.txt')))


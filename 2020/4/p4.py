
def is_valid(pprt):
    return all((f' {field}:' in pprt) for field in 'byr,iyr,eyr,hgt,hcl,ecl,pid'.split(','))


valid = 0
pprt = ''
for line in open('input.txt'):
    line = line.strip()
    if not line:
        valid += is_valid(pprt)
        pprt = ''
    pprt += '\n ' + line
valid += is_valid(pprt)

print(valid)


def is_valid_2_(pprt):
    fields = {}
    for pair in pprt.split():
        k,v = pair.split(':')
        fields[k] = v

    try:
      if not (1920 <= int(fields['byr']) <= 2002):
          print('bad byr')
          return False
      if not (2010 <= int(fields['iyr']) <= 2020):
          print('bad iyr')
          return False
      if not (2020 <= int(fields['eyr']) <= 2030):
          print('bad eyr')
          return False
      hgt = fields['hgt']
      if 'cm' not in hgt and 'in' not in hgt:
          print('bad hgt')
          return False
      if 'cm' in hgt and not (150 <= int(hgt[:-2]) <= 193):
          print('bad hgt')
          return False
      if 'in' in hgt and not (59 <= int(hgt[:-2]) <= 76):
          print('bad hgt')
          return False
      hcl = fields['hcl']
      if not hcl[0] == '#' or not all(c in 'abcdef0123456789' for c in hcl[1:]):
          print('bad hcl')
          return False
      ecl = fields['ecl']
      if not ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']: return False
      pid = fields['pid']
      if len(pid) != 9: return False
      if not all(p in '0123456789' for p in pid): return False
    except:
        return False

    return True

def is_valid_2(pprt):
    v = is_valid_2_(pprt)
    print(v, pprt)
    return v


valid = 0
pprt = ''
for line in open('input.txt'):
    line = line.strip()
    if not line:
        valid += is_valid_2(pprt)
        pprt = ''
    pprt += '\n ' + line
valid += is_valid_2(pprt)

print(valid)


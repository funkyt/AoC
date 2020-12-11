nums = []
for line in open('input.txt'):
    nums.append(int(line))

print(nums)

for p in nums:
    for q in nums:
        for r in nums:
            if p+q+r == 2020:
                print(p, q, r, p*q*r)

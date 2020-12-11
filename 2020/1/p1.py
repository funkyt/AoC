nums = []
for line in open('input.txt'):
    nums.append(int(line))

print(nums)

for p in nums:
    for q in nums:
        if p+q == 2020:
            print(p, q, p*q)

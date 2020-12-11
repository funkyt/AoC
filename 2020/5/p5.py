seats = []
for line in open('input.txt'):
    line = line.strip()
    row = int(line[0:7].replace('F', '0').replace('B','1'), 2)
    col = int(line[7:].replace('R', '1').replace('L', '0'), 2)
    seats.append(8*row+col)

print(max(seats))

for j in range(min(seats), max(seats)+1):
    if (j-1) in seats and (j+1) in seats and j not in seats:
        print(j)


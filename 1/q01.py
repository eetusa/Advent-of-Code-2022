from aocd import lines

total_calories = []
current = 0
for line in lines:
    if line == '':
        total_calories.append(int(current))
        current = 0
        continue
    current = current + int(line)

total_calories.sort()
print(sum(total_calories[-3:]))
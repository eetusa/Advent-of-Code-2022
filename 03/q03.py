from aocd import lines

def getItemPriority(char):
    ascii_value = ord(char)
    if (ascii_value > 96):
        return ascii_value-96
    return ascii_value-38

def splitIntoCompartments(line):
    halfpoint = int(len(line)/2)
    compartments = [line[0:halfpoint], line[halfpoint:]]
    return compartments

def findCommonItemInNCompartments(compartments):
    common = []
    for idx, x in enumerate(compartments):
        if (idx == 0):
            for c in x:
                common.append(c)
        else:
            common_temp = common[:]
            for c in common_temp:
                if c not in x:
                    common.remove(c)
    return common[0]

def solve(data_lines, group_size):
    sum = 0
    group = []
    index = 1
    for line in data_lines:
        group.append(line)
        if index % group_size == 0:
            if group_size == 1:
                group = splitIntoCompartments(group[0])
            common = findCommonItemInNCompartments(group)
            priority = getItemPriority(common)
            sum = sum + priority
            group.clear()
        index = index + 1
    return sum

ans_a = solve(lines, 1)
print("a",ans_a)
ans_b = solve(lines, 3)
print("b:",ans_b)
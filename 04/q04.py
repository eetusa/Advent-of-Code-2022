from aocd import lines

class Range:
    def __init__(self, a: list):
        self.lower = int(a[0])
        self.upper = int(a[1])

    def doesContainRange(self, b):
        if (b.lower >= self.lower and b.upper <= self.upper):
            return True
        return False

    def doesPartlyOverlap(self, b):
        if (self.lower < b.lower and self.upper < b.lower) or (self.lower > b.upper and self.upper > b.upper):
            return False
        return True

def areRangesFullyOverlapped(ranges):
    if ranges[0].doesContainRange(ranges[1]):
        return True
    return ranges[1].doesContainRange(ranges[0])

def areRangesPartlyOverlapped(ranges):
    if ranges[0].doesPartlyOverlap(ranges[1]):
        return True
    return ranges[1].doesPartlyOverlap(ranges[0])

def getRangesFromLine(line: str):
    split = line.split(",")
    return [Range(split[0].split("-")), Range(split[1].split("-"))]

def solve(name: str, func):
    count = 0
    for line in lines:
        ranges = getRangesFromLine(line)
        if func(ranges):
            count = count + 1
    print(name+":", count)

solve("a", areRangesFullyOverlapped)
solve("b", areRangesPartlyOverlapped)


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

def puzzle_a():
    count = 0
    for line in lines:
        ranges = getRangesFromLine(line)
        if areRangesFullyOverlapped(ranges):
            count = count + 1
    print("a:", count)

def puzzle_b():
    count = 0
    for line in lines:
        ranges = getRangesFromLine(line)
        if areRangesPartlyOverlapped(ranges):
            count = count + 1
    print("b:",count)

puzzle_a()
puzzle_b()

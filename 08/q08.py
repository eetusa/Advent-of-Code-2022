from aocd import lines
from functools import reduce

def is_visible_from_edge(i, j, y_direction, x_direction, array):
    if (y_direction != 0):
        if (i == 0 or i == len(array)-1):
            return True
    if (x_direction != 0):
        if (j == 0 or j == len(array[i])-1):
            return True
    own_height = array[i][j]
    row = i + y_direction
    column = j + x_direction
    while row >= 0 and row < len(array) and column >= 0 and column < len(array[i]):
        compare_height = array[row][column]
        if (compare_height >= own_height):
            return False
        row = row + y_direction
        column = column + x_direction
    return True

def is_visible(i, j, array):
    if is_visible_from_edge(i, j, 1, 0, array):
        return True
    if is_visible_from_edge(i, j, -1, 0, array):
        return True
    if is_visible_from_edge(i, j, 0, 1, array):
        return True
    if is_visible_from_edge(i, j, 0, -1, array):
        return True
    return False

def get_scenic_score(i, j, y_direction, x_direction, array):
    score = 0
    own_height = array[i][j]
    row = i + y_direction
    column = j + x_direction
    while row >= 0 and row < len(array) and column >= 0 and column < len(array[i]):
        score = score + 1
        compare_height = array[row][column]
        if (compare_height >= own_height):
            return score
        row = row + y_direction
        column = column + x_direction
    return score

def get_total_scenic_score(i, j, array):
    # Edges are always 0 and the result is a multiplication -> return 0 from any edge
    if (j == 0 or j == len(array[i])-1 or i == 0 or i == len(array)-1):
        return 0
    scores = [get_scenic_score(i, j, 1, 0, array), get_scenic_score(i, j, -1, 0, array), get_scenic_score(i, j, 0, 1, array), get_scenic_score(i, j, 0, -1, array)]
    return reduce(lambda x, y: x*y, scores)

def solve_a(array):
    total_visible = 0
    for i, row in enumerate(array):
        for j, column in enumerate(row):
            if is_visible(i, j, array):
                total_visible = total_visible + 1
    print("a:",total_visible)

def solve_b(array):
    best_score = 0
    for i, row in enumerate(array):
        for j, column in enumerate(row):
            scenic_score = get_total_scenic_score(i, j, array)
            if scenic_score > best_score:
                best_score = scenic_score
    print("b:", best_score)

solve_a(lines)
solve_b(lines)
from aocd import lines
input = lines[0]

def check_non_repeating_values(array: list):
    characters = {}
    for c in array:
        if c in characters:
            return False
        else:
            characters[c] = 1
    return True

def find_marker(line: str, n_unique_chars: int):
    for i in range(0, len(line)):
        if i < n_unique_chars:
            continue
        found_marker = check_non_repeating_values(line[(i-n_unique_chars):i])
        if found_marker:
            return i

def solve(line, n_unique_chars: int):
    ans = find_marker(line, n_unique_chars)
    print(ans)

solve(input, 4)
solve(input, 14)
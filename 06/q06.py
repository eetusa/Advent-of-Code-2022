from aocd import lines
input = lines[0]

def check_non_repeating_values(array):
    return len(set(array)) == len(array)

def find_marker(line: str, n_unique_chars: int):
    for i in range(0, len(line)-n_unique_chars):
        found_marker = check_non_repeating_values(line[i:i+n_unique_chars])
        if found_marker:
            return i + n_unique_chars

def solve(line, n_unique_chars: int):
    ans = find_marker(line, n_unique_chars)
    print(ans)

solve(input, 4)
solve(input, 14)
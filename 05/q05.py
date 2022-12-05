from aocd import lines
import re

# Initial stack:
#
#    [V] [G]             [H]        
#[Z] [H] [Z]         [T] [S]        
#[P] [D] [F]         [B] [V] [Q]    
#[B] [M] [V] [N]     [F] [D] [N]    
#[Q] [Q] [D] [F]     [Z] [Z] [P] [M]
#[M] [Z] [R] [D] [Q] [V] [T] [F] [R]
#[D] [L] [H] [G] [F] [Q] [M] [G] [W]
#[N] [C] [Q] [H] [N] [D] [Q] [M] [B]
#
# Example command:
# move 2 from 2 to 1

class Stacks():
    def __init__(self, lines):
        self.lines = lines
        self.initialize_stack_rows()

    def initialize_stack_rows(self):
        self.stacks = {}
        for line in self.lines:
            if (len(line) == 0):
                break
            for idx, c in enumerate(line):
                if c == '[':
                    column = int(idx/4)+1
                    if column in self.stacks:
                        self.stacks[column].append(line[idx+1])
                    else:
                        self.stacks[column] = [line[idx+1]]

    def move_from_stack_to_stack(self, amount: int, source: int, target: int, keep_order: bool):
        containers_to_move = []
        for i in range(0, amount):
            if keep_order:
                containers_to_move.insert(0, self.stacks.get(source)[i])
            else:
                containers_to_move.append(self.stacks.get(source)[i])
        for container in containers_to_move:
            self.stacks[target].insert(0, container)
            self.stacks[source].pop(0)

    def act_move_order(self, line: str, keep_order: bool):
        amount, source, target = re.findall(r'\d+', line)
        if keep_order:
            self.move_from_stack_to_stack(int(amount), int(source), int(target), True)
        else:
            self.move_from_stack_to_stack(int(amount), int(source), int(target), False)

    def print_ans(self):
        ans = ""
        for key in sorted(self.stacks):
            ans = ans + self.stacks[key][0]
        print(ans)

    def reset(self):
        self.initialize_stack_rows()

    def solve_a(self):
        for line in self.lines:
            if len(line) == 0 or line[0] != 'm':
                continue
            self.act_move_order(line, False)
        self.print_ans()
        self.reset()
    
    def solve_b(self):
        for line in self.lines:
            if len(line) == 0 or line[0] != 'm':
                continue
            self.act_move_order(line, True)
        self.print_ans()
        self.reset()

stacks = Stacks(lines)
stacks.solve_a()
stacks.solve_b()

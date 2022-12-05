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
#
# 'move 2 from 2 to 1'

class Stacks():
    def __init__(self, lines):
        self.lines = lines
        self.reset_stack()

    def reset_stack(self):
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

    def move_from_stack_to_stack(self, amount: int, source: int, target: int, keep_stack_order: bool):
        containers_to_move = []
        for i in range(0, amount):
            if keep_stack_order:
                containers_to_move.insert(0, self.stacks.get(source)[i])
            else:
                containers_to_move.append(self.stacks.get(source)[i])
        for container in containers_to_move:
            self.stacks[target].insert(0, container)
            self.stacks[source].pop(0)

    def act_move_order(self, line: str, keep_stack_order: bool):
        amount, source, target = list(map(int, re.findall(r'\d+', line)))
        if keep_stack_order:
            self.move_from_stack_to_stack(amount, source, target, True)
        else:
            self.move_from_stack_to_stack(amount, source, target, False)

    def print_ans(self):
        ans = ""
        for key in sorted(self.stacks):
            ans = ans + self.stacks[key][0]
        print(ans)

    def solve(self, keep_stack_order: bool):
        for line in self.lines:
            if len(line) == 0 or line[0] != 'm':
                continue
            self.act_move_order(line, keep_stack_order)
        self.print_ans()
        self.reset_stack()

stacks = Stacks(lines)
stacks.solve(False)
stacks.solve(True)

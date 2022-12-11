import re
from aocd import lines
from functools import reduce

def get_numbers(line: str) -> "list[int]":
    return [int(i) for i in re.findall(r'\b\d+\b', line)]

class Monkey():
    def __init__(self, no: int, starting_items: "list[int]", operation: str, test: str, if_true: str, if_false: str) -> None:
        self.no = no
        self.items = starting_items
        self.operation = self.get_operation(operation)
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.inspect_count = 0

    def inspect_item(self, mod: int, relief: bool):
        if len(self.items) == 0:
            return None
        self.inspect_count = self.inspect_count + 1    # increment inspect count
        item = self.items.pop(0)                        # take first item on list
        item = self.apply_operation_to_item(item, mod)  # operation
        if relief:
            item = self.apply_boredom(item)             # relief
        return self.test_result(item)                   # test and return

    def apply_boredom(self, item):
        return item//3

    def test_result(self, item):
        if item % self.test == 0:
            return (self.if_true, item)
        return (self.if_false, item)

    def test_pass(self, item):
        return item % self.test == 0

    def get_operation(self, line):
        value = get_numbers(line)
        if len(value) == 0:
            value = "-1"
        else:
            value = value[0]
        if "*" in line:
            return ("*", value)
        if "+" in line:
            return ("+", value)
        return None

    def apply_operation_to_item(self, item: int, mod: int):
        val = 0
        if self.operation[0] == "*":
            if self.operation[1] == "-1":
                val = item * item
            else:
                val = item * self.operation[1]
        elif self.operation[0] == "+":
            if self.operation[1] == "-1":
                val = item + item
            else:
                val = item + self.operation[1]
        if mod:
            val = val % mod # modulo solution not working with part a some reason, disabled for part a
        return val

    def add_item(self, item):
        self.items.append(item)

#A group of monkeys is called a troop.
class Troop():
    def __init__(self, lines) -> None:
        self.monkeys: dict = {}
        self.lines = lines
        self.init_monkeys()
        self.relief = False
        self.mod = self.get_mod()

    def init_monkeys(self):
        monkey_no: int = None
        starting_items = []
        operation = ""
        test = ""
        if_true: int = None
        if_false: int = None
        for line in self.lines:
            if "Monkey" in line:
                monkey_no = get_numbers(line)[0]
            if "Starting items" in line:
                starting_items =   get_numbers(line)
            if "Operation" in line:
                operation = line[13:]
            if "Test" in line:
                test = get_numbers(line)[0]
            if "If true" in line:
                if_true = get_numbers(line)[0]
            if "If false" in line:
                if_false = get_numbers(line)[0]
            if line == '':
                self.monkeys[monkey_no] = Monkey(monkey_no, starting_items, operation, test, if_true, if_false)
        self.monkeys[monkey_no] = Monkey(monkey_no, starting_items, operation, test, if_true, if_false) # last one when all lines have been read

    def get_mod(self):
        mod = 1
        for key in self.monkeys:
            monkey = self.monkeys[key]
            mod *= monkey.test
        return mod

    def do_monkey_round(self, monkey: Monkey):
        while True:
            result: tuple = monkey.inspect_item(self.mod, self.relief) # returns (monkey_no, item_worry_level)
            if result == None:
                break
            target_monkey: Monkey = self.monkeys[result[0]]
            target_monkey.add_item(result[1])

    def run(self, rounds, relief: bool, mod: bool = False):
        if not mod:
            self.mod = None
        self.relief = relief
        for i in range(0, rounds):
            for m in range(0, len(self.monkeys)):
                monkey: Monkey = self.monkeys[m]
                self.do_monkey_round(monkey)
        monkey_businesses = []
        for key in self.monkeys:
            monkey = self.monkeys[key]
            monkey_businesses.append(monkey.inspect_count)
        monkey_businesses.sort(reverse=True)
        print(reduce(lambda x, y: x*y, monkey_businesses[:2]))

troop = Troop(lines)
troop.run(20, relief=True)
troop = Troop(lines)
troop.run(10000, relief=False, mod=True)
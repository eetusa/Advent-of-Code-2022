from aocd import lines
import math 
import re
import time

test_input = ["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"]
test_input2 = ["R 5", "U 8", "L 8", "D 3", "R 17", "D 10", "L 25", "U 20"]

class Point():
    def __init__(self, x, y, point: 'Point'):
        self.x = x
        self.y = y
        self.head = point
        self.positions = {}
        self.positions[(self.x, self.y)] = 1

    def move_up(self):
        self.y = self.y + 1
    
    def move_down(self):
        self.y = self.y - 1

    def move_left(self):
        self.x = self.x - 1

    def move_right(self):
        self.x = self.x + 1

    def __str__(self):
        return "(x: " + str(self.x) + ", y: " + str(self.y)+")"

    def __repr__(self) -> str:
        return str(self)

    def update_positions(self):
        if (self.x, self.y) in self.positions:
            self.positions[(self.x, self.y)] = self.positions.get((self.x, self.y), 0) + 1
        else:
            self.positions[(self.x, self.y)] = 1

    def print_total_unique_positions(self):
        return len(self.positions)

    def updated_head(self):
        x = self.head.x
        y = self.head.y
        dx = math.dist([self.x], [x])
        dy = math.dist([self.y], [y])
        if (dx == 0 and dy == 0): return
        if dx == 0:
            if dy <= 1:
                return
            else:
                if self.y > y:
                    self.move_down()
                else:
                    self.move_up()
            return
        if dy == 0:
            if dx <= 1:
                return
            else:
                if x > self.x:
                    self.move_right()
                else:
                    self.move_left()
            return
        if dy == 2 or dx == 2:
            if y > self.y:
                self.move_up()
            else:
                self.move_down()
            if x > self.x:
                self.move_right()
            else:
                self.move_left()

class Plank():
    def __init__(self, tail_len: int, x_range: int, y_range: int):
        self.head = None
        self.tail_len = tail_len
        self.tail: list[Point] = None
        self.reset()
 
        ############################################################
        # Only used for printing the tail, not relevant for solution
        self.step = Point(0, 0, None) 
        self.x_range = x_range
        self.y_range = y_range
        self.do_print = False
        self.one_step_at_a_time = False
        ############################################################

    def reset(self):
        self.head = Point(0, 0, None)
        self.tail: list[Point] = []
        for i in range(0, self.tail_len):
            if (i == 0):
                self.tail.append(Point(0, 0, self.head))
            else:
                self.tail.append(Point(0, 0, self.tail[len(self.tail)-1]))

    def parse_command(self, line):
        value = re.search('[0-9]+', line).group()
        direction = line[0]
        return [direction, value]

    def move_head_to_dir(self, direction):
        if (direction == 'U'):
            self.head.move_up();
        if (direction == 'L'):
            self.head.move_left();
        if (direction == 'D'):
            self.head.move_down();
        if (direction == 'R'):
            self.head.move_right();
        return self.head

    def update_tail(self):
        for tail in self.tail:
            tail_x_init = tail.x # Only for printing, not relevant for solution
            tail_y_init = tail.y # Only for printing, not relevant for solution
            tail.updated_head()
            tail.update_positions()

            # Only for printing, not relevant for solution
            if self.do_print and self.one_step_at_a_time: 
                if tail.x != tail_x_init or tail.y != tail_y_init:
                    time.sleep(0.05)
                    self.print_rope()

    def get_total_uniq_pos_of_last_of_tail(self):
        return self.tail[len(self.tail)-1].print_total_unique_positions()

    def go(self, commands, part: str):
        self.reset()
        if self.do_print: self.print_rope()
        for command in commands:
            if self.do_print: print(command)
            cmd = self.parse_command(command)
            cmd_value = int(cmd[1])
            for i in range(0, cmd_value):
                self.move_head_to_dir(cmd[0])
                self.update_tail()
            if self.do_print and not self.one_step_at_a_time: 
                self.print_rope()
        print(part,"\t|",self.get_total_uniq_pos_of_last_of_tail())

    ########################################################
    ########### ONLY FOR FUN - PRINTING THE ROPE ###########
    ########################################################
    def get_char_for_map(self, x, y):
        if self.head.x == x and self.head.y == y:
            return 'H'
        for i in range(0, len(self.tail)):
            tail = self.tail[i]
            if tail.x == x and tail.y == y:
                return str(i+1)
        if self.step.x == x and self.step.y == y:
            return "s"
        return "."

    def t_x(self, x):
        return -self.x_range + x - 1

    def t_y(self, y):
        return self.y_range - y + 1

    def print_rope(self):
        print("*"*(self.x_range*2+1))
        for y in range(0, (self.x_range*2+1)):
            line = ""
            for x in range(0, (self.y_range*2+1)):
                tx = self.t_x(x)
                ty = self.t_y(y)
                line = line + self.get_char_for_map(tx, ty)
            print(line)
        print("*"*(self.x_range*2+1))

    def set_printing(self, do_print: bool = False, one_step_at_a_time: bool = False):
        self.do_print = do_print
        self.one_step_at_a_time = one_step_at_a_time
    ########################################################


plank = Plank(1, 12, 12)
plank.go(test_input, "a-test")
plank.go(lines, "a") #a

plank = Plank(9, 15, 15)
plank.set_printing(do_print=True, one_step_at_a_time=False)
plank.go(test_input2, "b-test")

plank.set_printing(do_print=False)
plank.go(lines, "b") #b
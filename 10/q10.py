from aocd import lines
from enum import Enum
import re

class CommandType(Enum):
    NOOP = 0,
    ADDX = 1

class Command():
    def __init__(self, line):
        self.type: CommandType = None
        self.value: int = None
        self.execution_time = None
        self.parse_command(line)
    
    def parse_command(self, line):
        if "noop" in line:
            self.type = CommandType.NOOP
            self.execution_time = 1
            return
        else:
            self.type = CommandType.ADDX
            self.execution_time = 2
        value = int(re.search('[0-9]+', line).group())
        if '-' in line:
            value = -value
        self.value = value

class Processor():
    def __init__(self) -> None:
        self.value = 1
        self.cycle = 0
        self.blocked_for_n_turns = 0
        self.queued_command = None
        self.commands = None
        self.signal_strenghts = []

    def set_commands(self, commands):
        self.commands = list(map(lambda cmd: Command(cmd), commands))

    def act_command(self, cmd: Command):
        self.blocked_for_n_turns = self.blocked_for_n_turns + cmd.execution_time
        self.queued_command = cmd

    def is_executing(self):
        if self.blocked_for_n_turns == 0:
            return False
        return True

    def increment_cycle(self):
        self.cycle = self.cycle + 1
        if self.blocked_for_n_turns > 0:
            self.blocked_for_n_turns = self.blocked_for_n_turns - 1

    def finish_execution_of_command(self, cmd: Command):
        if cmd.type == CommandType.ADDX:
            self.value = self.value + cmd.value
        self.queued_command = None

    def do_cycle(self):
        self.increment_cycle()
        if len(self.commands) == 0: # if no more commands left, return cycle as -1 to and processing
            return -1
        if not self.is_executing():
            if self.queued_command != None:
                self.finish_execution_of_command(self.queued_command)
            command = self.commands.pop(0)
            self.act_command(command)
        if (self.cycle == 20 or (self.cycle-20)%40==0):
            self.signal_strenghts.append(self.value*self.cycle)
        return self.cycle
        
class CRT():
    def __init__(self, processor: Processor) -> None:
        self.processor = processor
        self.width = 40
        self.sprite_position = self.processor.value
        self.cursor_position = 0
        self.drawing_row = ""

    def get_pixel_value(self):
        if self.cursor_position >= self.sprite_position - 1 and self.cursor_position <= self.sprite_position + 1:
            return "#"
        return "."
        
    def draw_pixel(self):
        self.drawing_row = self.drawing_row + self.get_pixel_value()

    def print_row(self):
        print(self.drawing_row)
        self.drawing_row = ""
        self.cursor_position = 0

    def handle_cycle(self):
        processor_cycle = self.processor.do_cycle()
        self.sprite_position = self.processor.value
        self.draw_pixel()
        self.cursor_position = self.cursor_position + 1
        if (self.cursor_position % self.width == 0):
            self.print_row()
        return processor_cycle

    def solve(self):
        print("b-part:")
        while True:
            cycle = self.handle_cycle()
            if (cycle == -1):
                break
        print(f"\na-part: {sum(self.processor.signal_strenghts)}")

processor = Processor()
processor.set_commands(lines)
crt = CRT(processor)
crt.solve()
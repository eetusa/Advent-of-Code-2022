from aocd import lines
import re
from enum import Enum

class CommandType(Enum):
    CD = 0,
    LS = 1

class OutputType(Enum):
    DIR = 0,
    FILE = 1

class Command():
    def __init__(self, line):
        self.type = self.get_type(line)
        self.value = self.get_value(line)

    def get_type(self, line):
        command = None
        if "cd" == line[2:4]:
            command = CommandType.CD
        elif "ls" == line[2:4]:
            command = CommandType.LS
        return command

    def get_value(self, line):
        if len(line) < 5:
            return None
        return line[5:len(line)]

    def toString(self):
        return str(self.type) + ", " + str(self.value)

class File():
    def __init__(self, name, size):
        self.name: str = name
        self.size: int = size

    def __str__(self):
        return str(self.size)
    
    def __repr__(self):
        return str(self)

class Output():
    def __init__(self, line):
        self.type: OutputType = self.get_type(line)
        self.value = self.get_value(line)

    def get_value(self, line):
        if self.type == OutputType.FILE:
            return re.search('[0-9]+', line).group()
        else:
            return line[4:len(line)]

    def get_type(self, line):
        output = OutputType.FILE
        if "dir " in line:
            output = OutputType.DIR
        return output

    def toString(self):
        return str(self.type) + ", " + str(self.value)

class Directory():
    def __init__(self, name, parent: 'Directory'):
        self.name = name
        self.subdirs: list['Directory'] = []
        self.files: list[File] = []
        self.size_from_files = -1
        self.total_size = -1
        self.parent = parent

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return str(self)

    def add_file(self, file: File):
        self.files.append(file)

    def set_size_from_files(self):
        sum = 0
        for file in self.files:
            sum = sum + file.size
        self.size_from_files = sum

    def get_size_from_files(self):
        self.set_size_from_files()
        return self.size_from_files

    def set_total_size(self):
        if self.total_size != -1:
            return self.total_size
        else:
            sum = self.get_size_from_files()
            for d in self.subdirs:
                sum = sum + d.get_total_size()
            self.total_size = sum
    
    def get_total_size(self):
        if self.total_size == -1:
            self.set_total_size()
        return self.total_size

class Crawler():
    def __init__(self):
        self.current_dir = None
        self.path = [] # useless in solution, usable only as visualization for the crawling process
        self.root = None

    def parse_line(self, line):
        if line[0] == '$':
            command = Command(line)
            self.act_command(command)
        else:
            output = Output(line)
            self.act_output(output)

    def cd_to_dir(self, dir_name: str):
        self.path.append(dir_name)
        for directory in self.current_dir.subdirs:
            if directory.name == dir_name:
                self.current_dir = directory
                return
    
    def cd_to_parent(self):
        self.path.pop()
        self.current_dir = self.current_dir.parent

    def act_command(self, command: Command):
        if (command.type == CommandType.CD):
            if (command.value == "/"):
                self.root = Directory("/", None)
                self.path.append("/")
                self.current_dir = self.root
            elif command.value == "..":
                self.cd_to_parent()
            else:
                self.cd_to_dir(command.value)
                
    def act_output(self, output: Output):
        if output.type == OutputType.DIR:
            self.current_dir.subdirs.append(Directory(output.value, self.current_dir))
        if output.type == OutputType.FILE:
            self.current_dir.add_file(File("placeholder", int(output.value)))
        return

    def investigate(self, lines):
        for line in lines:
            self.parse_line(line)
        self.root.get_total_size() # sets total sizes for all directories recursively as a side effect

    def get_all(self, result: list, dir: Directory):
        result.append(dir)
        for d in dir.subdirs:
            self.get_all(result, d)
        return result

    def solve_a(self):
        all: list[Directory] = []
        threshold = 100000
        self.get_all(all, self.root)
        sum = 0

        for d in all:
            if d.total_size <= threshold:
                sum = sum + d.total_size
        print("a:",sum)

    def solve_b(self):
        threshold, best_value, currently_free = 30000000, 9999999999999, 70000000 - self.root.get_total_size()
        best_dir = None 
        all: list[Directory] = []
        all = self.get_all(all, self.root)

        for d in all:
            new_value = currently_free + d.get_total_size()
            if new_value >= threshold and new_value < best_value:
                best_value = new_value
                best_dir = d
        print("b:",best_dir.get_total_size())
        
crawler = Crawler()
crawler.investigate(lines)
crawler.solve_a()
crawler.solve_b()


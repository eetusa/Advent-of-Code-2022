from aocd import lines
from enum import Enum
import copy

class CellType(Enum):
    AIR = 0,
    SAND = 1,
    ROCK = 2,
    VOID = 3,
    SAND_SOURCE = 4

class Cell():
    def __init__(self, i, j, type, matrix) -> None:
        self.i = i
        self.j = j
        self.type: CellType = type
        self.matrix = matrix
        self.static = None

    def __str__(self) -> str:
        return "("+str(self.i)+", "+str(self.j)+")"

    def __repr__(self) -> str:
        return str(self)

    def step(self):
        pass

class SandProducer(Cell):
    def __init__(self, i, j, matrix):
        super().__init__(i, j, CellType.SAND_SOURCE, matrix)

    def step(self):
        sand_i = self.i+1
        sand_j = self.j
        self.matrix[sand_i][sand_j] = Sand(sand_i, sand_j, self.matrix)
        print("producer step")

class Sand(Cell):
    def __init__(self, i, j, matrix):
        super().__init__(i, j, CellType.SAND, matrix)
        self.static = False

    def step(self):
        i = self.i
        j = self.j
        if self.matrix[i+1][j].type == CellType.AIR:
            self.matrix[i+1][j] = Sand(i+1, j, self.matrix)
            self.matrix[i][j] = Cell(i, j, CellType.AIR, self.matrix)
            return 1
        self.static = True
        return -1

class World():
    def __init__(self, input) -> None:
        self.height = None
        self.width = None
        self.min_draw_x = None
        self.min_draw_y = None
        self.void_limit = None
        self.get_xy_ranges(input)

        self.matrix: 'list[list[Cell]]' = []
        self.sand_source = (500,0)
        self.init_world()
        self.parse_input(input)

    def init_world(self):
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if (j, i) == self.sand_source:
                    row.append(SandProducer(i, j, self.matrix))
                elif (i > self.void_limit):
                    row.append(Cell(i, j, CellType.VOID, self.matrix))
                else:
                    row.append(Cell(i, j, CellType.AIR, self.matrix))
            self.matrix.append(row)

    def parse_input(self, input):
        for line in input:
            split = [x.strip() for x in line.split("->")]
            for i in range(len(split)-1):
                s1 = split[i].split(',')
                s2 = split[i+1].split(',')
                self.set_rock_from_points(s1[0], s1[1], s2[0], s2[1])

    def set_rock_from_points(self, x0, y0, x1, y1):
        line = list(self.line(int(x0), int(y0), int(x1), int(y1)))
        for c in line:
            x = c[0]
            y = c[1]
            self.matrix[y][x].type = CellType.ROCK

    def line(self, x0, y0, x1, y1):
        points = []
        deltax = x0-x1
        deltay = y0-y1
        if deltax != 0 and deltay != 0:
            print("SLOPE! ERROR!")
        if deltax > 0:
            y = y0
            for x in range(x1, x0+1):
                points.append((x, y))
        if deltax < 0:
            y = y0
            for x in range(x0, x1+1):
                points.append((x, y))
        if deltay > 0:
            x = x0
            for y in range(y1, y0+1):
                points.append((x, y))
        if deltay < 0:
            x = x0
            for y in range(y0, y1+1):
                points.append((x, y))
        return points


    def print_world(self):
        for i in range(self.height):
            row = str(i)+ " "
            if (i < 10):
                row += " "
            for j in range(self.min_draw_x,self.width):
                cell = self.matrix[i][j]
                if cell.type == CellType.AIR:
                    row += ". "
                elif cell.type == CellType.ROCK:
                    row += "# "
                elif cell.type == CellType.SAND:
                    row += "O "
                elif cell.type == CellType.SAND_SOURCE:
                    row += "+"
                else:
                    row += "_ "
            print(row)
    
    def get_xy_ranges(self, data):
        min_x = 999999
        min_y = 999999
        max_x = -999999
        max_y = -999999
        for line in data:
            split = [x.strip() for x in line.split("->")]
            for i in range(len(split)):
                s1 = split[i].split(',')
                x = int(s1[0])
                y = int(s1[1])
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
        self.height = max_y + 3
        self.width = max_x + 2
        self.void_limit = max_y
        self.min_draw_x = min_x - 2
        self.min_draw_y = 0

class Simulator():
    def __init__(self, world: World) -> None:
        self.cycles = 0
        self.world = copy.deepcopy(world)
        self.world.print_world()
        self.sand_moving = False

    def simulate(self):
        while True:
            for i in range(len(self.world.matrix)):
                for j in range(len(self.world.matrix[i])):
                    cell = self.world.matrix[i][j]
                    if isinstance(cell, SandProducer):
                        if not self.sand_moving:
                            cell.step()
                            self.sand_moving = True
                            print("sand move")
                    elif isinstance(cell, Sand):
                        if cell.static:
                            did_move = cell.step()
                            if did_move == -1:
                                self.sand_moving = False
                                print("Sand not move")
                        else:
                            break
        self.world.print_world()

test_input = ["498,4 -> 498,6 -> 496,6", "503,4 -> 502,4 -> 502,9 -> 494,9"]

world = World(test_input)
simulator = Simulator(world)
simulator.simulate()
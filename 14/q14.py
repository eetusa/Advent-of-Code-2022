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
        self.cycle = 0

    def __str__(self) -> str:
        return "("+str(self.i)+", "+str(self.j)+", "+str(self.type)+")"

    def __repr__(self) -> str:
        return str(self)

    def step(self):
        pass

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
            return self.matrix[i+1][j]
        elif self.matrix[i+1][j-1].type == CellType.AIR:
            self.matrix[i+1][j-1] = Sand(i+1, j-1, self.matrix)
            self.matrix[i][j] = Cell(i, j, CellType.AIR, self.matrix)
            return self.matrix[i+1][j-1]
        elif self.matrix[i+1][j+1].type == CellType.AIR:
            self.matrix[i+1][j+1] = Sand(i+1, j+1, self.matrix)
            self.matrix[i][j] = Cell(i, j, CellType.AIR, self.matrix)
            return self.matrix[i+1][j+1]

        if self.matrix[i+1][j].type == CellType.VOID:
            return None
        elif self.matrix[i+1][j-1].type == CellType.VOID:
            return None
        elif self.matrix[i+1][j+1].type == CellType.VOID:
            return None
        self.static = True
        return self

class World():
    def __init__(self, input, has_floor = False) -> None:
        self.height = None
        self.width = None
        self.min_draw_x = None
        self.min_draw_y = None
        self.void_limit = None
        self.producer: tuple = None
        self.has_floor = has_floor
        self.floor_level = None
        self.get_xy_ranges(input)
        self.matrix: 'list[list[Cell]]' = []
        self.sand_source = (500,0)
        self.init_world()
        self.parse_input(input)

    def init_world(self):
        prod_i = -1
        prod_j = -1
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if (j, i) == self.sand_source:
                    row.append(Cell(i, j, CellType.AIR, self.matrix))
                    prod_i, prod_j = i, j
                elif (i > self.void_limit and not self.has_floor):
                    row.append(Cell(i, j, CellType.VOID, self.matrix))
                elif (i == self.floor_level and self.has_floor):
                    row.append(Cell(i, j, CellType.ROCK, self.matrix))
                else:
                    row.append(Cell(i, j, CellType.AIR, self.matrix))
            self.matrix.append(row)
        self.producer = (prod_i, prod_j)

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
                if ((i,j) == self.producer):
                    row += "+"
                else:
                    cell = self.matrix[i][j]
                    if cell.type == CellType.AIR:
                        row += ". "
                    elif cell.type == CellType.ROCK:
                        row += "# "
                    elif cell.type == CellType.SAND:
                        row += "O "
                    else:
                        row += "_ "
            print(row)
    
    # define ranges for matrix and drawing from input
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
        self.width = max_x + 3
        if self.has_floor:
            self.width = self.width*2
        self.floor_level = max_y + 2
        self.void_limit = max_y
        self.min_draw_x = min_x - 2
        if (self.has_floor): 
            self.min_draw_x = self.min_draw_x - int(self.min_draw_x/20)
        self.min_draw_y = 0

class Simulator():
    def __init__(self, world: World) -> None:
        self.cycle = 0
        self.world = copy.deepcopy(world)
        self.sand_moving = False
        self.sand_produced = 0
        self.simulating = True
        self.active_sand: Sand = None

    def produce_sand(self):
        sand_i = self.world.producer[0]
        sand_j = self.world.producer[1]
        if self.world.matrix[sand_i][sand_j].type == CellType.AIR:
            self.world.matrix[sand_i][sand_j] = Sand(sand_i, sand_j, self.world.matrix)
            return self.world.matrix[sand_i][sand_j]
        return None

    def sim(self):
        while self.simulating:
            self.cycle += 1
            if self.active_sand is not None and not self.active_sand.static:
                self.active_sand = self.active_sand.step()
                if self.active_sand == None:
                    self.simulating = False
                    break
            else:
                self.sand_produced += 1
                self.active_sand = self.produce_sand()
                if self.active_sand == None:
                    self.simulating = False
                    break
            #self.world.print_world()                                           # for fun, drawing the simulation
            #input("")
        if self.world.has_floor:
            print("b",self.sand_produced-1)
        else:
            print("a",self.sand_produced-1)


test_input = ["498,4 -> 498,6 -> 496,6", "503,4 -> 502,4 -> 502,9 -> 494,9"]
world_a_test = World(test_input, False)
world_b_test = World(test_input, True)
simulator = Simulator(world_a_test)
simulator.sim()
simulator = Simulator(world_b_test)
simulator.sim()

world_a = World(lines, False)
world_b = World(lines, True)
simulator = Simulator(world_a)
simulator.sim()
simulator = Simulator(world_b)
simulator.sim()

# The whole simulation would be a lot more efficient if the matrix only handled number values with no classes,
# which I knew in advance. But the whole structure ended up being pretty bad anyways, so just going with numbers
# would have probably been better & cleaner.
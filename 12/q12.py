import math
from aocd import lines

class Node():
    def __init__(self, i, j, height) -> None:
        self.height = self.get_height(height)
        self.parent = None
        self.g_cost = None
        self.h_cost = None
        self.f_cost = None
        self.height_symbol = height
        self.i = i
        self.j = j

    def __eq__(self, __o: object) -> bool:
        if type(__o) == tuple:
            return self.i == __o[0] and self.j == __o[1]
        if type(__o) == Node:
            return self.i == __o.i and self.j == __o.j

    def get_height(self, height):
        return ord(height)-96

    def __str__(self) -> str:
        return "["+str(self.i)+", "+str(self.j)+"]"

    def __repr__(self) -> str:
        return str(self)

    def set_parent(self, parent: 'Node'):
        self.parent = parent

    def set_f_cost(self):
        self.f_cost = self.h_cost + self.g_cost

    def distance_to(self, other: 'Node'):
        return math.sqrt((self.i - other.i)**2 + (self.j - other.j)**2)

class Grid():
    def __init__(self, input) -> None:
        self.input = input
        self.start = None
        self.goal = None
        self.open: 'list[Node]' = []
        self.closed = []
        self.matrix: 'list[list[Node]]' = self.get_matrix(self.input)

    def reset(self):
        self.start = None
        self.goal = None
        self.open: 'list[Node]' = []
        self.closed = []
        self.matrix: 'list[list[Node]]' = self.get_matrix(self.input)

    def get_matrix(self, input):
        matrix = []
        for i, line in enumerate(input):
            row = []
            for j, c in enumerate(line):
                if c == 'S':
                    row.append(Node(i, j, 'a'))
                    self.start = (i, j)
                elif c == 'E':
                    row.append(Node(i, j, 'z'))
                    self.goal = (i, j)
                else:
                    row.append(Node(i, j, c))
                    
            matrix.append(row)
        return matrix

    def sort_open(self):
        self.open.sort(key = lambda x: x.f_cost)

    def get_starting_node(self):
        return self.matrix[self.start[0]][self.start[1]]

    def get_goal_node(self):
        return self.matrix[self.goal[0]][self.goal[1]]

    def get_possible_next_steps(self, node: Node) -> 'list[Node]':
        i, j = node.i, node.j
        steps = []
        current_height = self.matrix[i][j].height
        if i > 0:
            di = i-1
            if self.matrix[di][j].height <= current_height + 1 and self.matrix[di][j] not in self.closed:
                steps.append(self.matrix[di][j])
        if i < len(self.matrix)-1:
            di = i+1
            if self.matrix[di][j].height <= current_height + 1 and self.matrix[di][j] not in self.closed:
                steps.append(self.matrix[di][j])
        if j > 0:
            dj = j-1
            if self.matrix[i][dj].height <= current_height + 1 and self.matrix[i][dj] not in self.closed:
                steps.append(self.matrix[i][dj])
        if j < len(self.matrix[i])-1:
            dj = j+1
            if self.matrix[i][dj].height <= current_height + 1 and self.matrix[i][dj] not in self.closed:
                steps.append(self.matrix[i][dj])
        return steps

    def get_h_cost(self, node: Node):
        return node.distance_to(self.get_goal_node())

    def get_cost():
        pass

    def construct_route(self):
        route = []
        current = self.get_goal_node()
        while True:
            route.append(current)
            if current.parent == None:
                break
            current = current.parent
        self.print_route(route)
        return ((len(route)-1), route)

    def print_route(self, route):
        route_tuples = list(map(lambda x: (x.i, x.j), route))
        for i in range(len(self.matrix)):
            row = ""
            for j in range(len(self.matrix[i])):
                if (i,j) in route_tuples:
                    row = row + "■"
                else:
                    row = row + self.matrix[i][j].height_symbol
            print(row)
        print("Route length:",len(route)-1)

    def find_all_abc_subroutes(self):
        all_abcs = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                current = self.matrix[i][j]
                if current.height == 1:
                    steps = self.get_possible_next_steps(current)
                    for step in steps:
                        if step.height == 2:
                            sub_steps = self.get_possible_next_steps(step)
                            for sub_step in sub_steps:
                                if sub_step.height == 3:
                                    all_abcs.append(current)
                                    continue
        return all_abcs

    def solve(self, starting_node: Node = None):
        if starting_node != None:
            self.start = (starting_node.i, starting_node.j)
        self.get_starting_node().g_cost = 0
        self.get_starting_node().h_cost = self.get_h_cost(self.get_starting_node())
        self.open.append(self.get_starting_node())

        while True:
            self.sort_open()
            current = self.open.pop(0)
            self.closed.append(current)
            if current == self.goal:
                break
            steps = self.get_possible_next_steps(current)
            for step in steps:
                if step not in self.open or current.g_cost + 1 < step.g_cost:
                    step.g_cost = current.g_cost + 1
                    step.h_cost = self.get_h_cost(step)
                    step.set_f_cost()
                    step.set_parent(current)
                if step not in self.open:
                    self.open.append(step)
        return self.construct_route()

    def solve_a(self):
        print("Solving best route from start (part a)")
        result = self.solve()
        print("a, best route is of length:",result[0])
        print()

    def solve_b(self):
        print("Solving best scenic route (part b)")
        self.reset()
        abcs = self.find_all_abc_subroutes()
        shortest = 99999
        best_node = None
        for idx, abc in enumerate(abcs):
            self.reset()
            print("Solving route " + str(idx+1) +"/" + str(len(abcs)) + "...")
            result = self.solve(abc)
            if result[0] < shortest:
                shortest = result[0]
                best_node = result[1]
        print("b, best scenic route is of length:",shortest)

# test_input = ["Sabqponm", "abcryxxl", "accszExk", "acctuvwj", "abdefghi"]
# grid = Grid(test_input)
# grid.solve_a()
# grid.solve_b()

grid = Grid(lines)
grid.solve_a()
grid.solve_b()
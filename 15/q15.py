from __future__ import division 
#from aocd import lines
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
import os
from matplotlib import pyplot as plt
import itertools

test_input = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)
with open(abs_file_path) as file:
    lines = [line.rstrip() for line in file]
test_input = test_input.split("\n")

def Line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def get_intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = int(Dx / D)
        y = int(Dy / D)
        return x,y
    else:
        return False

def manhattan_distance(x1, y1, x2, y2):
    return (abs(x1-x2)+abs(y1-y2))

class Diamond():
    def __init__(self, input_line: str) -> None:
        self.sensor = None
        self.beacon = None
        self.parse_line(input_line)
        self.corners = self.get_corners()

    def get_corners(self):
        corners = []
        d = manhattan_distance(self.sensor[0], self.sensor[1], self.beacon[0], self.beacon[1])
        corners.append((self.sensor[0] - d, self.sensor[1]))
        corners.append((self.sensor[0], self.sensor[1] + d))
        corners.append((self.sensor[0] + d, self.sensor[1]))
        corners.append((self.sensor[0], self.sensor[1] - d))
        return corners

    def parse_line(self, line):
        sensor_beacon_pair = []
        reading = False
        current = ""
        for c in line:
            if (not c.isnumeric() and c != '-') and reading:
                reading = False
                sensor_beacon_pair.append(int(current))
                current = ""
            if reading:
                current += c
            if c == "=":
                reading = True
        sensor_beacon_pair.append(int(current))
        self.sensor = (sensor_beacon_pair[0], sensor_beacon_pair[1])
        self.beacon = (sensor_beacon_pair[2], sensor_beacon_pair[3])

    def get_no_of_beacon_sensor_on_row(self, row):
        count = 0
        if self.beacon[1] == row:
            count += 1
        if self.sensor[1] == row:
            count += 1
        return count

    def get_intersections_with_row(self, row):
        mid_y = self.sensor[1]
        top_y = self.corners[1][1]
        btm_y = self.corners[3][1]
        intersections = []
        if row >= mid_y and row <= top_y:
            L1 = Line(self.corners[0], self.corners[1])
            LY = Line((0, row), (1, row))
            L2 = Line(self.corners[1], self.corners[2])
            R1 = get_intersection(L1, LY)
            R2 = get_intersection(L2, LY)
            intersections.append(R1)
            intersections.append(R2)
        elif row < mid_y and row >= btm_y:
            L1 = Line(self.corners[0], self.corners[3])
            LY = Line((0, row), (1, row))
            L2 = Line(self.corners[3], self.corners[2])
            R1 = get_intersection(L1, LY)
            R2 = get_intersection(L2, LY)
            intersections.append(R1)
            intersections.append(R2)
        else:
            return None
        return intersections

def tuple_tuples_lower_bound(tuple_tuple):
    return tuple_tuple[0][0]

def get_line_len(line: list):
    return abs(line[0]-line[1])+1

def get_lines_total_len(lines):
    total = 0
    for line in lines:
        total += get_line_len(line)
    return total

def get_no_of_beacons_sensors_on_row(arr: 'list[Diamond]', row):
    beacons_sensors = []
    for d in arr:
        s = d.sensor
        b = d.beacon
        if b not in beacons_sensors and b[1] == row:
            beacons_sensors.append(b)
        if s not in beacons_sensors and s[1] == row:
            beacons_sensors.append(s)
    return len(beacons_sensors)

def get_scanned_points_no_on_row(diamonds: 'list[Diamond]', row):
    lines = []
    for d in diamonds:    
        intersections = d.get_intersections_with_row(row)
        if intersections:
            lines.append( (intersections[0], intersections[1]) )
    lines.sort(key=tuple_tuples_lower_bound)
    only_x = list(map(lambda x: [x[0][0], x[1][0]], lines))
    merged = [only_x[0]]
    for current in only_x:
        previous = merged[-1]
        if current[0] <= previous[1]:
            previous[1] = max(previous[1], current[1])
        else:
            merged.append(current)
    total_on_row = get_lines_total_len(merged) - get_no_of_beacons_sensors_on_row(diamonds, row)
    print("a:",total_on_row)

def get_combined_polygon(ds: 'list[Diamond]'):
    polygons = []
    for idx, d in enumerate(ds):
        polygon_geom = Polygon(d.corners)
        polygon = gpd.GeoDataFrame(index=[idx], crs='epsg:4326', geometry=[polygon_geom])       
        polygons.append(polygon)
    rdf = gpd.GeoDataFrame( pd.concat( polygons, ignore_index=True ) )
    rdf.shape
    geoms = rdf['geometry'].tolist()
    intersection_iter = gpd.GeoDataFrame(gpd.GeoSeries([poly[0].union(poly[1]) for poly in  itertools.combinations(geoms, 2) if poly[0].union(poly[1])]), columns=['geometry'])
    union_iter: Polygon = intersection_iter.unary_union
    df = gpd.GeoDataFrame()
    df['index'] = "0"
    df['geometry'] = [ union_iter ]
    df = df.set_geometry('geometry')
    df.loc[[0],'geometry'].plot()
    plt.savefig("combined_polygon.png")
    return union_iter

def get_polygon_inner_ring(polygon):
    interior_ring = polygon.interiors[0].coords.xy
    interior_ring = list(zip(interior_ring[0], interior_ring[1]))
    return interior_ring

def get_freq(x,y):
    m = 4000000
    return x*m + y

def get_all_points_next_to_point(p):
    x, y = p[0], p[1]
    all_points = []
    all_points.append((x+1, y))
    all_points.append((x-1, y))
    all_points.append((x, y+1))
    all_points.append((x, y-1))
    return all_points

def point_next_to_all_given_points(arr: list):
    points = []
    for idx, p in enumerate(arr):
        ap = get_all_points_next_to_point(p)
        if idx == 0:
            points += ap
        else:
            for pp in points:
                if pp not in ap:
                    points.remove(pp)
    return (int(points[0][0]), int(points[0][1]))


def solve_b(scanned_areas):
    combined_polygon = get_combined_polygon(scanned_areas)              # combine all polygons
    polygon_interior_ring = get_polygon_inner_ring(combined_polygon)    # find polygon interior ring
    p = point_next_to_all_given_points(polygon_interior_ring)           # find the one wide/height point that is inside the interior ring
    val = get_freq(p[0], p[1])                                          # get ans
    print("b:",val)

row = 2000000
#row = 10                                                               # row value for test_input
scanned_areas = []
for line in lines:
    d = Diamond(line)
    scanned_areas.append(d)

get_scanned_points_no_on_row(scanned_areas, row)                        # a
solve_b(scanned_areas)                                                  # b

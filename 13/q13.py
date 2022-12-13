import ast
from aocd import data
from functools import cmp_to_key

def compare(l_v, r_v):
    if isinstance(l_v, int) and isinstance(r_v, int):
        if l_v < r_v:
            return 1
        if l_v > r_v:
            return -1
        return 0
    else:
        if isinstance(r_v, int):
            r_v = [r_v]
        if isinstance(l_v, int):
            l_v = [l_v]
        for c in (compare(lz, rz) for lz, rz in zip(l_v,r_v)):
            if c != 0:
                return c
        if len(l_v) < len(r_v):
            return 1
        if len(l_v) > len(r_v):
            return -1
        return 0

def solve(data):
    packets_data = data.split('\n')
    packets = []
    for packet_data in packets_data:
        if packet_data != '':
            packets.append(ast.literal_eval(packet_data))
    idxs = []
    for i in range(0,len(packets)-1,2):
        if compare(packets[i], packets[i+1]) == 1:
            idxs.append(int(i/2 + 1))
    print("a:",sum(idxs))
    dividers = [ [[2]], [[6]] ]
    sorted_packets = sorted(packets + dividers, key=cmp_to_key(compare), reverse=True)
    decoder = (sorted_packets.index(dividers[0])+1) * (sorted_packets.index(dividers[1])+1)
    print("b:",decoder)

import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "test_input.txt"
abs_file_path = os.path.join(script_dir, rel_path)
with open(abs_file_path) as file:
    test_input = file.read()

solve(test_input)
solve(data)
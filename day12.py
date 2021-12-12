
from collections import defaultdict
from dataclasses import dataclass
from pprint import pp
from typing import Counter


@dataclass
class Colours:
    green = "\033[92m"
    red = "\033[91m"
    endc = "\033[0m"

    @classmethod
    def wrap(cls, color, text):
        return color + text + cls.endc

def green(t):
    return Colours.wrap(Colours.green, t)


def red(t):
    return Colours.wrap(Colours.red, t)


def find_all_paths(graph, start, end, path=[], depth=0):
    if depth > 100:
        raise Exception("Depth too deep")
    d = "----" * depth

    path = path + [start]
    if start == end:
        return [path]
    
    if not start in graph:
        return []
    
    paths = []
    for node in graph[start]:

        big_cave = node.isupper()

        if big_cave:
            can_traverse = True
        elif node == "start":
            can_traverse = False
        else:
            small_counter = Counter([n for n in path if n.islower() and n != "start"])
            visited_caves = small_counter[node]
            if 2 in small_counter.values():
                can_traverse = visited_caves < 1
            else:
                can_traverse = visited_caves < 2

            #print(d, "Visits", small_counter, "this count", visited_caves, "can traverse", can_traverse)

        if can_traverse:
            #print(f"{d} OK {start} to {node} {node.upper() == node} : node={node} : {path}")
            newpaths = find_all_paths(graph, node, end, path, depth=depth+1)
            for newpath in newpaths:
                paths.append(newpath)
        else:
            pass#print(red(f"{d} XXXXX not going from {start} to {node} {node.upper() == node}: node={node} : {path}"))
    return paths


def process_instructions(test_data):

    test_data = [td for td in test_data.split("\n") if td]

    graph = defaultdict(list)
    for line in test_data:
        a, b = line.split("-")
        if b != "start":
            graph[a].append(b)
        if b != "end":
            graph[b].append(a)

    from pprint import pprint
    pprint(graph)

    paths = find_all_paths(graph, "start", "end")

    for path in paths:
        print("ALL", path)

    return len(paths)


def test_day_short1_input():
    test_instructions = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""
    result = process_instructions(test_instructions)
    assert result == 36

def test_day_short2_input():
    test_instructions = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""
    result = process_instructions(test_instructions)
    assert result == 103

def test_day_short3_input():
    test_instructions = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""
    result = process_instructions(test_instructions)
    assert result == 3509

def test_day_real_input():
    test_instructions = open("day12_input").read()
    result = process_instructions(test_instructions)
    assert result == 83475

from collections import defaultdict, deque
from dataclasses import dataclass
from pprint import pp
from typing import List
from itertools import permutations


@dataclass
class Node:
    start: str
    end: str

    def next_nodes(self, nodes):
        return list(filter(lambda n: self.end == n.start, nodes))


def flatten(l):
    return [item for sublist in l for item in sublist]

@dataclass
class Cave:
    nodes: List[Node]

    def print(self):
        for node in self.nodes:
            print(f"{node.start} -> {node.end}")

    def traverse(self, node_name):
        nexts = list(filter(lambda n: n.start == node_name, self.nodes))

        print(f"Traversing... {node_name} -> {nexts}")
        if node_name == "end":
            return [node_name]

        paths = []
        for next_node in nexts:
            further_path = self.traverse(next_node.end)
            print(f"Processing NEXT with {next_node} -> {further_path}")
            if further_path == ["end"]:
                pass
            else:
                paths.append([node_name] + flatten(further_path))
        
        return paths

# Code by Eryk Kopczyński
def find_shortest_path(graph, start, end, path=[], depth=0):
    path = path + [start]
    if start == end:
        return path
    if start not in graph :
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path, depth=depth+1)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

def find_all_paths(graph, start, end, path=[], depth=0):
    if depth > 100:
        raise Exception("Depth too deep")
    d = "----" * depth

    #print(f"{d} from {start} to {end}")
    path = path + [start]
    if start == end:
        return [path]
    #if end == "end":
    #    return [path]
    if not start in graph:
        return []
    paths = []
    for node in graph[start]:
        #if node not in path:
        can_traverse = node.upper() == node or node not in path
        if can_traverse:
            print(f"{d} OK {start} to {node} {node.upper() == node} : node={node} : {path}")
            newpaths = find_all_paths(graph, node, end, path, depth=depth+1)
            for newpath in newpaths:
                paths.append(newpath)
        else:
            print(f"{d} XXXXX not going from {start} to {node} {node.upper() == node}: node={node} : {path}")
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

    shortest = find_shortest_path(graph, "start", "end")

    print("Shortest", shortest)

    paths = find_all_paths(graph, "start", "end")

    for path in paths:
        print("ALL", path)

    return len(paths)

    cave = Cave([])

    cave.print()
    print("xxx")

    #paths = cave.traverse("start")
    #for p in paths:
    #    print(p)

    return -1


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
    assert result == 10

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
    assert result == 19

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
    assert result == 226

def test_day_real_input():
    test_instructions = open("day12_input").read()
    result = process_instructions(test_instructions)
    assert result == 3230
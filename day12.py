
from collections import defaultdict
from dataclasses import dataclass
from typing import Counter, Dict


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


def flatten(l):
    return [item for sublist in l for item in sublist]


@dataclass
class Cave:
    nodes: Dict
    small_cave_single_visit_limit = 2
    small_cave_multiple_visit_limit = 1

    @classmethod
    def from_definition(cls, lines):
        graph = defaultdict(list)
        for line in lines:
            a, b = line.split("-")
            if b != "start":
                graph[a].append(b)
            if b != "end":
                graph[b].append(a)
        return cls(graph)

    @staticmethod
    def is_big_cave(node):
        return node.isupper()

    @staticmethod
    def is_small_cave(node):
        return node.islower() and node != "start"

    def small_caves_in_path(self, path):
        return filter(Cave.is_small_cave, path)

    def can_traverse(self, node, path):
        if node == "start":
            return False
        elif Cave.is_big_cave(node):
            return True
        else:
            counter = Counter(self.small_caves_in_path(path))
            visited_caves = counter[node]
            if self.small_cave_single_visit_limit in counter.values():
                return visited_caves < self.small_cave_multiple_visit_limit
            else:
                return visited_caves < self.small_cave_single_visit_limit

    def find_all_paths(self, start, end, path=[], depth=0):
        
        path = path + [start]
        if start == end:
            return [path]

        paths = [
            self.find_all_paths(node, end, path, depth + 1)
            for node in self.nodes[start]
            if self.can_traverse(node, path)
        ]
        
        return flatten(paths)


def process_instructions(test_data):

    test_data = [td for td in test_data.split("\n") if td]

    cave = Cave.from_definition(test_data)

    paths = cave.find_all_paths("start", "end")

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

from typing import List
from dataclasses import dataclass
from collections import defaultdict
import networkx as nx


class Colours:
    green = "\033[92m"
    red = "\033[91m"
    blue = "\033[0;34m"
    endc = "\033[0m"
    
    @classmethod
    def wrap(cls, color, text):
        return color + text + cls.endc


def format(x, color=None):
    if color:
        return Colours.wrap(color, f"{x:2}")
    else:
        return f"{x:2}"

def red(t):
    return Colours.wrap(Colours.red, t)


def green(t):
    return Colours.wrap(Colours.green, t)


@dataclass
class Grid:
    rows: List[List[int]]

    def __str__(self):
        output = f"BOARD\n"
        output += "- "
        output += "".join([
            format(x, color=Colours.blue)
            for x in range(len(self.rows[0]))]
        ) + "\n"
        for i, row in enumerate(self.rows):
            output += format(i, color=Colours.blue) + " "
            output += "".join(format(x) for x in row) + "\n"
        return output

    def with_path(self, paths):
        output = f"BOARD\n"
        output += " - "
        output += "".join([
            format(x, color=Colours.blue)
            for x in range(len(self.rows[0]))]
        ) + "\n"
        for i, row in enumerate(self.rows):
            output += format(i, color=Colours.blue) + " "
            output += "".join(self.format_in_path(x, i, j, paths) for j, x in enumerate(row)) + "\n"
        return output

    def format_in_path(self, val, i, j, paths):
        if (i, j) in paths:
            return Colours.wrap(Colours.red, f"{val:2}")
        else:
            return f"{val:2}"

    def add_points(self, p1, p2):
        return (p1[0] + p2[0], p1[1] + p2[1])

    def get_neighbours(self, i, j):
        points_around = [
            self.add_points((i, j), p) for p in [
                (0, 1),
                (1, 0),
                (0, -1),
                (-1, 0),
            ]
        ]

        all_points_in_range = [
            p
            for p in points_around
            if p[0] >= 0
            and p[1] >= 0
            and p[0] < len(self.rows)
            and p[1] < len(self.rows[i])
        ]
        return set(all_points_in_range)

    def graph(self):
        routes = defaultdict(list)
        for i, row in enumerate(self.rows):
            for j, val in enumerate(row):
                neighbours = self.get_neighbours(i, j)
                if neighbours:
                    for neighbour in neighbours:
                        neighbour_val = self.rows[neighbour[0]][neighbour[1]]
                        routes[(i ,j)].append((neighbour[0], neighbour[1], neighbour_val))
                else:
                    routes[(i, j)] = []
        return routes

def process(test_data):

    grid = Grid(test_data)
    print(grid)

    graph = nx.DiGraph()

    for i, row in enumerate(test_data):
        for j, val in enumerate(row):
            loc = (i, j)
            neightbours = grid.get_neighbours(*loc)
            graph.add_node(loc)
            for n in neightbours:
                graph.add_edge(loc, n, weight=test_data[n[0]][n[1]])

    start = (0, 0)
    end = (len(test_data) - 1, len(test_data[0]) - 1)
    sp = nx.shortest_path(graph, end, start, weight="weight")
    print(start, end)
    print(grid.with_path(sp))

    risks = [test_data[i][j] for i, j in sp if (i, j) != (0, 0)]

    print("shortest_path", sum(risks))

    return sum(risks)

def process_instructions(test_data):
    test_data = [td for td in test_data.split("\n") if td]
    test_data = [[int(t) for t in td] for td in test_data if td]
    return process(test_data)


def test_day_short_input():
    test_instructions = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
    result = process_instructions(test_instructions)
    assert result == 40

def test_day_very_short_input():
    test_instructions = """
11634
13813
21367
36942
"""
    result = process_instructions(test_instructions)
    assert result == 19


def test_day_real_input():
    test_instructions = open("day15_input").read()
    result = process_instructions(test_instructions)
    assert result == 621, result

if __name__ == "__main__":
    #test_day_very_short_input()
    #test_day_short_input()
    test_day_real_input()
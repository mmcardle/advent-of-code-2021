
from dataclasses import dataclass
from typing import List

MAX = 9

class Colours:
    green = "\033[92m"
    red = "\033[91m"
    blue = "\033[0;34m"
    endc = "\033[0m"
    
    @classmethod
    def wrap(cls, color, text):
        return color + text + cls.endc


def format(x, color=None):
    if x > MAX:
        return Colours.wrap(Colours.red, f"{x:2}")
    elif color:
        return Colours.wrap(color, f"{x:2}")
    else:
        return f"{x:2}"


@dataclass
class Grid:
    rows: List[List[int]]
    step_number: int = 0
    flashed = []
    flash_count = 0

    def __post_init__(self):
        self.flashed = []
        self.flash_count = 0

    def __str__(self):
        output = f"BOARD (step={self.step_number})\n"
        output += " - "
        output += " ".join([
            format(x, color=Colours.blue)
            for x in range(len(self.rows[0]))]
        ) + "\n"
        for i, row in enumerate(self.rows):
            output += format(i, color=Colours.blue) + " "
            output += " ".join(format(x) for x in row) + "\n"
        return output

    def add_points(self, p1, p2):
        return (p1[0] + p2[0], p1[1] + p2[1])

    def get_neighbours(self, i, j):
        points_around = [
            self.add_points((i, j), p) for p in [
                (1, 0),
                (0, 1),
                (-1, 0),
                (0, -1),
                (1, 1),
                (-1, -1),
                (-1, 1),
                (1, -1),
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


    def flash(self, i, j):
        self.flash_count += 1
        self.rows[i][j] = self.rows[i][j] + 1
        neighbours = self.get_neighbours(i, j)
        print(
            Colours.wrap(Colours.red, "FLASH"),
            "at",
            Colours.wrap(Colours.green, str(i)),
            Colours.wrap(Colours.green, str(j)),
            "- Points near", i, j, neighbours
        )
        for ni, nj in neighbours:
            print("bump neighbour of", i, j, ":", ni, nj)
            self.rows[ni][nj] = self.rows[ni][nj] + 1
        for ni, nj in neighbours:
            print("check neighbour of", i, j, ":", ni, nj)
            self.check_value(ni, nj)

    def check_value(self, i, j):
        print(
            "Checking", i, j, "value (", self.rows[i][j] -1, "->", self.rows[i][j],
            ") flashed =", self.flashed
        )
        if self.rows[i][j] > MAX:
            if (i, j) not in self.flashed:
                self.flashed.append((i, j))
                self.flash(i, j)
            else:
                print(Colours.wrap(Colours.blue, "Already flashed"), i, j)

    def step(self):
        for i, row in enumerate(self.rows):
            for j in range(len(row)):
                self.rows[i][j] += 1
        print(self)
        for i, row in enumerate(self.rows):
            for j in range(len(row)):
                self.check_value(i, j)
        for (i, j) in self.flashed:
            self.rows[i][j] = 0
        self.step_number += 1

        all_flashed = True
        for row in self.rows:
            if set(row) != {0}:
                all_flashed = False
        if all_flashed:
            return True

        self.flashed = []

        return False


def process_instructions(test_data, iterations=1):

    rows = [[int(v) for v in line] for line in [td for td in test_data.split("\n") if td]]
    grid = Grid(rows)

    for _ in range(iterations):
        all_flashed = grid.step()
        if all_flashed:
            break
    return grid


def test_day_short_input1():
    test_instructions = """
11111
19991
19191
19991
11111
"""
    grid = process_instructions(test_instructions, 2)
    assert grid.flash_count == 9

def test_day_short_input2():
    test_instructions = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
    grid = process_instructions(test_instructions, 100)
    assert grid.flash_count == 1656

def test_day_real_input():
    test_instructions = """
4764745784
4643457176
8322628477
7617152546
6137518165
1556723176
2187861886
2553422625
4817584638
3754285662
"""
    grid = process_instructions(test_instructions, 1000)
    assert grid.step_number == 517
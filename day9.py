from dataclasses import dataclass
from typing import List

X = "X"


@dataclass
class Colours:
    green = "\033[92m"
    red = "\033[91m"
    endc = "\033[0m"

    @classmethod
    def wrap(cls, color, text):
        return color + text + cls.endc


def colorise(text, color=Colours.green):
    if "9" in text:
        return Colours.wrap(Colours.red, text)
    else:
        return Colours.wrap(color, text)


@dataclass
class Grid:
    rows: List[List[int]]

    def __hash__(self) -> int:
        return hash("".join(str(cell) for cell in row) for row in self.rows)

    def __str__(self) -> str:
        return "\n".join(
            " ".join(colorise(str(cell)) for cell in row) for row in self.rows
        )

    def low_points(self) -> int:

        low_points = []

        for i in range(len(self.rows)):
            for j in range(len(self.rows[i])):
                value_at_point = self.rows[i][j]
                up = self.rows[i - 1][j] if i > 0 else X
                down = self.rows[i + 1][j] if i < len(self.rows) - 1 else X
                left = self.rows[i][j - 1] if j > 0 else X
                right = self.rows[i][j + 1] if j < len(self.rows[i]) - 1 else X

                adjacent_values = [x for x in [up, down, left, right] if x != X]

                higher_comparison = [x for x in adjacent_values if x > value_at_point]

                if len(adjacent_values) == len(higher_comparison):
                    low_points.append([i, j, value_at_point])

        return low_points

    def risk(self):
        low_points = [v for (i, j, v) in self.low_points()]
        return sum([p + 1 for p in low_points])

    def add_points(self, p1, p2):
        return (p1[0] + p2[0], p1[1] + p2[1])

    def around(self, i, j):
        points_around = [
            self.add_points((i, j), p) for p in [(1, 0), (0, 1), (-1, 0), (0, -1)]
        ]

        all_points_in_range = [
            p
            for p in points_around
            if p[0] >= 0
            and p[1] >= 0
            and p[0] < len(self.rows)
            and p[1] < len(self.rows[i])
        ]

        return list(filter(lambda p: self.rows[p[0]][p[1]] != 9, all_points_in_range))

    points_cache = {}

    def points_around(self, i, j, exclude=None):

        if (i, j) in self.points_cache:
            return self.points_cache[(i, j)]

        if not exclude:
            exclude = []

        points_around = self.around(i, j)
        points_around_excluded = [p for p in points_around if p not in exclude]

        for new_point in points_around_excluded:
            new_exclude = exclude + [(i, j)]
            points_around.extend(
                self.points_around(new_point[0], new_point[1], exclude=new_exclude)
            )

        self.points_cache[(i, j)] = points_around

        return points_around

    def basins(self):

        size_of_basins = []

        for (i, j, v) in self.low_points():
            points_in_basin = set(self.points_around(i, j))
            points_in_basin = [self.rows[p[0]][p[1]] for p in points_in_basin]
            size_of_basins.append(len(points_in_basin))

        top3 = sorted(size_of_basins, reverse=True)[0:3]
        return top3[0] * top3[1] * top3[2]

    def largest_basins(self):

        return self.basins()


def process_instructions(test_data):
    rows = [td for td in test_data.split("\n") if td]
    grid = Grid([[int(v) for v in row] for row in rows])
    return grid


def test_grid_add_points():
    test_instructions = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
    grid = process_instructions(test_instructions)
    assert grid.around(0, 1) == [(0, 0)]
    # assert grid.add_points((0, 0), (1, 1)) == (1, 1)


def test_day_short_input():
    test_instructions = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""
    grid = process_instructions(test_instructions)
    assert grid.risk() == 15
    x = grid.largest_basins()
    assert x == 1134
    assert False


def test_day_real_input():
    test_instructions = open("day9_input").read()
    grid = process_instructions(test_instructions)
    assert grid.risk() == 456
    assert grid.largest_basins() == 1047744

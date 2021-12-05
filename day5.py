
from dataclasses import dataclass
from typing import List

PIPE = "."

@dataclass
class Colours:
    green = "\033[92m"
    red = "\033[91m"
    endc = "\033[0m"
    
    @classmethod
    def wrap(cls, color, text):
        return color + text + cls.endc

    def __repr__(self):
        return f"{self.__class__.__name__}({self.rows})"


def colorise(text):
    if type(text) == str and str(text) == PIPE:
        return text
    value = int(text)
    if value == 1:
        return Colours.wrap(Colours.green, text)
    if value > 1:
        return Colours.wrap(Colours.red, text)
    return text


@dataclass
class Vent:
    x1: int
    y1: int
    x2: int
    y2: int

    def __str__(self):
        return f"{self.x1},{self.y1} -> {self.x2},{self.y2}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"

    @staticmethod
    def dangerous(value):
        return (value != PIPE and int(value) > 1)

    @staticmethod
    def ranged(x, y):
        if x > y:
            return range(x, y - 1, -1)
        if x < y:
            return range(x, y + 1)
        else:
            return []


@dataclass
class Grid:
    rows: List[List[int]]

    def __str__(self):
        return f"{self.__class__.__name__}\n"

    def debug(self):
        output = f"{self.__class__.__name__} (danger={self.danger()})\n"
        for row in self.rows:
            output += " ".join(colorise(str(f"{x:1}")) for x in row) + "\n"
        return output

    @classmethod
    def dangerous(cls, value):
        return (value != PIPE and int(value) > 1)

    def danger(self):
        return sum(
            1 for row in self.rows for x in row
            if Vent.dangerous(x)
        )

    def add_pipe_at(self, x, y):
        current = self.rows[y][x]
        if current == PIPE:
            self.rows[y][x] = 1
        else:
            self.rows[y][x] = current + 1

    def add_vent(self, vent: Vent):
        if vent.x1 == vent.x2:
            for y in Vent.ranged(vent.y1, vent.y2):
                self.add_pipe_at(vent.x1, y)
        
        elif vent.y1 == vent.y2:
            for x in Vent.ranged(vent.x1, vent.x2):
                self.add_pipe_at(x, vent.y1)
        else:
            x_range = Vent.ranged(vent.x1, vent.x2)
            y_range = Vent.ranged(vent.y1, vent.y2)
            for xd, yd in zip(x_range, y_range):
                self.add_pipe_at(xd, yd)


def process_instructions(test_data):

    test_data = [td for td in test_data.split("\n") if td]

    vents = []
    vent_range = 10
    for instruction in test_data:
        split = instruction.split(" -> ")
        x0_str, y0_str = split[0].split(",")
        x1_str, y1_str = split[1].split(",")
        x1, y1, x2, y2 = int(x0_str), int(y0_str), int(x1_str), int(y1_str)
        vent = Vent(x1, y1, x2, y2)
        vents.append(vent)
        vent_range = max(vent_range, max(x1, x2), max(y1, y2))

    grid = Grid(
        [["." for _ in range(vent_range + 1)] for y in range(vent_range + 1)]
    )

    for vent in vents:
        grid.add_vent(vent)

    return grid


def test_day_short_input():
    test_instructions = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""
    result = process_instructions(test_instructions)
    assert result.danger() == 12
    print(result.debug())
    assert False


def test_day_real_input():
    test_instructions = open("day5_input").read()
    result = process_instructions(test_instructions)
    assert result.danger() == 22037

from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Colours:
    green = "\033[92m"
    red = "\033[91m"
    endc = "\033[0m"

    @classmethod
    def wrap(cls, color, text):
        return color + text + cls.endc

def red(t):
    return Colours.wrap(Colours.red, t)

def green(t):
    return Colours.wrap(Colours.green, t)


@dataclass
class Grid:
    points: List[Tuple[int, int]]

    def __str__(self):
        return self.print_grid()

    def print_grid(self, fold=None):
        output = "Grid:\n"
        max_y = max(self.points, key=lambda x: x[1])[1]
        max_x = max(self.points, key=lambda x: x[0])[0]

        output += "  "
        for x in range(max_x + 1):
            if fold and fold[0] == "x" and fold[1] == x:
                output += red(" |")
            output += green(f"{x:2}")
        output += "\n"
        
        for y in range(min(self.points, key=lambda x: x[1])[1], max_y + 1):
            if fold is not None and fold[0] == "y" and y == fold[1]:
                output += "  "
                output += red("--" * (max_x + 1))
                output += "\n"
            output += green(f"{y:2}")
            for x in range(min(self.points, key=lambda x: x[0])[0], max_x + 1):
                if fold is not None and fold[0] == "x" and x == fold[1]:
                    output += red(" |")
                if (x, y) in self.points:
                    output += " #"
                else:
                    output += " ."
            output += "\n"
        return output + "\n"

    def fold(self, fold):
        axis, num = fold
        #print("BEFORE:", axis, num)
        #print(self.print_grid(fold))

        max_y = max(self.points, key=lambda x: x[1])[1]
        max_x = max(self.points, key=lambda x: x[0])[0]

        #print("Max Y:", max_y)
        #print("Max X:", max_x)

        new_points = []

        if axis == "y":
            for point in self.points:
                if point[1] > num:
                    new_point = (point[0], max_y - point[1])
                    new_points.append(new_point)
                else:
                    new_points.append(point)
        
        if axis == "x":
            for point in self.points:
                if point[0] > num:
                    new_point = (max_x - point[0], point[1])
                    new_points.append(new_point)
                else:
                    new_points.append(point)

        self.points = list(set(new_points))

        #print("AFTER:", axis, num)
        #print(self.print_grid(fold))


def process_data(points, folds, num_folds):
    
    grid = Grid(points)

    if not num_folds:
        num_folds = len(folds)
    
    for fold in folds[:num_folds]:
        grid.fold(fold)

    print(grid)

    return grid


def process_instructions(test_data, num_folds=1):

    preface = "fold along "

    test_data = [td for td in test_data.split("\n") if td]

    points = [
        tuple(map(int, td.split(","))) for td in test_data
        if not td.startswith(preface)
    ]

    folds = [
        td[len(preface):].split("=") for td in test_data
        if td.startswith(preface)
    ]

    folds = [(str(x[0]), int(x[1])) for x in folds]

    #print(points)
    #print(folds)

    return process_data(points, folds, num_folds)


def test_day_short_input():
    test_instructions = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""
    grid = process_instructions(test_instructions, 1)
    assert len(grid.points) == 17


def test_day_real_input_1fold():
    test_instructions = open("day13_input").read()
    grid = process_instructions(test_instructions, 1)
    assert len(grid.points)  == 814


def test_day_real_input_all_folds():
    test_instructions = open("day13_input").read()
    grid = process_instructions(test_instructions, None)
    assert len(grid.points)  == 108
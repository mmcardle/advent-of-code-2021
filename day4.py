
from dataclasses import dataclass
import pdb
from typing import Counter, List

@dataclass

class Colours:
    green = "\033[92m"
    red = "\033[91m"
    endc = "\033[0m"
    
    @classmethod
    def wrap(cls, color, text):
        return color + text + cls.endc


def colorise(x):
    if "X" in x:
        return Colours.wrap(Colours.red, x)
    else:
        return x

@dataclass
class Board:
    index: int
    rows: List[List[int]]

    def __post_init__(self):
        self.rows = [list(row) for row in self.rows]

    def __str__(self):
        output = f"BOARD {self.index}\n"
        for row in self.rows:
            output += " ".join(colorise(str(f"{x:2}")) for x in row) + "\n"
        return output

    def __repr__(self):
        return f"Board({self.rows})"

    def winning_score(self):
        score = 0
        for row in self.rows:
            for number in row:
                if number != "X":
                    print("score"   , score)
                    score += number
        return score

    def check_win(self):
        for row in self.rows:
            if set(row) == {"X"}:
                return True

        columns = [list(column) for column in zip(*self.rows)]
        for column in columns:
            if set(column) == {"X"}:
                return True
        return False

    def mark(self, number):
        for row in self.rows:
            if number in row:
                row[row.index(number)] = "X"
                return

@dataclass
class Bingo:
    numbers: List[int]
    boards: List[Board]

    def __str__(self):
        output = "BINGO\n"
        for board in self.boards:
            output += str(board) + "\n"
        return output
    
    def play(self):
        for number in self.numbers:
            for board in self.boards:
                board.mark(number)
                if board.check_win():
                    return board, number


def process_instructions(test_data):

    test_data = [td for td in test_data.split("\n") if td]

    numbers = [int(x) for x in test_data[0].split(",")]
    board_numbers = test_data[1:]
    board_numbers = [board_numbers[i:i + 5] for i in range(0, len(board_numbers), 5)]

    boards = []

    for i, board in enumerate(board_numbers):
        rows = []
        for row in board:
            rows.append([int(n) for n in row.split()])
        boards.append(Board(i + 1, rows))

    bingo = Bingo(numbers, boards)
    return bingo


def test_day4_short_input():
    test_instructions = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""
    bingo = process_instructions(test_instructions)
    winning_board, winning_number = bingo.play()
    score = winning_board.winning_score() * winning_number
    assert score == 4512
    assert winning_board.index == 3
    print(bingo)
    print("WINNNER")
    print("winning_number", winning_number)
    print(winning_board)
    print(winning_board.winning_score())
    assert False


def test_day4_real_input():
    test_input = open("day4_input").read()
    bingo = process_instructions(test_input)
    winning_board, winning_number = bingo.play()
    score = winning_board.winning_score() * winning_number
    assert score == 44736
    assert winning_board.index == 42
    print(bingo)
    print("WINNNER")
    print("winning_number", winning_number)
    print(winning_board)
    print(winning_board.winning_score())
    assert False
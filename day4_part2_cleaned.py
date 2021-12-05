
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
    if X in text:
        return Colours.wrap(color, text)
    else:
        return text


@dataclass
class Board:
    index: int
    rows: List[List[int]]
    has_won: bool = False

    def __post_init__(self):
        self.rows = [list(row) for row in self.rows]

    def __str__(self):
        output = f"{self.__class__.__name__} {self.index} (won={self.has_won})\n"
        for row in self.rows:
            if self.row_has_won(row):
                output += " ".join(colorise(str(f"{x:2}")) for x in row) + "\n"
            else:
                output += " ".join(colorise(str(f"{x:2}"), color=Colours.red) for x in row) + "\n"
        return output

    def __repr__(self):
        return f"{self.__class__.__name__}({self.rows})"

    def winning_score(self):
        return sum([n for row in self.rows for n in row if n != X])

    def columns(self):
        return [list(column) for column in zip(*self.rows)]

    def row_has_won(self, row):
        return set(row) == {X}

    def column_has_won(self, column):
        return set(column) == {X}

    def check_win(self):
        for row in self.rows:
            if self.row_has_won(row):
                return True

        for column in self.columns():
            if self.column_has_won(column):
                return True
        return False

    def mark(self, number):
        for row in self.rows:
            if number in row:
                row[row.index(number)] = X
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
                if not board.has_won:
                    board.mark(number)
                if board.check_win():
                    non_winning_boards = [board for board in self.boards if not board.has_won]
                    
                    board.has_won = True

                    if len(non_winning_boards) == 1 and board.has_won:
                        last_board = non_winning_boards[0]
                        if last_board.check_win():
                            last_board.has_won = True
                            return last_board, number

        raise Exception("No winner")


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
    last_board_to_win, winning_number = bingo.play()
    score = last_board_to_win.winning_score() * winning_number
    assert score == 1924
    assert last_board_to_win.index == 2


def test_day4_real_input():
    test_input = open("day4_input").read()
    bingo = process_instructions(test_input)
    last_board_to_win, winning_number = bingo.play()
    score = last_board_to_win.winning_score() * winning_number
    assert score == 1827
    assert last_board_to_win.index == 40
    print(bingo)

if __name__ == "__main__":
    test_day4_real_input()
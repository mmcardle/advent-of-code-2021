
from functools import lru_cache
from typing import List


@lru_cache(maxsize=None)
def pascals_triangle(n: int):
    return sum(list(range(1, n + 1)))


def sum_diff_list(val: int, lst: List):
    return sum([pascals_triangle(abs(v - val)) for v in lst])


def process_instructions(test_data: str):
    test_data = [int(val) for val in test_data.split(",") if val]
    return min([sum_diff_list(i, test_data) for i in range(0, max(test_data))])


def test_day_short_input():
    test_instructions = """16,1,2,0,4,2,7,1,2,14"""
    result = process_instructions(test_instructions)
    assert result == 168


def test_day_real_input():
    test_instructions = open("day7_input").read()
    result = process_instructions(test_instructions)
    assert result == 94004208


def test_pascals_triangle():
    assert pascals_triangle(1) == 1
    assert pascals_triangle(5) == 15
    assert pascals_triangle(11) == 66
    assert pascals_triangle(9) == 45
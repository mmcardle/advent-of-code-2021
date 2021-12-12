
from dataclasses import dataclass


@dataclass
class Data:
    gamma: int


def process_instructions(test_data):

    test_data = [td for td in test_data.split("\n") if td]

    return -1


def test_day_short_input():
    test_instructions = """
XXXX
"""
    result = process_instructions(test_instructions)
    assert result == 99999


def test_day_real_input():
    test_instructions = open("day3_input").read()
    result = process_instructions(test_instructions)
    assert result == 99999
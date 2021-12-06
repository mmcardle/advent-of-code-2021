
from collections import Counter
from dataclasses import dataclass
from typing import Dict

MAX_AGE = 8
MIN_AGE = 0
REBORN_AGE = 6


@dataclass
class FishTracker():
    fish_ages: Dict

    @classmethod
    def from_string(cls, string):
        data = Counter([int(x) for x in string.strip("\n").split(",")])
        return cls(data)

    def age_fish(self):
        new_ages = {x: 0 for x in range(0, MAX_AGE + 1)}
        dead_fish = 0
        for age in range(MAX_AGE, MIN_AGE -1, -1):

            number_of_fish = self.fish_ages[age]

            if age == MIN_AGE:
                # Fish has died
                new_ages[MAX_AGE] = number_of_fish
                dead_fish = number_of_fish
            else:
                # Age the fish
                new_ages[age - 1] = number_of_fish
        
        new_ages[REBORN_AGE] += dead_fish
        self.fish_ages = new_ages

    def sum(self):
        return sum(self.fish_ages.values())


def process_instructions(test_data, days):

    fish_tracker = FishTracker.from_string(test_data)
    for _ in range(0, days):
        fish_tracker.age_fish()

    return fish_tracker.sum()


def test_day_short_input():
    test_instructions = """
3,4,3,1,2
"""
    result = process_instructions(test_instructions, 80)
    assert result == 5934


def test_day_real_input():
    test_instructions = open("day6_input").read()
    result = process_instructions(test_instructions, 256)
    assert result == 1702631502303

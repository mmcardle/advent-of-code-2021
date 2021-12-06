
from dataclasses import dataclass


@dataclass
class Fish:
    days: int

    def age(self):
        self.days -= 1
        if self.days == -1:
            self.days = 6
            return Fish(days=8)
        else:
            return None
        
    def __str__(self) -> str:
        return str(self.days)


def process_instructions(test_data, days):

    fishes = [Fish(int(x)) for x in test_data.split(",")]

    for i in range(0, days):
        new_fishes = []
        for fish in fishes:
            new_fish = fish.age()
            new_fishes.append(fish)
            if new_fish:
                new_fishes.append(new_fish)
        
        fishes = new_fishes

    return len(fishes)


def test_day_short_input():
    test_instructions = """
3,4,3,1,2
"""
    result = process_instructions(test_instructions, 80)
    assert result == 4268


def test_day_real_input():
    test_instructions = open("day6_input").read()
    result = process_instructions(test_instructions, 256)
    assert result == 379114
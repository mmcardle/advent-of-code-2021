
from dataclasses import dataclass
from typing import Counter


ONE, ZERO = '1', '0'

@dataclass
class Power:
    gamma: int
    epsilon: int
    oxygen : int
    scrubber: int

    def power(self):
        return self.gamma * self.epsilon

    def life_support(self):
        return self.oxygen * self.scrubber


def calculate_gamma_and_epsilon(test_data):
    zipped = list(zip(*test_data))
    gamma = ""
    epsilon = ""
    for z in zipped:
        counter = Counter(z)
        most_common = ONE if counter[ONE] > counter[ZERO] else ZERO

        gamma += ONE if most_common == ONE else ZERO
        epsilon += ZERO if most_common == ONE else ONE

    return int(gamma, 2), int(epsilon, 2)

def calculate_oxygen(data):
    iteration = 0
    while len(data) > 1:
        counter_1_0 = Counter([x[iteration] for x in data])
        most_common = ONE if counter_1_0[ONE] >= counter_1_0[ZERO] else ZERO
        data = [val for val in data if val[iteration] == most_common]
        iteration += 1
        if len(data) == 1:
            return int(data[0], 2)

    raise Exception("Could not find oxygen")


def calculate_scrubber(data):
    iteration = 0
    while len(data) > 1:
        counter_1_0 = Counter([x[iteration] for x in data])
        most_common = ONE if counter_1_0[ONE] < counter_1_0[ZERO] else ZERO
        data = [val for val in data if val[iteration] == most_common]
        iteration += 1
        if len(data) == 1:
            return int(data[0], 2)

    raise Exception("Could not find scrubber")


def process_instructions(test_data):

    test_data = [td for td in test_data.split("\n") if td]

    gamma, epsilon = calculate_gamma_and_epsilon(test_data)

    oxygen = calculate_oxygen(test_data)

    scrubber = calculate_scrubber(test_data)

    return Power(gamma, epsilon, oxygen, scrubber)


def test_day3_short_input():
    test_instructions = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""
    power = process_instructions(test_instructions)
    assert power.power() == 198
    assert power.life_support() == 230


def test_day2_real_input():
    test_instructions = open("day3_input").read()
    power = process_instructions(test_instructions)
    assert power.power() == 2250414
    assert power.life_support() == 6085575
from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class DirectionType(Enum):
    FORWARD = auto()
    UP = auto()
    DOWN = auto()


@dataclass
class Instruction:
    direction: DirectionType
    distance: int

    @classmethod
    def from_raw(cls, instruction: str):
        raw_instruction = instruction.split(" ")
        assert len(raw_instruction) == 2
        return cls(DirectionType[raw_instruction[0].upper()], int(raw_instruction[1]))


@dataclass
class SubmarineStatus:
    horozontal: int = 0
    depth: int = 0
    aim: int = 0

    def sum(self):
        return self.depth * self.horozontal


def parse_instructions(instructions: str):
    return [
        Instruction.from_raw(raw_instruction)
        for raw_instruction in instructions.split("\n")
        if raw_instruction
    ]


def follow_instructions(instructions: List[Instruction]) -> SubmarineStatus:
    horozontal = 0
    depth = 0
    aim = 0

    for instruction in instructions:
        match instruction.direction:
            case DirectionType.FORWARD:
                horozontal += instruction.distance
                depth += instruction.distance * aim
            case DirectionType.UP:
                aim -= instruction.distance
            case DirectionType.DOWN:
                aim += instruction.distance

    return SubmarineStatus(horozontal, depth, aim)


def process_instructions(instructions: str):

    parsed_instructions = parse_instructions(instructions)

    final_position = follow_instructions(parsed_instructions)

    return final_position


def test_day2_short_input():
    test_instructions = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""
    position = process_instructions(test_instructions)
    assert position.sum() == 900


def test_day2_real_input():
    test_instructions = open("day2_test_input").read()
    position = process_instructions(test_instructions)
    assert position.sum() == 1741971043

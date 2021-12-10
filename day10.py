
from collections import deque

start_characters = ["{", "(", "[", "<"]
end_characters = ["}", ")", "]", ">"]


def match(start, end):
    if start == "{" and end == "}": return True
    if start == "[" and end == "]": return True
    if start == "(" and end == ")": return True
    if start == "<" and end == ">": return True
    return False

def inverse(c):
    if c == "{": return "}"
    if c == "[": return "]"
    if c == "(": return ")"
    if c == "<": return ">"
    if c == "}": return "{"
    if c == "]": return "["
    if c == ")": return "("
    if c == ">": return "<"
    raise Exception(f"Unknown char {c}")


def validate_line(line):
    
    chars = [ch for ch in line]
    current_char = chars.pop(0)
    working_queue = deque([current_char])

    try:
        while current_char := chars.pop(0):
            if current_char in start_characters:
                working_queue.append(current_char)
            if current_char in end_characters:
                last = working_queue[-1]
                if match(last, current_char):
                    working_queue.pop()
                else:
                    return current_char
            if len(working_queue) == 0:
                working_queue.append(chars.pop(0))
    except IndexError:
        # No more chracters to process
        pass

    score = 0
    for current_char in reversed(working_queue):
        ci = inverse(current_char)
        score *= 5
        if ci == ")": score += 1
        if ci == "]": score += 2
        if ci == "}": score += 3
        if ci == ">": score += 4

    return score


def process_instructions(test_data):

    test_data = [td for td in test_data.split("\n") if td]

    invalid_chars = []
    part2_scores = []
    for line in test_data:
        first_invalid = validate_line(line)
        if type(first_invalid) == int:
            part2_scores.append(first_invalid)
        invalid_chars.append(first_invalid)

    part1_score = 0
    for inv in invalid_chars:
        if inv == ")": part1_score += 3
        if inv == "]": part1_score += 57
        if inv == "}": part1_score += 1197
        if inv == ">": part1_score += 25137

    part2_scores = sorted(part2_scores)
    
    return part1_score, middle_item(part2_scores)


def middle_item(l):
    return l[len(l)//2]


def test_day_short_input():
    test_instructions = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
    score1, score2 = process_instructions(test_instructions)
    assert score1 == 26397
    assert score2 == 288957


def test_day_real_input():
    test_instructions = open("day10_input").read()
    score1, score2 = process_instructions(test_instructions)
    assert score1 == 265527
    assert score2 == 3969823589
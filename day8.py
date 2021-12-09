
from dataclasses import dataclass
from typing import Counter


@dataclass
class Data:
    gamma: int


def process_signals(signal_list):
    
    lengths = {
        len(signal): signal for signal in signal_list
    }

    print(lengths)

    ONE = lengths[2]
    SEVEN = lengths[3]
    FOUR = lengths[4]
    EIGHT = lengths[7]

    return(ONE, SEVEN, FOUR, EIGHT)

def resort(x):
    return "".join(sorted(x))

def process_instructions_part1(test_data):

    count = 0
    for test_line in test_data.split("\n"):
        print(test_line)
        signal, output = test_line.split(" | ")
        signal_list = signal.split()
        output_list = output.split()
        lengths = [len(x) for x in output_list]
        print(lengths)
        count += lengths.count(2) + lengths.count(4) + lengths.count(3) + lengths.count(7)

    return count


def process_signal(signal):

    mapping = {}

    for d in signal:
        if len(d) == 2: mapping[d] = 1
        if len(d) == 4: mapping[d] = 4
        if len(d) == 7: mapping[d] = 8
        if len(d) == 3: mapping[d] = 7

    length5 = [x for x in signal if len(x) == 5]
    print("length5", length5)

    count5 = Counter("".join(length5))
    print(count5)

    left_vertical_1, left_vertical_2 = [x for x in count5 if count5[x] == 1]
    print("LEFT HAND Vertical lines are", left_vertical_1, left_vertical_2)

    for x in length5:
        if left_vertical_1 not in x and not left_vertical_2 in x:
            mapping[x] = 3
            print("3 is", x)
            THREE = x


    length6 = [x for x in signal if len(x) == 6]
    print("length6", length6)

    count6 = Counter("".join(length6))
    print("count6", count6)

    # cannot be middle
    not_middle = [x for x in count5 if count5[x] in [1, 2]]
    print("not_middle", not_middle)

    middle = [x for x in count6 if count6[x] == 2 and x not in not_middle][0]
    print("middle", middle)
    ZERO = None
    for x in length6:
        if middle not in x:
            mapping[x] = 0
            ZERO = x
            print("0 is", x)
    print("ZERO", ZERO)
    print()
    for x in [l for l in length6 if l != ZERO]:
        if left_vertical_1 in x and left_vertical_2 in x:
            mapping[x] = 6
            print("6 is", x)
        else:
            mapping[x] = 9
            print("9 is", x)
            NINE = x

    if left_vertical_1 in NINE:
        left_vertical_lower = left_vertical_1
    else:
        left_vertical_lower = left_vertical_2
    
    print(THREE)
    for x in [f for f in length5 if f != THREE]:
        print("XXX", x)
        if left_vertical_lower not in x:
            mapping[x] = 2
            print("2 is", x)
        else:
            mapping[x] = 5
            print("5 is", x)
            FIVE = x
    print(mapping)

    return mapping



def process_instructions_part2(test_data):

    asum = 0
    for test_line in test_data.split("\n"):
        print("TEST LINE", test_line)
        signal, output = test_line.split(" | ")
        signal_list = signal.split()
        output_list = output.split()

        print("SIGNAL_LIST", signal_list)
        mapping = process_signal(signal_list)
        
        print("mapping", mapping)

        sorted_mapping = {resort(x): mapping[x] for x in mapping}

        print("sorted_mapping", sorted_mapping)

        digits = ""
        for v in output_list:
            print("V", v, sorted_mapping[resort(v)])

            digits += str(sorted_mapping[resort(v)])
        
        print(digits)

        asum = asum + int(digits)

    return asum


def test_day_short_input1():
    test_instructions = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""
    assert process_instructions_part1(test_instructions) == 0
    assert process_instructions_part2(test_instructions) == 5353

def test_day_short_input2():
    test_instructions = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
    assert process_instructions_part1(test_instructions) == 26
    assert process_instructions_part2(test_instructions) == 61229


def test_day_real_input():
    test_instructions = open("day8_input").read()
    assert process_instructions_part1(test_instructions) == 383
    assert process_instructions_part2(test_instructions) == 998900


"""
    
    print(signal_list)
    print("output_list", output_list)
    
    output_list_sorted = [resort(x) for x in output_list]
    print("output_list_sorted", output_list_sorted)

    ONE, SEVEN, FOUR, EIGHT = process_signals(signal_list)

    print("ONE", ONE)
    print("SEVEN", SEVEN)
    print("FOUR", FOUR)
    print("EIGHT", EIGHT)

    NUM_ONE =  output_list.count(resort(ONE))
    NUM_SEVEN = output_list.count(resort(SEVEN))
    NUM_FOUR =  output_list.count(resort(FOUR))
    NUM_EIGHT =  output_list.count(resort(EIGHT))

    #count += NUM_ONE + NUM_SEVEN + NUM_FOUR + NUM_EIGHT

    print("NUM_ONES", NUM_ONE)
    print("NUM_SEVEN", NUM_SEVEN)
    print("NUM_FOUR", NUM_FOUR)
    print("NUM_EIGHT", NUM_EIGHT)
"""
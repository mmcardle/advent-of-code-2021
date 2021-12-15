
from dataclasses import dataclass
from collections import deque
from typing import Counter, Dict


from multiprocessing import Pool


class PolymerCacheKey():

    def __init__(self, polymer: str, steps: int):
        self.polymer = polymer
        self.steps = steps

    def __eq__(self, other):
        return self.polymer == other.polymer and self.steps == other.steps

    def __hash__(self):
        return hash(self.polymer) + hash(self.steps)


def getCharCountsIter(polymerPair: str, pairInsertionRules: Dict, steps: int, polymerCache: Dict):
    
    charCount = {}
    if steps == 0:
        #print("XXX0")
        charCount[polymerPair[1]] = charCount.get(polymerPair[1], 0) + 1
    elif PolymerCacheKey(polymerPair, steps) in polymerCache:
        #print("XXX1")
        charCount = polymerCache.get(PolymerCacheKey(polymerPair, steps))
    elif polymerPair not in pairInsertionRules:
        #print("XXX2")
        charCount[polymerPair[1]] = charCount.get(polymerPair[1], 0) + 1
    else:
        #print("XXX3")
        nextPolymer = polymerPair[0] + pairInsertionRules[polymerPair] + polymerPair[1]
        for i in range(0, len(nextPolymer) - 1):
            nextCharCount = getCharCountsIter(nextPolymer[i:i + 2], pairInsertionRules, steps - 1, polymerCache)
            for character in nextCharCount.keys():
                charCount[character] = charCount.get(character, 0) + nextCharCount.get(character)

    polymerCache[PolymerCacheKey(polymerPair, steps)] = charCount

    return charCount


def getCharCounts(polymer: str, pairInsertionRules: Dict, steps: int):
    polymerCache = {}
    charCount = {}
    
    charCount[polymer[0]] = 1

    print("X0", polymer, "steps", steps)
    
    for i in range(0, len(polymer) - 1):
        nextCharCount = getCharCountsIter(polymer[i:i + 2], pairInsertionRules, steps, polymerCache)
        print("X2", i, nextCharCount)
        for character in nextCharCount.keys():
            charCount[character] = charCount.get(character, 0) + nextCharCount.get(character)

    return charCount


def process_instructions(test_data, interations=1):

    test_data = [td for td in test_data.split("\n") if td]
    polymer = test_data[0]
    insertions = {}
    for i in test_data[1:]:
        pair, c = i.split(" -> ")
        insertions[pair] = c

    charCounts = getCharCounts(polymer, insertions, interations)

    _min = min(charCounts.values())
    _max = max(charCounts.values())

    print(charCounts)

    print("min", _min)
    print("max", _max)

    print("result", _max - _min)

    return _max - _min



test_instructions = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

def test_day_short_input2():

    result = process_instructions(test_instructions, 40)


def test_day_real_input():
    test_instructions = open("day14_input").read()
    result = process_instructions(test_instructions, 40)


if __name__ == "__main__":
    test_day_real_input()
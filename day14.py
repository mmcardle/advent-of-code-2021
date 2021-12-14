
from dataclasses import dataclass
from collections import deque
from math import perm
from typing import Counter, List
import concurrent.futures
import sys
from itertools import permutations

from multiprocessing import Pool

@dataclass
class Node:
    c: str
    next: 'Node' = None
    count: int = 1

    def __str__(self):
        return f'{self.c}({self.count})'

    def __repr__(self) -> str:
        return f'{self}'

    def recursive(self):
        x = self.c
        next1 = self.next
        while next1 is not None:
            x += next1.c
            next1 = next1.next
        return x

    def check_yerself(self, insertions):
        if self.next is None:
            return []
        
        for insertion in insertions:
            if insertion[0][0] == self.c and insertion[0][1] == self.next.c:
                #print(f'Comparing {self.c}{self.next.c} -> FOUND {insertion}')
                return (self, insertion[1])

        return []

    def insert_yerself(self, c):
        new_node = Node(c, next=self.next)
        self.next = new_node
        return new_node

    def next_node(self):
        return self.next


def process2(polymer, insertions, iterations):
    print("Polymer", polymer)
   
    import pdb; pdb.set_trace()

    

    print([x for x in reversed(polymer)])
    next = None
    for x in reversed(polymer):
        n = Node(x[0], next)
        next = n
    
    first = next
    node = next
    print("First", first, first.next, first.next.next, first.next.next.next, first.next.next.next.next)

    for i in range(1, iterations + 1):
        new_insertions = deque()
        while next_one := node.next_node():
            new_ones = node.check_yerself(insertions)
            new_insertions.append(new_ones)
            node = next_one

        for new_ones in new_insertions:
            node2, c = new_ones
            node2.insert_yerself(c)

        inter_result = first.recursive()
        print(f"After {i}:", Counter(inter_result))

        node = first
    
    result = first.recursive()
    #print("Result", result)
    counter = Counter(result)
    ordered_counter = sorted(counter.values(), key=lambda x: x, reverse=True)
    diff = ordered_counter[0] - ordered_counter[-1]
    print(diff)
    return diff


def func(pair, polymer_zip):
    new_insertions = deque()
    duo, ch = pair
    #print(f"{duo} -> {ch}")
    duo_tuple = tuple(duo)

    for i, x in enumerate(polymer_zip):
        if x == duo_tuple:
            #print(f"Found {i} {duo_tuple}")
            new_insertions.append(
                (i,
                    (polymer_zip[i][0], ch),
                    (ch, polymer_zip[i][1])
                )
            )
    return new_insertions

def process(pool, polymer_zip, insertions):
    results = []
    future_to_url = {pool.submit(func, pair, polymer_zip): pair for pair in insertions}
    for future in concurrent.futures.as_completed(future_to_url):
        results.append(future.result())
    for new_insertions in results:
        for insertion in new_insertions:
            #print(insertion)
            polymer_zip[insertion[0]] = insertion[1]
            polymer_zip.insert(insertion[0] + 1, insertion[2])
    return polymer_zip


def process_instructions(test_data, iterations=1):

    test_data = [td for td in test_data.split("\n") if td]
    polymer = test_data[0]
    insertions = [c.split(" -> ") for c in test_data[1:] if c]

    return process2(polymer, insertions, iterations)



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
    assert process_instructions(test_instructions, 10) == 1588
    #process_instructions(test_instructions, 40)


def test_day_real_input(filename):
    test_instructions = open(filename).read()
    process_instructions(test_instructions, 10)
    process_instructions(test_instructions, 40)


if __name__ == "__main__":
    test_day_short_input2()
    #test_day_real_input(sys.argv[1])
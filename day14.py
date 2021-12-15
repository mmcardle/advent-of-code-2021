
from dataclasses import dataclass
from collections import deque
from math import perm
from typing import Counter, List
import concurrent.futures
import sys
from itertools import permutations, combinations

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

    def next_node(self):
        return self.next


def process2(polymer, insertions, iterations):

    cache_iterations = 10

    letters = set("".join([x[0] for x in insertions]))
    print(letters)
    letter_perms = list(permutations(letters, 2))
    
    for letter in letters:
        letter_perms.append((letter, letter))
    
    cache = {}
    results_cache = {}
    for letter_perm in letter_perms:
        diff, result = process3("".join(letter_perm), insertions, cache_iterations)
        print("Letter Permutation", letter_perm, "".join(letter_perm), Counter(result))
        cache[letter_perm] = Counter(result)
        results_cache[letter_perm] = result

    #print("Pre Canned Results")
    #for letter, result in cache.items():
    #    print(letter, Counter(result))

    print("X", len(polymer))
    next_level = iteration(1 * cache_iterations, polymer, cache, results_cache)
    
    print("X", len(next_level))
    next_level = iteration(2 * cache_iterations, next_level, cache, results_cache)
    
    print("X", len(next_level))
    next_level = iteration(3 * cache_iterations, next_level, cache, results_cache)
    
    print("X", len(next_level))
    next_level = iteration(4 * cache_iterations, next_level, cache, results_cache, return_result=False)


def iteration(level, polymer, cache, results_cache, return_result=True):
    print(f"\nNow doing level {level}", len(polymer))

    the_count = Counter()
    next_level = ""
    zipped_polymer = zip(polymer, polymer[1:])
    l_zip = len(polymer)
    for i, t in enumerate(zipped_polymer):
        the_count += cache[t]
        
        if i < l_zip - 1:
            the_count[t[1]] -= 1
            if return_result:
                next_level += results_cache[t][:-1]
        else:
            if return_result:
                next_level += results_cache[t]

    print(f"Iteration Count {level}", the_count)
    return next_level


def process3(polymer, insertions, iterations, cache=None):
    #print("Polymer", polymer)

    if cache is None:
        cache = {}
   
    next = None
    for x in reversed(polymer):
        n = Node(x[0], next)
        next = n
    
    first = next
    node = next

    for i in range(1, iterations + 1):
        new_insertions = deque()
        while next_one := node.next:
            new_ones = node.check_yerself(insertions)
            new_insertions.append(new_ones)
            node = next_one

        for new_ones in new_insertions:
            node2, c = new_ones
            node2.insert_yerself(c)

        inter_result = first.recursive()
        #print(f"After {i}:", Counter(inter_result))

        node = first
    
    result = first.recursive()
    #print("Result", result)
    counter = Counter(result)
    #print(counter)
    ordered_counter = sorted(counter.values(), key=lambda x: x, reverse=True)
    diff = ordered_counter[0] - ordered_counter[-1]
    #print(diff)
    return diff, result


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

    process2(polymer, insertions, iterations)
    exit()
    n1 = 1
    n2 = 5
    n3 = 30
    d, r = process3(polymer, insertions, n1)
    print(f"LINKED - {n1:2} ", Counter(r))
    d, r = process3(polymer, insertions, n2)
    print(f"LINKED - {n2:2} ", Counter(r))
    d, r = process3(polymer, insertions, n3)
    print(f"LINKED - {n3:2} ", Counter(r))


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
    process_instructions(test_instructions, 4)
    #process_instructions(test_instructions, 21)


def test_day_real_input(filename):
    test_instructions = open(filename).read()
    process_instructions(test_instructions, 10)
    process_instructions(test_instructions, 40)


if __name__ == "__main__":
    test_day_short_input2()
    #test_day_real_input(sys.argv[1])
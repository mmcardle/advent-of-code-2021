
from dataclasses import dataclass
from collections import deque
from typing import Counter


from multiprocessing import Pool


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


def process(polymer_zip, insertions):

    pool = Pool(processes=8)
    results = [pool.apply(func, args=(pair, polymer_zip)) for pair in insertions]

    for new_insertions in results:
        for insertion in new_insertions:
            #print(insertion)
            polymer_zip[insertion[0]] = insertion[1]
            polymer_zip.insert(insertion[0] + 1, insertion[2])

            # Works with delete
            #del polymer_zip[insertion[0]]
            #polymer_zip.insert(insertion[0], insertion[1])
            #polymer_zip.insert(insertion[0] + 1, insertion[2])

    return polymer_zip

    #print(f"\n\nPolymer = {polymer_zip}")

    new_insertions = deque()
    
    with Pool() as pool:
        for pair in insertions:

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

                #polymer_zip[i] = (polymer_zip[i][0], ch, polymer_zip[i][1])

    #print("X1", polymer_zip)

    for insertion in new_insertions:
        #print(insertion)
        del polymer_zip[insertion[0]]
        #print("X1 -- ", polymer_zip)
        polymer_zip.insert(insertion[0], insertion[1])
        #print("X1 -- ", polymer_zip)
        polymer_zip.insert(insertion[0] + 1, insertion[2])
        #print("X1 -- ", polymer_zip)

    #for i, p in enumerate(polymer_zip):
    #    if len(p) == 3:
    #        polymer_zip[i] = (p[0], p[1])
    #        polymer_zip.insert(i + 1, (p[1], p[2]))

    #print("X2", polymer_zip)
    
    return polymer_zip


    new_polymer = [
        x[:-1] if i < len(polymer_zip) -1 else x
        for i, x in enumerate(polymer_zip)
    ]
    print("New Polymer = ", new_polymer)
    
    result = ""
    for x in new_polymer:
        result += "".join(x)
    
    print(f"Result = {result}")
    new_polymer_zip = deque(list(zip(result, result[1:])))

    print(f"New polymer zip = {new_polymer_zip}")
    return new_polymer_zip

    result = ""
    #print(result)
    #return result



def process_instructions(test_data, interations=1):

    test_data = [td for td in test_data.split("\n") if td]
    polymer = test_data[0]
    insertions = [c.split(" -> ") for c in test_data[1:] if c]

    polymer_zip = deque(list(zip(polymer, polymer[1:])))

    for i in range(0, interations):
        print(i, len(polymer_zip))
        polymer_zip = process(polymer_zip, insertions)

    new_polymer = [
        x[:-1] if i < len(polymer_zip) -1 else x
        for i, x in enumerate(polymer_zip)
    ]
    #print("Result Polymer = ", new_polymer)
    
    result = ""
    for x in new_polymer:
        result += "".join(x)

    #print("result = ", result)
    
    return result



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

def test_day_xxx_input():
    result = process_instructions(test_instructions, 2)
    assert len(result) == 13
    c = Counter(result)


def test_day_short_input2():

    result = process_instructions(test_instructions, 10)
    #assert len(result) == 3073
    #c = Counter(result)
    #print(c)
    #vals = list(c.values())
    #print(vals)
    #assert vals[0] - vals[-1] == 704

    result = process_instructions(test_instructions, 20)
    #assert len(result) == 196609, len(result)
    #c = Counter(result)
    #vals = list(c.values())
    #assert vals[0] - vals[-1] == 704


if __name__ == "__main__":
    test_day_short_input2()


def test_day_real_input():
    test_instructions = open("day14_input").read()
    result = process_instructions(test_instructions, 10)
    assert len(result) == 19457
    c = Counter(result)
    print(c)
    vals = list(c.values())
    print(vals)
    assert vals[0] - vals[-1] == 2509

    test_instructions = open("day14_input").read()
    result = process_instructions(test_instructions, 10)
    assert len(result) == 19457
    c = Counter(result)
    print(c)
    vals = list(c.values())
    print(vals)
    assert vals[0] - vals[-1] == 2509
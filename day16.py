
from dataclasses import dataclass


@dataclass
class Data:
    gamma: int



def bin_to_int(s): return int(s, 2)

def to_binary(data):
    return "".join([
        bin(int(d, 16))[2:].zfill(4) for d in data
    ])


def parse_literal(binary):
    version = binary[:3]
    tid = binary[3:6]
    
    chunk = binary[6:11]
    chunks = [chunk[1:]]
    start = 6
    end = 11

    have_read = 0
    
    while chunk[0] != "0":
        start += 5
        end += 5 
        chunk = binary[start:end]
        chunks.append(chunk[1:])
        have_read += 5

    value = bin_to_int("".join(chunks))

    rest = binary[11+have_read:]
    
    return version, tid, None, value, rest


def parse_operator_by_length(binary):
    version = binary[:3]
    tid = binary[3:6]
    length_id = binary[6:7]
    total = bin_to_int(binary[7:7+15])

    return version, tid, length_id, total, binary[7+15:]


def parse_subpacket_by_number(binary):
    version = binary[:3]
    tid = binary[3:6]
    length_id = binary[6:7]
    number_of_subpackets_to_read = bin_to_int(binary[7:7+11])

    if number_of_subpackets_to_read == 0:
        raise Exception()

    binary = binary[7+11:]

    return version, tid, length_id, number_of_subpackets_to_read, binary


def match(binary, spacer):

    version = binary[:3]
    tid = binary[3:6]

    if tid == "100":
        version, tid, lid, value, rest = parse_literal(binary)
        print(f"{spacer} version={bin_to_int(version)} type={bin_to_int(tid)} literal={value}")
        return version, tid, lid, value, rest 

    type_id = binary[6:7]

    if type_id == "0":
        result = parse_operator_by_length(binary)
        print(f"{spacer} version={bin_to_int(version)} type={bin_to_int(tid)} length={len(result[4])}")
        return result

    if type_id == "1":
        result = parse_subpacket_by_number(binary)
        print(f"{spacer} version={bin_to_int(version)} type={bin_to_int(tid)} num={result[3]}")
        return result

    print("OPPS", binary)
    raise Exception("unknown")

    return binary[6:]


def process(binary, depth=0):
    if set(binary) == {"0"}:
        raise Exception(binary)
    if depth:
        spacer = "--" * depth
    else:
        spacer = ""
    
    if len(binary) > 50:
        print(spacer, "Raw", len(binary), binary[0:50], "...")
    else:
        print(spacer, "Raw", len(binary), binary)

    while binary:
        result = match(binary, spacer)
        version, tid, length_id, subpackets, binary = result
        if length_id == "1":
            counter = 0
            while counter < subpackets:
                binary = process(binary, depth+1)
                counter += 1
        elif length_id == "0":
            subpacket_binary = binary[0:subpackets]
            binary = process(subpacket_binary, depth+1)
            #binary = binary[subpackets:]
        elif length_id == None:
            pass#print(spacer, "Literal???", subpackets)
        else:
            raise Exception(length_id)

        if set(binary) == {"0"}:
            break

        binary = binary
    
    return binary


def process_instructions(test_data):

    print("\n\n ### Test Data", test_data[0:50])

    test_data = [td for td in test_data.split("\n") if td]

    packets = []
    for td in test_data:
        binary = to_binary(td)
        packet = process(binary)
        packets.append(packet)

    return packets


def test_day_short_input():
    test_instructions = """
XXXX
"""
    result = process_instructions(test_instructions)
    assert result == 99999


def test_day_real_input():

    version, tid, lid, value, binary = parse_literal(to_binary("D2FE28"))
    assert version == "110"
    assert tid == "100"
    assert lid == None
    assert value == 2021
    #assert binary == "", binary

    version, tid, length_id, subpackets, binary = parse_operator_by_length(to_binary("38006F45291200"))
    assert version == "001"
    assert tid == "110"
    assert length_id == "0"
    assert subpackets == 27, subpackets
    assert binary == "1101000101001010010001001000000000"

    version, tid, length_id, subpackets, binary = parse_subpacket_by_number(to_binary("EE00D40C823060"))
    assert version == "111"
    assert tid == "011"
    assert length_id == "1"
    #assert subpackets == ['01010000001', '10010000010', '00110000011']
    #assert subpackets == '010100000011001000001000110000011'
    assert subpackets == 3
    assert binary == "01010000001100100000100011000001100000", binary

    print("#### TEST COMPLETE ####")
    packets = process_instructions("8A004A801A8002F478")

    print("#### REAL RUN ####")

    test_instructions = open("day16_input").read()
    result = process_instructions(test_instructions)
    assert result == 99999

if __name__ == "__main__":
    #test_day_short_input()
    test_day_real_input()
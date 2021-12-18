
from dataclasses import dataclass, field
from functools import cached_property
from enum import Enum
from typing import List, Tuple, Dict, Callable

import sys

sys.setrecursionlimit(1500)

class Operator(Enum):
    Operator = 6
    OperatorWithSubPackets = 3


class OperatorType(Enum):
    TotalLength = 15
    NumberOfSubPackets = 11


class PacketType(Enum):
    Sum = 0
    Product = 1
    Minimum = 2
    Maximum = 3
    Literal = 4
    GreaterThan = 5
    LessThan = 6
    EqualTo = 7

OperatorMap = {
    PacketType.Sum: "+",
    PacketType.Product: "*",
    PacketType.Minimum: "min",
    PacketType.Maximum: "max",
    PacketType.GreaterThan: ">",
    PacketType.LessThan: "<",
    PacketType.EqualTo: "==",
}

def bin_to_int(s):
    return int(s, 2)


def bin_to_hex(s):
    return hex(bin_to_int(s))[2:]


def binary(data):
    return "".join([
        bin(int(d, 16))[2:].zfill(4) for d in data
    ])


@dataclass
class Packet:
    binary: str
    value: int = None
    children: List['Packet'] = field(default_factory=list)
    executed: bool = False
    parsed: bool = False
    depth: int = 0

    LENGTHS = {
        0: OperatorType.TotalLength,
        1: OperatorType.NumberOfSubPackets,
    }

    #def __post_init__(self):
    #    self.packet_next()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self.__str__()}>"

    def __str__(self) -> str:
        if self.value:
            return f"Value={self.value}"
        else:
            if self.length == OperatorType.TotalLength:
                return f"{self.literal_type.name} length={len(self.children)} {self.length.name}"
            else:
                return f"{self.literal_type.name} children={len(self.children)} {self.length.name}"

    @cached_property
    def version(self):
        return int(self.binary[0:3], 2)

    @cached_property
    def type(self):
        package_int = int(self.binary[3:6], 2)
        if package_int == PacketType.Literal.value:
            return PacketType.Literal
        return Operator.Operator

    @cached_property
    def literal_type(self):
        package_int = int(self.binary[3:6], 2)
        return PacketType(package_int)

    @cached_property
    def operator_type(self):
        return PacketType(self.length)

    @cached_property
    def length(self):
        length_val = int(self.binary[6:7])
        return self.LENGTHS[length_val]

    def execute(self, depth=0):
        d = "  " * depth
        print(d, "", self)
        
        if self in self.children:
            raise Exception("Circular reference")
        
        if self.executed:
            raise Exception(f"Already executed {self}")
        
        self.executed = True
        new_depth = depth + 1

        if self.literal_type == PacketType.Product:
            product = 1
            print("LENGHT", len(self.children))
            for child in self.children:
                product *= child.execute(new_depth)
            return product
        if self.literal_type == PacketType.Sum:
            return sum([c.execute(new_depth) for c in self.children])
        if self.literal_type == PacketType.Minimum or self.literal_type == PacketType.Maximum:
            if self.literal_type == PacketType.Minimum:
                return min([c.execute(new_depth) for c in self.children])
            else:
                return max([c.execute(new_depth) for c in self.children])
        if self.literal_type == PacketType.GreaterThan:
            return 1 if self.children[0].execute(new_depth) > self.children[1].execute(new_depth) else 0
        if self.literal_type == PacketType.LessThan:
            return 1 if self.children[0].execute(new_depth) < self.children[1].execute(new_depth) else 0
        if self.literal_type == PacketType.EqualTo:
            if len(self.children) == 2:
                lhs = self.children[0].execute(new_depth)
                rhs = self.children[1].execute(new_depth)
                return 1 if lhs == rhs else 0
            else:
                operators = [c for c in self.children if c.type == Operator.Operator]
                return 1 if len(set([op.execute(new_depth) for op in operators])) <= 1 else 0
                
        if self.literal_type == PacketType.Literal:
            return self.value
        raise NotImplementedError

    def as_output(self):
        if self.type == Operator.Operator:
            return self.literal_type
        elif self.type == PacketType.Literal:
            return self.value
        return "?????"
    
    def process_literal(self):
        #print(" -- Literal bin ", self.binary)
        literal_data = self.binary[6:]
        #print(" -- Literal Data      ", literal_data)
        literal_split = [literal_data[i:i + 5] for i in range(0, len(literal_data), 5)]
        #print(" -- Literal Split", literal_split)
        
        literal = None
        literal_string = ""
        try:
            while literal_part := literal_split.pop(0):
                #print(" -- Literal Part", literal_part)
                literal_string += literal_part[1:]
                if literal_part.startswith("0"):
                    literal = bin_to_int(literal_string)
                    break
        except IndexError:
            pass
        #print(" -- Literal", literal)
        d = "  " * self.depth
        print(d, " -- Process Literal", self.literal_type, "Value", literal)
        self.value = literal
        rest = "".join(literal_split)
        if not rest or set(rest) == {"0"}:
            return None
        print(d, " -- Rest After literal parse == ", len(rest))
        #p = Packet(rest)
        #self.children.append(p)
        return len(literal_data) - len(rest), rest
    
    def process_operator(self):
        
        if self.length == OperatorType.TotalLength:
            total_length_binary = self.binary[7:7 + self.length.value]
            total_length = int(total_length_binary, 2)
            d = "  " * self.depth
            print(d, " -- Process Operator", self.literal_type, "Total Length of subpackets", total_length)

            #sub_packets = self.binary[7 + self.length.value:]
            sub_packet_binary = self.binary[7 + self.length.value:7 + self.length.value + total_length]
            
            sub_packet = Packet(sub_packet_binary, depth=self.depth + 1)
            self.children.append(sub_packet)
            xxxx = sub_packet.parse()
            if type(xxxx) == str:
                rest = xxxx
            else:
                _, rest = xxxx
            print("XXXX", xxxx)
            x = 0
            while rest:
                print(d, "REST", rest)
                sub_packet = Packet(rest, depth=self.depth + 1)
                self.children.append(sub_packet)
                print(d, "xxxx", rest)
                xxxx = sub_packet.parse()
                if type(xxxx) == str:
                    rest = xxxx
                elif type(xxxx) == tuple:
                    _, rest = xxxx
                else:
                    break
                x += 1

            #print(" -- Subpacket", sub_packet)
            #while sub_packet:
            #    print("appending", sub_packet)
            #    self.children.append(sub_packet)
            #    if sub_packet.children:
            #        sub_packet = sub_packet.children[0]
            #    else:
            #        break
            child_length = sum([len(c.binary) for c in self.children])
            print("XXXX", self, total_length, "CHILDREN=", child_length)
            #assert child_length == total_length, (child_length, total_length)
            #return rest
        elif self.length == OperatorType.NumberOfSubPackets:
            total_subpackets_binary = self.binary[7:7 + self.length.value]
            total_subpackets = int(total_subpackets_binary, 2)
            d = "  " * self.depth
            print(d, " -- Process Operator", self.literal_type, "Total Number of subpackets", total_subpackets, 'self.length.value', self.length.value)
            to_read = self.binary[7 + self.length.value:]
            num_children = 0
            while len(self.children) < total_subpackets:
                print("LOOPER LOOPER", len(to_read))
                sub_packet = Packet(to_read, depth=self.depth + 1)
                xxx = sub_packet.parse()
                if xxx:
                    _, overflow = xxx
                to_read = overflow
                self.children.append(sub_packet)
                num_children += 1
                if self.depth > 5:
                    raise Exception("Too deep")
            
            #self.children.append(sub_packet.children[0])
            #subpacket_count = 0
            #while sub_packet and subpacket_count < total_subpackets:
            #    self.children.append(sub_packet)
            #    if sub_packet.children:
            #        sub_packet = sub_packet.children[0]
            #        subpacket_count += 1
            #    else:
            #        break
            print("YYYY", self,  total_subpackets, "CHILDREN=", len(self.children))
            assert len(self.children) == total_subpackets

                       
            print("After READING ", len(overflow), "left", overflow[0:200], "...")
            
            return overflow

    def parse(self):
        print("\n ### PARSE ### ", self, "LENGTH=", len(self.binary))
        #import pdb; pdb.set_trace()
        #if self.depth > 2:
        #    raise Exception(f"DEPTH {self}")
        
        self.parsed = True
        if self.type == Operator.Operator:
            result = self.process_operator()
        elif self.type == PacketType.Literal:
            result = self.process_literal()
        else:
            raise Exception("Unknown packet type")

        return result

def process(raw_data):

    print(f"\n############ {raw_data}")

    packet = Packet(binary(raw_data))
    version_number = packet.version
    packet.parse()

    #for c in packet.children:
    #    print(" -- Child", c)
    #while packet:
    #    print("Processing:", packet)
    #    #print("Version:", packet.version)
    #    #print("Type:", packet.type)
    #    #print("Length:", packet.length)
    #    packet = packet.packet_next()
    #    version_number += packet.version if packet else 0
    #    if packet:
    #        packets.append(packet)

    #print([str(p) for p in packets])

    return version_number, packet


def process_instructions(test_data):

    test_data = [td for td in test_data.split("\n") if td]

    versions = []
    for td in test_data:
        version, packet = process(td)

        print("\n\n############ EXECUTION PHASE #############")
        print(" -- First Execution Packet -> ", packet)
        result = packet.execute()
        print("############ RESULT #############")
        print(result)
        versions.append(version)
    
    for c in packet.children:
        print(" -- Child", c)
        versions.append(c.version)
        for cc in c.children:
            versions.append(c.version)
            print(" -- --  Child", c)
            for ccc in cc.children:
                versions.append(c.version)
                print(" -- --  Child", c)

    print("VERSIONS", versions)
    print(sum(versions))

    return versions


def test_day_short_input():
    test_instructions = """
D2FE28
38006F45291200
EE00D40C823060
8A004A801A8002F478
620080001611562C8802118E34
C0015000016115A2E0802F182340
A0016C880162017C3686B18A3D4780
"""
    result = process_instructions(test_instructions)

def test_day_short_input_part2():
    test_instructions = """
C200B40A82
04005AC33890
880086C3E88112
CE00C43D881120
D8005AC2A8F0
F600BC2D8F
9C005AC2F8F0
9C0141080250320F1802104A08
"""

    assert process("C200B40A82")[1].execute() == 3
    assert process("04005AC33890")[1].execute() == 54
    assert process("880086C3E88112")[1].execute() == 7
    assert process("CE00C43D881120")[1].execute() == 9
    assert process("D8005AC2A8F0")[1].execute() == 1
    assert process("F600BC2D8F")[1].execute() == 0
    assert process("9C005AC2F8F0")[1].execute() == 0
    assert process("9C0141080250320F1802104A08")[1].execute() == 1

    result = process_instructions(test_instructions)


def test_day_real_input_viper():
    test_instructions = open("day16_input_viper").read()
    result = process_instructions(test_instructions)


def test_day_real_input():
    test_instructions = open("day16_input").read()
    result = process_instructions(test_instructions)



if __name__ == "__main__":
    #test_day_short_input()
    #test_day_short_input_part2()
    #test_day_real_input()
    test_day_real_input_viper()
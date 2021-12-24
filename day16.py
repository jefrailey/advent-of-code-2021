"""
--- Day 16: Packet Decoder ---

As you leave the cave and reach open waters, you receive a transmission from the Elves back on the ship.

The transmission was sent using the Buoyancy Interchange Transmission System (BITS), a method of packing numeric expressions into a binary sequence. Your submarine's computer has saved the transmission in hexadecimal (your puzzle input).

The first step of decoding the message is to convert the hexadecimal representation into binary. Each character of hexadecimal corresponds to four bits of binary data:

0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111

The BITS transmission contains a single packet at its outermost layer which itself contains many other packets. The hexadecimal representation of this packet might encode a few extra 0 bits at the end; these are not part of the transmission and should be ignored.

Every packet begins with a standard header: the first three bits encode the packet version, and the next three bits encode the packet type ID. These two values are numbers; all numbers encoded in any packet are represented as binary with the most significant bit first. For example, a version encoded as the binary sequence 100 represents the number 4.

Packets with type ID 4 represent a literal value. Literal value packets encode a single binary number. To do this, the binary number is padded with leading zeroes until its length is a multiple of four bits, and then it is broken into groups of four bits. Each group is prefixed by a 1 bit except the last group, which is prefixed by a 0 bit. These groups of five bits immediately follow the packet header. For example, the hexadecimal string D2FE28 becomes:

110100101111111000101000
VVVTTTAAAAABBBBBCCCCC

Below each bit is a label indicating its purpose:

    The three bits labeled V (110) are the packet version, 6.
    The three bits labeled T (100) are the packet type ID, 4, which means the packet is a literal value.
    The five bits labeled A (10111) start with a 1 (not the last group, keep reading) and contain the first four bits of the number, 0111.
    The five bits labeled B (11110) start with a 1 (not the last group, keep reading) and contain four more bits of the number, 1110.
    The five bits labeled C (00101) start with a 0 (last group, end of packet) and contain the last four bits of the number, 0101.
    The three unlabeled 0 bits at the end are extra due to the hexadecimal representation and should be ignored.

So, this packet represents a literal value with binary representation 011111100101, which is 2021 in decimal.

Every other type of packet (any packet with a type ID other than 4) represent an operator that performs some calculation on one or more sub-packets contained within. Right now, the specific operations aren't important; focus on parsing the hierarchy of sub-packets.

An operator packet contains one or more packets. To indicate which subsequent binary data represents its sub-packets, an operator packet can use one of two modes indicated by the bit immediately after the packet header; this is called the length type ID:

    If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
    If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.

Finally, after the length type ID bit and the 15-bit or 11-bit field, the sub-packets appear.

For example, here is an operator packet (hexadecimal string 38006F45291200) with length type ID 0 that contains two sub-packets:

00111000000000000110111101000101001010010001001000000000
VVVTTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB

    The three bits labeled V (001) are the packet version, 1.
    The three bits labeled T (110) are the packet type ID, 6, which means the packet is an operator.
    The bit labeled I (0) is the length type ID, which indicates that the length is a 15-bit number representing the number of bits in the sub-packets.
    The 15 bits labeled L (000000000011011) contain the length of the sub-packets in bits, 27.
    The 11 bits labeled A contain the first sub-packet, a literal value representing the number 10.
    The 16 bits labeled B contain the second sub-packet, a literal value representing the number 20.

After reading 11 and 16 bits of sub-packet data, the total length indicated in L (27) is reached, and so parsing of this packet stops.

As another example, here is an operator packet (hexadecimal string EE00D40C823060) with length type ID 1 that contains three sub-packets:

11101110000000001101010000001100100000100011000001100000
VVVTTTILLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBCCCCCCCCCCC

    The three bits labeled V (111) are the packet version, 7.
    The three bits labeled T (011) are the packet type ID, 3, which means the packet is an operator.
    The bit labeled I (1) is the length type ID, which indicates that the length is a 11-bit number representing the number of sub-packets.
    The 11 bits labeled L (00000000011) contain the number of sub-packets, 3.
    The 11 bits labeled A contain the first sub-packet, a literal value representing the number 1.
    The 11 bits labeled B contain the second sub-packet, a literal value representing the number 2.
    The 11 bits labeled C contain the third sub-packet, a literal value representing the number 3.

After reading 3 complete sub-packets, the number of sub-packets indicated in L (3) is reached, and so parsing of this packet stops.

For now, parse the hierarchy of the packets throughout the transmission and add up all of the version numbers.

Here are a few more examples of hexadecimal-encoded transmissions:

    8A004A801A8002F478 represents an operator packet (version 4) which contains an operator packet (version 1) which contains an operator packet (version 5) which contains a literal value (version 6); this packet has a version sum of 16.
    620080001611562C8802118E34 represents an operator packet (version 3) which contains two sub-packets; each sub-packet is an operator packet that contains two literal values. This packet has a version sum of 12.
    C0015000016115A2E0802F182340 has the same structure as the previous example, but the outermost packet uses a different length type ID. This packet has a version sum of 23.
    A0016C880162017C3686B18A3D4780 is an operator packet that contains an operator packet that contains an operator packet that contains five literal values; it has a version sum of 31.

Decode the structure of your hexadecimal-encoded BITS transmission; what do you get if you add up the version numbers in all packets?
"""
from dataclasses import dataclass, field
from typing import Generator, Optional
import math
import operator
from enum import IntEnum

import pytest

class Type(IntEnum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER = 5
    LESS = 6
    EQUAL = 7

@dataclass
class Packet:
    version: int
    type: Type
    value: Optional[int] = None
    children: list["Packet"] = field(default_factory=list)

def solve_part_one(packet: str) -> int:
    """Return the sum of the encoded version numbers."""
    bits = to_bits(packet)
    root, __ = parse_packet(bits)
    if root is None:
        raise Exception(f"Unable to parse packet, {packet=}.")
    queue = [root]
    version_sum = 0
    while queue:
        current = queue.pop(0)
        version_sum += current.version
        queue.extend(current.children)
    return version_sum


@pytest.mark.parametrize(
    "packet,expected",
    (
        ["8A004A801A8002F478", 16],
        ["620080001611562C8802118E34", 12],
        ["C0015000016115A2E0802F182340", 23],
        ["A0016C880162017C3686B18A3D4780", 31],
    ),
)
def test_solve_part_one(packet: str, expected: int) -> None:
    actual = solve_part_one(packet)
    assert actual == expected


def to_bits(hexadecimal: str) -> str:
    """Return the binary representation of the hexadecimal with a length that is a multiple of four.

    The binary representation is left padded with zeros to reach the desired length.
    """
    bits = bin(int(hexadecimal, base=16))[2:]
    current_length = len(bits)
    desired_length = current_length
    if desired_length % 4:
        desired_length += 4 - (desired_length % 4)
    bits = f"{bits:0>{desired_length}}"
    return bits


@pytest.mark.parametrize(
    "hexadecimal,expected",
    (
        ["D2FE28", "110100101111111000101000"],
        ["38006F45291200", "00111000000000000110111101000101001010010001001000000000"],
        ["EE00D40C823060", "11101110000000001101010000001100100000100011000001100000"],
    ),
)
def test_to_bits(hexadecimal: str, expected: str) -> None:
    actual = to_bits(hexadecimal)
    assert actual == expected


def parse_packet(packet: str) -> tuple[Optional[Packet], str]:
    """Return a Packet from the binary representation."""
    if not packet or packet.count("0") == len(packet):
        return None, ""
    version = int(packet[0:3], base=2)
    type_id = int(packet[3:6], base=2)
    if type_id == Type.LITERAL:
        current_idx = 6
        number_bits: list[str] = []
        while True:
            prefix, *rest = packet[current_idx : current_idx + 5]
            number_bits.extend(rest)
            current_idx += 5
            if prefix == "0":
                break
        value = int("".join(number_bits), base=2)
        remainder = packet[current_idx:]
        return (
            Packet(version=version, type=Type(type_id), value=value),
            remainder,
        )
    length_type_id = int(packet[6], base=2)
    # Else it's a operator
    if length_type_id == 0:
        # The 15 bits after the length type id represent the total length in bits of sub-packets
        sub_packet_bit_count = int(packet[7 : 7 + 15], base=2)
        sub_packets_bits = packet[7 + 15 : 7 + 15 + sub_packet_bit_count]
        children: list[Packet] = []
        while sub_packets_bits:
            child, sub_packets_bits = parse_packet(sub_packets_bits)
            if child:
                children.append(child)
        remainder = packet[7 + 15 + sub_packet_bit_count :]
        return (Packet(version=version, type=Type(type_id), children=children), remainder)
    elif length_type_id == 1:
        # The next 11 bits are a number that represents the number of sub-packets immediately
        # contained by this packet.
        sub_packet_count = int(packet[7 : 7 + 11], base=2)
        packet = packet[7 + 11 :]
        count = 0
        children = []
        while count < sub_packet_count:
            child, packet = parse_packet(packet)
            if child:
                children.append(child)
            count += 1
        remainder = packet
        return (Packet(version=version, type=Type(type_id), children=children), remainder)
    raise Exception(f"Could not parse {packet=}")


@pytest.mark.parametrize(
    "packet,expected",
    (
        ["D2FE28", Packet(version=6, type=Type(4), value=2021)],
        [
            "38006F45291200",
            Packet(
                version=1,
                type=Type(6),
                children=[
                    Packet(version=6, type=Type(4), value=10),
                    Packet(version=2, type=Type(4), value=20),
                ],
            ),
        ],
        [
            "EE00D40C823060",
            Packet(
                version=7,
                type=Type(3),
                children=[
                    Packet(version=2, type=Type(4), value=1),
                    Packet(version=4, type=Type(4), value=2),
                    Packet(version=1, type=Type(4), value=3),
                ],
            ),
        ],
    ),
)
def test_parse_packet(packet: str, expected: Packet) -> None:
    bits = to_bits(packet)
    actual, __ = parse_packet(bits)
    assert actual == expected


"""
--- Part Two ---

Now that you have the structure of your transmission decoded, you can calculate the value of the expression it represents.

Literal values (type ID 4) represent a single number as described above. The remaining type IDs are more interesting:

    Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
    Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
    Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
    Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
    Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.

Using these rules, you can now work out the value of the outermost packet in your BITS transmission.

For example:

    C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
    04005AC33890 finds the product of 6 and 9, resulting in the value 54.
    880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
    CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
    D8005AC2A8F0 produces 1, because 5 is less than 15.
    F600BC2D8F produces 0, because 5 is not greater than 15.
    9C005AC2F8F0 produces 0, because 5 is not equal to 15.
    9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.

What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS transmission?
"""


def solve_part_two(packet: str) -> int:
    """Return the value encoded in the packet."""
    bits = to_bits(packet)
    parsed, __ = parse_packet(bits)
    if not parsed:
        raise ValueError(f"Invalid packet, {packet=}, could not be parsed!")
    return interpret(parsed)


def interpret(packet: Packet) -> int:
    """Return the value encoded in the packet."""
    # Tree walk interpreter
    children: Generator[int, None,None] = (interpret(child) for child in packet.children)
    try:
        match packet.type:
            case Type.SUM:
                return sum(children)
            case Type.PRODUCT:
                return math.prod(children)
            case Type.MINIMUM:
                return min(children)
            case Type.MAXIMUM:
                return max(children)
            case Type.LITERAL:
                return int(packet.value or 0)  # Account for possible None of a non-literal
            case Type.GREATER:
                return int(operator.gt(*children))
            case Type.LESS:
                return int(operator.lt(*children))
            case Type.EQUAL:
                return int(operator.eq(*children))
            case _:
                raise ValueError(f"Packet has invalid type: {packet.type}")
    except Exception as exception:
        raise ValueError(f'Packet, {packet=}, could not be interpreted.') from exception


@pytest.mark.parametrize(
    "packet,expected",
    (
        ["C200B40A82", 3],

        # Per the problem, "04005AC33890 finds the product of 6 and 9, resulting in the value 54."
        # However, `0x04005AC33890` is `0b1000000000001011010110000110011100010010000`, which
        # starts with a sum packet, not a product packet. Interpreting the Packet produced by that
        # causes `max()` to throw a `ValueError` because its argument is an empty sequence.
        # ["04005AC33890", 54],
        ["880086C3E88112", 7],
        ["CE00C43D881120", 9],
        ["D8005AC2A8F0", 1],
        ["F600BC2D8F", 0],
        ["9C005AC2F8F0", 0],
        ["9C0141080250320F1802104A08", 1],
    ),
)
def test_solve_part_two(packet: str, expected: int) -> None:
    actual = solve_part_two(packet)
    assert actual == expected


if __name__ == "__main__":
    from pathlib import Path

    input_file = Path("./input16.txt")
    with input_file.open() as f:
        packet = f.readline()
    print(
        "Decode the structure of your hexadecimal-encoded BITS transmission; what do you get if you add up the version numbers in all packets?",
        solve_part_one(packet),
        sep="\n\t",
    )
    print(
        "What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS transmission?",
        solve_part_two(packet),
        sep="\n",
    )

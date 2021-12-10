"""
--- Day 8: Seven Segment Search ---

You barely reach the safety of the cave when the whale smashes into the cave mouth, collapsing it. Sensors indicate another exit to this cave at a much greater depth, so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that the four-digit seven-segment displays in your submarine are malfunctioning; they must have been damaged during the escape. You'll be in a lot of trouble without them, so you'd better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of seven segments named a through g:

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

So, to render a 1, only segments c and f would be turned on; the rest would be off. To render a 7, only segments a, c, and f would be turned on.

The problem is that the signals which control the segments have been mixed up on each display. The submarine is still trying to display numbers by producing output on signal wires a through g, but those wires are connected to segments randomly. Worse, the wire/segment connections are mixed up separately for each four-digit display! (All of the digits within a display use the same connections, though.)

So, you might know that only signal wires b and g are turned on, but that doesn't mean segments b and g are turned on: the only digit that uses two segments is 1, so it must mean segments c and f are meant to be on. With just that information, you still can't tell which wire (b/g) goes to which segment (c/f). For that, you'll need to collect more information.

For each display, you watch the changing signals for a while, make a note of all ten unique signal patterns you see, and then write down a single four digit output value (your puzzle input). Using the signal patterns, you should be able to work out which pattern corresponds to which digit.

For example, here is what you might see in a single entry in your notes:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf

(The entry is wrapped here to two lines so it fits; in your notes, it will all be on a single line.)

Each entry consists of ten unique signal patterns, a | delimiter, and finally the four digit output value. Within an entry, the same wire/segment connections are used (but you don't know what the connections actually are). The unique signal patterns correspond to the ten different ways the submarine tries to render a digit using the current wire/segment connections. Because 7 is the only digit that uses three segments, dab in the above example means that to render a 7, signal lines d, a, and b are on. Because 4 is the only digit that uses four segments, eafb means that to render a 4, signal lines e, a, f, and b are on.

Using this information, you should be able to work out which combination of signal wires corresponds to each of the ten digits. Then, you can decode the four digit output value. Unfortunately, in the above example, all of the digits in the output value (cdfeb fcadb cdfeb cdbaf) use five segments and are more difficult to deduce.

For now, focus on the easy digits. Consider this larger example:

be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
fgae cfgab fg bagce

Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be able to tell which combinations of signals correspond to those digits. Counting only digits in the output values (the part after | on each line), in the above example, there are 26 instances of digits that use a unique number of segments (highlighted above).

In the output values, how many times do digits 1, 4, 7, or 8 appear?
"""

from typing import NamedTuple

import pytest

TEST_ENTRIES = [
        "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
        "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
        "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
        "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
        "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
        "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
        "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
        "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
        "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
        "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",
    ]


class Display(NamedTuple):
    signal: str
    output: str


def parse_entry(entry: str) -> Display:
    return Display(*entry.split(" | "))


def test_parse_entry() -> None:
    entry = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    expected = Display(
        "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab",
        "cdfeb fcadb cdfeb cdbaf",
    )
    actual = parse_entry(entry)
    assert actual == expected


def count_unique_digits(display: Display) -> int:
    """Return the count of digits 1, 4, 7, and 8 in the Display's output."""
    valid_lengths = {
        2,  # 1
        3,  # 7
        4,  # 4
        7,  # 8
    }
    return sum(len(output) in valid_lengths for output in display.output.split(" "))


@pytest.mark.parametrize(
    "display,expected",
    [
        (
            Display(
                "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb",
                "fdgacbe cefdb cefbgd gcbe",
            ),
            2,
        ),
        (
            Display(
                "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec",
                "fcgedb cgb dgebacf gc",
            ),
            3,
        ),
        (
            Display(
                "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef",
                "cg cg fdcagb cbg",
            ),
            3,
        ),
        (
            Display(
                "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega",
                "efabcd cedba gadfec cb",
            ),
            1,
        ),
        (
            Display(
                "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga",
                "gecf egdcabf bgf bfgea",
            ),
            3,
        ),
        (
            Display(
                "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf",
                "gebdcfa ecba ca fadegcb",
            ),
            4,
        ),
        (
            Display(
                "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf",
                "cefg dcbef fcge gbcadfe",
            ),
            3,
        ),
        (
            Display(
                "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd",
                "ed bcgafe cdgba cbgef",
            ),
            1,
        ),
        (
            Display(
                "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg",
                "gbdfcae bgc cg cgb",
            ),
            4,
        ),
        (
            Display(
                "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc",
                "fgae cfgab fg bagce",
            ),
            2,
        ),
    ],
)
def test_count_unique_digits(display: Display, expected: int) -> None:
    assert count_unique_digits(display) == expected


def solve_part_one(entries: list[str]) -> int:
    """Return the count of digits 1, 4, 7, and 8."""
    return sum(count_unique_digits(parse_entry(entry)) for entry in entries)


def test_solve_part_one() -> None:
    expected = 26
    actual = solve_part_one(TEST_ENTRIES)
    assert actual == expected


"""
--- Part Two ---

Through a little deduction, you should now be able to determine the remaining digits. Consider again the first example above:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf

After some careful analysis, the mapping between signal wires and segments only make sense in the following configuration:

 dddd
e    a
e    a
 ffff
g    b
g    b
 cccc

So, the unique signal patterns would correspond to the following digits:

    acedgfb: 8
    cdfbe: 5
    gcdfa: 2
    fbcad: 3
    dab: 7
    cefabd: 9
    cdfgeb: 6
    eafb: 4
    cagedb: 0
    ab: 1

Then, the four digits of the output value can be decoded:

    cdfeb: 5
    fcadb: 3
    cdfeb: 5
    cdbaf: 3

Therefore, the output value for this entry is 5353.

Following this same process for each entry in the second, larger example above, the output value of each entry can be determined:

    fdgacbe cefdb cefbgd gcbe: 8394
    fcgedb cgb dgebacf gc: 9781
    cg cg fdcagb cbg: 1197
    efabcd cedba gadfec cb: 9361
    gecf egdcabf bgf bfgea: 4873
    gebdcfa ecba ca fadegcb: 8418
    cefg dcbef fcge gbcadfe: 4548
    ed bcgafe cdgba cbgef: 1625
    gbdfcae bgc cg cgb: 8717
    fgae cfgab fg bagce: 4315

Adding all of the output values in this larger example produces 61229.

For each entry, determine all of the wire/segment connections and decode the four-digit output values. What do you get if you add up all of the output values?

"""

digits_to_segments = {0: 6, 1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6}


def translate_signal(signals: list[str]) -> dict[frozenset[str], int]:
    """Return a map of frozensets of signals to the digits they represent"""
    digits = {digit: "" for digit in range(10)}
    fives = set('')
    sixes = set('')
    for signal in signals:
        match len(signal):
            case 2:
                digits[1] = signal
            case 3:
                digits[7] = signal
            case 4:
                digits[4] = signal
            case 5:
                fives.add(signal)
            case 6:
                sixes.add(signal)
            case 7:
                digits[8] = signal
    for signal in fives:
        if len(set(digits[4]).intersection(set(signal))) == 2:
            digits[2] = signal
        elif len(set(digits[7]).intersection(set(signal))) == 3:
            digits[3] = signal
        else:
            digits[5] = signal
    for signal in sixes:
        if not set(digits[4]).union(set(digits[3])).symmetric_difference(set(signal)):
            digits[9] = signal
    sixes.remove(digits[9])
    # We could get lower left from (3 + 7) - 2 and then loop over sixes once.
    lower_left = (set(digits[8]) - set(digits[9])).pop()
    for signal in sixes:
        if (set(digits[5] + lower_left) == set(signal)):
            digits[6] = signal
        else:
            digits[0] = signal
    top = (set(digits[7]) - set(digits[1])).pop()
    lower_right = (set(digits[3]) - set(digits[2])).pop()
    upper_right = (set(digits[9]) - set(digits[5])).pop()
    middle = (set(digits[8]) - set(digits[0])).pop()
    upper_left = (set(digits[9]) - set(digits[3])).pop()
    bottom = (set(digits[8]) - set([top, middle, upper_left, upper_right, lower_left, lower_right])).pop()
    return {
        frozenset([top, bottom, upper_left, upper_right, lower_left, lower_right]): 0,
        frozenset([upper_right, lower_right]): 1,
        frozenset([top, middle, bottom, upper_right, lower_left]): 2,
        frozenset([top, middle, bottom, upper_right, lower_right]): 3,
        frozenset([middle, upper_left, upper_right, lower_right]): 4,
        frozenset([top, middle, bottom, upper_left, lower_right]): 5,
        frozenset([top, middle, bottom, upper_left, lower_left, lower_right]): 6,
        frozenset([top, upper_right, lower_right]): 7,
        frozenset([top, middle, bottom, upper_left, upper_right, lower_left, lower_right]): 8,
        frozenset([top, middle, bottom, upper_left, upper_right, lower_right]): 9,
    }

def decode_output(display: Display) -> int:
    signal_map = translate_signal(display.signal.split(' '))
    value = [
        str(signal_map[frozenset(output)])
        for output in display.output.split(' ')
    ]
    return int(''.join(value))

def solve_part_two(entries: list[str]) -> int:
    parsed = [parse_entry(entry) for entry in entries]
    return sum(decode_output(display) for display in parsed)

def test_solve_part_two() -> None:
    expected = 61229
    actual = solve_part_two(TEST_ENTRIES)
    assert actual == expected

if __name__ == "__main__":
    from pathlib import Path

    input_file = Path("./input08.txt")
    with input_file.open() as f:
        entries = [
            line.strip("\n").strip()
            for line in f.readlines()
            if line.strip("\n").strip()
        ]
    print(
        "In the output values, how many times do digits 1, 4, 7, or 8 appear?",
        solve_part_one(entries),
        sep="\n\t",
    )
    print(
        "For each entry, determine all of the wire/segment connections and decode the four-digit output values. What do you get if you add up all of the output values?",
        solve_part_two(entries),
        sep="\n\t",
    )

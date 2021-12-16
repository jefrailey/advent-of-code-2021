from collections import Counter
import math

import pytest

TEST_RULES = [
    "CH -> B",
    "HH -> N",
    "CB -> H",
    "NH -> C",
    "HB -> C",
    "HC -> B",
    "HN -> C",
    "NN -> C",
    "BH -> H",
    "NC -> B",
    "NB -> B",
    "BN -> B",
    "BB -> N",
    "BC -> B",
    "CC -> N",
    "CN -> C",
]

TEST_RULES_MAP = {
    "CH": "B",
    "HH": "N",
    "CB": "H",
    "NH": "C",
    "HB": "C",
    "HC": "B",
    "HN": "C",
    "NN": "C",
    "BH": "H",
    "NC": "B",
    "NB": "B",
    "BN": "B",
    "BB": "N",
    "BC": "B",
    "CC": "N",
    "CN": "C",
}


def solve_part_one(template: str, rules: list[str]) -> int:
    """Return the difference between the quantity of the most and least common elements after ten rounds of pair insertion."""
    rules_map = map_rules(rules)
    pairs = to_pairs(template)
    pair_counts = Counter(pairs)
    for _ in range(10):
        pair_counts = insert(pair_counts, rules_map)
    counts: Counter[str] = Counter()
    for pair, count in pair_counts.items():
        left, right = pair
        counts[left] += count
        counts[right] += count
    return math.ceil(max(count for count in counts.values()) / 2) - math.ceil(
        min(count for count in counts.values()) / 2
    )


def to_pairs(polymer: str) -> list[str]:
    return [
        polymer[i : i + 2] for i in range(len(polymer)) if len(polymer[i : i + 2]) == 2
    ]


def test_solve_part_one() -> None:
    expected = 1588
    template = "NNCB"
    actual = solve_part_one(template, TEST_RULES)
    assert actual == expected


def insert(pair_counts: Counter[str], rules_map: dict[str, str]) -> Counter[str]:
    """Return a polymer with elements inserted per the pair insertion rules."""
    new_counts: Counter[str] = Counter(pair_counts)
    for pair, count in pair_counts.items():
        new_counts[pair] -= count
        middle = rules_map[pair]
        left = "".join([pair[0], middle])
        right = "".join([middle, pair[1]])
        new_counts[left] += count
        new_counts[right] += count
    return new_counts


@pytest.mark.parametrize(
    "polymer,rules,expected",
    (
        ["NN", TEST_RULES_MAP, "NCN"],
        ["NC", TEST_RULES_MAP, "NBC"],
        ["CB", TEST_RULES_MAP, "CHB"],
        ["NNCB", TEST_RULES_MAP, "NCNBCHB"],
        ["NCNBCHB", TEST_RULES_MAP, "NBCCNBBBCBHCB"],
        ["NBCCNBBBCBHCB", TEST_RULES_MAP, "NBBBCNCCNBBNBNBBCHBHHBCHB"],
        [
            "NBBBCNCCNBBNBNBBCHBHHBCHB",
            TEST_RULES_MAP,
            "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB",
        ],
    ),
)
def test_insert(polymer: str, rules: dict[str, str], expected: str) -> None:
    pair_counts = Counter(to_pairs(polymer))
    actual = insert(pair_counts, rules)
    assert actual == Counter(to_pairs(expected))


def map_rules(rules: list[str]) -> dict[str, str]:
    """Return a map of element pairs to the element that should be inserted between them."""
    map_: dict[str, str] = {}
    for rule in rules:
        pair, insertee = rule.split(" -> ")
        map_[pair] = insertee
    return map_


"""
--- Part Two ---

The resulting polymer isn't nearly strong enough to reinforce the submarine. You'll need to run more steps of the pair insertion process; a total of 40 steps should do it.

In the above example, the most common element is B (occurring 2192039569602 times) and the least common element is H (occurring 3849876073 times); subtracting these produces 2188189693529.

Apply 40 steps of pair insertion to the polymer template and find the most and least common elements in the result. What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?
"""


def solve_part_two(template: str, rules: list[str]) -> int:
    """Return the difference between the quantity of the most and least common elements after forty rounds of pair insertion."""
    rules_map = map_rules(rules)
    pairs = to_pairs(template)
    pair_counts = Counter(pairs)
    for _ in range(40):
        pair_counts = insert(pair_counts, rules_map)
    counts: Counter[str] = Counter()
    for pair, count in pair_counts.items():
        left, right = pair
        counts[left] += count
        counts[right] += count
    return max(count for count in counts.values()) - min(
        count for count in counts.values()
    )


def test_solve_part_two() -> None:
    expected = 2188189693529
    template = "NNCB"
    actual = solve_part_two(template, TEST_RULES)
    assert actual == expected


if __name__ == "__main__":
    from pathlib import Path

    input_file = Path("./input14.txt")
    with input_file.open() as f:
        template = ""
        rules: list[str] = []
        for idx, line in enumerate(f.readlines()):
            line = line.strip().strip("\n")
            if idx == 0:
                template = line
            elif line:
                rules.append(line)
    print(
        "What do you get if you take the quantity of the most common element and subtract the quantity of the least common element?",
        solve_part_one(template, rules),
        sep="\n\t",
    )
    print(
        "",
        solve_part_two(template, rules),
        sep="\n",
    )

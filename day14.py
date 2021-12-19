from collections import Counter

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
    return _solve(template, rules, 10)


def _solve(template: str, rules: list[str], steps: int) -> int:
    """Return the difference between the quantity of the most and least common elements after a given number of rounds."""
    rules_map = map_rules(rules)
    counts = Counter(
        template[i : i + 2]
        for i in range(len(template))
        if len(template[i : i + 2]) == 2
    )
    counts.update(template)
    for _ in range(steps):
        counts = insert(counts, rules_map)
    element_counts = [count for (key, count) in counts.items() if len(key) == 1]
    return max(element_counts) - min(element_counts)


def test_solve_part_one() -> None:
    expected = 1588
    template = "NNCB"
    actual = solve_part_one(template, TEST_RULES)
    assert actual == expected


def insert(counts: Counter[str], rules_map: dict[str, str]) -> Counter[str]:
    """Return a polymer with elements inserted per the pair insertion rules."""
    new_counts: Counter[str] = Counter(counts)
    pairs = ((key, count) for (key, count) in counts.items() if len(key) == 2)
    for pair, count in pairs:
        new_counts[pair] -= count
        new_element = rules_map[pair]
        left_pair = "".join([pair[0], new_element])
        right_pair = "".join([new_element, pair[1]])
        new_counts[left_pair] += count
        new_counts[right_pair] += count
        new_counts[new_element] += count
    return new_counts


@pytest.mark.parametrize(
    "initial_counts,rules,expected",
    (
        [
            Counter({"NN": 1}),
            TEST_RULES_MAP,
            Counter({"NN": 0, "C": 1, "NC": 1, "CN": 1}),
        ],
        [
            Counter({"NC": 1}),
            TEST_RULES_MAP,
            Counter({"NC": 0, "NB": 1, "BC": 1, "B": 1}),
        ],
        [
            Counter({"CB": 1}),
            TEST_RULES_MAP,
            Counter({"CB": 0, "CH": 1, "HB": 1, "H": 1}),
        ],
        [
            Counter({"NN": 1, "NC": 1, "CB": 1}),
            TEST_RULES_MAP,
            Counter(
                {
                    "NN": 0,
                    "CB": 0,
                    "C": 1,
                    "NC": 1,
                    "CN": 1,
                    "CH": 1,
                    "HB": 1,
                    "H": 1,
                    "NB": 1,
                    "BC": 1,
                    "B": 1,
                }
            ),
        ],
    ),
)
def test_insert(
    initial_counts: Counter[str], rules: dict[str, str], expected: Counter[str]
) -> None:
    actual = insert(initial_counts, rules)
    assert actual == expected


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
    return _solve(template, rules, 40)


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

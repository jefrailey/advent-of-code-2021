"""
--- Day 7: The Treachery of Whales ---

A giant whale has decided your submarine is its next meal, and it's much faster than you are. There's nowhere to run!

Suddenly, a swarm of crabs (each in its own tiny submarine - it's too deep for them otherwise) zooms in to rescue you! They seem to be preparing to blast a hole in the ocean floor; sensors indicate a massive underground cave system just beyond where they're aiming!

The crab submarines all need to be aligned before they'll have enough power to blast a large enough hole for your submarine to get through. However, it doesn't look like they'll be aligned before the whale catches you! Maybe you can help?

There's one major catch - crab submarines can only move horizontally.

You quickly make a list of the horizontal position of each crab (your puzzle input). Crab submarines have limited fuel, so you need to find a way to make all of their horizontal positions match while requiring them to spend as little fuel as possible.

For example, consider the following horizontal positions:

16,1,2,0,4,2,7,1,2,14

This means there's a crab with horizontal position 16, a crab with horizontal position 1, and so on.

Each change of 1 step in horizontal position of a single crab costs 1 fuel. You could choose any horizontal position to align them all on, but the one that costs the least fuel is horizontal position 2:

    Move from 16 to 2: 14 fuel
    Move from 1 to 2: 1 fuel
    Move from 2 to 2: 0 fuel
    Move from 0 to 2: 2 fuel
    Move from 4 to 2: 2 fuel
    Move from 2 to 2: 0 fuel
    Move from 7 to 2: 5 fuel
    Move from 1 to 2: 1 fuel
    Move from 2 to 2: 0 fuel
    Move from 14 to 2: 12 fuel

This costs a total of 37 fuel. This is the cheapest possible outcome; more expensive outcomes include aligning at position 1 (41 fuel), position 3 (39 fuel), or position 10 (71 fuel).

Determine the horizontal position that the crabs can align to using the least fuel possible. How much fuel must they spend to align to that position?

"""

from typing import NamedTuple
import math


TEST_INPUT = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


class PositionAndCost(NamedTuple):
    position: int
    cost: int


def determine_best_position(positions: list[int]) -> PositionAndCost:
    """Return the position to move all crabs to that minimizes fuel spent.

    Assume crab ships burn one fuel per unit of movement.
    """
    # Can we do better than this O(n^2) algorithm?
    costs = dict(zip(positions, [math.inf] * len(positions)))
    for end in range(min(positions), max(positions) + 1):
        costs[end] = sum(abs(end - start) for start in positions)
    min_position = min(costs.keys(), key=lambda x: costs[x])
    return PositionAndCost(position=min_position, cost=int(costs[min_position]))


def test_determine_best_position() -> None:
    expected = PositionAndCost(2, 37)
    actual = determine_best_position(TEST_INPUT)
    assert actual == expected


def solve_part_one(positions: list[int]) -> int:
    """Return the minimum amount of fuel required to move all crabs to the same position."""
    return determine_best_position(positions).cost


def test_solve_part_one() -> None:
    expected = 37
    actual = solve_part_one(TEST_INPUT)
    assert actual == expected


"""
--- Part Two ---

The crabs don't seem interested in your proposed solution. Perhaps you misunderstand crab engineering?

As it turns out, crab submarine engines don't burn fuel at a constant rate. Instead, each change of 1 step in horizontal position costs 1 more unit of fuel than the last: the first step costs 1, the second step costs 2, the third step costs 3, and so on.

As each crab moves, moving further becomes more expensive. This changes the best horizontal position to align them all on; in the example above, this becomes 5:

    Move from 16 to 5: 66 fuel
    Move from 1 to 5: 10 fuel
    Move from 2 to 5: 6 fuel
    Move from 0 to 5: 15 fuel
    Move from 4 to 5: 1 fuel
    Move from 2 to 5: 6 fuel
    Move from 7 to 5: 3 fuel
    Move from 1 to 5: 10 fuel
    Move from 2 to 5: 6 fuel
    Move from 14 to 5: 45 fuel

This costs a total of 168 fuel. This is the new cheapest possible outcome; the old alignment position (2) now costs 206 fuel instead.

Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an escape route! How much fuel must they spend to align to that position?
"""


def solve_part_two(positions: list[int]) -> int:
    """Return the minimum amount of fuel required to move all crabs to the same position.

    Take into account that the crab ships do not burn fuel at a constant rate.
    """
    return determine_best_position_modified_burn(positions).cost


def determine_best_position_modified_burn(positions: list[int]) -> PositionAndCost:
    """Return the position to move all crabs to that minimizes fuel spent.

    Assume crab ships burn an incraesing amount of fuel per unit of movement.
    """
    # Can we do better than this O(n^2) algorithm?
    costs = dict(zip(positions, [math.inf] * len(positions)))
    for end in range(min(positions), max(positions) + 1):
        costs[end] = sum(
            calculate_accelerated_fuel_cost(start, end) for start in positions
        )
    min_position = min(costs.keys(), key=lambda x: costs[x])
    return PositionAndCost(position=min_position, cost=int(costs[min_position]))


def calculate_accelerated_fuel_cost(a: int, b: int) -> int:
    """Return the fuel required to move from one position to another.

    The marginal fuel per space cost increases by one for each space
    moved. That is, it takes one fuel to move one space, but three
    fuel (1 + 2) to move two spaces.
    """
    diff = abs(a - b)
    return (diff * (diff + 1)) // 2


def test_determine_best_position_modified_burn() -> None:
    expected = PositionAndCost(position=5, cost=168)
    actual = determine_best_position_modified_burn(TEST_INPUT)
    assert actual == expected


def test_solve_part_two() -> None:
    expected = 168
    actual = solve_part_two(TEST_INPUT)
    assert actual == expected


if __name__ == "__main__":
    from pathlib import Path

    input_file = Path("./input07.txt")
    with input_file.open() as f:
        positions = [int(position) for position in f.readline().strip("\n").split(",")]
    print(
        "Determine the horizontal position that the crabs can align to using the least fuel possible. How much fuel must they spend to align to that position?",
        solve_part_one(positions),
        sep="\n\t",
    )
    print(
        "Determine the horizontal position that the crabs can align to using the least fuel possible so they can make you an escape route! How much fuel must they spend to align to that position?",
        solve_part_two(positions),
        sep="\n\t",
    )

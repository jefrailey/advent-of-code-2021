"""
--- Day 2: Dive! ---

Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

    forward X increases the horizontal position by X units.
    down X increases the depth by X units.
    up X decreases the depth by X units.

Note that since you're on a submarine, down and up affect your depth, and so they have the opposite result of what you might expect.

The submarine seems to already have a planned course (your puzzle input). You should probably figure out where it's going. For example:

forward 5
down 5
forward 8
up 3
down 8
forward 2

Your horizontal position and depth both start at 0. The steps above would then modify them as follows:

    forward 5 adds 5 to your horizontal position, a total of 5.
    down 5 adds 5 to your depth, resulting in a value of 5.
    forward 8 adds 8 to your horizontal position, a total of 13.
    up 3 decreases your depth by 3, resulting in a value of 2.
    down 8 adds 8 to your depth, resulting in a value of 10.
    forward 2 adds 2 to your horizontal position, a total of 15.

After following these instructions, you would have a horizontal position of 15 and a depth of 10. (Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?

"""

from typing import NamedTuple


X = int
Depth = int


class Position(NamedTuple):
    x: X
    depth: Depth


def follow_course(instructions: list[str]) -> Position:
    """Return a Position after following course instructions."""
    x = 0
    depth = 0
    for instruction in instructions:
        direction, distance = instruction.split(" ")
        distance = int(distance)
        if direction == "forward":
            x += distance
        elif direction == "down":
            depth += distance
        elif direction == "up":
            depth -= distance
    return Position(x, depth)


def test_follow_course() -> None:
    instructions = [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2",
    ]
    expected = Position(15, 10)
    actual = follow_course(instructions)
    assert actual == expected


def solve_part_one(instructions: list[str]) -> int:
    """Return the product of the horizontal position and the depth reached."""
    position = follow_course(instructions)
    return position.x * position.depth


def test_solve_part_one() -> None:
    instructions = [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2",
    ]
    expected = 15 * 10
    actual = solve_part_one(instructions)
    assert actual == expected


"""
--- Part Two ---

Based on your calculations, the planned course doesn't seem to make any sense. You find the submarine manual and discover that the process is actually slightly more complicated.

In addition to horizontal position and depth, you'll also need to track a third value, aim, which also starts at 0. The commands also mean something entirely different than you first thought:

    down X increases your aim by X units.
    up X decreases your aim by X units.
    forward X does two things:
        It increases your horizontal position by X units.
        It increases your depth by your aim multiplied by X.

Again note that since you're on a submarine, down and up do the opposite of what you might expect: "down" means aiming in the positive direction.

Now, the above example does something different:

    forward 5 adds 5 to your horizontal position, a total of 5. Because your aim is 0, your depth does not change.
    down 5 adds 5 to your aim, resulting in a value of 5.
    forward 8 adds 8 to your horizontal position, a total of 13. Because your aim is 5, your depth increases by 8*5=40.
    up 3 decreases your aim by 3, resulting in a value of 2.
    down 8 adds 8 to your aim, resulting in a value of 10.
    forward 2 adds 2 to your horizontal position, a total of 15. Because your aim is 10, your depth increases by 2*10=20 to a total of 60.

After following these new instructions, you would have a horizontal position of 15 and a depth of 60. (Multiplying these produces 900.)

Using this new interpretation of the commands, calculate the horizontal position and depth you would have after following the planned course. What do you get if you multiply your final horizontal position by your final depth?
"""


def follow_course_with_aim(instructions: list[str]) -> Position:
    """Return a Position after following course instructions taking into account aim."""
    x = 0
    depth = 0
    aim = 0
    for instruction in instructions:
        direction, distance = instruction.split(" ")
        distance = int(distance)
        if direction == "down":
            aim += distance
        elif direction == "up":
            aim -= distance
        elif direction == "forward":
            x += distance
            depth += aim * distance
    return Position(x, depth)


def test_follow_course_with_aim() -> None:
    instructions = [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2",
    ]
    expected = Position(15, 60)
    actual = follow_course_with_aim(instructions)
    assert actual == expected


def solve_part_two(instructions: list[str]) -> int:
    position = follow_course_with_aim(instructions)
    return position.x * position.depth


def test_solve_part_two() -> None:
    instructions = [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2",
    ]
    expected = 15 * 60
    actual = solve_part_two(instructions)
    assert actual == expected


if __name__ == "__main__":
    from pathlib import Path

    input_file = Path("./input02.txt")
    with input_file.open() as f:
        input_ = list(f.readlines())
    print(
        "What do you get if you multiply your final horizontal position by your final depth?",
        solve_part_one(input_),
        sep="\n\t",
    )
    print(
        "Using this new interpretation of the commands, what do you get if you multiply your final horizontal position by your final depth?",
        solve_part_two(input_),
        sep="\n\t",
    )

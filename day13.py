"""
--- Day 13: Transparent Origami ---

You reach another volcanically active part of the cave. It would be nice if you could do some kind of thermal imaging so you could tell ahead of time which caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you activate it, you are greeted with:

Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.

Apparently, the Elves have never used this feature. To your surprise, you manage to find the manual; as you go to open it, page 1 falls out. It's a large sheet of transparent paper! The transparent paper is marked with random dots and includes instructions on how to fold it up (your puzzle input). For example:

6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5

The first section is a list of dots on the transparent paper. 0,0 represents the top-left coordinate. The first value, x, increases to the right. The second value, y, increases downward. So, the coordinate 3,0 is to the right of 0,0, and the coordinate 0,7 is below 0,0. The coordinates in this example form the following pattern, where # is a dot on the paper and . is an empty, unmarked position:

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Then, there is a list of fold instructions. Each instruction indicates a line on the transparent paper and wants you to fold the paper up (for horizontal y=... lines) or left (for vertical x=... lines). In this example, the first fold instruction is fold along y=7, which designates the line formed by all of the positions where y is 7 (marked here with -):

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Because this is a horizontal line, fold the bottom half up. Some of the dots might end up overlapping after the fold is complete, but dots will never appear exactly on a fold line. The result of doing this fold looks like this:

#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........

Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the transparent paper is folded; after the fold is complete, those dots appear in the top left corner (at 0,0 and 0,1). Because the paper is transparent, the dot just below them in the result (at 0,3) remains visible, as it can be seen through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots merge together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....

Because this is a vertical line, fold left:

#####
#...#
#...#
#...#
#####
.....
.....

The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the first fold. After the first fold in the example above, 17 dots are visible - dots that end up overlapping after the fold is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on your transparent paper?
"""


# Model dots on paper as a set of points
# When a fold occurs
# create a new set
# iterate over the points in the old set
# if the current point has y or x value greater than the fold,
# determine its new position add that to the new set
# else add it to the new set

from typing import NamedTuple


class Dot(NamedTuple):
    x: int
    y: int


Paper = set[Dot]


def make_paper(dots: list[str]) -> Paper:
    """Return Paper created from a list coordinates of dots."""
    paper: Paper = set()
    for dot in dots:
        x, y = dot.split(",")
        paper.add(Dot(x=int(x), y=int(y)))
    return paper


def fold(paper: Paper, axis: str, value: int) -> Paper:
    """Return Paper folded along the given axis."""
    folded: Paper = set()
    for dot in paper:
        if axis == "x" and dot.x > value:
            folded_x = value - (dot.x - value)
            dot = Dot(x=folded_x, y=dot.y)
        elif axis == "y" and dot.y > value:
            folded_y = value - (dot.y - value)
            dot = Dot(x=dot.x, y=folded_y)
        folded.add(dot)
    return folded


def solve_part_one(dots: list[str], instructions: list[str]) -> int:
    """Return the number of visible dots after completing the first fold instruction."""
    paper = make_paper(dots)
    instruction = instructions[0]
    instruction = instruction.replace("fold along ", "")
    axis, value = instruction.split("=")
    value = int(value)
    paper = fold(paper, axis, value)
    return len(paper)


def test_solve_part_one() -> None:
    dots = [
        "6,10",
        "0,14",
        "9,10",
        "0,3",
        "10,4",
        "4,11",
        "6,0",
        "6,12",
        "4,1",
        "0,13",
        "10,12",
        "3,4",
        "3,0",
        "8,4",
        "1,10",
        "2,14",
        "8,10",
        "9,0",
    ]
    folds = ["fold along y=7", "fold along x=5"]
    expected = 17
    actual = solve_part_one(dots, folds)
    assert actual == expected


"""
--- Part Two ---

Finish folding the transparent paper according to the instructions. The manual says the code is always eight capital letters.

What code do you use to activate the infrared thermal imaging camera system?
"""


def solve_part_two(dots: list[str], instructions: list[str]) -> str:
    """Return a string representation of the paper after following the folding instructions."""
    paper = make_paper(dots)
    for instruction in instructions:
        instruction = instruction.replace("fold along ", "")
        axis, value = instruction.split("=")
        value = int(value)
        paper = fold(paper, axis, value)
    max_x = max(paper, key=lambda dot: dot.x).x
    max_y = max(paper, key=lambda dot: dot.y).y
    display: list[str] = []
    for y in range(0, max_y + 1):
        row: list[str] = []
        for x in range(0, max_x + 1):
            if (x, y) in paper:
                row.append("#")
            else:
                row.append(".")
        row.append("\n")
        display.append("".join(row))
    return "".join(display)


if __name__ == "__main__":
    from pathlib import Path

    input_file = Path("./input13.txt")
    with input_file.open() as f:
        dots: list[str] = []
        instructions: list[str] = []
        for line in f.readlines():
            line = line.strip().strip("\n")
            if not line:
                continue
            if line.startswith("fold"):
                instructions.append(line)
            else:
                dots.append(line)
    print(
        "How many dots are visible after completing just the first fold instruction on your transparent paper?",
        solve_part_one(dots, instructions),
        sep="\n\t",
    )
    print(
        "What code do you use to activate the infrared thermal imaging camera system?",
        solve_part_two(dots, instructions),
        sep="\n",
    )

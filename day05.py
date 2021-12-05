"""
--- Day 5: Hydrothermal Venture ---

You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

    An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

"""

from collections import Counter
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Line(NamedTuple):
    start: Point
    stop: Point

    @property
    def is_horizontal(self) -> bool:
        """Return True if the line is horizontal."""
        return self.start.y == self.stop.y

    @property
    def is_vertical(self) -> bool:
        """Return True if the line is vertical."""
        return self.start.x == self.stop.x

    @property
    def points(self) -> list[Point]:
        if self.is_horizontal:
            min_x, max_x = sorted([self.start.x, self.stop.x])
            y = self.start.y
            return [Point(x=min_x + i, y=y) for i in range(max_x - min_x + 1)]
        elif self.is_vertical:
            min_y, max_y = sorted([self.start.y, self.stop.y])
            x = self.start.x
            return [Point(x=x, y=min_y + i) for i in range(max_y - min_y + 1)]
        else:
            # The line is diagonal at a 45 degree angle
            # The slope should either be 1 or -1
            rise = self.stop.y - self.start.y
            run = self.stop.x - self.start.x
            slope = rise / run
            if slope not in [1, -1]:
                raise ValueError(
                    f"The diagonal Lines must be at a 45 degree angle. Got slope of {slope=}."
                )
            dx = 1
            if self.stop.x < self.start.x:
                dx = -1
            dy = 1
            if self.stop.y < self.start.y:
                dy = -1
            points = [
                Point(x=self.start.x + (dx * i), y=self.start.y + (dy * i))
                for i in range(abs(rise) + 1)
            ]
            return points


def solve_part_one(raw_segments: list[str]) -> int:
    """Return the number of intersection points of horizontal and vertical lines."""
    lines = [
        Line(
            *(
                Point(*(int(number) for number in point.split(",")))
                for point in segment.split(" -> ")
            )
        )
        for segment in raw_segments
    ]
    horizontal_and_vertical = [
        line for line in lines if line.is_horizontal or line.is_vertical
    ]
    plane: Counter[Point] = Counter()
    for line in horizontal_and_vertical:
        plane.update(line.points)
    return sum(1 for point in plane if plane[point] >= 2)


TEST_SEGMENTS = [
    "0,9 -> 5,9",
    "8,0 -> 0,8",
    "9,4 -> 3,4",
    "2,2 -> 2,1",
    "7,0 -> 7,4",
    "6,4 -> 2,0",
    "0,9 -> 2,9",
    "3,4 -> 1,4",
    "0,0 -> 8,8",
    "5,5 -> 8,2",
]


def test_solve_part_one() -> None:
    expected = 5
    actual = solve_part_one(TEST_SEGMENTS)
    assert actual == expected


"""
--- Part Two ---

Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

    An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
    An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.

Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....

You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
"""


def test_diagonal_lines() -> None:
    line = Line(Point(1, 1), Point(3, 3))
    expected = [Point(1, 1), Point(2, 2), Point(3, 3)]
    actual = line.points
    assert actual == expected


def solve_part_two(raw_segments: list[str]) -> int:
    """Return the number of intersection points of horizontal, vertical, and diagonal lines."""
    lines = [
        Line(
            *(
                Point(*(int(number) for number in point.split(",")))
                for point in segment.split(" -> ")
            )
        )
        for segment in raw_segments
    ]
    plane: Counter[Point] = Counter()
    for line in lines:
        plane.update(line.points)
    return sum(1 for point in plane if plane[point] >= 2)


def pretty_print_intersections(plane: Counter[Point]) -> None:
    """Print a plane with intersection counts."""
    max_x = max(point.x for point in plane.keys())
    max_y = max(point.y for point in plane.keys())
    for y in range(max_y + 1):
        row: list[str] = []
        for x in range(max_x + 1):
            point = Point(x, y)
            marker = "."
            if point in plane:
                marker = str(plane.get(point))
            row.append(marker)
        print("".join(row), end="\n")


def test_solve_part_two() -> None:
    expected = 12
    actual = solve_part_two(TEST_SEGMENTS)
    assert actual == expected


if __name__ == "__main__":
    from pathlib import Path

    input_file = Path("./input05.txt")
    with input_file.open() as f:
        segments = [line.strip("\n") for line in f.readlines() if line.strip("\n")]
    print(
        "Consider only horizontal and vertical lines. At how many points do at least two lines overlap?",
        solve_part_one(segments),
        sep="\n\t",
    )
    print(
        "Consider all of the lines. At how many points do at least two lines overlap?",
        solve_part_two(segments),
        sep="\n\t",
    )

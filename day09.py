"""
--- Day 9: Smoke Basin ---

These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?

"""

from typing import NamedTuple
import pytest
import math

TEST_HEIGHTMAP = [
    "2199943210",
    "3987894921",
    "9856789892",
    "8767896789",
    "9899965678",
]
TEST_GRID = [
    [2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
    [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
    [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
    [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
    [9, 8, 9, 9, 9, 6, 5, 6, 7, 8],
]

Grid = list[list[int]]


def find_lowpoints(grid: Grid) -> list[int]:
    """Return a list of heights that are local minima."""
    lowpoints: list[int] = []
    for row_idx, row in enumerate(grid):
        for height_idx, height in enumerate(row):
            neighbors = find_neighbors(grid, row_idx, height_idx)
            if height < min(neighbors):
                lowpoints.append(height)
    return lowpoints


def test_find_lowpoints() -> None:
    expected = [0, 1, 5, 5]
    actual = find_lowpoints(TEST_GRID)
    assert sorted(actual) == sorted(expected)


def find_neighbors(grid: Grid, row: int, column: int) -> list[int]:
    """Return the value of the cardinally adjacent neighbors to the element at the given index."""
    max_row = len(grid) - 1
    max_column = len(grid[0]) - 1
    up = (row - 1, column)
    down = (row + 1, column)
    left = (row, column - 1)
    right = (row, column + 1)
    return [
        grid[row][column]
        for (row, column) in (up, down, left, right)
        if 0 <= row <= max_row and 0 <= column <= max_column
    ]


@pytest.mark.parametrize(
    "grid,row,column,expected",
    (
        [TEST_GRID, 0, 0, [1, 3]],
        [TEST_GRID, 0, 1, [2, 9, 9]],
        [TEST_GRID, 0, 9, [1, 1]],
        [TEST_GRID, 4, 0, [8, 8]],
        [TEST_GRID, 4, 9, [7, 9]],
        [TEST_GRID, 2, 5, [7, 9, 9, 9]],
    ),
)
def test_find_neighbors(grid: Grid, row: int, column: int, expected: list[int]) -> None:
    assert sorted(find_neighbors(grid, row, column)) == sorted(expected)


def solve_part_one(grid: Grid) -> int:
    """Return the sum of the risk levels on all low points of the hightmap."""
    local_minima = find_lowpoints(grid)
    return sum(minima + 1 for minima in local_minima)


def convert_heightmap_to_grid(heightmap: list[str]) -> Grid:
    """Return a list of lists of heights from the heightmap as a list of strings."""
    return [[int(height) for height in row] for row in heightmap]


def test_convert_heightmap_to_grid() -> None:
    expected = TEST_GRID
    actual = convert_heightmap_to_grid(TEST_HEIGHTMAP)
    assert actual == expected


"""
--- Part Two ---

Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678

The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678

The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?
"""


class Point(NamedTuple):
    x: int
    y: int
    value: int


def find_lowpoint_coordinates(grid: Grid) -> list[Point]:
    """Return a list of heights that are local minima."""
    lowpoints: list[Point] = []
    for row_idx, row in enumerate(grid):
        for height_idx, height in enumerate(row):
            neighbors = find_neighbors(grid, row_idx, height_idx)
            if height < min(neighbors):
                lowpoints.append(
                    Point(x=height_idx, y=row_idx, value=grid[row_idx][height_idx])
                )
    return lowpoints


def test_find_lowpoint_coordinates() -> None:
    expected = [
        Point(1, 0, 1),
        Point(9, 0, 0),
        Point(2, 2, 5),
        Point(6, 4, 5),
    ]
    actual = find_lowpoint_coordinates(TEST_GRID)
    assert sorted(actual) == sorted(expected)


Basin = list[Point]


def solve_part_two(grid: Grid) -> int:
    """Return the product of the three largest basins."""
    minimas = find_lowpoint_coordinates(grid)
    basins = [find_basin(grid, minima) for minima in minimas]
    sizes = [len(basin) for basin in basins]
    return math.prod(sorted(sizes)[-3:])


def test_solve_part_two() -> None:
    expected = 1134
    actual = solve_part_two(TEST_GRID)
    assert actual == expected


def find_basin(grid: Grid, lowpoint: Point) -> Basin:
    """Return the basin that contains the lowpoint."""
    basin: set[Point] = set()
    candidates: list[Point] = [lowpoint]
    while candidates:
        # TODO: replace with deque
        candidate = candidates.pop(0)
        basin.add(candidate)
        candidates.extend(
            [
                neighbor
                for neighbor in find_neighbor_coordinates(grid, candidate)
                if neighbor.value != 9 and neighbor not in basin
            ]
        )
    return list(basin)


@pytest.mark.parametrize(
    "grid,lowpoint,expected",
    (
        [TEST_GRID, Point(1, 0, 1), [Point(1, 0, 1), Point(0, 0, 2), Point(0, 1, 3)]],
        [
            TEST_GRID,
            Point(9, 0, 0),
            [
                Point(5, 0, 4),
                Point(6, 0, 3),
                Point(7, 0, 2),
                Point(8, 0, 1),
                Point(9, 0, 0),
                Point(6, 1, 4),
                Point(8, 1, 2),
                Point(9, 1, 1),
                Point(9, 2, 2),
            ],
        ],
    ),
)
def test_find_basin(grid: Grid, lowpoint: Point, expected: Basin) -> None:
    actual = find_basin(grid, lowpoint)
    assert sorted(actual) == sorted(expected)


def find_neighbor_coordinates(grid: Grid, point: Point) -> list[Point]:
    """Return the coordinates of the cardinally adjacent neighbors to the element at the given point."""
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1
    up = (point.x, point.y - 1)
    down = (point.x, point.y + 1)
    left = (point.x - 1, point.y)
    right = (point.x + 1, point.y)
    return [
        Point(x, y, value=grid[y][x])
        for (x, y) in (up, down, left, right)
        if 0 <= x <= max_x and 0 <= y <= max_y
    ]


if __name__ == "__main__":
    from pathlib import Path

    input_file = Path("./input09.txt")
    with input_file.open() as f:
        heightmap = [
            line.strip().strip("\n")
            for line in f.readlines()
            if line.strip().strip("\n")
        ]
        grid = convert_heightmap_to_grid(heightmap)
    print(
        "Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?",
        solve_part_one(grid),
        sep="\n\t",
    )
    print(
        "What do you get if you multiply together the sizes of the three largest basins?",
        solve_part_two(grid),
        sep="\n\t",
    )

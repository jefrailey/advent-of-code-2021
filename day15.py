"""
--- Day 15: Chiton ---

You've almost reached the exit of the cave, but the walls are getting closer together. Your submarine can barely still fit, though; the main problem is that the walls of the cave are covered in chitons, and it would be best not to bump any of them.

The cavern is large, but has a very low ceiling, restricting your motion to two dimensions. The shape of the cavern resembles a square; a quick scan of chiton density produces a map of risk level throughout the cave (your puzzle input). For example:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

You start in the top left position, your destination is the bottom right position, and you cannot move diagonally. The number at each position is its risk level; to determine the total risk of an entire path, add up the risk levels of each position you enter (that is, don't count the risk level of your starting position unless you enter it; leaving it adds no risk to your total).

Your goal is to find a path with the lowest total risk. In this example, a path with the lowest total risk is highlighted here:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

The total risk of this path is 40 (the starting position is never entered, so its risk is not counted).

What is the lowest total risk of any path from the top left to the bottom right?
"""

from queue import PriorityQueue
from typing import NamedTuple
import sys

TEST_RISK_MAP = [
    [1, 1, 6, 3, 7, 5, 1, 7, 4, 2],
    [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
    [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
    [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
    [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
    [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
    [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
    [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
    [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
    [2, 3, 1, 1, 9, 4, 4, 5, 8, 1],
]

Grid = list[list[int]]


class Node(NamedTuple):
    x: int
    y: int
    risk: int


def solve_part_one(risk_map: Grid) -> int:
    """Return the lowest total risk of any path from the top left to the bottom right."""
    nodes = [
        Node(x, y, risk)
        for (y, row) in enumerate(risk_map)
        for (x, risk) in enumerate(row)
    ]
    node_map = {(node.x, node.y): node for node in nodes}
    start = nodes[0]
    end = nodes[-1]
    risks = {node: sys.maxsize for node in nodes}
    risks[start] = 0
    queue: PriorityQueue[tuple[int, Node]] = PriorityQueue()
    queue.put((risks[start], start))
    while not queue.empty():
        risk, node = queue.get()
        if node == end:
            return risk
        up = (0, -1)
        down = (0, 1)
        left = (-1, 0)
        right = (1, 0)
        neighbors = [
            node_map[(node.x + x, node.y + y)]
            for x, y in [up, down, left, right]
            if (node.x + x, node.y + y) in node_map
        ]
        for neighbor in neighbors:
            current_distance = risks[neighbor]
            risk_through_node = risk + neighbor.risk
            if risk_through_node < current_distance:
                risks[neighbor] = risk_through_node
                queue.put((risk_through_node, neighbor))
    raise Exception(f"No path from start, {start}, to end, {end}, could be found.")


def test_solve_part_one() -> None:
    expected = 40
    actual = solve_part_one(TEST_RISK_MAP)
    assert actual == expected


def solve_part_two() -> int:
    return 0


if __name__ == "__main__":
    from pathlib import Path

    input_file = Path("./input15.txt")
    with input_file.open() as f:
        risk_map = [
            [int(space) for space in line.strip().strip("\n")]
            for line in f.readlines()
            if line.strip().strip("\n")
        ]
    print(
        "What is the lowest total risk of any path from the top left to the bottom right?",
        solve_part_one(risk_map),
        sep="\n\t",
    )
    # print(
    #     "",
    #     solve_part_two(),
    #     sep="\n",
    # )

"""
--- Day 12: Passage Pathing ---

With your submarine's subterranean subsystems subsisting suboptimally, the only way you're getting out of this cave anytime soon is by finding a path yourself. Not just a path - the only way to know if you've found the best path is to find all of them.

Fortunately, the sensors are still mostly working, and so you build a rough map of the remaining caves (your puzzle input). For example:

start-A
start-b
A-c
A-b
b-d
A-end
b-end

This is a list of how all of the caves are connected. You start in the cave named start, and your destination is the cave named end. An entry like b-d means that cave b is connected to cave d - that is, you can move between them.

So, the above cave system looks roughly like this:

    start
    /   \
c--A-----b--d
    \\   /
     end

Your goal is to find the number of distinct paths that start at start, end at end, and don't visit small caves more than once. There are two types of caves: big caves (written in uppercase, like A) and small caves (written in lowercase, like b). It would be a waste of time to visit any small cave more than once, but big caves are large enough that it might be worth visiting them multiple times. So, all paths you find should visit small caves at most once, and can visit big caves any number of times.

Given these rules, there are 10 paths through this example cave system:

start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end

(Each line in the above list corresponds to a single path; the caves visited by that path are listed in the order they are visited and separated by commas.)

Note that in this cave system, cave d is never visited by any path: to do so, cave b would need to be visited twice (once on the way to cave d and a second time when returning from cave d), and since cave b is small, this is not allowed.

Here is a slightly larger example:

dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc

The 19 paths through it are as follows:

start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end

Finally, this even larger example has 226 paths through it:

fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW

How many paths through this cave system are there that visit small caves at most once?
"""
from dataclasses import dataclass, field

import pytest


@dataclass
class Cave:
    name: str
    neighbors: list["Cave"] = field(default_factory=list)

    @property
    def is_big(self) -> bool:
        return self.name.isupper()

    @property
    def is_small(self) -> bool:
        return self.name.islower()

    def __hash__(self):
        return hash(self.name)


def connections_to_caves(connections: list[str]) -> list[Cave]:
    """Return a list of Caves from a list of connections between caves.

    Connections should be in the format '<name>-<name>'.
    """
    caves: dict[str, Cave] = {}
    for connection in connections:
        from_name, to_name = connection.split("-")
        from_ = caves.setdefault(from_name, Cave(from_name))
        to = caves.setdefault(to_name, Cave(to_name))
        from_.neighbors.append(to)
        to.neighbors.append(from_)
    return list(caves.values())


def solve_part_one(connections: list[str]) -> int:
    """Return the number of paths through the cave system that visit small caves at most once."""

    # Convert connections into a set of nodes
    caves = connections_to_caves(connections)
    paths = find_paths(caves)
    return len(paths)


def test_solve_part_one() -> None:
    connections = [
        "fs-end",
        "he-DX",
        "fs-he",
        "start-DX",
        "pj-DX",
        "end-zg",
        "zg-sl",
        "zg-pj",
        "pj-he",
        "RW-he",
        "fs-DX",
        "pj-RW",
        "zg-RW",
        "start-pj",
        "he-WI",
        "zg-he",
        "pj-fs",
        "start-RW",
    ]
    expected = 226
    actual = solve_part_one(connections)
    assert actual == expected


def find_paths(caves: list[Cave]) -> list[str]:
    """Return a list of paths, as a sequence of cave names, through the caves."""
    start = None
    end = None
    for cave in caves:
        if cave.name == "start":
            start = cave
        elif cave.name == "end":
            end = cave
    if not start:
        raise Exception("Start cave could not be found!")
    if not end:
        raise Exception("End cave could not be found!")
    return delve(start, [], set(), end)


def delve(cave: Cave, path: list[str], visited: set[Cave], stop: Cave) -> list[str]:
    """Return a list of paths from the starting cave to the stopping cave."""
    path.append(cave.name)
    if cave == stop:
        return [",".join(path)]
    paths: list[str] = []
    if cave.is_small:
        visited.add(cave)
    for neighbor in cave.neighbors:
        if neighbor not in visited:
            paths.extend(
                delve(cave=neighbor, path=list(path), visited=set(visited), stop=stop)
            )
    return paths


@pytest.mark.parametrize(
    "connections,expected",
    (
        (
            [
                "start-A",
                "start-b",
                "A-c",
                "A-b",
                "b-d",
                "A-end",
                "b-end",
            ],
            [
                "start,A,b,A,c,A,end",
                "start,A,b,A,end",
                "start,A,b,end",
                "start,A,c,A,b,A,end",
                "start,A,c,A,b,end",
                "start,A,c,A,end",
                "start,A,end",
                "start,b,A,c,A,end",
                "start,b,A,end",
                "start,b,end",
            ],
        ),
        (
            [
                "dc-end",
                "HN-start",
                "start-kj",
                "dc-start",
                "dc-HN",
                "LN-dc",
                "HN-end",
                "kj-sa",
                "kj-HN",
                "kj-dc",
            ],
            [
                "start,HN,dc,HN,end",
                "start,HN,dc,HN,kj,HN,end",
                "start,HN,dc,end",
                "start,HN,dc,kj,HN,end",
                "start,HN,end",
                "start,HN,kj,HN,dc,HN,end",
                "start,HN,kj,HN,dc,end",
                "start,HN,kj,HN,end",
                "start,HN,kj,dc,HN,end",
                "start,HN,kj,dc,end",
                "start,dc,HN,end",
                "start,dc,HN,kj,HN,end",
                "start,dc,end",
                "start,dc,kj,HN,end",
                "start,kj,HN,dc,HN,end",
                "start,kj,HN,dc,end",
                "start,kj,HN,end",
                "start,kj,dc,HN,end",
                "start,kj,dc,end",
            ],
        ),
    ),
)
def test_find_paths(connections: list[str], expected: list[str]) -> None:
    caves = connections_to_caves(connections)
    actual = find_paths(caves)
    assert sorted(actual) == sorted(expected)


"""
--- Part Two ---

After reviewing the available paths, you realize you might have time to visit a single small cave twice. Specifically, big caves can be visited any number of times, a single small cave can be visited at most twice, and the remaining small caves can be visited at most once. However, the caves named start and end can only be visited exactly once each: once you leave the start cave, you may not return to it, and once you reach the end cave, the path must end immediately.

Now, the 36 possible paths through the first example above are:

start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end

The slightly larger example above now has 103 paths through it, and the even larger example now has 3509 paths through it.

Given these new rules, how many paths through this cave system are there?
"""


def solve_part_two(connections: list[str]) -> int:
    """Return the number of paths through the caves if one small cave can be visited twice."""
    caves = connections_to_caves(connections)
    paths = find_paths_two(caves)
    return len(paths)


@pytest.mark.parametrize(
    "connections,expected",
    (
        (
            [
                "dc-end",
                "HN-start",
                "start-kj",
                "dc-start",
                "dc-HN",
                "LN-dc",
                "HN-end",
                "kj-sa",
                "kj-HN",
                "kj-dc",
            ],
            103,
        ),
        (
            [
                "fs-end",
                "he-DX",
                "fs-he",
                "start-DX",
                "pj-DX",
                "end-zg",
                "zg-sl",
                "zg-pj",
                "pj-he",
                "RW-he",
                "fs-DX",
                "pj-RW",
                "zg-RW",
                "start-pj",
                "he-WI",
                "zg-he",
                "pj-fs",
                "start-RW",
            ],
            3509,
        ),
    ),
)
def test_solve_part_two(connections: list[str], expected: int) -> None:
    actual = solve_part_two(connections)
    assert actual == expected


def find_paths_two(caves: list[Cave]) -> list[str]:
    """Return a list of paths, as a sequence of cave names, through the caves if one small cave can be visited twice."""
    start = None
    end = None
    for cave in caves:
        if cave.name == "start":
            start = cave
        elif cave.name == "end":
            end = cave
    if not start:
        raise Exception("Start cave could not be found!")
    if not end:
        raise Exception("End cave could not be found!")
    return delve_two(start, [], {}, end)


def test_find_paths_two() -> None:
    connections = [
        "start-A",
        "start-b",
        "A-c",
        "A-b",
        "b-d",
        "A-end",
        "b-end",
    ]
    caves = connections_to_caves(connections)
    expected = [
        "start,A,b,A,b,A,c,A,end",
        "start,A,b,A,b,A,end",
        "start,A,b,A,b,end",
        "start,A,b,A,c,A,b,A,end",
        "start,A,b,A,c,A,b,end",
        "start,A,b,A,c,A,c,A,end",
        "start,A,b,A,c,A,end",
        "start,A,b,A,end",
        "start,A,b,d,b,A,c,A,end",
        "start,A,b,d,b,A,end",
        "start,A,b,d,b,end",
        "start,A,b,end",
        "start,A,c,A,b,A,b,A,end",
        "start,A,c,A,b,A,b,end",
        "start,A,c,A,b,A,c,A,end",
        "start,A,c,A,b,A,end",
        "start,A,c,A,b,d,b,A,end",
        "start,A,c,A,b,d,b,end",
        "start,A,c,A,b,end",
        "start,A,c,A,c,A,b,A,end",
        "start,A,c,A,c,A,b,end",
        "start,A,c,A,c,A,end",
        "start,A,c,A,end",
        "start,A,end",
        "start,b,A,b,A,c,A,end",
        "start,b,A,b,A,end",
        "start,b,A,b,end",
        "start,b,A,c,A,b,A,end",
        "start,b,A,c,A,b,end",
        "start,b,A,c,A,c,A,end",
        "start,b,A,c,A,end",
        "start,b,A,end",
        "start,b,d,b,A,c,A,end",
        "start,b,d,b,A,end",
        "start,b,d,b,end",
        "start,b,end",
    ]
    actual = find_paths_two(caves)
    assert sorted(actual) == sorted(expected)


def delve_two(
    cave: Cave,
    path: list[str],
    visited: dict[Cave, int],
    stop: Cave,
    has_visited_small_cave_twice: bool = False,
) -> list[str]:
    """Return a list of paths from the starting cave to the stopping cave passing through a single small cave twice."""
    path.append(cave.name)
    if cave == stop:
        return [",".join(path)]
    paths: list[str] = []
    if cave.is_small:
        if cave in visited:
            visited[cave] += 1
        else:
            visited[cave] = 1
        if visited[cave] == 2:
            has_visited_small_cave_twice = True
    for neighbor in cave.neighbors:
        if neighbor.name == "start":
            continue
        if neighbor in visited:
            if visited[neighbor] >= 2:
                continue
            if visited[neighbor] == 1 and has_visited_small_cave_twice:
                continue
        paths.extend(
            delve_two(
                cave=neighbor,
                path=list(path),
                visited=dict(visited),
                stop=stop,
                has_visited_small_cave_twice=has_visited_small_cave_twice,
            )
        )
    return paths


if __name__ == "__main__":
    from pathlib import Path

    input_file = Path("./input12.txt")
    with input_file.open() as f:
        connections = [
            line.strip().strip("\n")
            for line in f.readlines()
            if line.strip().strip("\n")
        ]
    print(
        "How many paths through this cave system are there that visit small caves at most once?",
        solve_part_one(connections),
        sep="\n\t",
    )
    print(
        "",
        solve_part_two(connections),
        sep="\n\t",
    )

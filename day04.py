"""
--- Day 4: Giant Squid ---

You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight. What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are marked as follows (shown here adjacent to each other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

At this point, the third board wins because it has at least one complete row or column of marked numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first. What will your final score be if you choose that board?

"""


class Board:
    """Represent a Bingo board."""

    def __init__(self, *numbers: int, size: int = 5):
        self._numbers = set(numbers)
        self._draws: list[int] = []
        self.rows = [set(numbers[size * i : (size * i) + size]) for i in range(size)]
        self.columns = [
            set(number for (idx, number) in enumerate(numbers) if idx % size == i)
            for i in range(size)
        ]

    def mark(self, draw: int) -> None:
        """Mark number drawn on board if present."""
        self._draws.append(draw)
        if draw not in self._numbers:
            return
        self._numbers.remove(draw)
        for row in self.rows:
            if draw in row:
                row.remove(draw)
        for column in self.columns:
            if draw in column:
                column.remove(draw)

    @property
    def has_won(self) -> bool:
        """Return True if this board has won."""
        for row in self.rows:
            if not row:
                return True
        for column in self.columns:
            if not column:
                return True
        return False

    @property
    def score(self) -> int:
        """Return the score of this board."""
        if not self.has_won:
            return 0
        last_draw = self._draws[-1]
        unmarked = self._numbers
        sum_unmarked = sum(number for number in unmarked)
        return last_draw * sum_unmarked


def solve_part_one(draws: list[int], boards: list[Board]) -> int:
    """Return the score of the first board to win."""
    for draw_count, draw in enumerate(draws):
        for board in boards:
            board.mark(draw)
            if draw_count >= 4 and board.has_won:
                return board.score
    raise Exception("Could not solve part one!")


TEST_DRAWS = [
    7,
    4,
    9,
    5,
    11,
    17,
    23,
    2,
    0,
    14,
    21,
    24,
    10,
    16,
    13,
    6,
    15,
    25,
    12,
    22,
    18,
    20,
    8,
    19,
    3,
    26,
    1,
]
TEST_BOARDS = [
    Board(
        22,
        13,
        17,
        11,
        0,
        8,
        2,
        23,
        4,
        24,
        21,
        9,
        14,
        16,
        7,
        6,
        10,
        3,
        18,
        5,
        1,
        12,
        20,
        15,
        19,
    ),
    Board(
        3,
        15,
        0,
        2,
        22,
        9,
        18,
        13,
        17,
        5,
        19,
        8,
        7,
        25,
        23,
        20,
        11,
        10,
        24,
        4,
        14,
        21,
        16,
        12,
        6,
    ),
    Board(
        *[
            int(number)
            for number in """
14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""".replace(
                "\n", " "
            ).split(
                " "
            )
            if number
        ]
    ),
]


def test_solve_part_one() -> None:
    expected = 4512
    actual = solve_part_one(TEST_DRAWS, TEST_BOARDS)
    assert actual == expected


"""
--- Part Two ---

On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?

"""


def solve_part_two(draws: list[int], boards: list[Board]) -> int:
    """Return the score of the last board to win."""
    candidates = list(boards)
    for draw in draws:
        next_candidates: list[Board] = []
        for candidate in candidates:
            candidate.mark(draw)
            if not candidate.has_won:
                next_candidates.append(candidate)
        if not next_candidates:
            return candidates[-1].score
        candidates = next_candidates
    raise Exception("Could not solve part two!")


def test_solve_part_two() -> None:
    expected = 1924
    actual = solve_part_two(TEST_DRAWS, TEST_BOARDS)
    assert actual == expected


if __name__ == "__main__":
    from pathlib import Path

    input_file = Path("./input04.txt")
    with input_file.open() as f:
        boards: list[Board] = []
        board_numbers: list[int] = []
        draws = []
        for idx, line in enumerate(line.strip("\n") for line in f.readlines()):
            if idx == 0:
                draws = [int(draw) for draw in line.split(",")]
            elif not line and idx > 1:
                boards.append(Board(*board_numbers))
                board_numbers = []
            else:
                board_numbers.extend(
                    [int(number) for number in line.split(" ") if number]
                )
    print(
        "What is the final score of the board that will win first?",
        solve_part_one(draws, boards),
        sep="\n\t",
    )
    print(
        "Figure out which board will win last. Once it wins, what would its final score be?",
        solve_part_two(draws, boards),
        sep="\n\t",
    )

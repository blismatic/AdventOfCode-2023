from aocd import get_data
from credentials import session

from typing import Literal
from pprint import pprint
import re

example_input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

# example_input = """..#
# OO.
# .OO"""


def parse(puzzle_input):
    """Parse input."""
    print(puzzle_input)
    print()
    result = puzzle_input.split("\n")
    print()
    return result


def tilt(
    dish: list[str], direction: Literal["North", "South", "East", "West"]
) -> list[str]:
    """Helper function to simulate tilting the dish in a specific direction."""
    if direction != "North":
        raise NotImplementedError

    dish_columns = swap_rows_columns(dish)
    print(repr(dish_columns))
    print()
    new_columns = []
    for _, column in enumerate(dish_columns):
        new_column = []
        groups = re.findall(r"[^#]+|#+", column)
        print(_, groups)


def swap_rows_columns(input_list: list) -> list:
    """Helper function to swap the rows and columns of a list."""
    columns = zip(*input_list)
    result = ["".join(e) for e in columns]
    return result


def part1(data):
    """Solve part 1."""
    pass


def part2(data):
    """Solve part 2."""
    pass


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    print(tilt(data, "North"))
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    solutions = solve(example_input)
    puzzle_input = get_data(day=14, year=2023, session=session)
    # solutions = solve(puzzle_input)

    # print("\n".join(str(solution) for solution in solutions))

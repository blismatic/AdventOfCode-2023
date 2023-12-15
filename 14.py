from aocd import get_data
from credentials import session

from typing import Literal
import re
from collections import Counter

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


def parse(puzzle_input):
    """Parse input."""
    # print(puzzle_input)
    # print()
    result = puzzle_input.split("\n")
    return result


def tilt(
    dish: list[str], direction: Literal["North", "South", "East", "West"]
) -> list[str]:
    """Helper function to simulate tilting the dish in a specific direction."""
    """
         -- NORTH TILT --       |       -- WEST TILT --       |       -- SOUTH TILT --        |       -- EAST TILT --
    O....#....      OOOO.#.O..  |  OOOO.#.O..      OOOO.#O...  |  OOOO.#O...      .....#....  |  .....#....      .....#....
    O.OO#....#      OO..#....#  |  OO..#....#      OO..#....#  |  OO..#....#      ....#.O..#  |  ....#.O..#      ....#...O#
    .....##...      OO..O##..O  |  OO..O##..O      OOO..##O..  |  OOO..##O..      O..O.##...  |  O..O.##...      ...OO##...
    OO.#O....O      O..#.OO...  |  O..#.OO...      O..#OO....  |  O..#OO....      O.O#......  |  O.O#......      .OO#......
    .O.....O#.      ........#.  |  ........#.      ........#.  |  ........#.      O.O....O#.  |  O.O....O#.      .....OOO#.
    O.#..O.#.#  ->  ..#....#.#  |  ..#....#.#  ->  ..#....#.#  |  ..#....#.#  ->  O.#..O.#.#  |  O.#..O.#.#  ->  .O#...O#.#
    ..O..#O..O      ..O..#.O.O  |  ..O..#.O.O      O....#OO..  |  O....#OO..      O....#....  |  O....#....      ....O#....
    .......O..      ..O.......  |  ..O.......      O.........  |  O.........      OO....OO..  |  OO....OO..      ......OOOO
    #....###..      #....###..  |  #....###..      #....###..  |  #....###..      #O...###..  |  #O...###..      #...O###..
    #OO..#....      #....#....  |  #....#....      #....#....  |  #....#....      #O..O#....  |  #O..O#....      #..OO#....
    """
    if direction in ["North", "South"]:
        # Rotate the dish so that each "row" is really a single column from the original dish
        rotated_dish = swap_rows_columns(dish)
        if direction == "North":
            rotated_dish = tilt(rotated_dish, "West")
        elif direction == "South":
            rotated_dish = tilt(rotated_dish, "East")
        return swap_rows_columns(rotated_dish)
    elif direction in ["East", "West"]:
        new_rows = []
        for row in dish:
            new_row = []
            groups = re.findall(r"[^#]+|#+", row)
            for group in groups:
                if any([char == "#" for char in group]):
                    new_row.append(group)
                c = Counter(group)
                new_group = ""
                if direction == "East":
                    # Since we are tilting to the east, we want to process O's last so that they "pile up" on the right
                    if "." in c:
                        new_group += "." * c["."]
                    if "O" in c:
                        new_group += "O" * c["O"]
                elif direction == "West":
                    # Since we are tilting to the west, we want to process O's first so tha they "pile up" on the left
                    if "O" in c:
                        new_group += "O" * c["O"]
                    if "." in c:
                        new_group += "." * c["."]
                new_row.append(new_group)
            new_rows.append("".join(new_row))
        return new_rows
    else:
        raise ValueError


def swap_rows_columns(input_list: list) -> list:
    """Helper function to swap the rows and columns of a list.
    ["abc",      ["aaa",
     "abc",  ->   "bbb",
     "abc"]       "ccc"]
    """
    columns = zip(*input_list)
    result = ["".join(e) for e in columns]
    return result


def calculate_total_load(dish: list[str]) -> int:
    """Helper function to calculate the total load of a given dish layout."""
    total_load = 0
    for idx, row in enumerate(dish, start=1):
        rank = len(dish) + 1 - idx
        c = Counter(row)
        if "O" in c:
            total_load += c["O"] * rank
    return total_load


def cycle(data: list[str]) -> list[str]:
    """Helper function to perform a single spin cycle."""
    data = tilt(data, "North")
    data = tilt(data, "West")
    data = tilt(data, "South")
    data = tilt(data, "East")
    return data


def part1(data):
    """Solve part 1."""
    dish = tilt(data, "North")
    return calculate_total_load(dish)


def part2(data):
    """Solve part 2."""
    iteration = 0
    hashmap = {iteration: data}

    # Keep performing cycles and adding the resulting layout to a hashmap until a loop has been detected
    while True:
        data = cycle(data)
        iteration += 1

        if data in hashmap.values():
            break

        hashmap[iteration] = data

    # Find the iteration of the original layout that the loop matches up with
    for key, value in hashmap.items():
        if value == data:
            loop_beginning = key

    # Calculate how many spin cycles it takes to perform a loop
    loop_distance = iteration - loop_beginning

    # How far from the start of the loop do we have to move, to get to the layout that our target would be?
    target = 1_000_000_000
    answer_offset = (target - loop_beginning) % loop_distance

    answer_iteration = loop_beginning + answer_offset
    layout_after_target_cycles = hashmap[answer_iteration]

    return calculate_total_load(layout_after_target_cycles)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    # solutions = solve(example_input)
    puzzle_input = get_data(day=14, year=2023, session=session)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

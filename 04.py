from aocd import get_data
from credentials import session

from pprint import pprint

example_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def parse(puzzle_input):
    """Parse input."""
    result = {}
    puzzle_input = puzzle_input.split("\n")
    for card in puzzle_input:
        metadata, numbers = card.split(": ")
        card_num = int(metadata.split(" ")[-1])
        winning_numbers, my_numbers = numbers.split(" | ")
        winning_numbers = [int(n) for n in winning_numbers.split(" ") if n]
        my_numbers = [int(n) for n in my_numbers.split(" ") if n]

        result.update(
            {card_num: {"winning_numbers": winning_numbers, "my_numbers": my_numbers}}
        )
    return result


def part1(data):
    """Solve part 1."""

    def value(winning_numbers: list[int], my_numbers: list[int]):
        """Helper function get the value of a scratchcard."""
        matches = 0
        for num in my_numbers:
            if num in winning_numbers:
                matches += 1

        if matches == 0:
            return 0
        else:
            return 2 ** (matches - 1)

    card_values = [
        value(data[card]["winning_numbers"], data[card]["my_numbers"]) for card in data
    ]
    return sum(card_values)


def part2(data):
    """Solve part 2."""
    pass


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    # solutions = solve(example_input)
    puzzle_input = get_data(day=4, year=2023, session=session)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

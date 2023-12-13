from aocd import get_data
from credentials import session

from pprint import pprint
from itertools import product

example_input = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def parse(puzzle_input):
    """Parse input."""
    # print(puzzle_input)
    # print()
    lines = puzzle_input.split("\n")
    result = []
    for line in lines:
        row, sizes = line.split(" ")
        damaged_springs = [int(n) for n in sizes.split(",")]
        result.append((row, damaged_springs))
    return result


def different_arrangements(record: str, sizes: list[int]) -> int:
    """Helper function that returns the number of different arrangements for a given record and sizes"""
    num_question_marks = record.count("?")
    combinations = product(".#", repeat=num_question_marks)

    # Get a list of strings for every possible combination
    possible_strings = []
    for combo in combinations:
        curr = iter(combo)
        replaced_string = "".join(
            char if char != "?" else next(curr) for char in record
        )
        possible_strings.append(replaced_string)

    # For each possible combination, check if it would make sense given the `sizes` constraint
    valid_amount = 0
    for possible_string in possible_strings:
        groupings = [e for e in possible_string.split(".") if e != ""]
        groupings_sizes = [len(e) for e in groupings]
        if groupings_sizes == sizes:
            valid_amount += 1
    return valid_amount


def part1(data):
    """Solve part 1."""
    arrangements = [different_arrangements(record, sizes) for record, sizes in data]
    return sum(arrangements)


def part2(data):
    """Solve part 2."""

    def unfold(record: str, sizes: list[int], copies: int = 5) -> tuple():
        """Helper function to unfold a condition record"""
        new_record = ""
        new_sizes = []
        for _ in range(copies):
            new_record += record + "?"
            new_sizes.extend(sizes)
        new_record = new_record[:-1]
        return new_record, new_sizes

    unfolded_data = [unfold(record, sizes) for record, sizes in data]
    part1(unfolded_data)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    # solution1 = part1(data)
    solution1 = None
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    solutions = solve(example_input)
    puzzle_input = get_data(day=12, year=2023, session=session)
    # solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

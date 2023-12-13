from aocd import get_data
from credentials import session

from pprint import pprint
from itertools import product
from functools import cache

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
        damaged_springs = tuple(int(n) for n in sizes.split(","))
        result.append([row, damaged_springs])
    # for _ in result:
    #     row, springs = _
    #     print(repr(row), repr(springs))
    return result


@cache
def different_arrangements_2(record: str, sizes: tuple[int]) -> int:
    # Base-case logic will go here
    if not sizes:
        if "#" not in record:
            return 1
        else:
            return 0

    if not record:
        return 0

    # Look at the next element in each record and size
    next_char = record[0]
    next_size = sizes[0]

    # Logic that treats the first character as pound-sign '#'
    def pound():
        # ... need to process this character and call different_arrangements_2 on a substring
        # If the first character is a pound, then the first n characters must be pounds, where n is the first size
        this_size = record[:next_size]
        this_size = this_size.replace("?", "#")

        # If the next size can't fit all the damaged springs, then abort
        if this_size != next_size * "#":
            return 0

        # If the rest of the record is just the last size, then we're done and there's only one possibility
        if len(record) == next_size:
            # Make sure this is the last sizes
            if len(sizes) == 1:
                # We are valid
                return 1
            else:
                # There's more sizes, we can't make it work
                return 0

        # Make sure the character that follows this size can be a separator
        if record[next_size] in "?.":
            # It *can* be a separator, so skip it and reduce to the next group
            return different_arrangements_2(record[next_size + 1 :], sizes[1:])

        # Can't be handled, there are no possibilities
        return 0

    def dot():
        # ... need to process this character and call different_arrangements_2 on a substring
        return different_arrangements_2(record[1:], sizes)

    if next_char == "#":
        # Test pound logic
        out = pound()
    elif next_char == ".":
        # Test dot logic
        out = dot()
    elif next_char == "?":
        # This character could be either character, so we'll explore both possibilities
        out = dot() + pound()
    else:
        raise RuntimeError

    # Help with debugging
    print(record, sizes, "->", out)
    return out


# def different_arrangements(record: str, sizes: tuple[int]) -> int:
#     """Helper function that returns the number of different arrangements for a given record and sizes"""
#     num_question_marks = record.count("?")
#     combinations = product(".#", repeat=num_question_marks)

#     # Get a list of strings for every possible combination
#     possible_strings = []
#     for combo in combinations:
#         curr = iter(combo)
#         replaced_string = "".join(
#             char if char != "?" else next(curr) for char in record
#         )
#         possible_strings.append(replaced_string)

#     # For each possible combination, check if it would make sense given the `sizes` constraint
#     valid_amount = 0
#     for possible_string in possible_strings:
#         groupings = [e for e in possible_string.split(".") if e != ""]
#         groupings_sizes = tuple(len(e) for e in groupings)
#         if groupings_sizes == sizes:
#             valid_amount += 1
#     return valid_amount


print(different_arrangements_2(record="???.###", sizes=(1, 1, 3)))
print()


def part1(data):
    """Solve part 1."""
    arrangements = [different_arrangements_2(record, sizes) for record, sizes in data]
    return sum(arrangements)


def part2(data):
    """Solve part 2."""

    def unfold(record: str, sizes: tuple[int], copies: int = 5) -> tuple():
        """Helper function to unfold a condition record"""
        new_record = ""
        new_sizes = []
        for _ in range(copies):
            new_record += record + "?"
            new_sizes.extend(sizes)
        new_record = new_record[:-1]
        new_sizes = tuple(new_sizes)
        return new_record, tuple(new_sizes)

    unfolded_data = [unfold(record, sizes) for record, sizes in data]
    return part1(unfolded_data)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution2 = None
    solution1 = None
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    # solutions = solve(example_input)
    puzzle_input = get_data(day=12, year=2023, session=session)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

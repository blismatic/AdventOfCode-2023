from aocd import get_data
from credentials import session

import re

def parse(puzzle_input):
    """Parse input."""
    # print(puzzle_input)
    result = puzzle_input.split("\n")
    return result

def part1(data):
    """Solve part 1."""
    sum = 0
    for line in data:
        nums = [c for c in line if c.isnumeric()]
        first, last = nums[0], nums[-1]
        calibration_value = int(first + last)
        sum += calibration_value
    return sum

def part2(data):
    """Solve part 2."""
    sum = 0
    word_to_integer = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9"
    }
    for line in data:
        nums = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)
        nums = [word_to_integer[e] if e in word_to_integer else e for e in nums]
        first, last = nums[0], nums[-1]
        calibration_value = int(first + last)
        sum += calibration_value
    return sum

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)
    
    return solution1, solution2

if __name__ == "__main__":
    puzzle_input = get_data(day=1, year=2023, session=session)
    solutions = solve(puzzle_input)
    
    print("\n".join(str(solution) for solution in solutions))
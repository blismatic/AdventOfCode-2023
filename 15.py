from aocd import get_data
from credentials import session

from pprint import pprint
import re
from collections import defaultdict, deque

example_input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


def parse(puzzle_input):
    """Parse input."""
    print(puzzle_input)
    print()
    result = re.findall(r"(\w+)([=-])(\d+)?", puzzle_input)
    return result


def hash(s: str) -> int:
    """Helper function to generate the hash value of a given string"""
    curr_value = 0
    for char in s:
        ascii_code = ord(char)
        curr_value += ascii_code
        curr_value *= 17
        curr_value = curr_value % 256
    return curr_value


def view_boxes(hashmap: dict) -> None:
    """Helper function to display any filled boxes from a dictionary. Used in part 2"""
    for box_num in hashmap:
        contents = " ".join(
            [f"[{label} {focal_length}]" for label, focal_length in hashmap[box_num]]
        )
        print(f"Box {box_num}: {contents}")


def focusing_power(box_num: int, slot: int, focal_length: int) -> int:
    """Helper function to calculate the focusing power of a particular lens"""
    fp = (1 + box_num) * slot * focal_length
    return fp


def part1(data):
    """Solve part 1."""
    steps = ["".join(t) for t in data]
    results = [hash(step) for step in steps]
    return sum(results)


def part2(data):
    """Solve part 2."""
    hashmap = defaultdict(deque)

    for step in data:
        label, operation, focal_length = step
        lens = (label, focal_length)
        box_num = hash(label)
        box = hashmap[box_num]

        if operation == "=":
            try:
                pos = next((i for i, tpl in enumerate(box) if tpl[0] == label))
                box.rotate(-pos)
                box.popleft()
                box.appendleft(lens)
                box.rotate(pos)
            except StopIteration:
                box.append(lens)
        elif operation == "-":
            try:
                pos = next((i for i, tpl in enumerate(box) if tpl[0] == label))
                box.rotate(-pos)
                box.popleft()
                if len(box) == 0:
                    del hashmap[box_num]
                    continue
                box.rotate(pos)
            except StopIteration:
                pass

        # print(f'After "{label}{operation}{focal_length}":')
        # view_boxes(hashmap)
        # print()

    total_focusing_power = 0
    for box_num in hashmap:
        box = hashmap[box_num]
        for slot, lens in enumerate(box, start=1):
            focal_length = int(lens[1])
            total_focusing_power += focusing_power(box_num, slot, focal_length)
    return total_focusing_power


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    # solutions = solve(example_input)
    puzzle_input = get_data(day=15, year=2023, session=session)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

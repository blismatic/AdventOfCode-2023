from aocd import get_data
from credentials import session

from pprint import pprint
from shapely.geometry import Polygon

example_input = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""


def parse(puzzle_input):
    """Parse input."""
    # print(puzzle_input)
    # print()
    lines = puzzle_input.split("\n")
    dig_plan = []
    for line in lines:
        direction, meters, color_code = line.split(" ")
        dig_plan.append((direction, int(meters), color_code[2:-1]))
    return dig_plan


def perimeter(vertices: list[tuple[int]]) -> int:
    """Helper function to calculate the perimiter of a shape given a list of vertices."""
    total = 0
    n = len(vertices)
    for i in range(n - 1):
        curr = vertices[i]
        next = vertices[i + 1]

        x1, y1 = curr
        x2, y2 = next

        if x2 == x1:
            # x coordinates stayed the same, must be moving vertically.
            total += abs(y2 - y1)
        elif y2 == y1:
            # y coordinates stayed the same, must be moving horizontally.
            total += abs(x2 - x1)
    return total


def part1(data):
    """Solve part 1."""
    curr_x = 0
    curr_y = 0
    dig_site = [(curr_x, curr_y)]
    for instruction in data:
        direction, meters, _ = instruction
        if direction == "U":
            curr_y += meters
        elif direction == "D":
            curr_y -= meters
        elif direction == "L":
            curr_x -= meters
        elif direction == "R":
            curr_x += meters
        dig_site.append((curr_x, curr_y))

    perim = perimeter(dig_site)
    inside_area = Polygon(dig_site).area

    # Pick's theorem
    return int(inside_area + (perim / 2) - 1)


def part2(data):
    """Solve part 2."""
    new_data = []
    for instruction in data:
        color_code = instruction[2]

        distance_in_meters = int(color_code[:5], 16)
        last_digit = int(color_code[-1])
        if last_digit == 0:
            direction = "R"
        elif last_digit == 1:
            direction = "D"
        elif last_digit == 2:
            direction = "L"
        elif last_digit == 3:
            direction = "U"

        # We include None in the tuple because part1 expects a list of 3-tuples
        new_data.append((direction, distance_in_meters, None))

    return part1(new_data)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    # solutions = solve(example_input)
    puzzle_input = get_data(day=18, year=2023, session=session)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

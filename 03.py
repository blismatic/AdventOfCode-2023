from aocd import get_data
from credentials import session

from functools import reduce


def parse(puzzle_input):
    """Parse input."""
    engine_schematic = puzzle_input.split("\n")

    number_data = []
    for y, row in enumerate(engine_schematic):
        temp = {"num": "", "coords": []}
        for x, col in enumerate(row):
            if col.isnumeric():
                temp["num"] += col
                temp["coords"].append((y, x))
                if (
                    x == len(row) - 1 and temp["num"]
                ):  # Edge case where number ends on the right edge
                    number_data.append(temp)
            else:
                if temp["num"]:
                    number_data.append(temp)
                temp = {"num": "", "coords": []}

    return {"engine_schematic": engine_schematic, "number_data": number_data}


def get_adjacent_coords(num: dict) -> list[tuple]:
    """Generates a list of 2-tuples, representing the y,x coordinates of each point surrounding a number."""
    coords = num["coords"]
    complete_adjacent_coords = []
    for _, coordinate in enumerate(coords):
        y, x = coordinate
        adjacent_coords = []
        n = (y - 1, x)
        s = (y + 1, x)
        adjacent_coords.extend([n, s])
        if _ == 0:  # First number
            nw = (y - 1, x - 1)
            w = (y, x - 1)
            sw = (y + 1, x - 1)
            adjacent_coords.extend([nw, w, sw])
        if (
            _ == len(coords) - 1 or len(coords) == 1
        ):  # Last number (or a 1-digit number)
            ne = (y - 1, x + 1)
            e = (y, x + 1)
            se = (y + 1, x + 1)
            adjacent_coords.extend([ne, e, se])
        complete_adjacent_coords.extend(adjacent_coords)
    return complete_adjacent_coords


def is_symbol(y: int, x: int, schematic: list) -> bool:
    """Checks if the provided y,x coordinate in a schematic is a symbol or not."""
    try:
        if schematic[y][x].isnumeric() or schematic[y][x] == ".":
            return False
        return True
    except IndexError:
        return False


def part1(data):
    """Solve part 1."""
    part_nums = []
    for num in data["number_data"]:
        adjacent_coords = get_adjacent_coords(num)
        for adjacent_coord in adjacent_coords:
            y, x = adjacent_coord
            if is_symbol(y, x, data["engine_schematic"]):
                part_nums.append(num["num"])
                continue

    return sum([int(part_num) for part_num in part_nums])


def part2(data):
    """Solve part 2."""

    # General thought process:
    # Make a dictionary where the:
    # - key is a 2-tuple of (y,x) coordinates for each gear (* symbol)
    # - value for each key is a list, where each element is a number connecting to that gear (* symbol)
    #
    # Initialize an empty list to keep track of valid gear ratios.
    # Loop through the dictionary looking at the value for each key. If the length of a value is exactly 2, multiply the 2 elements and append the result to the list of valid gear ratios.
    # Return the sum of the valid_gear_ratios list.

    def gear_ratio(part_numbers: list[str]) -> int:
        """Helper function to calculate a gear's gear ratio"""
        if len(part_numbers) != 2:
            return 0  # Since we are summing all the gear ratios, we can just return 0 for anything that doesn't fit the criteria
        return reduce(
            (lambda x, y: x * y), [int(part_num) for part_num in part_numbers]
        )

    def create_gear_dict(schematic: list[str], number_data: list[dict]) -> dict:
        """Helper function to create a dictionary of gear coordinates, and the part numbers attached to those gears."""
        master_dictionary = {}
        for num_object in number_data:
            adjacent_coords = get_adjacent_coords(num_object)
            for adjacent_coord in adjacent_coords:
                y, x = adjacent_coord
                if is_symbol(y, x, schematic) and schematic[y][x] == "*":
                    if adjacent_coord not in master_dictionary:
                        # If this gear has not been seen before, the value for it in the dictionary should be a list so that we can call .append() any other time we see the same gear.
                        master_dictionary.update({adjacent_coord: [num_object["num"]]})
                    else:
                        master_dictionary[adjacent_coord].append(num_object["num"])
        return master_dictionary

    gear_dictionary = create_gear_dict(data["engine_schematic"], data["number_data"])
    gear_ratios = [gear_ratio(part_nums) for part_nums in gear_dictionary.values()]
    return sum(gear_ratios)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    puzzle_input = get_data(day=3, year=2023, session=session)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

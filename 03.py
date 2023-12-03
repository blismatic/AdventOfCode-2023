from aocd import get_data
from credentials import session


def parse(puzzle_input):
    """Parse input."""
    print(puzzle_input)
    print()
    engine_schematic = puzzle_input.split("\n")

    number_data = []
    for y, row in enumerate(engine_schematic):
        temp = {"num": "", "coords": []}
        for x, col in enumerate(row):
            if col.isnumeric():
                temp["num"] += col
                temp["coords"].append((y, x))
            else:
                if temp["num"]:
                    number_data.append(temp)
                temp = {"num": "", "coords": []}

    # for num in number_data[18:21]:
    # print(num)
    return {"engine_schematic": engine_schematic, "number_data": number_data}


def part1(data):
    """Solve part 1."""

    def get_adjacent_coords(num: dict) -> list[tuple]:
        """Generates a list of 2-tuples, representing the y,x coordinates of each point surrounding a number."""
        coords = num["coords"]
        # print(coords)
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

    # print()
    # print(data["number_data"][20], get_adjacent_coords(data["number_data"][20]))

    part_nums = []
    for num in data["number_data"]:
        adjacent_coords = get_adjacent_coords(num)
        for adjacent_coord in adjacent_coords:
            y, x = adjacent_coord
            if is_symbol(y, x, data["engine_schematic"]):
                part_nums.append(num["num"])
                continue

    print(part_nums[:30])
    return sum([int(part_num) for part_num in part_nums])


def part2(data):
    """Solve part 2."""
    pass


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    test_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    # data = parse(test_input)
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    puzzle_input = get_data(day=3, year=2023, session=session)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

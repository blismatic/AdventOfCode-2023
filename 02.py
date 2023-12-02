from aocd import get_data
from credentials import session


def parse(puzzle_input):
    """Parse input."""
    result = puzzle_input.split("\n")

    games = []
    for game in result:
        game_info = {}

        title, information = game.split(": ")
        id_number = title.split(" ")[1]
        game_info["id"] = id_number

        rounds = [s.split(", ") for s in information.split("; ")]
        rounds_info = []

        for round in rounds:
            single_round_info = {}
            for cube_type in round:
                amount, color = cube_type.split(" ")
                single_round_info[color] = amount

            rounds_info.append(single_round_info)

        game_info["rounds"] = rounds_info
        games.append(game_info)

    return games


def part1(data):
    """Solve part 1."""

    def is_possible(game: dict, constraints: dict) -> bool:
        for round in game["rounds"]:
            for cube_type in round:
                if int(round[cube_type]) > constraints[cube_type]:
                    return False
        return True

    # If bag loaded with 12 red, 13 green, and 14 blue...
    constraints = {"red": 12, "green": 13, "blue": 14}
    possible_games = [game for game in data if is_possible(game, constraints)]

    return sum([int(game["id"]) for game in possible_games])


def part2(data):
    """Solve part 2."""

    def fewest_cubes(game: dict) -> dict:
        minimums = {"red": 0, "green": 0, "blue": 0}
        for round in game["rounds"]:
            for cube_color in round:
                amt = int(round[cube_color])
                if amt > minimums[cube_color]:
                    minimums[cube_color] = amt
        return minimums

    def power(minimums: dict) -> int:
        red = minimums["red"]
        green = minimums["green"]
        blue = minimums["blue"]

        return red * green * blue

    powers = [power(fewest_cubes(game)) for game in data]
    return sum(powers)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    puzzle_input = get_data(day=2, year=2023, session=session)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

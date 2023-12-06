from aocd import get_data
from credentials import session

from pprint import pprint

example_input = """Time:      7  15   30
Distance:  9  40  200"""


def parse(puzzle_input):
    """Parse input."""
    print(puzzle_input)
    print()
    races = []
    time_line, distance_line = puzzle_input.split("\n")
    times = [e for e in time_line.split(": ")[1].split(" ") if e]
    distances = [e for e in distance_line.split(": ")[1].split(" ") if e]
    # print(times)
    # print(distances)
    for time, distance in zip(times, distances):
        races.append((int(time), int(distance)))
    # pprint(races)
    return races


def ways_to_win(time: int, distance_to_beat: int) -> int:
    """Helper function that returns the number of ways to win a given race"""
    total = 0
    for hold in range(1, time):
        speed = hold
        travel_time = time - hold
        distance = speed * travel_time

        if distance > distance_to_beat:
            total += 1
    return total


def part1(data):
    """Solve part 1."""
    race_win_data = [ways_to_win(time, distance) for time, distance in data]
    result = 1
    for win_data in race_win_data:
        result *= win_data
    return result


def part2(data):
    """Solve part 2."""
    actual_time = int("".join([str(time) for time, _ in data]))
    actual_distance = int("".join([str(distance) for _, distance in data]))

    return ways_to_win(actual_time, actual_distance)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    # solutions = solve(example_input)
    puzzle_input = get_data(day=6, year=2023, session=session)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

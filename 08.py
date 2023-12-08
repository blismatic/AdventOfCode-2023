from aocd import get_data
from credentials import session

from pprint import pprint
from math import lcm


example_input = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

example_input_2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

example_input_3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def parse(puzzle_input):
    """Parse input."""
    print(puzzle_input)
    print()
    instructions, nodes = puzzle_input.split("\n\n")
    nodes = nodes.split("\n")

    network = {}
    for node in nodes:
        value, children = node.split(" = ")
        left, right = children.split(", ")
        left = left[1:]
        right = right[:-1]

        network[value] = (left, right)
    return instructions, network


def part1(data):
    """Solve part 1."""
    instructions, network = data
    current_node = "AAA"
    steps = 0

    while current_node != "ZZZ":
        instruction = instructions[steps % len(instructions)]

        if instruction == "L":
            current_node = network[current_node][0]
        elif instruction == "R":
            current_node = network[current_node][1]

        steps += 1
    return steps


def part2(data):
    """Solve part 2."""
    instructions, network = data
    current_nodes = [node for node in network.keys() if node.endswith("A")]
    steps = 0
    intervals = [None] * len(current_nodes)

    while not all(i for i in intervals):
        # The first time each starting node reaches a node ending with a "Z", record that amount of steps.
        for idx, node in enumerate(current_nodes):
            if node.endswith("Z") and not intervals[idx]:
                intervals[idx] = steps

        instruction = instructions[steps % len(instructions)]

        if instruction == "L":
            current_nodes = [network[node][0] for node in current_nodes]
        elif instruction == "R":
            current_nodes = [network[node][1] for node in current_nodes]

        steps += 1

    # After every starting node's "interval" has been found, the least common multiple of them all will be when they all line up simultaneously.
    return lcm(*intervals)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    # solutions = solve(example_input)
    puzzle_input = get_data(day=8, year=2023, session=session)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

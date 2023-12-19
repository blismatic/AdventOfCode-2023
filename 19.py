from aocd import get_data
from credentials import session

from pprint import pprint
import re

example_input = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""


def parse(puzzle_input):
    """Parse input."""
    # print(puzzle_input)
    # print()
    workflows, part_ratings = puzzle_input.split("\n\n")
    workflows = workflows.split("\n")
    part_ratings = part_ratings.split("\n")

    # Construct a dictionary to contain the workflows, where:
    # key = name of the workflow.
    # value = list of 4-tuples, containing the attribute to look at, the comparison operator, the number to compare against, and the workflow it should be sent to.
    formatted_workflows = {}
    for raw_workflow in workflows:
        x = re.match(r"([a-zA-Z]+){(.+)}", raw_workflow)

        name = x.group(1)
        raw_rules = x.group(2).split(",")

        rules = []
        for rule in raw_rules[:-1]:
            components = re.findall(r"([a-zA-Z]+)|([<>])|(\d+)|([a-zA-Z]+)", rule)
            result = [
                match
                for group in components
                if (match := next(filter(None, group), None))
            ]
            result[2] = int(result[2])
            rules.append(tuple(result))
        final_dest = raw_rules[-1]
        rules.append((None, None, None, final_dest))

        formatted_workflows[name] = rules

    # Construct a list of dicts, where each dict is a single part split into it's x, m, a, and s attributes
    formatted_parts = []
    for part in part_ratings:
        part = part[1:-1].split(",")
        temp_part = {}
        for category in part:
            attribute, rating = category.split("=")
            temp_part[attribute] = int(rating)
        formatted_parts.append(temp_part)

    return formatted_workflows, formatted_parts


def output_of_workflow(part: dict, workflow: list[tuple]) -> str:
    """Helper function that takes a part and runs it through a single workflow, and outputs where that part should go next."""
    for idx, rule in enumerate(workflow):
        attribute, operator, num, destination = rule

        # If we are at the last rule in the workflow, just return the destination
        if idx == len(workflow) - 1:
            return destination

        if operator == ">":
            comparison = part[attribute] > num
        elif operator == "<":
            comparison = part[attribute] < num

        if comparison:
            return destination


def part_value(part: dict) -> int:
    """Helper function to sum up the x, m, a, and s rating of a given part."""
    return sum(part.values())


def part1(data):
    """Solve part 1."""
    workflows, parts = data

    # Get a list of all the accepted parts
    accepted_parts = []
    for part in parts:
        destination = "in"
        while not (destination == "A" or destination == "R"):
            destination = output_of_workflow(part, workflows[destination])

        if destination == "A":
            accepted_parts.append(part)

    # Return the sum of all of the accepted parts ratings
    return sum([part_value(p) for p in accepted_parts])


def part2(data):
    """Solve part 2."""


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    solutions = solve(example_input)
    puzzle_input = get_data(day=19, year=2023, session=session)
    # solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

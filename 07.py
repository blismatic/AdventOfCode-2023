from aocd import get_data
from credentials import session

from pprint import pprint
from collections import Counter

example_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def parse(puzzle_input):
    """Parse input."""
    print(puzzle_input)
    print()
    result = puzzle_input.split("\n")
    result = [tuple(e.split(" ")) for e in result]
    return result


def part1(data):
    """Solve part 1."""
    card_values = {
        "A": "14",
        "K": "13",
        "Q": "12",
        "J": "11",
        "T": "10",
        "9": "09",
        "8": "08",
        "7": "07",
        "6": "06",
        "5": "05",
        "4": "04",
        "3": "03",
        "2": "02",
    }

    def get_value(hand):
        counter = Counter(hand)
        unique_cards = set(hand)

        value = ""

        # Five of a kind
        if 5 in counter.values():
            value += "7"
        # Four of a kind
        elif 4 in counter.values():
            value += "6"
        # Full house
        elif 3 in counter.values() and 2 in counter.values():
            value += "5"
        # Three of a kind
        elif 3 in counter.values():
            value += "4"
        # Two pair
        elif len(unique_cards) == 3 and 2 in counter.values():
            value += "3"
        # One pair
        elif len(unique_cards) == 4:
            value += "2"
        # High card
        else:
            value += "1"

        for card in hand:
            value += card_values[card]

        return int(value)

    weakest_to_strongest_hands = sorted(data, key=lambda x: get_value(x[0]))
    total_winnings = 0

    for rank, hand_and_bid in enumerate(weakest_to_strongest_hands, start=1):
        hand, bid = hand_and_bid
        total_winnings += rank * int(bid)
    return total_winnings


def part2(data):
    """Solve part 2."""
    card_values = {
        "A": "14",
        "K": "13",
        "Q": "12",
        "T": "10",
        "9": "09",
        "8": "08",
        "7": "07",
        "6": "06",
        "5": "05",
        "4": "04",
        "3": "03",
        "2": "02",
        "J": "01",
    }


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    # solutions = solve(example_input)
    puzzle_input = get_data(day=7, year=2023, session=session)
    solutions = solve(puzzle_input)

    print("\n".join(str(solution) for solution in solutions))

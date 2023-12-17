"""Solution to the day 9 of Advent of Code"""

import argparse
import re
from typing import Callable, Literal

__author__ = "Wojtek Junior"

INPUT = "input.txt"
PART = Literal[1, 2]

NUMBER = re.compile(r"-*\d+")

parser = argparse.ArgumentParser(description="Part of the daily problem")
parser.add_argument(
    "-p",
    "--part",
    default=1,
    type=int,
    help="Part of the daily problem - 1 or 2",
)

OPERATION = Callable[[list[int], int], int]


def get_difference(numbers: list[int]) -> list[int]:
    """
    Returns a difference between consecutive numbers in a list in reverse.
    Output is the list of len(numbers) - 1 length.

    Parameters
    ----------
    numbers : list[int]
        List of numbers to calculate the difference for.

    Returns
    -------
    list[int]
        List of differences between consecutive numbers in reverse.
    """
    return [x - y for x, y in zip(numbers[1:], numbers[:-1])]


def extrapolate(numbers: list[int], starting_point: int, operation: OPERATION) -> int:
    """
    Extrapolates the list of numbers to the starting point
    using the specified operation.

    Parameters
    ----------
    numbers : list[int]
        List of numbers to extrapolate to history from.
    starting_point : int
        Starting point of the extrapolation - usually 0.
    operation : OPERATION
        Operation to use to extrapolate the list of numbers.

    Returns
    -------
    int
        Extrapolated history from the list of numbers.
    """
    differences = [numbers]

    while not all(number == 0 for number in numbers):
        numbers = get_difference(numbers)
        differences.append(numbers)

    for sequence in reversed(differences):
        starting_point = operation(sequence, starting_point)

    return starting_point


def main(part: PART) -> int:
    """
    Calculates the solution to the problem from Day 9.

    Parameters
    ----------
    part : PART
        Part of the daily problem - 1 or 2.

    Returns
    -------
    int
        Solution to the problem.
    """
    with open(INPUT, "r") as f:
        lines = f.readlines()

    histories = [[int(number) for number in NUMBER.findall(line)] for line in lines]
    starting_point = 0

    if part == 1:
        return sum(
            extrapolate(
                numbers=numbers,
                starting_point=starting_point,
                operation=lambda seq, x: seq[-1] + x,
            )
            for numbers in histories
        )

    elif part == 2:
        return sum(
            extrapolate(
                numbers=numbers,
                starting_point=starting_point,
                operation=lambda seq, x: seq[0] - x,
            )
            for numbers in histories
        )

    else:
        raise ValueError(f"Invalid part of the problem: '{part}', must be 1 or 2.")


if __name__ == "__main__":
    args = parser.parse_args()
    result = main(part=args.part)
    print(result)

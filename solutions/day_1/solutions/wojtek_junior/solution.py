"""Solution to the day 1 of Advent of Code"""

import argparse
import re
from typing import Literal, Pattern

__author__ = "Wojtek Junior"

INPUT = "input.txt"
PART = Literal[1, 2]

REPLACES = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

# regex to finall digits for specific part of the problem
REGEX: dict[int, Pattern] = {
    1: re.compile(r"\d"),
    2: re.compile(r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))"),
}


parser = argparse.ArgumentParser(description="Part of the daily problem")
parser.add_argument(
    "-p",
    "--part",
    default=1,
    type=int,
    help="Part of the daily problem - 1 or 2",
)


def get_number(line: str, part: PART) -> int:
    """
    Extracts int from a string that is constructed by taking
    the first occurence of digit and the last occurence of digit in this order.

    Parameters
    ----------
    line : str
        Line of the input file.
    part : PART
        Part of the daily problem - 1 or 2.

    Returns
    -------
    int
        Extracted int number from the line.
    """
    regex = REGEX[part]
    matches = regex.findall(line)
    matches = [REPLACES.get(m, m) for m in matches]
    return int(f"{matches[0]}{matches[-1]}")


def main(part: PART) -> int:
    """
    Calculates the solution to the problem from Day 1.

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

    return sum(get_number(line=line, part=part) for line in lines)


if __name__ == "__main__":
    args = parser.parse_args()
    result = main(part=args.part)
    print(result)

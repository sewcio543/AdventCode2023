import argparse
import os
import re
from typing import Iterable

PATH = os.path.join(os.path.dirname(__file__), 'input.txt')

__author__ = "Rafal"

MAPPING = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

REGEX = {
    1: re.compile(r"[A-Za-z]"),
    2: re.compile(r"(?=({0}|\d))".format("|".join(MAPPING.keys())))
}

parser = argparse.ArgumentParser(description="Part of the daily problem")
parser.add_argument(
    "-p",
    "--part",
    default=1,
    type=int,
    help="Part of the daily problem - 1 or 2",
)

def calculate_score(input: Iterable) -> int:
    """
    Calculates a score based on a sequence of integers by combining
    the first and last digit of each number to form a two-digit number.
    The total sum of these two-digit numbers is returned.

    Parameters:
    - input (Iterable): A sequence of strings.

    Returns:
    - int: The calculated score.
    """
    return sum(map(lambda x: int(f"{x[0]}{x[-1]}"), input))


def main(part: int = 1):

    with open(PATH) as f:

        lines = map(lambda x: x.strip(), f.readlines())

        match part:
            case 1:
                lines = map(lambda x: REGEX.get(part).sub("", x), lines)

            case 2:
                lines = map(lambda x: REGEX.get(part).findall(x), lines)
                lines = map(lambda row: "".join(MAPPING.get(x, x) for x in row), lines)

        print(calculate_score(lines))


if __name__ == "__main__":
    args = parser.parse_args()
    main(part=args.part)

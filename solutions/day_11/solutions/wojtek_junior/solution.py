"""Solution to the day 11 of Advent of Code"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from itertools import combinations
from typing import Literal

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


@dataclass
class Galaxy:
    """
    Dataclass representing a galaxy.

    Parameters
    ----------
    x : int
        X coordinate of the galaxy.
    y : int
        Y coordinate of the galaxy.
    """

    x: int
    y: int

    def distance(self, other: Galaxy) -> int:
        """
        Calculates the Manhattan distance between two galaxies.

        Parameters
        ----------
        other : Galaxy
            Other galaxy to calculate the distance to.

        Returns
        -------
        int
            Manhattan distance between two galaxies.
        """
        return abs(self.x - other.x) + abs(self.y - other.y)


def main(part: PART) -> int:
    """
    Calculates the solution to the problem from Day 11.

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
        lines = [line.strip("\n") for line in f.readlines()]

    # indices af all empty rows and columns
    empty_rows = [x for x, line in enumerate(lines) if all(x == "." for x in line)]
    empty_cols = [y for y in range(len(lines)) if all(line[y] == "." for line in lines)]

    # additional gap for one empty dimension
    GAP = 1 if part == 1 else 999999

    galaxies = [
        Galaxy(x=x, y=y)
        for y, line in enumerate(lines)
        for x, sign in enumerate(line)
        if sign == "#"
    ]

    for galaxy in galaxies:
        galaxy.y += sum(GAP for row in empty_rows if row < galaxy.y)
        galaxy.x += sum(GAP for col in empty_cols if col < galaxy.x)

    return sum(
        galaxy.distance(other)
        for galaxy, other in combinations(galaxies, 2)
        if galaxy != other
    )


if __name__ == "__main__":
    args = parser.parse_args()
    result = main(part=args.part)
    print(result)

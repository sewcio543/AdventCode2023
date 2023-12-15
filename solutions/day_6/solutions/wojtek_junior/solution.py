"""Solution to the day 6 of Advent of Code"""

import argparse
import re
from dataclasses import dataclass
from functools import reduce
from typing import Literal

__author__ = "Wojtek Junior"

INPUT = "input.txt"
PART = Literal[1, 2]

parser = argparse.ArgumentParser(description="Part of the daily problem")
parser.add_argument(
    "-p",
    "--part",
    default=1,
    type=int,
    help="Part of the daily problem - 1 or 2",
)

NUMBER_REGEX = re.compile(r"\d+")


@dataclass
class Record:
    """
    Dataclass representing a record of the race from the input file.

    Parameters
    ----------
    time: int
        Race time in miliseconds.
    distance: int
        Record distance to beat in milimeters.
    """

    time: int
    distance: int

    def brute_force(self) -> int:
        """
        Calculates the number of ways to beat the record using brute force.
        It checks every possible combination of time of pressing the button assuming
        the time is integer in miliseconds.

        Returns
        -------
        int
            Number of ways to beat the record.
        """
        return sum(
            1 for press in range(self.time + 1) if press * (self.time - press) > self.distance
        )

    def find_edges(self) -> int:
        """
        Calculates the number of ways to beat the record finding first
        and last possible time of pressing the button that beats the record.

        Function of distance is quadratic and simmetrical so the number of possible
        ways to beat the record is equal to the difference between the last and first + 1
        to include the first and last time.

        The result should be the same as using brute force but it is much faster
        for larger ranges.

        Returns
        -------
        int
            Number of ways to beat the record.

        Notes
        -----
        For problem description see: https://adventofcode.com/2023/day/6
        or markdown file from repository.
        """
        first = next(
            press
            for press in range(self.time + 1)
            if press * (self.time - press) > self.distance
        )
        last = next(
            press
            for press in range(self.time, 0, -1)
            if press * (self.time - press) > self.distance
        )
        return last - first + 1


def main(part: PART) -> int:
    """
    Calculates the solution to the problem from Day 6.

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
        times, distances = map(lambda line: NUMBER_REGEX.findall(line), f.readlines())

    if part == 1:
        records = (
            Record(time=int(time), distance=int(distance))
            for time, distance in zip(times, distances)
        )
        return reduce(lambda x, y: x * y, (record.find_edges() for record in records))

    elif part == 2:
        time = int("".join(times))
        distance = int("".join(distances))

        record = Record(time=time, distance=distance)
        return record.find_edges()

    else:
        raise ValueError(f"Invalid part of the problem: '{part}', must be 1 or 2.")


if __name__ == "__main__":
    args = parser.parse_args()
    result = main(part=args.part)
    print(result)

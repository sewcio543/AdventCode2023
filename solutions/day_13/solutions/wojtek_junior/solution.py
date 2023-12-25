"""Solution to the day 13 of Advent of Code"""

import argparse
from typing import Callable, Literal, Optional

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
CONDITION = Callable[[str, str], bool]

CONDITIONS: dict[int, CONDITION] = {
    1: lambda left, right: left.startswith(right) or right.startswith(left),
    2: lambda left, right: sum(1 for a, b in zip(left, right) if a != b) == 1,
}

ROWS_MULTIPLIER = 100
COLUMNS_MULTIPLIER = 1


def get_group_value(group: list[str], condition: CONDITION, multiplier: int) -> Optional[int]:
    """
    Finds a value of the group, looking for reflection satisfying the condition.
    Returns number of rows/columns to the left/above the reflection point, times multiplier.

    Parameters
    ----------
    group : list[str]
        Lines of one group of the input.
    condition : CONDITION
        Condition to be satisfied for lines to be a reflection.
    multiplier : int
        Multiplier for reflection index value.

    Returns
    -------
    Optional[int]
        Value of the group if reflection found, None otherwise.
    """
    for index, _ in enumerate(zip(group, group[1:])):
        left = "".join(group[index::-1])
        right = "".join(group[index + 1 :])

        if condition(left, right):
            return (index + 1) * multiplier

    return None


def main(part: PART) -> int:
    """
    Calculates the solution to the problem from Day 13.

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
        text = f.read().strip("\n")

    # split groups on empty lines
    groups = text.split("\n\n")
    condition = CONDITIONS.get(part)

    if condition is None:
        raise ValueError("Invalid part number, must be 1 or 2")

    groups_sum = 0

    for i, group in enumerate(groups):
        # try to find reflection on rows axis
        lines = group.split("\n")

        rows_ref = get_group_value(
            group=lines, condition=condition, multiplier=ROWS_MULTIPLIER
        )

        if rows_ref is not None:
            groups_sum += rows_ref
            # if found go to the next group
            continue

        # try to find reflection on columns axis
        transposed = ["".join(el) for el in map(list, zip(*lines))]
        col_ref = get_group_value(
            group=transposed, condition=condition, multiplier=COLUMNS_MULTIPLIER
        )

        # if reflection not found - invalid input
        if col_ref is None:
            print(i)
            raise ValueError("Invalid input group, no reflection on any axis found.")

        groups_sum += col_ref

    return groups_sum


if __name__ == "__main__":
    args = parser.parse_args()
    result = main(part=args.part)
    print(result)

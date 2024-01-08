"""Solution to the day 15 of Advent of Code"""

import argparse
from dataclasses import dataclass, field
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

N_BOXES = 256
MULTIPLIER = 17


@dataclass
class Lens:
    """
    Dataclass representing a lens in the box.
    Has information about the label and the amount of the lens.

    Parameters
    ----------
    label : str
        Label of the lens.
    amount : int
        Amount of the lens in the box.
    """

    label: str
    amount: int


@dataclass
class Box:
    """
    Dataclass representing a box of lens.
    Has information about the number of the box and the lenses in it.

    Parameters
    ----------
    number : int
        Number of the box.
    lenses : list[Lens], optional
        Lenses in the box, by default empty list.
    """

    number: int
    lenses: list[Lens] = field(default_factory=list)

    def remove(self, label: str) -> None:
        """
        Removes the lens with the given label from the box.
        If there is no lens with the given label, nothing happens.

        Parameters
        ----------
        label : str
            Label of the lens to remove.
        """
        for lens in self.lenses:
            if lens.label == label:
                self.lenses.remove(lens)
                return

    def modify(self, label: str, amount: int) -> None:
        """
        Modifies the amount of the lens with the given label.
        If there is no lens with the given label, adds it to the box.

        Parameters
        ----------
        label : str
            Label of the lens to modify.
        amount : int
            New amount of the lens.
        """
        for lens in self.lenses:
            if lens.label == label:
                lens.amount = amount
                return
        self.lenses.append(Lens(label, amount))


def run_hash_algorithm(string: str) -> int:
    """
    Runs the hash algorithm on the given string.

    Steps of the algorithm:
    * Determine the ASCII code for the current character of the string.
    * Increase the current value by the ASCII code you just determined.
    * Set the current value to itself multiplied by 17.
    * Set the current value to the remainder of dividing itself by 256.

    Parameters
    ----------
    string : str
        String to run the algorithm on.

    Returns
    -------
    int
        Result of the algorithm.
    """

    current_value = 0

    for char in string:
        current_value = (current_value + ord(char)) * MULTIPLIER % N_BOXES

    return current_value


def get_focusing_power(box: Box) -> int:
    """
    Calculates the focusing power of the given box.

    The value comes from multiplying three values together:
    * One plus the box number of the lens in question.
    * The slot number of the lens within the box.
    * The focal length of the lens.

    Parameters
    ----------
    box : Box
        Box to calculate the focusing power of.

    Returns
    -------
    int
        Focusing power of the box.
    """
    return (box.number + 1) * sum((i + 1) * lens.amount for i, lens in enumerate(box.lenses))


def main(part: PART) -> int:
    """
    Calculates the solution to the problem from Day 15.

    Parameters
    ----------
    part : PART
        Part of the daily problem - 1 or 2.

    Returns
    -------
    int
        Solution to the problem.
    """
    with open(INPUT) as f:
        steps = f.read().strip("\n").split(",")

    if part == 1:
        return sum(map(run_hash_algorithm, steps))

    elif part == 2:
        boxes = [Box(number) for number in range(N_BOXES)]

        for step in steps:
            if "-" in step:
                label = step[: step.index("-")]
                code = run_hash_algorithm(label)
                boxes[code].remove(label)
            elif "=" in step:
                label = step[: step.index("=")]
                code = run_hash_algorithm(label)
                amount = int(step[step.index("=") + 1 :])
                boxes[code].modify(label, amount)

        return sum(map(get_focusing_power, boxes))

    raise ValueError("Invalid part number. Choose one of: 1, 2.")


if __name__ == "__main__":
    args = parser.parse_args()
    result = main(part=args.part)
    print(result)

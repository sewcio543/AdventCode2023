"""Solution to the day 4 of Advent of Code"""

import argparse
import re
from collections import defaultdict
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

# regex for numbers in the card
NUMBER_REGEX = re.compile(r"\d+")
# regex for card suffix with card number
SUFFIX = re.compile(r"Card\s*(\d+):")


def get_card_number(line: str) -> int:
    """
    Extracts card number from the line and returns it as int.

    Parameters
    ----------
    line : str
        Line of the input text file to extract card number from.

    Raises
    ------
    ValueError
        If the line does not contain card number suffix.
    """
    suffix = SUFFIX.search(line)
    if not suffix:
        raise ValueError(f"Line '{line}' does not contain card number suffix")
    return int(suffix.group(1))


def get_winning_dict(lines: list[str]) -> dict[int, int]:
    """
    Creates and returns a dictionary with card number as key
    and number of correct guesses in the scratchcard as value.

    Parameters
    ----------
    lines : list[str]
        List of lines from the input text file.
    """
    winning_dict = {}

    for line in lines:
        card_number = get_card_number(line)
        line = SUFFIX.sub("", line)
        winning_dict[card_number] = get_number_of_correct_guesses(*line.split("|"))

    return winning_dict


def get_number_of_correct_guesses(winning: str, guess: str) -> int:
    """
    Returns number of correct guesses in the scratchcard
    based on provided winning and guess strings.

    Parameters
    ----------
    winning : str
        Strings from single line of input file containing winning numbers.
    guess : str
        Strings from single line of input file containing guess numbers.
    """
    winning_list = set(NUMBER_REGEX.findall(winning))
    guess_list = set(NUMBER_REGEX.findall(guess))
    return len(winning_list.intersection(guess_list))


def main(part: PART) -> int:
    """
    Calculates the solution to the day 4 of Advent of Code.

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

    if part == 1:
        wins = get_winning_dict(lines)
        # case if there is no winning numbers - 0 points
        return sum(2 ** (correct - 1) if correct else 0 for correct in wins.values())

    elif part == 2:
        scratchcards = defaultdict(int)
        wins = get_winning_dict(lines)

        def fill(card: int):
            """
            Recursive function to fill the scratchcard dict with number of copies
            of each card it produces as a result, excluding the original card.
            """
            # range starts from one to exlude the original card
            copies = [card + i for i in range(1, wins[card] + 1)]

            for copy in copies:
                # add one copy of the card
                scratchcards[copy] += 1
                # fill the scratchcard dict with copies produces as result of this copy
                fill(copy)

        for line in lines:
            card_number = get_card_number(line)
            # add one original card for each line
            scratchcards[card_number] += 1
            # fill the scratchcard dict with copies produces as result of the original card
            fill(card_number)

        # sum of all cards - both original and copies
        return sum(cards for cards in scratchcards.values())

    else:
        raise ValueError(f"Invalid part of the problem: '{part}', must be 1 or 2.")


if __name__ == "__main__":
    args = parser.parse_args()
    result = main(part=args.part)
    print(result)

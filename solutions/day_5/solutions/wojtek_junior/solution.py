"""Solution to the day 5 of Advent of Code"""

import argparse
import re
from itertools import pairwise
from typing import Any, Literal

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

# regex used to extract target seed numbers from first line of input file
SEEDS_REGEX = re.compile(r"seeds: (.*)\n")
map_re = r"[a-z]+-to-[a-z]+\smap:"
# regex used to extract entire string of the category (one mapping) with numbers
CATEGORY_REGEX = re.compile(rf"({map_re}.*?)(?=[a-z]|$)", re.DOTALL)
# regex used to extract range numbers from one line of category
NUMBERS_RANGE_REGEX = re.compile(r"\d+\s\d+\s\d+")


class RangeDict(dict):
    """
    A dictionary-like object that stores ranges as keys and values as values.
    It's used to optimize the mapping of the seeds to the map. In case of broad ranges,
    mapping is extremely large and slow to compute.
    This class allows to store the mapping in form of tuples and then retrieve the value
    by the key with assuming that mapping is linaer within the range.

    Assumption: ranges are non-overlapping

    Get method is overriden to allow for the linear mapping.
    """

    def get(self, __key: int) -> int:
        for i in self.keys():
            if i[0] <= __key < i[1]:
                # start of the range + linear distance from the start (+1 per unit)
                return self[i][0] + (__key - i[0])
        return __key


class ChainDict:
    """
    Class that allows to chain multiple dictionaries together.
    It's used to chain the mapping of the seeds to arrive at the final mapping
    from seed to location. It uses values retrieved from the previous dictionary
    as a key to the next dictionary.

    __getitem__ method is overriden to allow for the chaining.
    """

    def __init__(self, *dicts: dict) -> None:
        self.dicts = list(dicts)

    def chain(self, __dict: dict) -> None:
        """
        Add a dictionary to the chain.
        New dictionary will be added as the last one in the chain.

        Parameters
        ----------
        __dict : dict
            Dictionary to be added to the chain.
        """
        self.dicts += [__dict]

    def __getitem__(self, __key: Any) -> Any:
        key = __key

        for d in self.dicts:
            key = d.get(key)
        return key


def get_chain_dict(categories: list[str]) -> ChainDict:
    """
    Creates a chain of dictionaries that map seeds to the location.

    Parameters
    ----------
    categories : list[str]
        List of strings that contain mapping from input file.

    Returns
    -------
    ChainDict
        ChainDict object with mappings from seeds to the location.
    """
    chain = ChainDict()

    for category in categories:
        range_dict = RangeDict()
        for x in NUMBERS_RANGE_REGEX.findall(category):
            destination_start, source_start, range_ = map(int, x.split(" "))

            range_dict.update(
                RangeDict(
                    {
                        (source_start, source_start + range_): (
                            destination_start,
                            destination_start + range_,
                        )
                    }
                )
            )

        chain.chain(range_dict)
    return chain


def main(part: PART) -> int:
    """
    Calculates the solution to the problem from Day 5.

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
        text = f.read()

    matched = SEEDS_REGEX.search(text)
    if matched is None:
        raise ValueError("Seeds not found in the input file.")

    seeds = matched.group(1).split(" ")
    seeds = [int(x) for x in seeds]

    categories = CATEGORY_REGEX.findall(text)
    chain = get_chain_dict(categories)

    if part == 1:
        return min(chain[seed] for seed in seeds)

    #! TODO brute force - lol
    elif part == 2:
        return min(
            chain[number]
            for seed, range_ in zip(seeds[::2], seeds[1::2])
            for number in range(seed, seed + range_)
        )

    else:
        raise ValueError(f"Invalid part of the problem: '{part}', must be 1 or 2.")


if __name__ == "__main__":
    args = parser.parse_args()
    result = main(part=args.part)
    print(result)

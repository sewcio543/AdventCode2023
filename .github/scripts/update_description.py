"""
Script for updating the advent day problem description
in the problem.md file of a specific day.

CLI Arguments
-------------
day: int
    The day of the advent calendar to update markdown
    description of the problem for.

Usage
-----
>>> python update_description.py --day 3
>>> python update_description.py --d 5
"""

import argparse
import os

import requests
from bs4 import BeautifulSoup

HOST = "https://adventofcode.com"
ENDPOINT = "/2023/day/"
SELECTOR = ".day-desc"


parser = argparse.ArgumentParser(description="Update of daily problem")
parser.add_argument(
    "-d",
    "--day",
    required=True,
    type=int,
    help="Day of the advent calendar",
)


def main(day: int) -> None:
    """
    Sends a request to the advent of code website
    and updates the problem.md file with the description
    of the problem for a specific day if problem is available.

    Parameters
    ----------
    day : int
        The day of the advent calendar to update markdown
        description of the problem for.

    Raises
    ------
    ValueError
        If problem for the day is not available yet.
    """
    response = requests.get(f"{HOST}{ENDPOINT}{day}")

    if not response.ok:
        raise ValueError(f"Day '{day}' is not available yet.")

    soup = BeautifulSoup(response.text, "lxml")
    description = soup.select_one(SELECTOR)

    path = os.path.join("solutions", f"day_{day}", "problem.md")

    with open(path, "w") as file:
        file.write(str(description))


if __name__ == "__main__":
    args = parser.parse_args()
    main(day=args.day)

"""
Advent of code 2023 - day 2
"""


# Imports
# ------------------------------------------------------------------------------

import numpy as np


# Reading a file
# ------------------------------------------------------------------------------

PATH = r"input_2.txt"
file = open(PATH, "r", encoding="utf-8").read()
file = file.split("\n")
file = [elem for elem in file if len(elem) > 0]


# Data preparation
# ------------------------------------------------------------------------------

iter_idxs = [row.find(":") for row in file]
file = [row[idx + 2 :] for row, idx in zip(file, iter_idxs)]
file = [elem.replace(",", "", -1).replace(";", "", -1) for elem in file]
file = [elem.split(" ") for elem in file]
keys = [*range(1, len(file) + 1)]


# Functions definition
# ------------------------------------------------------------------------------


def _color_evaluation(color_name: str, row: list, purpose: str):

    """
    Depending of the purpose parameter returning if the row is checking predefined max balls\
    condition for single color or returning max value of color per game

    Parameters
    ----------
    color_name: str
        name of color to evaluate based on dictionary defined in function
    row: list
        game data to evaluate
    purpose: str
        'check' - checking if the amount of balls in round is lower than max number of balls
        'max' - returning max amount of balls per game

    Returns
    -------
    values: list
        for purpose 'check', returns values not meeting the max balls conditions
    values: int
        for purpose 'max', returns max from analyzed color
    """

    color_dict = {"blue": 14, "green": 13, "red": 12}

    indexes = [n for (n, e) in enumerate(row) if e == color_name]
    indexes = list(np.array(indexes) - 1)
    values = list(np.array(row)[indexes])

    if purpose == "check":
        values = [elem for elem in values if int(elem) > color_dict[color_name]]
    elif purpose == "max":
        values = max((int(elem) for elem in values))

    return values


def row_check(row: list, purpose: str) -> int:

    """
    Iterates over 3 analyzed colors the color_evaluation function, collects its outputs and \
    depending on purpose:
    - returns if the game is meeting the conditions
    - returns product of maximum values per color per game

    Parameters
    ----------
    row: list
        game data to evaluate
    purpose: str
        'check' - checking if the amount of balls in round is lower than max number of balls
        'max' - returning max amount of balls per game

    Raises
    ------
    AssertionError:
        When other purpose than 'check' or 'max' is defined

    Returns
    -------
    purpose == 'check':
        if the game is meeting defined ball amount condition for all colours
    purpose == 'max':
        product of all color max balls values per game
    """

    output = []
    output.append(_color_evaluation("blue", row, purpose))
    output.append(_color_evaluation("green", row, purpose))
    output.append(_color_evaluation("red", row, purpose))

    if purpose == "check":
        evaluation = int(len([elem for elem in output if elem]) > 0)
    elif purpose == "max":
        evaluation = int(np.prod(output))
    else:
        purposes_list = ["check", "max"]
        assert (
            purpose in purposes_list
        ), f"Wrong purpose defined! Should be on of: {purposes_list}"

    return evaluation


# Part 1
# ------------------------------------------------------------------------------

dict_values = {k: row_check(v, "check") for k, v in zip(keys, file)}
print(f"Part 1: {sum((key for key, val in dict_values.items() if val == 0))}")


# Part 2
# ------------------------------------------------------------------------------

print(f"Part 2: {sum((row_check(v, 'max') for v in file))}")

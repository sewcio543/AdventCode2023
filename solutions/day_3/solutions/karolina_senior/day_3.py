"""
Advent of code 2023 - day 3
"""


# Imports
# ------------------------------------------------------------------------------

import re
import numpy as np


# Reading a file
# ------------------------------------------------------------------------------

PATH = r'input_3.txt'
file = open(PATH, "r", encoding="utf-8").read()


# Function definitions
# ------------------------------------------------------------------------------

def _return_val(
    x: int,
    y: int,
    digits_type: bool
) -> int:

    """
    Depending on digits_type state, return x value if True or x+y value if False

    Parameters
    ----------
    x: int
        integer value present in all outputs
    y: int
        integer value to be added to x if digits_type is True
    digits_type: bool
        depending on it's state proper calculations are being made

    Returns
    -------
    integer value equal x or x+y
    """

    return x if digits_type is True else x+y


def generate_verified_indexes(
        file_var: str,
        digits_type: bool
) -> list:

    """
    Depending on line length, identifying neighbouring indexes in string\
    (which exactly is a matrix), and saving proper indexes depending on the type\
    regulated by digits_type boolean

    Parameters
    ----------
    file_var: str
        string matrix to extract the data from
    digits_type: bool
        depending on it's state proper calculations are being made by _return_val\
        function to store character indexes or digit indexes in proper list
    """

    # Evaluating len of a single line in file_var
    line_len = file_var.split('\n')
    line_len = len(line_len[1]) + 1

    # Identifying all digits and special characters indexes
    digit_indexes = [m.start() for m in re.finditer(r'\d', file_var)]
    char_indexes = [m.start() for m in re.finditer(r'[^.0-9]', file_var.replace('\n', '1', -1))]

    # Assigning possible neighbours locations to list
    pad_list = [1, -1, line_len-1, line_len, line_len+1, -(line_len+1), -line_len, -(line_len-1)]

    matches = [[_return_val(elem, add, digits_type) for add in pad_list if elem+add in char_indexes
                ] for elem in digit_indexes]
    matches = [elem for row in matches for elem in row]

    return matches


# Part 1
# ------------------------------------------------------------------------------

# Generate list of digit indexes neighbouring to a special characters indexes
match = [
    [a, b] for a, b in zip(
        generate_verified_indexes(file, True),
        generate_verified_indexes(file, False)
    )
]

# Get ranges of indexes for all numbers
numbers_indexes = [range(start, end) for start, end in zip(
    (m.start() for m in re.finditer(r'\d+', file)),
    (m.end() for m in re.finditer(r'\d+', file)))
]

# Filter numbers neighbouring any special char from all numbers
proper_nums = [idx for idx in numbers_indexes if any(elem[0] in idx for elem in match)]

# Join digits into numbers and summarize the results of received list of numbers
print(f"Part 1: {sum((int(''.join([file[i] for i in idx])) for idx in proper_nums))}")


# Part 2
# ------------------------------------------------------------------------------

# Add character index to matching numbers
match = [[[num, elem[1]] for elem in match if elem[0] in num][0] for num in proper_nums]

# Create a dictionary with list of matching numbers per character index
index = {k : list(filter(lambda elem: k == elem[1], match)) for k in set(elem[1] for elem in match)}

# Get list of numbers matching to a specific special character index
list_to_prod = [[int(''.join([file[i] for i in idx[0]])) for idx in index[key]] for key in index]

# Filter matches to 2 special characters, multiply values and sum results
print(f"Part 1: {sum((np.prod(elem) for elem in list_to_prod if len(elem) > 1))}")

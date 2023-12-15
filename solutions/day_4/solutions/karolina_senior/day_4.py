"""
Advent of code 2023 - day 4
"""


# Imports
# ------------------------------------------------------------------------------

import re


# Reading a file
# ------------------------------------------------------------------------------

PATH = r'input_4.txt'
file = open(PATH, "r", encoding="utf-8").read()
file = file.split('\n')
file = [elem for elem in file if len(elem) > 0]


# Function definitions
# ------------------------------------------------------------------------------

def row_operation(
    row: str
) -> int:

    """
    Identifying numbers between ':' and '|' as winning and after '|' as guesses,\
    calculating amount of matches per row minus 1 to treat as a power.

    Parameters
    ----------
    row: str
        single row of card data containing card {id}: {winning nums} | {guesses}

    Returns
    -------
    matches: int
        amount of matching guesses subtracted by 1
    """

    winning, to_check = [re.findall(r'\d+', card) for card in row.split(':')[1].split('|')]
    matches = len([elem for elem in to_check if elem in winning])

    return matches


# Part 1
# ------------------------------------------------------------------------------

# Apply row_operation for all rows of data in file
output_list = [row_operation(row) for row in file]
# # Treat function results as a power of 2 if is greater than -1 to obtain a result
part_1 = [(1, 2**(elem-1)) if elem-1 >= 0 else (1, 0) for elem in output_list]
print(f"Part 1: {sum((elem[1] for elem in part_1))}")


# Part 2
# ------------------------------------------------------------------------------

amounts = dict(enumerate([1]*len(output_list)))

for key, score in dict(enumerate(output_list)).items():
    score_range = [key + next for next in [*range(1, score+1)]]
    to_add = amounts[key]
    amounts.update({key: amounts[key] + to_add for key in score_range})

print(f'Part 2: {sum(amounts.values())}')

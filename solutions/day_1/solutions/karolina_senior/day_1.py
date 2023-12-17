"""
Advent of code 2023 - day 1
"""


# Reading a file
# ------------------------------------------------------------------------------

PATH = r"input_1.txt"
file = open(PATH, "r", encoding="utf-8").read()
file = file.split("\n")
file = [elem for elem in file if len(elem) > 0]


# Functions definition
# ------------------------------------------------------------------------------


def _find_type(row: str, key: str, right: bool) -> int:
    """
    Function returning proper find method applied on row to search for key\
    depending of direction parameter right

    Parameters:
    row: str
        text to search for the key
    key: str
        value to be founded in the row
    right: bool
        direction of searching

    Returns
    str.method(str) -> int:
        result of proper find method depending of right parameter returning\
        location of the key in row if exist or -1 if not present
        - rfind if right is True
        - find if right is False
    """

    return row.rfind(key) if right is True else row.find(key)


def get_indexes(row_list: list, right: bool):
    """
    Returns list of first locations of word or numerical digits from 1 to 9 per each row,\
    considering direction predefined by right parameter

    Parameters
    ----------
    row_list: list
        list of rows to search digits in
    right: bool
        direction of searching

    Returns
    -------
    key_loc: list
        list of first or last occurence of any of 1-9 digits per each row in row_list
    """

    map_dic = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
    }

    location = [
        [_find_type(row, key, right) for key in map_dic if _find_type(row, key, right) != -1]
        for row in row_list
    ]
    key_name = [
        [key for key in map_dic if _find_type(row, key, right) != -1] for row in row_list
    ]

    # Rearange results
    order = [sorted(range(len(row)), key=lambda i: row[i]) for row in location]
    key_name = [[key[i] for i in order[idx]] for idx, key in enumerate(key_name)]

    key_loc = [row[-int(right)] for row in key_name]
    key_loc = [map_dic[key] for key in key_loc]

    return key_loc


# Part 1
# ------------------------------------------------------------------------------

start = [[digit for digit in list(elem) if digit.isdigit()][0] for elem in file]
stop = [[digit for digit in list(elem) if digit.isdigit()][-1] for elem in file]
output = ["".join([a, b]) for a, b in zip(start, stop)]
print(f"Part 1: {sum((int(elem) for elem in output))}")


# Part 2
# ------------------------------------------------------------------------------

key_start = get_indexes(file, False)
key_end = get_indexes(file, True)
key_values = ["".join([str(start), str(end)]) for start, end in zip(key_start, key_end)]

print(f"Part 2: {str(sum((int(elem) for elem in key_values)))}")

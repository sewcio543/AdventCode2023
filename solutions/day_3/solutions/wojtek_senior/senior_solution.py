import numpy as np
import re
import os

PATH = os.path.join(os.path.dirname(__file__), "input.txt")
with open(PATH) as f:
    lines = [line.rstrip("\n") for line in f]


# randomly copied from stackoverflow/numpy which allows to pad to np.array with strings
def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get("padder", "?")
    vector[: pad_width[0]] = pad_value
    vector[-pad_width[1] :] = pad_value
    return vector


def number_close_to_character(num: re.Match, ex: re.Match, n_cols: int = 10) -> bool:
    """with padding we dont care now about the edges, so we can just check if the number is close to the special character"""
    ex_index = ex.span()[0]
    for i in range(num.span()[0], num.span()[1]):
        if (
            np.abs(i - ex_index) == n_cols
            or np.abs(i - ex_index) == n_cols - 1
            or np.abs(i - ex_index) == n_cols + 1
            or np.abs(i - ex_index) == 1
        ):
            return 1
    return 0


### solution part 1

# padding here
lines = [list(i) for i in lines]
lines = list(np.pad(lines, 1, mode=pad_with, padder="."))
lines = ["".join(i) for i in lines]

rows = len(lines)
cols = len(lines[0])
lines = ("").join(lines)
special_characters = list(set([i for i in lines if not i.isalnum() and i != "."]))
special_characters = "|".join(re.escape(x) for x in special_characters)
special_characters = [i for i in re.finditer(special_characters, lines)]
numbers = [i for i in re.finditer(r"\d+", lines)]


adjacent_sum = 0
for n in numbers:
    find = False
    for ex in special_characters:
        if number_close_to_character(num=n, ex=ex, n_cols=cols):
            find = True
    if find:
        continue
    adjacent_sum = adjacent_sum + int(n[0])
adjacent_sum


all_number = sum([int(i[0]) for i in numbers])
solution_p_1 = all_number - adjacent_sum
print(f" Solution to part 1 is: {solution_p_1}")


#### part 2

# we may have some duplication but i am lazy

# padding here
lines = [list(i) for i in lines]
lines = list(np.pad(lines, 1, mode=pad_with, padder="."))
lines = ["".join(i) for i in lines]

rows = len(lines)
cols = len(lines[0])
lines = ("").join(lines)

# just find stars now
stars = list(set([i for i in lines if i == "*"]))
stars = "|".join(re.escape(x) for x in stars)
stars = [i for i in re.finditer(stars, lines)]
numbers = [i for i in re.finditer(r"\d+", lines)]

# now looking for  EXACTLY 2 neighbours
adjacent_sum = 0
for ex in stars:
    n_found = []
    for n in numbers:
        if number_close_to_character(num=n, ex=ex, n_cols=cols):
            n_found.append(int(n[0]))
    if len(n_found) == 2:
        adjacent_sum = adjacent_sum + n_found[0] * n_found[1]
solution_p_2 = adjacent_sum

print(f" Solution to part 2 is: {solution_p_2}")

import numpy as np
import os

PATH = os.path.join(os.path.dirname(__file__), "input.txt")
with open(PATH) as f:
    lines = [line.rstrip("\n") for line in f]

HOW_MANY = 1000000


def row_appender(m: np.ndarray) -> np.ndarray:
    """Appends a row to a matrix if the sum of the row is 0"""
    new = m.copy()
    rows_to_append = [i for i, val in enumerate(new) if sum(val) == 0]
    counter = 0
    for value in rows_to_append:
        new = np.vstack(
            [
                new[0 : value + counter, :],
                new[value + counter, :],
                new[value + counter :, :],
            ]
        )
        counter += 1
    return new


def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """Calculates the Manhattan distance between two points"""
    return abs(x1 - x2) + abs(y1 - y2)


# Part 1

# some replacing to numbers so i can use np.array and .sum() later
# 1 means galaxy from the task, 0 nothing
lines = [line.replace(".", "0") for line in lines]
lines = [line.replace("#", "1") for line in lines]
lines = [list(map(int, line)) for line in lines]
m = np.array(lines)

# here/always?: appending column = appending row of transposed matrix
m = row_appender(m)
m = m.transpose()
m = row_appender(m)
m = m.transpose()

x_axis, y_axis = np.where(m == 1)[0], np.where(m == 1)[1]

counter = sum(
    manhattan_distance(x_axis[i], y_axis[i], x_axis[j], y_axis[j])
    for i in range(len(x_axis))
    for j in range(len(x_axis))
)

solution_1 = counter // 2  # because of double counting and i am lazy
print(solution_1)

# Part 2

# bitch, growth is constant, god bless manhattan metrics

start = 9414682  # calculated here :)
expanded_by_one = solution_1
const = expanded_by_one - start
how_many = HOW_MANY

# this formula does not work for how_many=1 for  0/1 for some reason - no idea tbf
solution_2 = start + (const * (how_many - 1))
print(solution_2)

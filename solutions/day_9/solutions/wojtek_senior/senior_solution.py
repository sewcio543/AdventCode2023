import numpy as np
import os
from functools import reduce

PATH = os.path.join(os.path.dirname(__file__), "input.txt")
with open(PATH) as f:
    lines = [line.rstrip("\n") for line in f]


def part_1_solution(l: tuple) -> int:
    """
    Sum the last numbers from the initial list and lists of differences until all numbers are 0
    """
    counter = 0
    a = l.copy()
    while set(a) != {0}:
        counter = counter + a[-1]
        a = np.diff(a)
    return counter


def part_2_solution(l: tuple) -> int:
    """
    Sum the numbers backwards from the initial list and lists of differences until all numbers are 0.
    """
    backward_numbers = []
    a = l.copy()
    while set(a) != {0}:
        backward_numbers.append(a[0])
        a = np.diff(a)
    backward_numbers.append(0)
    backward_numbers = backward_numbers[::-1]
    return reduce(lambda x, y: y - x, backward_numbers)


#########

lines = [[int(j) for j in line.split(" ")] for line in lines]

answer_p1 = sum([part_1_solution(i) for i in lines])
print(f" Solution to part 1 is: {answer_p1}")


answer_p2 = sum([part_2_solution(i) for i in lines])
print(f" Solution to part 12 is: {answer_p2}")

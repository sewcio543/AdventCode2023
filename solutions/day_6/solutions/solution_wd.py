import numpy as np
from functools import reduce

with open("solutions/day_6/solutions/input.txt") as f:
    lines = [line.rstrip("\n") for line in f]


def calculate_possible_scores(time):
    return np.array([i * (time - i) for i in range(time + 1)])


def when_reached(n, goal):
    counter = 0
    when = False
    while when is False:
        if (n - counter) * counter >= goal:
            when = True
        counter += 1
    return counter - 1


# Part 1W

times = lines[0].split(" ")
times = [int(i) for i in times if i.isdigit()]

distances = lines[1].split(" ")
distances = [int(i) for i in distances if i.isdigit()]

scores = [calculate_possible_scores(i) for i in times]
how_many = [np.sum(scores[i] > distances[i]) for i in range(len(scores))]
solution_1 = np.product(how_many)
print(solution_1)

# Part 2

times = lines[0].split(" ")
times = [int(i) for i in times if i.isdigit()]

distances = lines[1].split(" ")
distances = [int(i) for i in distances if i.isdigit()]

times = [int(reduce(lambda x, y: str(x) + str(y), times))]
distances = [int(reduce(lambda x, y: str(x) + str(y), distances))]

if int(distances[0]) % 2 == 0:
    solution_2 = times[0] + 1 - 2 * when_reached(times[0], distances[0])
else:
    solution_2 = times[0] + 1 - 2 * when_reached(times[0], distances[0]) - 2

print(solution_2)

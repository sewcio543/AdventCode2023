import regex as re
import os

PATH = os.path.join(os.path.dirname(__file__), "input.txt")
with open(PATH) as f:
    lines = [line.rstrip("\n") for line in f]

# dict both for str and input as regex.findall allows for overlapping = True
num_dict = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
}

# part 1
# find first/last digit in in each line, convert based on dict, concatenate and sum them
answer_p1 = sum(
    [
        int(re.findall(pattern=r"\d", string=i)[0] + re.findall(pattern=r"\d", string=i)[-1])
        for i in lines
    ]
)

print(f" Solution to part 1 is: {answer_p1}")

# part 2
# find first/last digit/ str from num_dict.keys() in in each line, convert based on dict, concatenate and sum them
# possible thanks to overlapped = True from regex library
p = ("|").join(list(num_dict.keys()))
answer_p2 = sum(
    [
        int(
            num_dict[re.findall(pattern=p, string=i, overlapped=True)[0]]
            + num_dict[re.findall(pattern=p, string=i, overlapped=True)[-1]]
        )
        for i in lines
    ]
)
print(f" Solution to part 2 is: {answer_p2}")

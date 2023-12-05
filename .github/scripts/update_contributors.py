import argparse
import re

FILE = "README.md"
SOLUTION_PATH = re.compile(r"solutions/day_\d{1,2}/solutions/*")


parser = argparse.ArgumentParser(description="Update contributors to the problem.")
parser.add_argument(
    "-f",
    "--file",
    required=True,
    type=str,
    help="File that was commited",
)
parser.add_argument(
    "-a",
    "--author",
    required=True,
    type=str,
    help="Author of the commit",
)


def main(file: str, author: str) -> None:
    with open(FILE, "r") as f:
        lines = f.readlines()

    match_ = SOLUTION_PATH.search(file)

    if match_ is None:
        print(f"File '{file}' is not a solution file.")
        return

    day_match = re.search(r"\d+", match_.group())

    if day_match is None:
        print(f"Day not found in {file}.")
        return

    day = int(day_match.group(0))
    problem_re = re.compile(rf"Day {day}")

    problem = next((line for line in lines if problem_re.search(line) is not None), None)

    if problem is None:
        print(f"Problem for day {day} not found in '{FILE}'.")
        return

    # one is for new line
    index = lines.index(problem) + 2
    lines.insert(index, f"* {author}\n")

    with open(FILE, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    args = parser.parse_args()
    main(file=args.file, author=args.author)

"""Solution to the day 8 of Advent of Code"""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from functools import reduce
from itertools import cycle
from typing import Callable, Iterable, Literal, Optional

__author__ = "Wojtek Junior"

INPUT = "input.txt"
PART = Literal[1, 2]

# direction to navigate the edges of node - go left or right
INSTRUCTION = Literal["L", "R"]

# regex for the node code
CODE_REGEX = re.compile(r"^[A-Z]{3}")
# regex for the node edges
DIRECTION_REGEX = re.compile(r"(?<!^)[A-Z]{3}")

parser = argparse.ArgumentParser(description="Part of the daily problem")
parser.add_argument(
    "-p",
    "--part",
    default=1,
    type=int,
    help="Part of the daily problem - 1 or 2",
)


@dataclass
class Node:
    """
    Dataclass representing a node in the graph.

    Parameters
    ----------
    code : str
        Code of the node.
    L : Node, optional
        Left node.
    R : Node, optional
        Right node.
    """

    code: str
    L: Optional[Node] = None
    R: Optional[Node] = None


# condition to break traversing the graph
BREAK_CONDITION = Callable[[Node], bool]


def get_next_node(node: Node, instruction: INSTRUCTION) -> Node:
    """
    Returns the next node in the graph based on the instruction.

    Parameters
    ----------
    node : Node
        Current node.
    instruction : INSTRUCTION
        Instruction to follow, go left or right.

    Returns
    -------
    Node
        Next node in the graph.
    """
    next_ = getattr(node, instruction)
    return next_


def get_steps(start: Node, instructions: Iterable, condition: BREAK_CONDITION) -> int:
    """
    Returns the number of steps to reach the node that satisfies the condition.

    Parameters
    ----------
    start : Node
        Starting node.
    instructions : Iterable
        Instructions to follow.
    condition : BREAK_CONDITION
        Condition to break traversing the graph.

    Returns
    -------
    int
        Number of steps to reach the node that satisfies the condition.
    """
    node = start

    for step, instruction in enumerate(cycle(instructions), start=1):
        node = get_next_node(node=node, instruction=instruction)

        if condition(node):
            return step

    # redundant, just for type checker's sake, always cycles iterable infinitely
    raise RuntimeWarning("No solution found")


def parse_graph(lines: list) -> dict[str, Node]:
    """
    Parses the graph from the input.

    Parameters
    ----------
    lines : list
        List of input lines with nodes.

    Returns
    -------
    dict[str, Node]
        Dictionary of nodes with codes as keys and Node objects as values.
    """
    graph_dict = {}

    for line in lines:
        code = CODE_REGEX.search(line).group()  # type: ignore
        L, R = DIRECTION_REGEX.findall(line)
        graph_dict[code] = {"L": L, "R": R}

    # Create the Node objects
    nodes = {code: Node(code) for code in graph_dict.keys()}

    # # Link the Node objects together
    for code, node in nodes.items():
        node.L = nodes.get(graph_dict[code]["L"])
        node.R = nodes.get(graph_dict[code]["R"])

    return nodes


def main(part: PART) -> int:
    """
    Calculates the solution to the problem from Day 8.

    Parameters
    ----------
    part : PART
        Part of the daily problem - 1 or 2.

    Returns
    -------
    int
        Solution to the problem.
    """
    with open(INPUT, "r") as f:
        lines = f.readlines()

    # instructions to follow are in the first line
    instructions = lines[0].strip("\n")
    # nodes of the graph start form the third line of input file
    nodes = parse_graph(lines[2:])

    if part == 1:
        start = nodes["AAA"]

        return get_steps(
            start=start,
            instructions=instructions,
            condition=lambda x: x.code == "ZZZ",
        )

    elif part == 2:

        def lcm_multiple(*args):
            """Calculates the least common multiple of multiple numbers."""

            def lcm(a, b):
                return abs(a * b) // math.gcd(a, b)

            return reduce(lcm, args)

        start = [node for code, node in nodes.items() if code.endswith("A")]
        steps = [
            get_steps(
                start=start,
                instructions=instructions,
                condition=lambda x: x.code.endswith("Z"),
            )
            for start in start
        ]
        # based on the assumption that following the set of intructions, starting from
        # any of the start nodes, graph will be traversed in the same number of steps.
        # Finding the least common multiple of the number of steps to reach the end
        # node from each of the start nodes will give the number of steps to reach the
        # end node from all of the start nodes at the same time.
        return lcm_multiple(*steps)

    else:
        raise ValueError(f"Invalid part of the problem: '{part}', must be 1 or 2.")


if __name__ == "__main__":
    args = parser.parse_args()
    result = main(part=args.part)
    print(result)

"""Solution to the day 10 of Advent of Code"""

import argparse
import re
from dataclasses import dataclass
from typing import Callable, Literal, Optional

from matplotlib.path import Path

__author__ = "Wojtek Junior"

INPUT = "input.txt"
PART = Literal[1, 2]
# possible methods to use for part 2 solution
# pick - using Pick's theorem
# matplotlib - using matplotlib.path.Path.contains_point
METHOD = Literal["pick", "matplotlib"]

parser = argparse.ArgumentParser(description="Part of the daily problem")
parser.add_argument(
    "-p",
    "--part",
    default=1,
    type=int,
    help="Part of the daily problem - 1 or 2",
)
parser.add_argument(
    "-m",
    "--method",
    default="pick",
    type=str,
    help="Method to use for 2 part solution - one of: 'pick' or 'matplotlib'",
)

# dictionary of all possible pipe connections
connections: dict[str, dict[str, set[str]]] = {
    "|": {"N": {"7", "F", "|"}, "S": {"L", "J", "|"}},
    "-": {"E": {"7", "J", "-"}, "W": {"L", "F", "-"}},
    "L": {"N": {"F", "7", "|"}, "E": {"J", "7", "-"}},
    "J": {"N": {"F", "7", "|"}, "W": {"L", "F", "-"}},
    "7": {"S": {"L", "J", "|"}, "W": {"F", "L", "-"}},
    "F": {"S": {"L", "J", "|"}, "E": {"7", "J", "-"}},
    ".": {},
}
# starting point on the map - unknown pipe
START = "S"


@dataclass
class Direction:
    """
    Dataclass representing a direction.

    Parameters
    ----------
    move : Callable
        Function to move to the next square. Callable that takes two integers
        with coordinates of the current square and returns a tuple with
        coordinates of the next square.
    counter : str
        Opposite direction.
    """

    move: Callable[[int, int], tuple[int, int]]
    counter: str


# dictionary of all possible directions with information about how to move
# to them and what is the opposite direction
directions = {
    "S": Direction(move=lambda x, y: (x, y + 1), counter="N"),
    "N": Direction(move=lambda x, y: (x, y - 1), counter="S"),
    "E": Direction(move=lambda x, y: (x + 1, y), counter="W"),
    "W": Direction(move=lambda x, y: (x - 1, y), counter="E"),
}
# set of all possible directions
DIRECTIONS = set(directions.keys())


# utility functions for calculations


def polygon_area(vertices: list[tuple]) -> float:
    """
    Calculates the area of a polygon using the Shoelace Algorithm.
    Source: www.101computing.net/the-shoelace-algorithm

    Parameters
    ----------
    vertices : list[tuple]
        List of vertices of the polygon.

    Returns
    -------
    float
        Area of the polygon.
    """
    numberOfVertices = len(vertices)
    sum1 = 0
    sum2 = 0

    for i in range(0, numberOfVertices - 1):
        sum1 = sum1 + vertices[i][0] * vertices[i + 1][1]
        sum2 = sum2 + vertices[i][1] * vertices[i + 1][0]

    sum1 = sum1 + vertices[numberOfVertices - 1][0] * vertices[0][1]
    sum2 = sum2 + vertices[0][0] * vertices[numberOfVertices - 1][1]

    area = abs(sum1 - sum2) / 2
    return area


def get_interior_point_number(area: float, n_vertices: int) -> int:
    """
    Calculates the number of interior points of a polygon using Pick's theorem.
    With Pick's theorem we can calculate the area of a polygon knowing the
    number of interior points and the number of vertices.
    Source: https://en.wikipedia.org/wiki/Pick%27s_theorem

    Parameters
    ----------
    area : float
        Area of the polygon.
    n_vertices : int
        Number of vertices of the polygon.

    Returns
    -------
    int
        Number of interior points of the polygon.
    """
    return int(area + 1 - n_vertices / 2)


class MapTraverser:
    """
    Class for traversing the map and finding the vertices of the polygon.
    Specific for the map from the problem.
    """

    def __init__(self, squares: list[str]) -> None:
        """
        Initializes the MapTraverser.

        Parameters
        ----------
        squares : list[str]
            List of strings each representing the map of one row from the input file.
        """
        self._start_x, self._start_y = self._get_starting_point(squares)
        self._squares = self._replace_starting_point(squares)

    def _get_starting_point(self, squares: list[str]) -> tuple[int, int]:
        """
        Finds the starting point on the map, represented by the unknown pipe marked "S".

        Parameters
        ----------
        squares : list[str]
            List of strings each representing the map of one row.

        Returns
        -------
        tuple[int, int]
            Tuple with coordinates of the starting point.
        """
        return next(
            (row.index(START), index) for index, row in enumerate(squares) if START in row
        )

    def _replace_starting_point(self, squares: list[str]) -> list[str]:
        """
        Replaces the starting point on the map with a pipe that can be connected
        with the pipes around it.

        Parameters
        ----------
        squares : list[str]
            List of strings each representing the map of one row.

        Returns
        -------
        list[str]
            List of strings each representing the map of one row with the starting
            point replaced.
        """
        x, y = self._start_x, self._start_y

        possible = set(connections.keys())

        for direction in directions.values():
            x, y = direction.move(self._start_x, self._start_y)
            element = squares[y][x]
            con = connections[element].get(direction.counter, set())
            possible = possible.intersection(con) or possible

        to_replace = next(iter(possible))
        squares[y] = squares[y].replace(START, to_replace)
        return squares

    def _is_move_valid(self, x: int, y: int, direction: str) -> bool:
        """
        Checks if the move to the next square with direction is valid.

        Parameters
        ----------
        x : int
            X coordinate of the current square.
        y : int
            Y coordinate of the current square.
        direction : str
            Direction to move to the next square.

        Returns
        -------
        bool
            True if the move int the direction is valid, False otherwise.
        """
        current = self._squares[y][x]
        new_x, new_y = directions[direction].move(x, y)
        try:
            next_ = self._squares[new_y][new_x]
            # if pipe on the possibly next square is conectable with the current pipe
            return next_ in connections[current].get(direction, set())
        except IndexError:
            # if out of map - return False
            return False

    def _get_next_move(self, x: int, y: int, exclude: Optional[str] = None) -> str:
        """
        Returns the next move from the current square.
        Based on assumption that going into one direction from current square
        there is only one possible move to the next square.

        Parameters
        ----------
        x : int
            X coordinate of the current square.
        y : int
            Y coordinate of the current square.
        exclude : str, optional
            Direction to exclude from the possible moves, by default None.
            None is only used when the function is called for the first time on
            the starting square. For each subsequent call, the direction that was
            used to get to the current square is excluded to avoid going back.

        Returns
        -------
        str
            Direction to move to the next square.

        Raises
        ------
        ValueError
            When no valid move is possible from the current square.
        """
        to_exclude = {exclude} if exclude is not None else set()

        for direction in DIRECTIONS - to_exclude:
            if self._is_move_valid(x=x, y=y, direction=direction):
                return direction

        raise ValueError(f"No valid move was possible from square ({x}, {y})")

    def get_vertices(self) -> list[tuple[int, int]]:
        """
        Returns a list of vertices of the polygon, based on provided list of lines
        from the input file and starting coordinates.

        Returns
        -------
        list[tuple[int, int]]
            List of vertices of the polygon with coordinates.
        """

        edges, direction, exclude = [], None, None
        x, y = self._start_x, self._start_y

        while not (self._start_x == x and self._start_y == y) or not len(edges):
            edges.append((x, y))
            direction = self._get_next_move(x=x, y=y, exclude=exclude)
            info = directions[direction]
            x, y = info.move(x, y)
            exclude = info.counter

        return edges


def main(part: PART, method: METHOD = "pick") -> int:
    """
    Calculates the solution to the problem from Day 10.

    Parameters
    ----------
    part : PART
        Part of the daily problem - 1 or 2.
    method : METHOD
        Method to use for 2 part solution - one of: 'pick' or 'matplotlib', by default "pick".

    Returns
    -------
    int
        Solution to the problem.
    """

    with open(INPUT, "r") as f:
        text = f.read()

    lines = text.strip("\n").split("\n")
    traverser = MapTraverser(lines)
    vertices = traverser.get_vertices()

    if part == 1:
        return int(len(vertices) / 2)

    elif part == 2:
        if method == "pick":
            area = polygon_area(vertices)
            n_vertices = len(vertices)
            return get_interior_point_number(area=area, n_vertices=n_vertices)

        elif method == "matplotlib":
            path = Path(vertices)  # type: ignore
            return sum(
                1
                for y in range(len(lines))
                for x in range(len(lines[0]))
                if path.contains_point((x, y)) and (x, y) not in vertices
            )
        else:
            raise ValueError(
                f"Unknown method: {method}, choose one of: 'pick' or 'matplotlib'"
            )

    else:
        raise ValueError(f"Unknown part: {part}, choose one of: 1 or 2")


def main(part: PART, method: METHOD = "pick") -> int:
    """
    Calculates the solution to the problem from Day 10.

    Parameters
    ----------
    part : PART
        Part of the daily problem - 1 or 2.
    method : METHOD
        Method to use for 2 part solution - one of: 'pick' or 'matplotlib', by default "pick".

    Returns
    -------
    int
        Solution to the problem.
    """

    with open(INPUT, "r") as f:
        text = f.read()

    lines = text.strip("\n").split("\n")
    traverser = MapTraverser(lines)
    vertices = traverser.get_vertices()

    if part == 1:
        return int(len(vertices) / 2)

    elif part == 2:
        if method == "pick":
            area = polygon_area(vertices)
            n_vertices = len(vertices)
            return get_interior_point_number(area=area, n_vertices=n_vertices)

        elif method == "matplotlib":
            path = Path(vertices)  # type: ignore
            return sum(
                1
                for y in range(len(lines))
                for x in range(len(lines[0]))
                if path.contains_point((x, y)) and (x, y) not in vertices
            )
        else:
            raise ValueError(
                f"Unknown method: {method}, choose one of: 'pick' or 'matplotlib'"
            )

    else:
        raise ValueError(f"Unknown part: {part}, choose one of: 1 or 2")


if __name__ == "__main__":
    args = parser.parse_args()
    result = main(part=args.part, method=args.method)
    print(result)

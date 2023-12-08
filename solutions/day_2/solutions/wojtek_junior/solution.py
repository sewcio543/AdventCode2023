"""Solution to the day 2 of Advent of Code"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from typing import Iterable, Literal

__author__ = "Wojtek Junior"

INPUT = "input.txt"
PART = Literal[1, 2]

parser = argparse.ArgumentParser(description="Part of the daily problem")
parser.add_argument(
    "-p",
    "--part",
    default=1,
    type=int,
    help="Part of the daily problem - 1 or 2",
)

# game suffix regex - to extract id of the game
SUFFIX = re.compile(r"^Game (\d+):")
# cube color regex - to extract color of the cube from move
COLOR = re.compile(r"(red|blue|green)")
# number of cubes of the color regex - to extract number of cubes of color from move
# extact the number form group 1 and color from group 2
NUMBER = re.compile(r"(\d+) (red|blue|green)")


@dataclass
class CubeGame:
    """
    Class representing a single game of cubes.

    Parameters
    ----------
    id : int
        Id of the game.
    moves : Iterable[CubesMove]
        Iterable of moves in the game.
    """

    id: int
    moves: Iterable[CubesMove]

    def is_possible(self, config: CubesMove) -> bool:
        """
        Checks if the game is possible to happend (all moves are possible to perform)
        if the configuration of cubes is given (with available number of cubes of each color).
        Game is not possible if any of the moves requires more cubes of any color
        than available in the configuration.

        Parameters
        ----------
        config : CubesMove
            CubesMove configuration to check against.

        Returns
        -------
        bool
            _description_
        """
        return all(move.is_possible(config) for move in self.moves)

    @property
    def power(self) -> int:
        """
        Calculates the power of the game.
        The power is the product of the minimum number of cubes of each color in the game
        to have to perform all the moves.

        Returns
        -------
        int
            Power of the game.
        """
        return (
            max(move.blue for move in self.moves)
            * max(move.red for move in self.moves)
            * max(move.green for move in self.moves)
        )


@dataclass
class CubesMove:
    """
    Class representing a single move of cubes.

    Parameters
    ----------
    blue : int
        Number of blue cubes.
    green : int
        Number of green cubes.
    red : int
        Number of red cubes.
    """

    blue: int = 0
    green: int = 0
    red: int = 0

    def is_possible(self, config: CubesMove) -> bool:
        """
        Checks if the move is possible to perform if the configuration of cubes is given.
        The move is not possible if it requires more cubes of any color
        than available in the configuration.

        Parameters
        ----------
        config : CubesMove
            CubesMove configuration with available number
            of cubes of each color to check against.

        Returns
        -------
        bool
            True if the move is possible to perform, False otherwise.
        """
        return (
            self.blue <= config.blue and self.green <= config.green and self.red <= config.red
        )


def get_game_id(line: str) -> int:
    """
    Extracts id of the game from the line.

    Parameters
    ----------
    line : str
        Line of the input file with game description.

    Returns
    -------
    int
        Id of the game as int.

    Raises
    ------
    ValueError
        If the line does not contain a proper suffix.
    """
    suffix = SUFFIX.search(line)

    if suffix is None:
        raise ValueError(f"Invalid line without a suffix: {line}")

    id_ = int(suffix.group(1))
    return id_


def get_move_dict(line: str) -> dict[str, int]:
    """
    Extracts dict with number of cubes of each color from the line.

    Parameters
    ----------
    line : str
        Line of the input file with move description.

    Returns
    -------
    dict[str, int]
        Dict with number of cubes of each color.
    """
    return {
        COLOR.search(cube).group(0): int(NUMBER.search(cube).group(1))  # type: ignore
        for cube in line.split(",")
    }


def get_game(line: str) -> CubeGame:
    """
    Extracts CubeGame from the line.

    Parameters
    ----------
    line : str
        Line of the input file with game description.

    Returns
    -------
    CubeGame
        CubeGame object representing the single game from line of input.
    """
    id_ = get_game_id(line)
    moves = [CubesMove(**get_move_dict(move)) for move in line.split(";")]
    return CubeGame(id=id_, moves=moves)


def main(part: PART) -> int:
    """
    Calculates the solution to the problem from Day 2.

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

    games = [get_game(line) for line in lines]

    if part == 1:
        return sum(game.id for game in games if game.is_possible(CONFIG))

    elif part == 2:
        return sum(game.power for game in games)

    else:
        raise ValueError(f"Invalid part of the problem: '{part}', must be 1 or 2.")


# global configuration of cubes to check against - for 1 part of the problem
# available number of cubes of each color - 14 blue, 13 green, 12 red
CONFIG = CubesMove(blue=14, green=13, red=12)


if __name__ == "__main__":
    args = parser.parse_args()
    result = main(part=args.part)
    print(result)

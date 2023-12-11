import argparse
import os
import re
from typing import Iterable
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

PATH = os.path.join(os.path.dirname(__file__), "input.txt")

__author__ = "Rafal"

REGEX = {
    "GAME_ID": re.compile(r"\d+(?=:)"),
    "TURN": re.compile(r"(\d+\s*[a-zA-Z]+(?:\s*,\s*\d+\s*[a-zA-Z]+)*)"),
    "COLOR": re.compile(r"(\d+)\s*([a-zA-Z]+)"),
}

parser = argparse.ArgumentParser(description="Part of the daily problem")
parser.add_argument(
    "-p",
    "--part",
    default=1,
    type=int,
    help="Part of the daily problem - 1 or 2",
)


class Validator(ABC):
    @abstractmethod
    def validate(self) -> bool:
        pass


class Part1Validator:
    def validate(self, obj) -> bool:
        return all(
            [
                obj.red <= 12,
                obj.blue <= 14,
                obj.green <= 13,
            ]
        )


class Turn:
    red: int = 0
    blue: int = 0
    green: int = 0
    validator: Validator = Part1Validator()

    def __init__(self, text: str, validator: Validator = Part1Validator()):
        self.validator = validator
        parts = [item.split() for item in text.split(", ")]
        [setattr(self, color.lower(), int(value)) for value, color in parts]

    def __repr__(self) -> str:
        return f"Turn: red: {self.red}, blue: {self.blue}, green: {self.green}"

    def validate(self) -> bool:
        return self.validator.validate(self)


class Game:
    _id: int
    turns: list[Turn]

    def __init__(self, text: str, validator: Validator = Part1Validator()):
        self._id = re.search(REGEX["GAME_ID"], text).group(0)
        self._validator = validator
        self._turns = self.parse_turns(text)

    @property
    def id(self):
        return int(self._id)

    def parse_turns(self, text: str) -> list[Turn]:
        return list(
            map(lambda x: Turn(x, validator=self._validator), re.findall(REGEX["TURN"], text))
        )

    def validate(self) -> bool:
        return all([turn.validate() for turn in self._turns])

    def get_power(self) -> int:
        return (
            max(x.red for x in self._turns)
            * max(x.blue for x in self._turns)
            * max(x.green for x in self._turns)
        )

    def __repr__(self) -> str:
        return f"Game {self._id}, Turns: {self._turns}"


def main(part: int = 2):
    with open(PATH) as f:
        lines = list(map(lambda x: Game(x), f.readlines()))
        match part:
            case 1:
                print(sum([game.id for game in lines if game.validate()]))
            case 2:
                print(sum(game.get_power() for game in lines))


if __name__ == "__main__":
    tic = time.perf_counter()
    args = parser.parse_args()
    main(part=args.part)
    print(f"Time elapsed: {time.perf_counter() - tic:0.8f} seconds")

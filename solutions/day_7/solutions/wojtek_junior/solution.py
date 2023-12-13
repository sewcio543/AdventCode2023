"""Solution to the day 7 of Advent of Code"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from typing import Literal, Optional

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


@dataclass
class GameSettigns:
    """
    Dataclass containing information about the game, such as
    * order of cards
    * card considered as joker in the game (if any)

    Parameters
    ----------
    order : list[str]
        List of cards in order of their weight in the game.
        Used for comparison between hands if their figures are the same.
    joker : Optional[str], optional
        Card considered as joker in the game, by default None
    """

    order: list[str]
    joker: Optional[str] = None


JOKER = "J"

SETUPS: dict[int, GameSettigns] = {
    1: GameSettigns(
        order=["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"],
        joker=None,
    ),
    2: GameSettigns(
        order=["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"],
        joker=JOKER,
    ),
}


def split_line(line: str) -> tuple[list[str], int]:
    """
    Splits line from input file into list of cards and bid for hand.

    Parameters
    ----------
    line : str
        Single line from input file.

    Returns
    -------
    tuple[list[str], int]
        Tuple containing list of cards and bid for hand in that order.
    """
    cards, bid = line.split(" ")
    return list(cards), int(bid)


@dataclass
class Hand:
    """
    Class representing single hand in the game.

    Parameters
    ----------
    cards : list[str]
        List of cards in hand.
    bid : int
        Bid for hand.
    settings : GameSettigns
        Settings of the game, dataclass containing information about order of cards
        and card that is a joker in the game (if any).
    """

    cards: list[str]
    bid: int
    settings: GameSettigns

    def __post_init__(self) -> None:
        """Sets up hand protected attributes after initialization."""

        # counter of how many cards of each kind are in hand
        cards_count = Counter(self.cards)

        # if joker is enabled and there are cards other than joker in hand
        if self.settings.joker is not None and not all(card == JOKER for card in self.cards):
            # remove jokers if exist from cards count and get number of jokers in hand
            jokers = cards_count.pop(JOKER, 0)

            if cards_count:
                # jokers are replaced by most common card in hand to maximize the score
                most_common = max(cards_count.keys(), key=cards_count.__getitem__)
                cards_count[most_common] += jokers

        self._counter = Counter(cards_count.values())
        self._cards_count = cards_count

    @property
    def encoded(self) -> str:
        """
        Encodes hand into string representation that is used to compare hands.
        String is of number of cards length.
        For each combination in hand of 4 cards - each char represents number of cards
        that have x number of occurrences in hand:
        * {'Q': 4}  -> '1000'
        * {'Q': 3, 'K': 1}  in hand -> '0101'
        * {'Q': 2, 'K': 2} in hand -> '0020'
        * {'Q': 2, 'K': 1, 'A': 1} in hand -> '0012'
        * {'Q': 1, 'K': 1, 'A': 1, 'J': 1} in hand -> '0004'

        Encoded strings for different hands can be the same and are not conclusive
        in case of comparing hands. In such case, order of cards factors in.
        See '__gt__' method.

        Returns
        -------
        str
            Encoded string representation of hand.
        """
        return "".join([str(self._counter.get(x, 0)) for x in range(len(self.cards), 0, -1)])

    def __gt__(self, other: Hand) -> bool:
        if self.encoded == other.encoded:
            # hand has the same figures - check thier weight
            return self._gt_order(other)

        return self.encoded > other.encoded

    def _gt_order(self, other: Hand) -> bool:
        """Compares hands based on thier weights in case of equal figures."""
        for card1, card2 in zip(self.cards, other.cards):
            if card1 == card2:
                continue
            return self.settings.order.index(card1) < self.settings.order.index(card2)
        raise ValueError("Equal hands")


def main(part: PART) -> int:
    """
    Calculates the solution to the problem from Day 7.

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
        lines = map(lambda line: line.strip("\n"), f.readlines())

    setup = SETUPS[part]
    hands = [Hand(*split_line(line), settings=setup) for line in lines]
    return sum(hand.bid * index for index, hand in enumerate(sorted(hands), start=1))


if __name__ == "__main__":
    args = parser.parse_args()
    result = main(part=args.part)
    print(result)

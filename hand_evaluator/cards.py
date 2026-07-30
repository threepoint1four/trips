# cards taken in the form of "AH" (Ace of Hearts), "2D" (Two of Diamonds), etc.

from enum import Enum, IntEnum
from typing import List


class Suit(Enum):
    HEARTS = "H"
    DIAMONDS = "D"
    CLUBS = "C"
    SPADES = "S"


class Rank(IntEnum):
    """Card ranks in poker (2-Ace)"""
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Card:
    """Represents a single playing card"""
    
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit
    
    def __repr__(self) -> str:
        rank_str = {
            Rank.TWO: "2",
            Rank.THREE: "3",
            Rank.FOUR: "4",
            Rank.FIVE: "5",
            Rank.SIX: "6",
            Rank.SEVEN: "7",
            Rank.EIGHT: "8",
            Rank.NINE: "9",
            Rank.TEN: "T",
            Rank.JACK: "J",
            Rank.QUEEN: "Q",
            Rank.KING: "K",
            Rank.ACE: "A"
        }
        return (rank_str[self.rank] + self.suit.value)

    def __eq__(self, other) -> bool:
        if (not isinstance(other, Card)):
            return NotImplemented
        return (self.rank == other.rank and self.suit == other.suit)

    def __lt__(self, other) -> bool:
        if (not isinstance(other, Card)):
            return NotImplemented
        return self.rank.value < other.rank.value

    @classmethod
    def from_string(cls, card_str: str) -> 'Card':
        """Create a Card instance from a string like 'AH' or '2D'."""
        rank_map = {
            "2": Rank.TWO,
            "3": Rank.THREE,
            "4": Rank.FOUR,
            "5": Rank.FIVE,
            "6": Rank.SIX,
            "7": Rank.SEVEN,
            "8": Rank.EIGHT,
            "9": Rank.NINE,
            "10": Rank.TEN,
            "T": Rank.TEN,
            "J": Rank.JACK,
            "Q": Rank.QUEEN,
            "K": Rank.KING,
            "A": Rank.ACE,
        }
        suit_map = {
            "H": Suit.HEARTS,
            "D": Suit.DIAMONDS,
            "C": Suit.CLUBS,
            "S": Suit.SPADES,
        }
        rank_text = card_str[:-1].upper()
        suit_char = card_str[-1].upper()
        return cls(rank_map[rank_text], suit_map[suit_char])

    @classmethod
    def hand_from_listofstrings(cls, card_strs: List[str]) -> 'Hand':
        list_of_cards = [cls.from_string(card_str) for card_str in card_strs]
        return Hand(list_of_cards)


class Hand:
    """Represents a 5-card poker hand"""
    
    def __init__(self, cards: List[Card]):
        if len(cards) != 5:
            raise ValueError("A hand must consist of exactly 5 cards.")
        self.cards = sorted(cards, reverse=True)  # Sort cards by rank descending
    
    def get_ranks(self) -> List[int]:
        return [card.rank.value for card in self.cards]
    
    def get_suits(self) -> List[str]:
        return [card.suit.value for card in self.cards]


    
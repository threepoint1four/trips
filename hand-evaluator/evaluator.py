from enum import Enum, IntEnum
from typing import Tuple, List
from cards import Card, Hand, Rank, Suit


class HandRank(IntEnum):
    ROYAL_FLUSH = 10
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class HandEvaluator:
    """Evaluates and ranks poker hands"""
    
    @staticmethod
    def evaluate(hand: Hand) -> Tuple[HandRank, Tuple]:
        """
        Evaluate a 5-card hand and return its rank type and tiebreaker values.
        
        Returns:
            Tuple of (HandRank enum, tuple of tiebreaker values)
            e.g., (HandRank.PAIR, (13, 12, 11, 10))  # Pair of Aces with K, Q, J kickers
        """
        # check pairs + trips + quads
        # i realize some hands do not need kickers but fuck that
        # i'll just return it anyways; what if the casino sneaks in a few extra cards... you never know!
        rank_counts = HandEvaluator.get_rank_counts(hand)
        if 4 in rank_counts.values():
            return [HandRank.FOUR_OF_A_KIND, (max(k for k, v in rank_counts.items() if v == 4),)]
        elif sorted(list(rank_counts.values())) == [2, 3]:
            return [HandRank.FULL_HOUSE, (max(k for k, v in rank_counts.items() if v == 3), max(k for k, v in rank_counts.items() if v == 2))]
        elif 3 in rank_counts.values():
            return [HandRank.THREE_OF_A_KIND, (max(k for k, v in rank_counts.items() if v == 3),)]
        elif list(rank_counts.values()).count(2) == 2:
            return [HandRank.TWO_PAIR, tuple(sorted([k for k, v in rank_counts.items() if v == 2], reverse=True))]
        elif 2 in rank_counts.values():
            return [HandRank.ONE_PAIR, (max(k for k, v in rank_counts.items() if v == 2),)]

        # check flush & straight
        flush_checker = HandEvaluator.is_flush(hand)
        straight_checker = HandEvaluator.is_straight(hand)

        # returns for royal flush, straight flush, flush, 
        
        if (HandEvaluator.is_flush(hand) and HandEvaluator.is_straight(hand)[0] and HandEvaluator.is_straight(hand)[1] == 14):
            return [HandRank.ROYAL_FLUSH, [1e9]]
        elif (HandEvaluator.is_flush(hand) and HandEvaluator.is_straight(hand)[0]):
            return [HandRank.STRAIGHT_FLUSH, (HandEvaluator.is_straight(hand)[1],)]
        elif (HandEvaluator.is_flush(hand) and not HandEvaluator.is_straight(hand)[0]):
            return [HandRank.FLUSH, tuple(sorted([k for k in rank_counts.keys()], reverse=True))]
        elif (not HandEvaluator.is_flush(hand) and HandEvaluator.is_straight(hand)[0]):
            return [HandRank.STRAIGHT, (HandEvaluator.is_straight(hand)[1],)]

        # if none of the above cases are satisfied, return high card with sorted kickers
        return [HandRank.HIGH_CARD, tuple(sorted([k for k in rank_counts.keys()], reverse=True))]

    @staticmethod
    def is_flush(hand: Hand) -> bool:
        """
        Check if the hand is a flush

        Returns: True/False

        """
        list_of_suits = hand.get_suits()
        return len(set(list_of_suits)) == 1
    
    @staticmethod
    def is_straight(hand: Hand) -> Tuple[bool, int]:
        """
        Check if the hand is a straight.
        
        Returns:
            Tuple of (True/False, Kicker Rank)
        """
        ranks = hand.get_ranks()
        ranks.sort()
        # Handle Ace-low straight (A-2-3-4-5)
        if ranks == [2, 3, 4, 5, 14]:  # Ace is high (14) but can be low in this case
            return True, 5
        for i in range(4):
            if (ranks[i] + 1 != ranks[i + 1]):
                return False, -1
        return True, ranks[-1]
    
    @staticmethod
    def get_rank_counts(hand: Hand) -> dict:
        """
        Count occurrences of each rank.
        
        Returns:
            Dict mapping rank -> count, e.g., {13: 2, 12: 1, 11: 1, 10: 1}
        """
        rank_counts = {}
        for card in hand.cards:
            rank_counts[card.rank.value] = rank_counts.get(card.rank.value, 0) + 1
        return rank_counts
    
    @staticmethod
    def compare_hands(hand1: Hand, hand2: Hand) -> int:
        """
        Compare two hands.
        
        Returns:
            1 if hand1 is better
            -1 if hand2 is better
            0 if hands are equal
        """
        hr1 = HandEvaluator.evaluate(hand1)[0]
        hr2 = HandEvaluator.evaluate(hand2)[0]
        if (hr1>hr2):
            return 1
        elif (hr1<hr2):
            return -1
        else: 
            # If hand ranks are equal, compare tiebreakers
            tiebreaker1 = HandEvaluator.evaluate(hand1)[1]
            tiebreaker2 = HandEvaluator.evaluate(hand2)[1]
            if tiebreaker1 > tiebreaker2:
                return 1
            elif tiebreaker1 < tiebreaker2:
                return -1
            else:
                return 0


def parse_card(card_str: str) -> Card:
    """
    Parse a card string like 'AH' (Ace of Hearts) into a Card object.
    Supports formats: AH, 2D, KS, 10C, etc.
    """
    return Card.from_string(card_str)
    # yeah this does the same thing as from_string but whatever, it's probably a bit nicer


def find_best_hand(community_cards: List[Card], hole_cards: List[Card]) -> Hand:
    """
    Given 5 community cards and 2 hole cards (7 total), find the best 5-card hand.
    """
    from itertools import combinations
    card_selection = community_cards + hole_cards
    best_hand = None
    for combination in combinations(card_selection, 5):
        hand = Hand(list(combination))
        if ((best_hand is None) or (HandEvaluator.compare_hands(hand, best_hand) == 1)):
            best_hand = hand
    return best_hand



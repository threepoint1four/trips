import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from hand_evaluator.cards import Card, Rank, Suit, Hand
from hand_evaluator.evaluator import HandEvaluator, find_best_hand

def calculate_odds(hole_cards: list[Card], community_cards: list[Card]):
    wins = 0
    total = 0
    personal_best = find_best_hand(community_cards, hole_cards)
    for _ in range(10000000):
        #initialize random opponent hands
        a = random.choice([Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE])
        b = random.choice([Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE])
        suit_a = random.choice([Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES])
        suit_b = random.choice([Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES])
        opponent_hole_cards = [Card(a, suit_a), Card(b, suit_b)]
        opponent_best = find_best_hand(community_cards, opponent_hole_cards)
        if HandEvaluator.compare_hands(personal_best, opponent_best) == 1:
            wins += 1
        total += 1
    return wins / total

def main():
    hole_input = input("Enter your hole cards (e.g., 'AH KH' for Ace of Hearts and King of Hearts): ")
    hole_cards = [Card.from_string(card_str) for card_str in hole_input.split()]
    community_input = input("Enter the community cards (e.g., '2D 3C 4H' for 2 of Diamonds, 3 of Clubs, and 4 of Hearts): ")
    community_cards = [Card.from_string(card_str) for card_str in community_input.split()]
    odds = calculate_odds(hole_cards, community_cards)
    print(f"Estimated odds of winning: {odds:.1%}")


if __name__ == "__main__":
    main()


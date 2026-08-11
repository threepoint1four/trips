import os
import sys
import random
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from hand_evaluator.cards import Card, Rank, Suit, Hand
from hand_evaluator.evaluator import HandEvaluator, find_best_hand
from itertools import combinations

def calculate_odds(hole_cards: list[Card], community_cards: list[Card]):
    wins = 0
    total = 0

    if (len(community_cards) == 5):
        personal_best = find_best_hand(community_cards, hole_cards)
        deck = [Card(rank, suit) for rank in Rank for suit in Suit]
        for card in community_cards + hole_cards:
            if card in deck:
                deck.remove(card)
        for card1, card2 in combinations(deck, 2):
            if (card1 != card2):
                opponent_hole_cards = [card1, card2]
                opponent_best = find_best_hand(community_cards, opponent_hole_cards)
                if HandEvaluator.compare_hands(personal_best, opponent_best) == 1:
                    wins += 1
                total += 1

    if (len(community_cards) < 5):
        # If there are fewer than 5 community cards, we need to simulate the remaining community cards
        needed = 5 - len(community_cards)
        deck = [Card(rank, suit) for rank in Rank for suit in Suit]
        for card in community_cards + hole_cards:
            if card in deck:
                deck.remove(card)

        # Generate all combinations of the remaining community cards
        for additional in combinations(deck, needed):
            complete = community_cards + list(additional)
            personal_best = find_best_hand(complete, hole_cards)
            available_deck = [card for card in deck if card not in complete]

            # Now simulate opponent hands
            for card1, card2 in combinations(available_deck, 2):
                if (card1 != card2):
                    opponent_hole_cards = [card1, card2]
                    opponent_best = find_best_hand(complete, opponent_hole_cards)
                    if HandEvaluator.compare_hands(personal_best, opponent_best) == 1:
                        wins += 1
                    total += 1
    return wins / total

def main():
    hole_input = input("Enter your hole cards (e.g., 'AH KH' for Ace of Hearts and King of Hearts): ")
    hole_cards = [Card.from_string(card_str) for card_str in hole_input.split()]
    community_input = input("Enter the community cards (e.g., '2D 3C' for 2 of Diamonds and 3 of Clubs): ")
    community_cards = [Card.from_string(card_str) for card_str in community_input.split()]
    start = time.time()
    odds = calculate_odds(hole_cards, community_cards)
    end = time.time()
    print(f"Exact odds of winning: {odds:.3%}")
    print(f"Calculation took {end - start:.3f} seconds.")


if __name__ == "__main__":
    main()


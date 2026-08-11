import os
import sys
import random
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from hand_evaluator.cards import Card, Rank, Suit, Hand
from hand_evaluator.evaluator import HandEvaluator, find_best_hand

def calculate_odds(hole_cards: list[Card], community_cards: list[Card]):
    wins = 0
    total = 0
    for _ in range(10000):
        complete_community_cards = community_cards[:]
        deck = [Card(rank, suit) for rank in Rank for suit in Suit]
        for card in community_cards + hole_cards:
            if card in deck:
                deck.remove(card)
        needed = 5 - len(community_cards)
        for _ in range(needed):
            x = random.choice(deck)
            deck.remove(x)
            complete_community_cards.append(x)
        c1 = random.choice(deck)
        deck.remove(c1)
        c2 = random.choice(deck)
        deck.remove(c2)
        opponent_hole_cards = [c1, c2]
        personal_best = find_best_hand(complete_community_cards, hole_cards)
        opponent_best = find_best_hand(complete_community_cards, opponent_hole_cards)
        if HandEvaluator.compare_hands(personal_best, opponent_best) == 1:
            wins += 1
        total += 1
    return wins / total

def main():
    hole_input = input("Enter your hole cards (e.g., 'AH KH' for Ace of Hearts and King of Hearts): ")
    hole_cards = [Card.from_string(card_str) for card_str in hole_input.split()]
    community_input = input("Enter the community cards (e.g., '2D 3C 4H' for 2 of Diamonds, 3 of Clubs, and 4 of Hearts): ")
    community_cards = [Card.from_string(card_str) for card_str in community_input.split()]
    start = time.time()
    odds = calculate_odds(hole_cards, community_cards)
    end = time.time()
    print(f"Estimated odds of winning: {odds:.3%}")
    print(f"Calculation took {end - start:.3f} seconds.")


if __name__ == "__main__":
    main()


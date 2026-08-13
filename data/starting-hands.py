import csv
import random
import sys
import os
import time
from itertools import combinations

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from hand_evaluator.cards import Card, Rank, Suit
from odds_evaluator.exact_odds import exact_odds
from odds_evaluator.monte_carlo import estimate_odds

fields = ["hole_cards", "win_probability"]

output_path = os.path.join(os.path.dirname(__file__), "starting-hand-equities.csv")

with open(output_path, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=fields)
    writer.writeheader()
    start_time = time.time()
    poss_suits = [Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES]
    deck = [Card(rank, suit) for rank in Rank for suit in poss_suits]
    for card1 in deck:
        for card2 in deck:
            if (card1.rank == card2.rank and card1.suit == card2.suit):
                continue
            hole_cards = [card1, card2]
            community_cards = []
            odds = estimate_odds(hole_cards, community_cards, 100000)
            writer.writerow({
                "hole_cards": " ".join(str(card) for card in hole_cards),
                "win_probability": odds,
            })
    elapsed = time.time() - start_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    print(f"Data generation completed in {hours} hours, {minutes} minutes and {seconds} seconds.")
        
        




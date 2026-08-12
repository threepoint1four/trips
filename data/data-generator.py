import csv
import random
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from hand_evaluator.cards import Card, Rank, Suit
from odds_evaluator.exact_odds import exact_odds

fields = ["hole_cards", "community_cards", "win_probability"]

output_path = os.path.join(os.path.dirname(__file__), "dataset.csv")

with open(output_path, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=fields)
    writer.writeheader()
    start_time = time.time()
    main_deck = [Card(rank, suit) for rank in Rank for suit in Suit]
    for _ in range(1000):
        deck = main_deck[:]
        num_community_cards = random.choice([3, 4, 5])
        community_cards = random.sample(deck, num_community_cards)
        remaining_deck = [card for card in deck if card not in community_cards]
        hole_cards = random.sample(remaining_deck, 2)
        odds = exact_odds(hole_cards, community_cards)
        writer.writerow({
            "hole_cards": " ".join(str(card) for card in hole_cards),
            "community_cards": " ".join(str(card) for card in community_cards),
            "win_probability": odds,
        })
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    print(f"Data generation completed in {minutes} minutes and {seconds} seconds.")



        
        




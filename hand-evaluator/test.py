from cards import Card, Hand, Rank, Suit
from evaluator import HandEvaluator, HandRank


hand1 = Hand([Card.from_string(card_str) for card_str in input("Input 5 cards for the first hand: ").split()])
[hand_rank, tiebreaker] = HandEvaluator.evaluate(hand1)
rank_name = hand_rank.name.replace("_", " ").title()
print(f"Hand: {', '.join(str(card) for card in hand1.cards)}")
print(f"Rank: {rank_name}")
print(f"Tiebreaker: {tiebreaker}")

hand2 = Hand([Card.from_string(card_str) for card_str in input("Input 5 cards for the second hand: ").split()])
[hand_rank, tiebreaker] = HandEvaluator.evaluate(hand2)
rank_name2 = hand_rank.name.replace("_", " ").title()
print(f"Hand: {', '.join(str(card) for card in hand2.cards)}")
print(f"Rank: {rank_name2}")
print(f"Tiebreaker: {tiebreaker}")

checker = HandEvaluator.compare_hands(hand1, hand2)
if (checker):
    print("Hand 1 wins!" + (f" ({rank_name} beats {rank_name2})"))
elif (checker == -1):
    print("Hand 2 wins!" + (f" ({rank_name2} beats {rank_name})"))
else:
    print("It's a tie!" + (f" Both hands are a {rank_name} :) "))

        


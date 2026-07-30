from cards import Card, Hand, Rank, Suit
from evaluator import HandEvaluator, find_best_hand, parse_card

# two hand comparison test

"""

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
if (checker == 1):
    print("Hand 1 wins!" + (f" ({rank_name} beats {rank_name2})"))
elif (checker == -1):
    print("Hand 2 wins!" + (f" ({rank_name2} beats {rank_name})"))
else:
    print("It's a tie!" + (f" Both hands are a {rank_name} :) "))

"""

# best hand finder test with 1 person
"""
community_cards = [Card.from_string(card_str) for card_str in input("Input 5 community cards: ").split()]
hole_cards = [Card.from_string(card_str) for card_str in input("Input 2 hole cards: ").split()]
best_hand = find_best_hand(community_cards, hole_cards)
hand_rank, tiebreaker = HandEvaluator.evaluate(best_hand)
print(f"Best Hand: {', '.join(str(card) for card in best_hand.cards)}")
print(f"Rank: {hand_rank.name.replace('_', ' ').title()} with tiebreaker(s): {tiebreaker}")

"""

# best hand finder test with multiple players
community_cards = [Card.from_string(card_str) for card_str in input("Input 5 community cards: ").split()]
num_players = int(input("Input number of players: "))
hole_card_list = []
for i in range (num_players):
    hole_cards = [Card.from_string(card_str) for card_str in input(f"Input player {i+1}'s cards: ").split()]
    hole_card_list.append(hole_cards)
optimal_hands = [find_best_hand(community_cards, hole_cards) for hole_cards in hole_card_list]

evaluations = [HandEvaluator.evaluate(hand) for hand in optimal_hands]
best_eval = evaluations[0]
winning_indices = [0]

for index in range(1, len(evaluations)):
    current_eval = evaluations[index]
    comparison = HandEvaluator.compare_hands(optimal_hands[index], optimal_hands[winning_indices[0]])
    if comparison == 1:
        best_eval = current_eval
        winning_indices = [index]
    elif comparison == 0:
        winning_indices.append(index)

if len(winning_indices) == 1:
    # one winner
    winner_index = winning_indices[0]
    hand_rank, tiebreaker = evaluations[winner_index]
    rank_name = hand_rank.name.replace("_", " ").title()
    print(f"Player {winner_index + 1} wins with hand: {', '.join(str(card) for card in optimal_hands[winner_index].cards)}")
    print(f"Rank: {rank_name} | Tiebreaker: {tiebreaker}")
else:
    # handle ties
    winners_list = [index + 1 for index in winning_indices]
    hand_rank, tiebreaker = evaluations[winning_indices[0]]
    rank_name = hand_rank.name.replace("_", " ").title()
    print(f"Players {', '.join(str(winner) for winner in winners_list)} tie with hand rank: {rank_name}")
    print(f"Tiebreaker: {tiebreaker}")

    

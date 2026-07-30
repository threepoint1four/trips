import os
import random
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from hand_evaluator.cards import Card, Rank, Suit
from player import Player


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Rank for suit in Suit]
        self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self, num_cards) -> list[Card]:
        self.shuffle()
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards left in the deck to deal.")
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards


class Game:
    def __init__(self, players):
        self.players = players
        self.community_cards = []
        self.pot = 0
        self.current_round = 0  # 0: Pre-flop, 1: Flop, 2: Turn, 3: River
        self.active_players = list(players)

    def deal_hole_cards(self, deck) -> None:
        for player in self.players:
            player.receive_cards(deck.deal(2))

    def deal_flop(self, deck) -> None:
        self.community_cards.extend(deck.deal(3))

    def deal_turn(self, deck) -> None:
        self.community_cards.extend(deck.deal(1))

    def deal_river(self, deck) -> None:
        self.community_cards.extend(deck.deal(1))

    def betting_round(self, interactive: bool = True) -> None:
        self.active_players = [player for player in self.players if not player.folded]
        if not self.active_players:
            return

        active_bet = 0
        for position in range(len(self.active_players)):
            current_player = self.active_players[position]
            if current_player.folded:
                continue

            print("Your current cards are: ")
            print(current_player.hole_cards)
            if active_bet > 0 and current_player.current_bet < active_bet:
                if interactive:
                    input(f"{current_player.name}, it's your turn. Press Enter to continue...")
                    bet_amount = input("Enter the amount to bet. 0 to fold, or any positive amount to bet: ")
                    if int(bet_amount) == 0:
                        current_player.fold()
                        print(f"{current_player.name} has folded.")
                    elif int(bet_amount) > 0 and int(bet_amount) + current_player.current_bet >= active_bet:
                        current_player.bet(int(bet_amount))
                        self.pot += int(bet_amount)
                        active_bet = current_player.current_bet
                        print(f"{current_player.name} has bet {bet_amount}. Current pot is {self.pot}.")
                    else:
                        print(f"{current_player.name} cannot bet less than the active bet of {active_bet}. Please try again.")
                        position -= 1
                else:
                    call_amount = active_bet - current_player.current_bet
                    if current_player.chips <= 0:
                        current_player.fold()
                        print(f"{current_player.name} has folded.")
                    elif call_amount <= current_player.chips:
                        current_player.bet(call_amount)
                        self.pot += call_amount
                        active_bet = current_player.current_bet
                        print(f"{current_player.name} calls for {call_amount}.")
                    else:
                        current_player.bet(current_player.chips)
                        self.pot += current_player.chips
                        current_player.all_in = True
                        active_bet = current_player.current_bet
                        print(f"{current_player.name} goes all-in.")
            else:
                if interactive:
                    input(f"{current_player.name}, it's your turn. Press Enter to continue...")
                    bet_amount = input("Enter the amount to bet. 0 to fold, -1 to check, or any positive amount to bet: ")
                    if int(bet_amount) == 0:
                        current_player.fold()
                        print(f"{current_player.name} has folded.")
                    elif int(bet_amount) == -1:
                        print(f"{current_player.name} has checked.")
                    elif int(bet_amount) > 0:
                        current_player.bet(int(bet_amount))
                        self.pot += int(bet_amount)
                        active_bet = current_player.current_bet
                        print(f"{current_player.name} has bet {bet_amount}. Current pot is {self.pot}, and the active bet is {active_bet}.")
                    else:
                        print("Error, please try again")
                        position -= 1
                else:
                    print(f"{current_player.name} checks.")

"""
# wrong logic, only gives 1 winner

    def showdown_winner(self) -> Player:
        for player in self.active_players:
            player.evaluate_best_hand(self.community_cards)
        # Return the player object with the best hand
        winner = max(self.active_players, key=lambda p: (p.best_hand_rank, p.best_hand_tiebreaker))
        print(f"{winner.name} wins {self.pot} with hand {winner.best_hand}")
        return winner

"""

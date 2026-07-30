import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)

from hand_evaluator.evaluator import HandEvaluator
from game import Deck, Game
from player import Player


class PokerEngine:
    def __init__(self, player_names, starting_chips=1000, ante=10):
        self.players = [Player(name, starting_chips) for name in player_names]
        self.ante = ante
        self.community_cards = []
        self.pot = 0
        self.deck = None
        self.game = None
        self.current_round = "preflop"

    def reset(self):
        for player in self.players:
            player.reset_for_new_round()
        self.community_cards = []
        self.pot = 0
        self.current_round = "preflop"
        self.deck = Deck()
        self.game = Game(self.players)

    def post_ante(self):
        for player in self.players:
            player.bet(self.ante)
            self.pot += self.ante
        self.game.pot = self.pot

    def deal_hole_cards(self):
        self.game.deal_hole_cards(self.deck)
        self.community_cards = self.game.community_cards

    def deal_community_cards(self, count):
        if count == 3:
            self.game.deal_flop(self.deck)
        elif count == 1:
            if len(self.game.community_cards) == 3:
                self.game.deal_turn(self.deck)
            else:
                self.game.deal_river(self.deck)
        self.community_cards = self.game.community_cards
        return self.community_cards

    def run_betting_round(self, interactive: bool):
        self.game.active_players = [player for player in self.players if not player.folded]
        if (len(self.game.active_players)==1):
            self.game.active_players[0].chips+=self.pot
            print(f"Winner! " + self.game.active_players[0].name() + " has won {self.pot} chips.")
        else:
            self.game.pot = self.pot
            self.game.betting_round(interactive=True)
            self.pot = self.game.pot
            print("The following community cards are: ")
            print([x for x in self.game.community_cards])

    def evaluate_hands(self):
        for player in self.players:
            if not player.folded:
                player.evaluate_best_hand(self.community_cards)

    def determine_winners(self):
        active_players = [player for player in self.players if not player.folded and player.best_hand is not None]
        if not active_players:
            return []

        winners = [active_players[0]]
        best_player = active_players[0]

        for player in active_players[1:]:
            result = HandEvaluator.compare_hands(player.best_hand, best_player.best_hand)
            if result == 1:
                best_player = player
                winners = [player]
            elif result == 0:
                winners.append(player)

        return winners

    def play_hand(self):
        self.reset()
        self.post_ante()
        self.deal_hole_cards()
        self.current_round = "preflop"
        self.run_betting_round(interactive=True)

        self.deal_community_cards(3)
        self.current_round = "flop"
        self.run_betting_round(interactive=True)

        self.deal_community_cards(1)
        self.current_round = "turn"
        self.run_betting_round(interactive=True)

        self.deal_community_cards(1)
        self.current_round = "river"
        self.run_betting_round(interactive=True)

        self.evaluate_hands()
        winners = self.determine_winners()
        return {
            "community_cards": self.community_cards,
            "pot": self.pot,
            "winners": winners,
            "players": self.players,
        }

    def play_many_hands(self, hands=1):
        results = []
        for _ in range(hands):
            results.append(self.play_hand())
        return results

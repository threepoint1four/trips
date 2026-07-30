from hand_evaluator.cards import Card
from hand_evaluator.evaluator import HandEvaluator, find_best_hand

class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.current_bet = 0
        self.hole_cards = []
        self.best_hand = None
        self.best_hand_rank = None
        self.best_hand_tiebreaker = None
        self.folded = False
        self.all_in = False
        self.position = 0

    def __str__(self):
        return f"Player {self.name}: Chips={self.chips}, Current Bet={self.current_bet}, Hole Cards={[str(card) for card in self.hole_cards]}, Best Hand={self.best_hand}, Folded={self.folded}, All In={self.all_in}, Position={self.position}"
    
    def receive_cards(self, cards) -> None:
        self.hole_cards = cards
        self.best_hand = None  # reset best hand when new cards are received

    def reset_for_new_round(self) -> None:
        self.current_bet = 0
        self.hole_cards = []
        self.best_hand = None
        self.folded = False
        self.all_in = False

    def fold(self) -> None:
        self.folded = True

    def bet(self, amount) -> None:
        if amount > self.chips:
            raise ValueError(f"{self.name} does not have enough chips to bet {amount}.")
        self.chips -= amount
        self.current_bet += amount
        if self.chips == 0:
            self.all_in = True

    def evaluate_best_hand(self, community_cards) -> None:
        #void function that sets the best hand, best hand rank, and best hand tiebreaker for the given player and the given community cards
        self.best_hand = find_best_hand(community_cards, self.hole_cards)
        self.best_hand_rank, self.best_hand_tiebreaker = HandEvaluator.evaluate(self.best_hand)
        


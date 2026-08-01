# Trips

A small poker project that includes a hand evaluator and a simple hold'em engine.

## Overview

Trips consists of two main parts:

- Hand evaluator: evaluates poker hands and compares them using standard poker hand rankings.
- Hold'em engine: simulates a simple poker hand flow with players, a deck, community cards, and basic betting rounds.

### Notes

- FYI, some of the code is pretty shitty and the engine has a lot of bugs. For example, 
    - there is no privacy on the terminal line (so you can see other people's cards)
    - the betting system is very basic, but it technically works
    - there is a redundant betting round for some reason
- This is an ongoing project, created __without__ the use of coding agents like Claude Code 

## Structure

- hand_evaluator/
  - cards.py: card, rank, suit, and hand representations
  - evaluator.py: hand ranking and comparison logic
- hold_em_engine/
  - engine.py: basic hold'em game flow
  - game.py: deck and game state helpers
  - player.py: player state and chip tracking
  - game-test.py: simple interactive terminal demo

## Getting Started

### Running the Hand Evaluator

Use the evaluator directly if you want to test hand ranking logic.

```python
from hand_evaluator.cards import Card, Rank, Suit
from hand_evaluator.evaluator import HandEvaluator

hand = [Card(Rank.ACE, Suit.HEARTS), Card(Rank.KING, Suit.HEARTS), Card(Rank.QUEEN, Suit.HEARTS), Card(Rank.JACK, Suit.HEARTS), Card(Rank.TEN, Suit.HEARTS)]
print(HandEvaluator.evaluate(hand))
```

### Running the Hold'em Engine

Run the interactive terminal demo:

```bash
cd hold_em_engine
python3 game-test.py
```

You can also import the engine in Python:

```python
from engine import PokerEngine

engine = PokerEngine(["Alice", "Bob"], starting_chips=1000, ante=10)
result = engine.play_hand()
print(result["winners"])
print(result["pot"])
```
## Hand Evaluator Notes

- The evaluator ranks hands from high card up to royal flush.
- Tiebreakers are handled through a tuple-based system.
- From my own tests, the evaluator should be correct for all test cases. However, lmk if you find an edge case that is evaluated incorrectly.




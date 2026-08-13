# Trips

A small poker project that includes a hand evaluator and a simple hold'em engine.

## Overview

Trips consists of three main parts:

- Hand evaluator: evaluates poker hands and compares them using standard poker hand rankings.
- Hold'em engine: simulates a simple poker hand flow with players, a deck, community cards, and basic betting rounds.
- Odds evaluator: evaluates the odds of winning through Monte Carlo Simulations or direct computation

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
  - (data) plot_starting_hands.py: plotting helper that builds the consolidated preflop heatmap
- hold_em_engine/
  - engine.py: basic hold'em game flow
  - game.py: deck and game state helpers
  - player.py: player state and chip tracking
  - game-test.py: simple interactive terminal demo
- odds_evaluator/
  - exact_odds.py: direct brute-force computation of odds to win given hole_cards and community cards
  - monte_carlo.py: monte carlo simulations of random opponent cards and community cards 

Directory Tree (as of 8/13/2026):

```
├── LICENSE
├── README.md
├── data
│   ├── data-generator.py
│   ├── dataset.csv
│   ├── generations
│   │   ├── (no-ties)-gen5-345s.csv
│   │   ├── gen1.csv
│   │   ├── gen2.csv
│   │   ├── gen3-5s.csv
│   │   ├── gen4-45s.csv
│   │   ├── gen5-345s.csv
│   │   └── starting-hand-equities.csv
│   ├── plot_starting_hands.py
│   ├── starting-hand-equities.csv
│   ├── starting-hands-heatmaps.png
│   └── starting-hands.py
├── hand_evaluator
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-314.pyc
│   │   ├── __init__.pypy311.pyc
│   │   ├── cards.cpython-314.pyc
│   │   ├── cards.pypy311.pyc
│   │   ├── evaluator.cpython-314.pyc
│   │   └── evaluator.pypy311.pyc
│   ├── cards.py
│   ├── evaluator.py
│   ├── hand-evaluator.html
│   └── test.py
├── hold_em_engine
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── engine.cpython-314.pyc
│   │   ├── game.cpython-314.pyc
│   │   └── player.cpython-314.pyc
│   ├── engine.py
│   ├── game-test.py
│   ├── game.py
│   └── player.py
└── odds_evaluator
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-314.pyc
    │   ├── __init__.pypy311.pyc
    │   ├── exact_odds.cpython-314.pyc
    │   ├── exact_odds.pypy311.pyc
    │   ├── monte_carlo.cpython-314.pyc
    │   └── monte_carlo.pypy311.pyc
    ├── exact_odds.py
    └── monte_carlo.py
```

## Getting Started

### Running the Hand Evaluator

Use the evaluator directly if you want to test hand ranking logic.

```python
from hand_evaluator.cards import Card, Rank, Suit
from hand_evaluator.evaluator import HandEvaluator

hand = [Card(Rank.ACE, Suit.HEARTS), Card(Rank.KING, Suit.HEARTS), Card(Rank.QUEEN, Suit.HEARTS), Card(Rank.JACK, Suit.HEARTS), Card(Rank.TEN, Suit.HEARTS)]
print(HandEvaluator.evaluate(hand))
```

#### Hand Evaluator Notes

- The evaluator ranks hands from high card up to royal flush.
- Tiebreakers are handled through a tuple-based system.
- From my own tests, the evaluator should be correct for all test cases. However, lmk if you find an edge case that is evaluated incorrectly.

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

### Running the Odds Evaluator

Run the odds scripts from the repository root so Python can import the sibling packages correctly.

#### Monte Carlo estimator

This version estimates win probability by sampling random opponent hands and random remaining board cards.

```bash
cd /path/to/trips
python3 odds_evaluator/monte_carlo.py
```

Example input:

```text
Enter your hole cards (e.g., 'AH KH' for Ace of Hearts and King of Hearts): AH KH
Enter the community cards (e.g., '2D 3C 4H' for 2 of Diamonds, 3 of Clubs, and 4 of Hearts): 2D 3C 4H
```

It will print an estimated win probability such as:

```text
Estimated odds of winning: 49.800%
```

#### Exact odds calculator

This version computes the exact win probability by enumerating all valid remaining board and opponent-card combinations. It is slower, but it is exact instead of sampled.

```bash
cd /path/to/trips
python3 odds_evaluator/exact_odds.py
```

Example input:

```text
Enter your hole cards (e.g., 'AH KH' for Ace of Hearts and King of Hearts): AH KH
Enter the community cards (e.g., '2D 3C' for 2 of Diamonds and 3 of Clubs): 2D 3C
```

It prints a final probability such as:

```text
Exact odds of winning: 0.542
```

#### Notes

- Both scripts expect card strings in standard poker notation, like `AH`, `KC`, `2D`.
- For hole cards, separate cards with spaces: `AH KH`.
- For community cards, separate cards with spaces as well: `2D 3C 4H`.
- The exact calculator is much slower than the Monte Carlo estimator, especially when there are fewer community cards. It is best for smaller, deterministic checks rather than large batch generation.

### Starting-hand equity chart

You can visualize the preflop equities for all starting hands with the provided plot script. The script reads `data/starting-hand-equities.csv` (generated by `data/starting-hands.py`) and produces a single consolidated heatmap at [data/starting-hands-heatmaps.png](data/starting-hands-heatmaps.png).

- Install plotting dependencies (if you don't already have them):

```bash
python3 -m pip install numpy matplotlib seaborn
```

- Generate the chart (uses the CSV in `data/`):

```bash
python3 data/plot_starting_hands.py
```

- Output: [data/starting-hands-heatmaps.png](data/starting-hands-heatmaps.png)

Notes:
- The heatmap is a 13x13 matrix where the diagonal shows pocket pairs, the upper triangle shows suited combinations, and the lower triangle shows offsuit combinations. Values are shown as percentages (one decimal place).
- Colors map from red (low equity) → yellow → green (high equity).
- If you don't have `starting-hand-equities.csv` yet, `data/starting-hands.py` will generate it but may take a long time depending on Monte Carlo run settings; consider reducing the number of runs in `data/starting-hands.py` for a faster approximate dataset.



# created with the help of Github Copilot

import os
import sys
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    import seaborn as sns
except Exception:
    sns = None

from hand_evaluator.cards import Card, Rank


def load_equities(csv_path):
    pairs = defaultdict(list)
    suited = defaultdict(list)
    offsuit = defaultdict(list)

    with open(csv_path, "r") as f:
        # skip header
        next(f)
        for line in f:
            line = line.strip()
            if not line:
                continue
            hole, val = line.split(",")
            val = float(val)
            
            a_str, b_str = hole.split()
            a = Card.from_string(a_str)
            b = Card.from_string(b_str)
            r1 = a.rank.value
            r2 = b.rank.value
            if r1 == r2:
                pairs[r1].append(val)
            else:
                high, low = (r1, r2) if r1 > r2 else (r2, r1)
                if a.suit == b.suit:
                    suited[(high, low)].append(val)
                else:
                    offsuit[(high, low)].append(val)

    return pairs, suited, offsuit


def build_matrices(pairs, suited, offsuit):
    ranks = [r.value for r in list(Rank)][::-1]  # 2..A then reverse -> A..2
    # ensure order A, K, Q, ..., 2
    ranks = sorted(ranks, reverse=True)
    idx = {r: i for i, r in enumerate(ranks)}
    n = len(ranks)
    pairs_mat = np.full((n, n), np.nan)
    suited_mat = np.full((n, n), np.nan)
    offsuit_mat = np.full((n, n), np.nan)

    for r in ranks:
        i = idx[r]
        if pairs.get(r):
            pairs_mat[i, i] = sum(pairs[r]) / len(pairs[r])

    for (high, low), vals in suited.items():
        i = idx[high]
        j = idx[low]
        suited_mat[i, j] = sum(vals) / len(vals)

    for (high, low), vals in offsuit.items():
        i = idx[high]
        j = idx[low]
        offsuit_mat[j, i] = sum(vals) / len(vals)  # place offsuit in lower triangle

    labels = [
        "A",
        "K",
        "Q",
        "J",
        "T",
        "9",
        "8",
        "7",
        "6",
        "5",
        "4",
        "3",
        "2",
    ]

    return ranks, labels, pairs_mat, suited_mat, offsuit_mat


def plot_heatmap_combined(labels, pairs_mat, suited_mat, offsuit_mat, outpath):
    # Build a single combined matrix: diagonal=pairs, upper=suited, lower=offsuit
    n = pairs_mat.shape[0]
    combined = np.full((n, n), np.nan)
    # copy diagonal
    for i in range(n):
        if not np.isnan(pairs_mat[i, i]):
            combined[i, i] = pairs_mat[i, i] * 100.0
    # upper triangle: suited_mat
    for i in range(n):
        for j in range(n):
            if not np.isnan(suited_mat[i, j]):
                combined[i, j] = suited_mat[i, j] * 100.0
    # lower triangle: offsuit_mat
    for i in range(n):
        for j in range(n):
            if not np.isnan(offsuit_mat[i, j]):
                combined[i, j] = offsuit_mat[i, j] * 100.0

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    # color scale: red (0%) -> yellow (50%) -> green (100%)
    cmap = LinearSegmentedColormap.from_list("red_green", ["red", "yellow", "green"]) 
    vmin = np.nanmin(combined)
    vmax = np.nanmax(combined)
    im = ax.imshow(combined, cmap=cmap, vmin=vmin, vmax=vmax)

    # ticks and labels
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Second card", labelpad=8)
    ax.set_ylabel("First card", labelpad=8)
    ax.set_title("Starting-hand equities (%) — diagonal: pairs, upper: suited, lower: offsuit")

    # grid lines between cells
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", color="white", linestyle='-', linewidth=0.8)
    ax.tick_params(which="minor", bottom=False, left=False)

    # small padding for tick labels so they don't touch the axis
    ax.tick_params(axis='x', pad=6)
    ax.tick_params(axis='y', pad=6)

    # annotate with one decimal (e.g., 50.4). Choose contrasting text color
    for (i, j), val in np.ndenumerate(combined):
        if np.isnan(val):
            continue
        text = f"{val:.1f}"
        # Use black text for all annotations for consistent readability
        ax.text(j, i, text, ha="center", va="center", color="black", fontsize=8)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Win probability (%)')

    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    print(f"Saved consolidated heatmap to {outpath}")


def main():
    repo_dir = os.path.dirname(__file__)
    csv_path = os.path.join(repo_dir, "starting-hand-equities.csv")
    outpath = os.path.join(repo_dir, "starting-hands-heatmaps.png")
    pairs, suited, offsuit = load_equities(csv_path)
    ranks, labels, pairs_mat, suited_mat, offsuit_mat = build_matrices(pairs, suited, offsuit)
    plot_heatmap_combined(labels, pairs_mat, suited_mat, offsuit_mat, outpath)


if __name__ == "__main__":
    main()

"""Card ratings from a regularised logistic regression over all games.

Usage: python analysis/regression.py <runDir> [<runDir> ...] [--mode seen|deck]
                                     [--l2 X] [--min-n N] [--real real.csv] [--out out.csv]

GIH WR credits a card with the strength of the whole deck it sits in. Here every
game is one sample: P(player A wins) = sigmoid(b_play + sum_c w_c * (x_Ac - x_Bc)),
where x_Pc = 1 if player P had card c in hand (mode "seen") or in the deck (mode
"deck"). Each weight w_c is then the card's effect with the other cards held
fixed. Plain numpy, fitted with Newton steps (L2 penalty keeps rare cards near 0).
"""
import argparse

import numpy as np
import pandas as pd

from card_stats import BASICS, clean, load_decks, load_games


def build(run_dirs, mode):
    rows, y, play, index = [], [], [], {}
    for run in run_dirs:
        decks = load_decks(run)
        for g in load_games(run):
            if g["status"] != "ok" or g["winner"] is None:
                continue
            sides = {}
            for side, p in g["players"].items():
                if mode == "deck":
                    cards = decks[p["deck"]]
                else:
                    cards = {clean(c) for c in p["opening"] + p["drawn"]}
                sides[side] = cards - BASICS
            row = {}
            for side, sign in (("A", 1), ("B", -1)):
                for c in sides[side]:
                    j = index.setdefault(c, len(index))
                    row[j] = row.get(j, 0) + sign
            rows.append(row)
            y.append(1.0 if g["winner"] == "A" else 0.0)
            play.append(1.0 if g["on_play"] == "A" else -1.0)
    X = np.zeros((len(rows), len(index) + 1))
    for i, row in enumerate(rows):
        for j, v in row.items():
            X[i, j] = v
    X[:, -1] = play
    names = [None] * len(index)
    for c, j in index.items():
        names[j] = c
    return X, np.array(y), names


def fit(X, y, l2, iters=25):
    w = np.zeros(X.shape[1])
    pen = np.full(X.shape[1], l2)
    pen[-1] = 0.0  # don't shrink the play/draw term
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ w))
        grad = X.T @ (p - y) + pen * w
        H = (X * (p * (1 - p))[:, None]).T @ X + np.diag(pen)
        step = np.linalg.solve(H, grad)
        w -= step
        if np.abs(step).max() < 1e-6:
            break
    return w


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dirs", nargs="+")
    ap.add_argument("--mode", choices=["seen", "deck"], default="seen")
    ap.add_argument("--l2", type=float, default=5.0)
    ap.add_argument("--min-n", type=int, default=150, help="min games where the card appears")
    ap.add_argument("--real", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    X, y, names = build(args.run_dirs, args.mode)
    w = fit(X, y, args.l2)
    n = (X[:, :-1] != 0).sum(axis=0)
    df = pd.DataFrame({"card": names, "coef": w[:-1], "n": n}).sort_values("coef", ascending=False)
    print(f"Games: {len(y)}, cards: {len(names)}, play coef: {w[-1]:.3f}")
    if args.out:
        df.to_csv(args.out, index=False, float_format="%.4f")
    shown = df[df["n"] >= args.min_n]
    print(shown.head(20).to_string(index=False))

    if args.real:
        real = pd.read_csv(args.real)[["card", "GIH_WR", "GIH_n"]]
        m = shown.merge(real, on="card")
        m = m[m["GIH_n"] >= 200]
        print(f"\nSpearman vs 17Lands GIH WR ({len(m)} cards): "
              f"{m['coef'].rank().corr(m['GIH_WR'].rank()):.3f}")


if __name__ == "__main__":
    main()

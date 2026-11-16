"""How reproducible are the simulated card rankings?

Usage: python analysis/reliability.py <runDir> [--min-games N] [--real real.csv]

Splits the games of a run into two random halves, computes GIH WR per card in
each half and reports their rank correlation. Spearman-Brown projects that to
the reliability of the full run and of runs with more games. If the reliability
is low, a weak match with 17Lands may be noise rather than a wrong model.

With --real, also reports how well the full run and each half match 17Lands.
"""
import argparse
import random

import pandas as pd

from card_stats import compute, load_decks, load_games


def spearman(a: pd.Series, b: pd.Series) -> float:
    return a.rank().corr(b.rank())


def brown(r: float, k: float) -> float:
    """Spearman-Brown: reliability when the data grows by factor k."""
    return k * r / (1 + (k - 1) * r)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--min-games", type=int, default=100, help="min GIH games per half")
    ap.add_argument("--real", default=None)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    decks = load_decks(args.run_dir)
    games = list(load_games(args.run_dir))
    random.Random(args.seed).shuffle(games)
    half = len(games) // 2
    a, _ = compute(decks, games[:half])
    b, _ = compute(decks, games[half:])
    full, s = compute(decks, games)

    m = a.merge(b, on="card", suffixes=("_a", "_b"))
    m = m[(m["GIH_n_a"] >= args.min_games) & (m["GIH_n_b"] >= args.min_games)]
    r_half = spearman(m["GIH_WR_a"], m["GIH_WR_b"])
    r_full = brown(r_half, 2)
    print(f"Games: {s['games']}, cards with >= {args.min_games} GIH games in both halves: {len(m)}")
    print(f"Split-half rank correlation GIH WR: {r_half:.3f}")
    print(f"Estimated reliability of the full run: {r_full:.3f}")
    for k in [2, 4, 10]:
        print(f"  with {k}x the games: {brown(r_full, k):.3f}")

    if args.real:
        real = pd.read_csv(args.real)[["card", "GIH_WR", "GIH_n"]].rename(
            columns={"GIH_WR": "real", "GIH_n": "real_n"})
        cards = set(m["card"])
        f = full[full["card"].isin(cards)].merge(real, on="card")
        f = f[f["real_n"] >= 200]
        mm = m.merge(real, on="card")
        mm = mm[mm["real_n"] >= 200]
        print(f"\nAgainst 17Lands ({len(f)} cards):")
        print(f"  full run: {spearman(f['GIH_WR'], f['real']):.3f}")
        print(f"  half A:   {spearman(mm['GIH_WR_a'], mm['real']):.3f}")
        print(f"  half B:   {spearman(mm['GIH_WR_b'], mm['real']):.3f}")


if __name__ == "__main__":
    main()

"""Per-card win-rate statistics from simulated games, in the style of 17Lands.

Usage: python analysis/card_stats.py <runDir> [--min-games N] [--out cards.csv]

<runDir> must contain decks/*.dck and games/*.jsonl as written by
scripts/run_sim.sh.

Metrics per card (a game counts once per player side, however many copies the deck holds):
  GP   games played with the card in the main deck, GP WR their win rate
  OH   card in the opening hand (after mulligans)
  GD   card drawn later (library to hand, so tutors count too)
  GIH  in hand at some point = OH or GD
  GNS  in the deck but never seen
  IWD  improvement when drawn = GIH WR - GNS WR
Draws and timeouts are dropped. Basic lands are left out.
"""
import argparse
import glob
import json
import math
import os
import re
from collections import defaultdict

import pandas as pd

BASICS = {"Plains", "Island", "Swamp", "Mountain", "Forest", "Wastes"}


def clean(name: str) -> str:
    # Forge marks foils with a trailing "+" in deck files
    return name.rstrip("+").strip()


def read_deck(path: str) -> set[str]:
    cards, section = set(), None
    with open(path, encoding="utf8") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("["):
                section = line.strip("[]").lower()
                continue
            m = re.match(r"(\d+) (.+?)(\|.*)?$", line)
            if m and section == "main":
                cards.add(clean(m.group(2)))
    return cards


def wilson(wins: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    p = wins / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - r) / d, (c + r) / d)


def load_games(run_dir: str):
    for path in sorted(glob.glob(os.path.join(run_dir, "games", "*.jsonl"))):
        with open(path, encoding="utf8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    yield json.loads(line)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--min-games", type=int, default=50, help="min GIH games for the table")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    decks: dict[str, set[str]] = {}
    for p in glob.glob(os.path.join(args.run_dir, "decks", "*.dck")):
        decks[os.path.basename(p)[:-4]] = read_deck(p)

    # counters[card][metric] = [wins, games]
    stats: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    n_games = n_skipped = play_wins = 0
    turns = []

    for g in load_games(args.run_dir):
        if g["status"] != "ok" or g["winner"] is None:
            n_skipped += 1
            continue
        n_games += 1
        turns.append(g["turns"])
        if g["on_play"] == g["winner"]:
            play_wins += 1
        for side, pdata in g["players"].items():
            won = int(side == g["winner"])
            deck = decks[pdata["deck"]]
            opening = {clean(c) for c in pdata["opening"]}
            drawn = {clean(c) for c in pdata["drawn"]} - opening
            for card in deck - BASICS:
                metrics = ["GP"]
                if card in opening:
                    metrics += ["OH", "GIH"]
                elif card in drawn:
                    metrics += ["GD", "GIH"]
                else:
                    metrics += ["GNS"]
                for m in metrics:
                    stats[card][m][0] += won
                    stats[card][m][1] += 1

    rows = []
    for card, ms in stats.items():
        row = {"card": card}
        for m in ["GP", "OH", "GD", "GIH", "GNS"]:
            w, n = ms[m]
            row[f"{m}_n"] = n
            row[f"{m}_WR"] = w / n if n else math.nan
        lo, hi = wilson(*ms["GIH"])
        row["GIH_lo"], row["GIH_hi"] = lo, hi
        row["IWD"] = row["GIH_WR"] - row["GNS_WR"]
        rows.append(row)

    df = pd.DataFrame(rows).sort_values("GIH_WR", ascending=False)
    if args.out:
        df.to_csv(args.out, index=False, float_format="%.4f")

    print(f"Games used: {n_games} (skipped draws/timeouts/errors: {n_skipped})")
    if n_games:
        print(f"On-the-play win rate: {play_wins / n_games:.3f}   median turns: {pd.Series(turns).median():.0f}")
    shown = df[df["GIH_n"] >= args.min_games]
    print(f"Cards with >= {args.min_games} GIH games: {len(shown)} of {len(df)}\n")
    pd.set_option("display.width", 160)
    cols = ["card", "GP_n", "GP_WR", "GIH_n", "GIH_WR", "GIH_lo", "GIH_hi", "IWD"]
    fmt = shown[cols].copy()
    for c in ["GP_WR", "GIH_WR", "GIH_lo", "GIH_hi", "IWD"]:
        fmt[c] = (fmt[c] * 100).round(1)
    print("Top 25 by GIH WR:")
    print(fmt.head(25).to_string(index=False))
    print("\nBottom 15 by GIH WR:")
    print(fmt.tail(15).to_string(index=False))


if __name__ == "__main__":
    main()

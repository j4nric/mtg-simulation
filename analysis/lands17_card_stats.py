"""Per-card win rates from a 17Lands public game-data file.

Usage: python analysis/lands17_card_stats.py <game_data_public.SET.PremierDraft.csv.gz> <out.csv>

Uses the same definitions as card_stats.py, so both sides of the comparison are
computed alike: a game counts once per card whatever the number of copies,
GIH = in the opening hand or drawn (tutored cards count as drawn, as in the
simulation), GNS = in the deck but never seen. Basic lands are left out.
The output columns match what compare_17lands.py expects.

Download: https://17lands-public.s3.amazonaws.com/analysis_data/game_data/game_data_public.<SET>.PremierDraft.csv.gz
"""
import sys

import numpy as np
import pandas as pd

BASICS = {"Plains", "Island", "Swamp", "Mountain", "Forest", "Wastes"}


def main() -> None:
    src, out = sys.argv[1], sys.argv[2]
    header = pd.read_csv(src, nrows=0).columns
    cards = [c[len("deck_"):] for c in header if c.startswith("deck_") and c[len("deck_"):] not in BASICS]
    usecols = ["won"] + [f"{p}_{c}" for c in cards for p in ("deck", "opening_hand", "drawn", "tutored")
                         if f"{p}_{c}" in header]

    k = len(cards)
    acc = {m: np.zeros((2, k)) for m in ["GP", "OH", "GD", "GIH", "GNS"]}  # row 0 wins, row 1 games
    n_rows = 0
    for chunk in pd.read_csv(src, usecols=usecols, chunksize=100_000, dtype=np.int8,
                             converters={"won": lambda v: v == "True"}):
        won = chunk["won"].to_numpy(dtype=bool)
        def mat(prefix):
            cols = [f"{prefix}_{c}" for c in cards]
            present = [c for c in cols if c in chunk.columns]
            m = np.zeros((len(chunk), k), dtype=bool)
            idx = [cols.index(c) for c in present]
            m[:, idx] = chunk[present].to_numpy() > 0
            return m
        deck = mat("deck")
        oh = mat("opening_hand") & deck
        gd = (mat("drawn") | mat("tutored")) & deck & ~oh
        gih = oh | gd
        gns = deck & ~gih
        for name, m in [("GP", deck), ("OH", oh), ("GD", gd), ("GIH", gih), ("GNS", gns)]:
            acc[name][0] += m[won].sum(axis=0)
            acc[name][1] += m.sum(axis=0)
        n_rows += len(chunk)
        print(f"{n_rows} games ...", file=sys.stderr)

    df = pd.DataFrame({"card": cards})
    for name, (w, n) in acc.items():
        with np.errstate(invalid="ignore", divide="ignore"):
            df[f"{name}_WR"] = w / n
        df[f"{name}_n"] = n.astype(int)
    df["IWD"] = df["GIH_WR"] - df["GNS_WR"]
    df = df.sort_values("GIH_WR", ascending=False)
    df.to_csv(out, index=False, float_format="%.4f")
    print(f"{n_rows} games, {len(df)} cards -> {out}")


if __name__ == "__main__":
    main()

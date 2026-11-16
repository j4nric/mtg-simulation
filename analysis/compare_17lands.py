"""Compares simulated card stats with real 17Lands card ratings.

Usage:
  python analysis/compare_17lands.py <sim_cards.csv> <17lands.json|URL> [--min-games N]

<sim_cards.csv> comes from card_stats.py --out. The 17Lands file is the JSON of
https://www.17lands.com/card_ratings/data?expansion=TRK&format=PremierDraft
(download it in a browser if this machine cannot reach 17lands.com).

Reports the rank correlation (Spearman) of GIH WR and GP WR, and the cards on
which simulation and reality disagree most. Those are where Forge's AI misplays
or the draft AI misjudges a card.
"""
import argparse
import json
import urllib.request

import pandas as pd


def load_17lands(src: str) -> pd.DataFrame:
    if src.startswith("http"):
        with urllib.request.urlopen(src, timeout=60) as r:
            data = json.load(r)
    else:
        with open(src, encoding="utf8") as fh:
            data = json.load(fh)
    df = pd.DataFrame(data)
    return df.rename(columns={
        "name": "card",
        "ever_drawn_win_rate": "GIH_WR_17l",
        "ever_drawn_game_count": "GIH_n_17l",
        "win_rate": "GP_WR_17l",
        "game_count": "GP_n_17l",
        "drawn_improvement_win_rate": "IWD_17l",
    })[["card", "GIH_WR_17l", "GIH_n_17l", "GP_WR_17l", "GP_n_17l", "IWD_17l"]]


def spearman(a: pd.Series, b: pd.Series) -> float:
    return a.rank().corr(b.rank())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sim_csv")
    ap.add_argument("lands")
    ap.add_argument("--min-games", type=int, default=200, help="min GIH games on both sides")
    args = ap.parse_args()

    sim = pd.read_csv(args.sim_csv)
    real = load_17lands(args.lands)
    df = sim.merge(real, on="card", how="inner")
    df = df[(df["GIH_n"] >= args.min_games) & (df["GIH_n_17l"] >= args.min_games)].dropna(
        subset=["GIH_WR", "GIH_WR_17l"])

    print(f"Cards compared: {len(df)} (sim cards: {len(sim)}, 17Lands cards: {len(real)})")
    if len(df) < 10:
        print("Too few cards to compare.")
        return
    print(f"Spearman GIH WR: {spearman(df['GIH_WR'], df['GIH_WR_17l']):.3f}")
    print(f"Spearman GP WR:  {spearman(df['GP_WR'], df['GP_WR_17l']):.3f}")
    print(f"Spearman IWD:    {spearman(df['IWD'], df['IWD_17l']):.3f}")

    df["rank_sim"] = df["GIH_WR"].rank(ascending=False)
    df["rank_17l"] = df["GIH_WR_17l"].rank(ascending=False)
    df["rank_diff"] = df["rank_sim"] - df["rank_17l"]
    cols = ["card", "GIH_n", "GIH_WR", "GIH_WR_17l", "rank_sim", "rank_17l"]
    pd.set_option("display.width", 160)
    print("\nOverrated by the simulation (much higher rank than on 17Lands):")
    print(df.sort_values("rank_diff").head(15)[cols].to_string(index=False))
    print("\nUnderrated by the simulation:")
    print(df.sort_values("rank_diff", ascending=False).head(15)[cols].to_string(index=False))


if __name__ == "__main__":
    main()

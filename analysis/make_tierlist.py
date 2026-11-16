"""Turns predict_model.py's output into a Markdown tier list.

Usage: python analysis/make_tierlist.py <scores.csv> <SET> <out.md>

Tiers by percentile of the score within the set:
  A top 5 %, B next 15 %, C next 30 %, D next 30 %, F bottom 20 %.
"""
import argparse
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIERS = [("A", 0.95), ("B", 0.80), ("C", 0.50), ("D", 0.20), ("F", 0.0)]
RARITY = {0: "C", 1: "U", 2: "R", 3: "M"}


def colour(row) -> str:
    c = "".join(x for x in "WUBRG" if row[f"color_{x}"])
    return c or "farblos"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("scores")
    ap.add_argument("set")
    ap.add_argument("out")
    args = ap.parse_args()

    s = pd.read_csv(args.scores)
    f = pd.read_csv(os.path.join(ROOT, "data", "features.csv"))
    f = f[f["set"] == args.set][["card"] + [f"color_{x}" for x in "WUBRG"]]
    s = s.merge(f, on="card", how="left").fillna({f"color_{x}": 0 for x in "WUBRG"})
    s["pct"] = s["score"].rank(pct=True)
    s["tier"] = s["pct"].map(lambda p: next(t for t, lo in TIERS if p >= lo))

    lines = [f"# {args.set}: Tierliste (Vorhersage)", "",
             "Erzeugt mit `analysis/predict_model.py` und `analysis/make_tierlist.py`.",
             "Score = Modell aus Kartenwerten und Regeltext (gelernt an älteren Sets)",
             "plus Forge-Simulation mit blindem Draft. Höher ist besser; Einheit: Standardabweichungen",
             "der erwarteten GIH WR innerhalb des Sets.", ""]
    for tier, _ in TIERS:
        part = s[s["tier"] == tier].sort_values("score", ascending=False)
        lines += [f"## Tier {tier} ({len(part)} Karten)", "",
                  "| Karte | Farbe | Seltenheit | Score |", "|---|---|---|---|"]
        for _, r in part.iterrows():
            lines.append(f"| {r['card']} | {colour(r)} | {RARITY.get(int(r['rarity']), '?')} "
                         f"| {r['score']:.2f} |")
        lines.append("")
    with open(args.out, "w", encoding="utf8") as fh:
        fh.write("\n".join(lines))
    print(s["tier"].value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()

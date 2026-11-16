"""Writes a draft ranking that holds no knowledge of real results.

Usage: python analysis/make_blind_rankings.py <forge .rnk file> <out.rnk> [--seed N]

Forge's ranking files for older sets are derived from 17Lands win rates, so a
simulation drafted with them cannot show what it would have found on its own.
This ranking orders the same cards by rarity only (mythic > rare > uncommon >
common), random within a rarity, i.e. what a drafter knows before any data
exists. Pass the output to DraftSim as the fourth argument.
"""
import argparse
import random
import re

RARITY_ORDER = {"M": 0, "R": 1, "U": 2, "C": 3, "L": 4, "S": 4}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    cards = []
    with open(args.src, encoding="utf8") as fh:
        for line in fh:
            m = re.match(r"#(\d+)\|(.+?)\|(\w)\|(\w+)", line.strip())
            if m:
                cards.append((m.group(2), m.group(3)))

    rng = random.Random(args.seed)
    rng.shuffle(cards)
    cards.sort(key=lambda c: RARITY_ORDER.get(c[1], 5))

    with open(args.out, "w", encoding="utf8") as fh:
        fh.write("//Rank|Name|Rarity|Set\n")
        for i, (name, rarity) in enumerate(cards, 1):
            fh.write(f"#{i}|{name}|{rarity}|CUSTOM\n")
    print(f"{len(cards)} cards -> {args.out}")


if __name__ == "__main__":
    main()

"""Card features from Forge's card scripts, for rating cards before any play data exists.

Usage: python analysis/card_features.py <SET> [<SET> ...] --out features.csv
       FORGE_DIR (default ../card-forge/forge) must hold forge-gui/res.

One row per card of each set: rarity, mana value, colours, card types, power and
toughness, keywords and what the card's abilities do (removal, card draw, tokens
and so on), read from Forge's ability scripts, which are more regular than Oracle
text.
"""
import argparse
import glob
import os
import re

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORGE = os.environ.get("FORGE_DIR", os.path.join(ROOT, "..", "card-forge", "forge"))
RES = os.path.join(FORGE, "forge-gui", "res")

KEYWORDS = ["Flying", "Trample", "Deathtouch", "Lifelink", "Vigilance", "Haste", "First Strike",
            "Double Strike", "Menace", "Reach", "Ward", "Flash", "Hexproof", "Indestructible",
            "Defender", "Prowess", "Kicker", "Cycling", "Flashback", "Station", "Warp", "Offspring",
            "Ninjutsu", "Crew", "Equip", "Disguise", "Plot"]
TYPES = ["Creature", "Instant", "Sorcery", "Enchantment", "Artifact", "Land", "Planeswalker",
         "Legendary", "Aura", "Equipment", "Vehicle", "Saga", "Spacecraft", "Planet", "Room"]
APIS = ["Destroy", "DestroyAll", "DealDamage", "DamageAll", "ChangeZone", "Pump", "PumpAll",
        "Fight", "Counter", "Draw", "Token", "PutCounter", "GainLife", "LoseLife", "Mill",
        "Discard", "Tap", "TapAll", "Sacrifice", "Dig", "Scry", "Surveil", "Attach",
        "Animate", "CopyPermanent", "Mana", "Explore", "Connive", "AddTurn", "Debuff", "Effect",
        "Protection", "Untap", "ChangeZoneAll", "Charm"]
RARITY = {"C": 0, "U": 1, "R": 2, "M": 3}
COLORS = "WUBRG"


def edition_cards(code: str) -> dict[str, str]:
    """name -> rarity letter for every card listed in the set's edition file."""
    for path in glob.glob(os.path.join(RES, "editions", "*.txt")):
        with open(path, encoding="utf8") as fh:
            text = fh.read()
        if re.search(rf"^Code={code}\s*$", text, re.M):
            out = {}
            for m in re.finditer(r"^\S+ ([CURMSL]) (.+?)(?: @.*)?$", text, re.M):
                out.setdefault(m.group(2).strip(), m.group(1))
            return out
    raise ValueError(f"No edition file for {code}")


_SCRIPTS: dict[str, str] | None = None


def scripts() -> dict[str, str]:
    global _SCRIPTS
    if _SCRIPTS is None:
        _SCRIPTS = {}
        for path in glob.glob(os.path.join(RES, "cardsfolder", "**", "*.txt"), recursive=True):
            with open(path, encoding="utf8", errors="ignore") as fh:
                text = fh.read()
            m = re.search(r"^Name:(.+)$", text, re.M)
            if m:
                _SCRIPTS.setdefault(m.group(1).strip(), text)
    return _SCRIPTS


def mana_value(cost: str) -> tuple[int, set[str], int]:
    mv, colors, pips = 0, set(), 0
    for sym in cost.split():
        if sym.isdigit():
            mv += int(sym)
        elif sym == "X":
            continue
        else:
            mv += 1
            pips += 1
            colors |= {c for c in sym if c in COLORS}
    return mv, colors, pips


def features(name: str, rarity: str) -> dict | None:
    text = scripts().get(name)
    if text is None:
        return None
    front = text.split("\nALTERNATE")[0]
    cost = re.search(r"^ManaCost:(.+)$", front, re.M)
    cost = cost.group(1).strip() if cost else "no cost"
    mv, colors, pips = mana_value(cost if cost != "no cost" else "")
    types = re.search(r"^Types:(.+)$", front, re.M)
    types = types.group(1) if types else ""
    pt = re.search(r"^PT:(\*|\d+)/(\*|\d+)", front, re.M)
    power = int(pt.group(1)) if pt and pt.group(1).isdigit() else 0
    tough = int(pt.group(2)) if pt and pt.group(2).isdigit() else 0
    oracle = re.search(r"^Oracle:(.*)$", text, re.M)
    oracle = oracle.group(1) if oracle else ""

    f = {"card": name, "rarity": RARITY.get(rarity, 0), "mv": mv, "pips": pips,
         "n_colors": len(colors), "x_cost": int(" X" in " " + cost),
         "power": power, "toughness": tough, "pt_per_mv": (power + tough) / max(mv, 1),
         "oracle_len": len(oracle),
         "oracle": oracle.replace(name, "CARDNAME").replace("\\n", " "), "dfc": int("ALTERNATE" in text),
         "n_triggers": len(re.findall(r"^T:", text, re.M)),
         "n_statics": len(re.findall(r"^S:", text, re.M)),
         "n_activated": len(re.findall(r"^A:AB\$", text, re.M))}
    for c in COLORS:
        f[f"color_{c}"] = int(c in colors)
    for t in TYPES:
        f[f"type_{t}"] = int(re.search(rf"\b{t}\b", types) is not None)
    kw_text = " ".join(re.findall(r"^K:(.+)$", text, re.M)) + " " + oracle
    for k in KEYWORDS:
        f[f"kw_{k.replace(' ', '_')}"] = int(k.lower() in kw_text.lower())
    api_calls = re.findall(r"(?:SP|AB|DB)\$ ?(\w+)", text)
    for a in APIS:
        f[f"api_{a}"] = api_calls.count(a)

    # Removal: something that kills or removes an opponent's creature
    targets_creature = re.search(r"ValidTgts\$ [^|]*(Creature|Permanent)", text) is not None
    exile_or_bounce = re.search(r"ChangeZone[^\n]*Destination\$ (Exile|Hand|Library)", text) is not None
    shrink = re.search(r"NumDef\$ -", text) is not None
    f["removal"] = int(targets_creature and (
        "Destroy" in api_calls or "DealDamage" in api_calls or "Fight" in api_calls
        or exile_or_bounce or shrink))
    f["pacifism"] = int("Aura" in types and re.search(r"can't attack|can't block", oracle) is not None)
    f["card_advantage"] = api_calls.count("Draw") + api_calls.count("Dig") + api_calls.count("Token")
    return f


def set_features(code: str) -> pd.DataFrame:
    rows = []
    for name, rarity in edition_cards(code).items():
        if rarity in "SL":
            continue
        f = features(name, rarity)
        if f:
            f["set"] = code
            rows.append(f)
    return pd.DataFrame(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sets", nargs="+")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    df = pd.concat([set_features(s) for s in args.sets], ignore_index=True)
    df.to_csv(args.out, index=False)
    print(df.groupby("set").size().to_string())


if __name__ == "__main__":
    main()

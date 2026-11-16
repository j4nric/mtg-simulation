# MTG-Draft-Simulation

Bewertet die Karten eines Magic-Sets für Booster Draft (Arena, Bo1), indem KI-Spieler
in [Forge](https://github.com/Card-Forge/forge) draften und tausende Partien
gegeneinander spielen. Erstes Ziel: eine Tier-Liste für Star Trek (`TRK`), geeicht an
echten Daten von 17Lands.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `harness/src/DraftSim.java` | 8-Spieler-Drafts nur mit KI, schreibt 40-Karten-Decks als `.dck` |
| `harness/src/GameRunner.java` | spielt zufällige Paarungen in einem Prozess, eine JSON-Zeile pro Partie |
| `scripts/run_sim.sh` | Drafts plus parallele Spiel-Prozesse in einem Lauf |
| `analysis/card_stats.py` | Winrates pro Karte im Stil von 17Lands (GP, OH, GD, GIH, GNS, IWD) |
| `analysis/compare_17lands.py` | Vergleich der Simulation mit echten 17Lands-Werten |

## Ablauf

```bash
# einmalig: Forge neben diesem Repo bauen (Java 17+, Maven)
git clone --depth 1 https://github.com/Card-Forge/forge ../card-forge/forge
(cd ../card-forge/forge && mvn -B -pl forge-gui-desktop -am package -DskipTests -Dcheckstyle.skip)

# 500 Drafts, dann 2 Prozesse mit je 2500 Partien
scripts/run_sim.sh TRK 500 2500 2 data/trk_run1

python analysis/card_stats.py data/trk_run1 --out data/trk_run1/cards.csv
python analysis/compare_17lands.py data/trk_run1/cards.csv 17lands_trk.json
```

Faustregel: Anzahl Prozesse = CPU-Kerne / 2, weil Forges KI pro Partie schon etwa
zwei Kerne nutzt.

## Messwerte (Cloud-Container, 4 Kerne)

- Draft: rund 2 Sekunden pro 8er-Pod
- Spiele: rund 3.400 Partien pro Stunde mit 2 Prozessen, keine Abstürze in den ersten 300 Partien
- Profil: rund 60 % der Rechenzeit in KI-Entscheidungen, 40 % in der Regel-Engine

## Bekannte Einschränkungen

- Die Draft-KI pickt nach Forges Rangliste `res/draft/rankings/trk.rnk`; die Decks
  spiegeln deren Vorlieben wider.
- Arenas Hand-Glättung für Bo1 ist nicht nachgebildet.
- „Gezogen“ heißt Bibliothek → Hand, Tutoren zählen also mit.

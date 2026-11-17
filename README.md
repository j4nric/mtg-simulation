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
| `analysis/lands17_card_stats.py` | dieselben Kennzahlen aus den öffentlichen 17Lands-Rohdaten |
| `analysis/reliability.py` | Split-Half-Reproduzierbarkeit der Rangfolge |
| `analysis/regression.py` | Kartenwert per logistischer Regression über alle Partien |
| `analysis/make_blind_rankings.py` | Draft-Rangliste nur nach Seltenheit (ohne 17Lands-Wissen) |
| `analysis/card_features.py` | Merkmale pro Karte aus Forges Kartenskripten |
| `analysis/predict_model.py` | Vorhersagemodell (gelernt an älteren Sets) plus Simulation |
| `analysis/make_tierlist.py` | Tierliste als Markdown |
| `tierlists/TRK.md` | aktuelle TRK-Tierliste |

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

## Validierung an EOE (17Lands, 563.418 echte Partien)

Je rund 3.000 simulierte Partien, Spearman-Rangkorrelation mit echter GIH WR:

| Variante | Spearman | Reproduzierbarkeit |
|---|---|---|
| nur Seltenheit (Baseline) | 0,09 | – |
| Sim, Draft nach Forges Rangliste | 0,09 | 0,75 |
| Sim, Draft blind nach Seltenheit | 0,33 | 0,72 |
| Regression über beide Läufe | 0,25 | – |
| Forges eigene Rangliste (aus 17Lands abgeleitet) | 0,98 | – |

Die Simulation misst stabil, aber etwas anderes als echte Spieler: Forges KI
überschätzt Kreaturen und unterschätzt Removal, Tricks und Counter. Mehr Partien
helfen dagegen nicht.

## Vorhersagemodell

Die reine Simulation reicht nicht, deshalb lernt ein Modell (Ridge plus LightGBM) aus
17 älteren Sets, wie Kartenwerte und Regeltext mit der echten GIH WR zusammenhängen.
Die blinde Simulation des neuen Sets wird hinzuaddiert: Score = z(Modell) + 1,0 × z(Sim-GIH-WR),
bei wenig gespielten Karten zur Mitte hin geschrumpft.

Geprüft wird jedes Set mit einem Modell, das es nicht kennt (Spearman mit echter GIH WR):

| Variante | EOE | DFT | BLB | Mittel 17 Sets |
|---|---|---|---|---|
| nur Seltenheit | 0,17 | 0,37 | 0,42 | 0,28 |
| nur Simulation | 0,36 | 0,41 | 0,44 | – |
| Modell | 0,51 | 0,52 | 0,56 | 0,48 |
| Modell + Simulation | **0,55** | **0,62** | **0,63** | – |

```bash
S="EOE FIN TDM DFT DSK BLB OTJ MKM FDN WOE LCI MOM ONE BRO DMU SNC NEO"
python analysis/card_features.py $S TRK --out data/features.csv
scripts/run_sim.sh TRK 250 1000 2 data/trk_blind1 data/rankings/trk_blind.rnk
python analysis/card_stats.py data/trk_blind1 --out data/trk_blind1/cards.csv
python analysis/predict_model.py --train $S --text --sim-weight 1.0 --predict TRK --out data/trk_scores.csv
python analysis/make_tierlist.py data/trk_scores.csv TRK tierlists/TRK.md
```

## Bekannte Einschränkungen

- Die Draft-KI pickt nach Forges Rangliste `res/draft/rankings/trk.rnk`; die Decks
  spiegeln deren Vorlieben wider.
- Das Modell kennt die Farbstärke eines neuen Formats nicht; sobald echte 17Lands-Daten
  da sind, sind diese besser.
- Arenas Hand-Glättung für Bo1 ist nicht nachgebildet.
- „Gezogen“ heißt Bibliothek → Hand, Tutoren zählen also mit.

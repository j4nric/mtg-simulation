# Forge-Harness

Simuliert Booster-Drafts mit 8 KI-Spielern in [Forge](https://github.com/Card-Forge/forge)
und schreibt die gebauten 40-Karten-Decks als `.dck`-Dateien. Die Decks lassen sich
mit Forges Simulationsmodus gegeneinander spielen.

## Forge bauen

```bash
git clone --depth 1 https://github.com/Card-Forge/forge
cd forge && mvn -B -pl forge-gui-desktop -am package -DskipTests -Dcheckstyle.skip
```

## Harness bauen und Drafts simulieren

```bash
FORGE=/pfad/zu/forge
JAR=$FORGE/forge-gui-desktop/target/forge-gui-desktop-*-jar-with-dependencies.jar
javac -cp $JAR -d build $(find src -name '*.java')

# muss im Verzeichnis forge-gui laufen (dort liegt res/)
cd $FORGE/forge-gui
java -Djava.awt.headless=true -cp $JAR:<harness>/build DraftSim TRK 25 /pfad/zu/decks
```

## Partien spielen

```bash
cd $FORGE/forge-gui
java -cp $JAR forge.view.Main sim -D /pfad/zu/decks -d d0001_s0.dck d0001_s1.dck -n 10 -q -c 120
```

## Hinweise

- `AllAiBoosterDraft` liegt im Paket `forge.gamemodes.limited`, weil es auf geschützte
  Felder von `BoosterDraft` zugreift. Forges eigene Factory teilt die Booster aus, bevor
  Platz 0 zur KI werden kann, sodass dieser Platz sonst nur eine Runde draftet.
- Die Draft-KI pickt nach `res/draft/rankings/trk.rnk`. Die Decks spiegeln also die
  Vorlieben dieser Rangliste wider.

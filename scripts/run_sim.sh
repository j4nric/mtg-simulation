#!/usr/bin/env bash
# Simulates drafts and then AI-vs-AI games for one set.
#
# Usage: scripts/run_sim.sh <SET> <numDrafts> <gamesPerWorker> <workers> <outDir> [rankings.rnk]
#   rankings.rnk  draft by this ranking instead of Forge's (see analysis/make_blind_rankings.py)
#   FORGE_DIR  Forge checkout with a built forge-gui-desktop (default: ../card-forge/forge)
#
# Each worker is its own JVM. Forge's AI already uses about two cores per game,
# so workers = CPU cores / 2 gives the best throughput.
set -euo pipefail

SET=$1; DRAFTS=$2; GAMES=$3; WORKERS=$4; OUT=$(realpath -m "$5")
RANKINGS=${6:+$(realpath "$6")}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
FORGE_DIR=$(realpath "${FORGE_DIR:-$ROOT/../card-forge/forge}")
JAR=$(ls "$FORGE_DIR"/forge-gui-desktop/target/forge-gui-desktop-*-jar-with-dependencies.jar | head -1)
BUILD="$ROOT/harness/build"

mkdir -p "$BUILD" "$OUT/decks" "$OUT/games" "$OUT/logs"
javac -nowarn -cp "$JAR" -d "$BUILD" $(find "$ROOT/harness/src" -name '*.java')

cd "$FORGE_DIR/forge-gui"   # Forge looks for res/ in the working directory

if [ -z "$(ls -A "$OUT/decks")" ]; then
  echo "Drafting $DRAFTS pods of $SET ..."
  java -Xmx2g -Djava.awt.headless=true -cp "$JAR:$BUILD" DraftSim "$SET" "$DRAFTS" "$OUT/decks" ${RANKINGS:+"$RANKINGS"} \
    > "$OUT/logs/draft.log" 2>&1
  tail -1 "$OUT/logs/draft.log"
fi

echo "Playing $GAMES games in each of $WORKERS workers ..."
for w in $(seq 1 "$WORKERS"); do
  seed=$(( $(date +%s) * 100 + w ))
  java -Xmx2g -Djava.awt.headless=true -cp "$JAR:$BUILD" GameRunner \
    "$OUT/decks" "$GAMES" "$seed" "$OUT/games/games_$seed.jsonl" \
    > "$OUT/logs/worker_$seed.log" 2>&1 &
done
wait
echo "Done. $(cat "$OUT"/games/*.jsonl | wc -l) games in $OUT/games"

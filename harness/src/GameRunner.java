import com.google.common.eventbus.Subscribe;
import forge.GuiDesktop;
import forge.deck.Deck;
import forge.deck.io.DeckSerializer;
import forge.game.Game;
import forge.game.GameRules;
import forge.game.GameType;
import forge.game.Match;
import forge.game.card.Card;
import forge.game.event.GameEventCardChangeZone;
import forge.game.event.GameEventTurnBegan;
import forge.game.player.Player;
import forge.game.player.RegisteredPlayer;
import forge.game.zone.ZoneType;
import forge.gui.GuiBase;
import forge.model.FModel;
import forge.player.GamePlayerUtil;
import forge.util.MyRandom;
import forge.view.TimeLimitedCodeBlock;

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * Plays many AI-vs-AI games between randomly paired decks in a single JVM and
 * writes one JSON line per game.
 *
 * Usage: GameRunner <decksDir> <numGames> <seed> <out.jsonl> [timeoutSec]
 * Must be started with the forge-gui directory as working directory (for res/).
 *
 * Per player the record lists the deck, whether the player was on the play,
 * the opening hand (cards in hand when turn 1 begins, i.e. after mulligans) and
 * every card that later moved from library to hand (draws and tutors).
 */
public class GameRunner {

    /** Collects opening hands and later library-to-hand moves via the game's event bus. */
    public static class DrawTracker {
        private final Game game;
        boolean started = false;
        String firstPlayer = null;
        final Map<String, List<String>> openingHand = new HashMap<>();
        final Map<String, List<String>> drawn = new HashMap<>();

        DrawTracker(Game game) { this.game = game; }

        @Subscribe
        public void onTurn(GameEventTurnBegan ev) {
            if (started) return;
            started = true;
            firstPlayer = ev.turnOwner().getName();
            for (Player p : game.getPlayers()) {
                List<String> hand = new ArrayList<>();
                for (Card c : p.getCardsIn(ZoneType.Hand)) hand.add(c.getName());
                openingHand.put(p.getName(), hand);
                drawn.put(p.getName(), new ArrayList<>());
            }
        }

        @Subscribe
        public void onZone(GameEventCardChangeZone ev) {
            if (!started || ev.from() == null || ev.to() == null) return;
            if (ev.from().zoneType() != ZoneType.Library || ev.to().zoneType() != ZoneType.Hand) return;
            String owner = ev.to().player().getName();
            drawn.computeIfAbsent(owner, k -> new ArrayList<>()).add(ev.card().getCurrentState().getName());
        }
    }

    public static void main(String[] args) throws Exception {
        File decksDir = new File(args[0]);
        int numGames = Integer.parseInt(args[1]);
        long seed = Long.parseLong(args[2]);
        File out = new File(args[3]);
        int timeoutSec = args.length > 4 ? Integer.parseInt(args[4]) : 120;

        GuiBase.setInterface(new GuiDesktop());
        FModel.initialize(null, null);

        File[] files = decksDir.listFiles((d, n) -> n.endsWith(".dck"));
        if (files == null || files.length < 2) throw new IllegalArgumentException("Need at least 2 decks in " + decksDir);
        Arrays.sort(files);
        Map<String, Deck> decks = new LinkedHashMap<>();
        for (File f : files) decks.put(f.getName().replace(".dck", ""), DeckSerializer.fromFile(f));
        List<String> names = new ArrayList<>(decks.keySet());

        Random rng = new Random(seed);
        MyRandom.setRandom(new Random(seed ^ 0x5DEECE66DL));

        GameRules rules = new GameRules(GameType.Draft);
        rules.setAppliedVariants(EnumSet.of(GameType.Draft));
        rules.setGamesPerMatch(1);

        long t0 = System.currentTimeMillis();
        int done = 0, draws = 0, errors = 0;
        try (PrintWriter pw = new PrintWriter(new FileWriter(out, true))) {
            for (int g = 0; g < numGames; g++) {
                String a = names.get(rng.nextInt(names.size()));
                String b;
                do { b = names.get(rng.nextInt(names.size())); } while (b.equals(a));

                List<RegisteredPlayer> players = new ArrayList<>();
                RegisteredPlayer ra = new RegisteredPlayer(decks.get(a));
                ra.setPlayer(GamePlayerUtil.createAiPlayer("A", 0));
                RegisteredPlayer rb = new RegisteredPlayer(decks.get(b));
                rb.setPlayer(GamePlayerUtil.createAiPlayer("B", 1));
                players.add(ra);
                players.add(rb);

                Match match = new Match(rules, players, "sim");
                Game game = match.createGame();
                game.setNoGUIUser();
                DrawTracker tracker = new DrawTracker(game);
                game.subscribeToEvents(tracker);

                long gs = System.currentTimeMillis();
                String status = "ok";
                try {
                    TimeLimitedCodeBlock.runWithTimeout(() -> match.startGame(game), timeoutSec, TimeUnit.SECONDS);
                } catch (TimeoutException e) {
                    status = "timeout";
                } catch (Throwable e) {
                    status = "error";
                    System.err.println("Game " + g + " (" + a + " vs " + b + ") failed: " + e);
                }
                long ms = System.currentTimeMillis() - gs;

                String winner = null;
                int turns = -1;
                if (status.equals("ok") && game.getOutcome() != null) {
                    turns = game.getOutcome().getLastTurnNumber();
                    if (!game.getOutcome().isDraw()) winner = game.getOutcome().getWinningLobbyPlayer().getName();
                }
                if (winner == null) {
                    if (status.equals("ok")) status = "draw";
                }
                switch (status) {
                    case "draw", "timeout" -> draws++;
                    case "error" -> errors++;
                    default -> { }
                }

                StringBuilder sb = new StringBuilder();
                sb.append("{\"seed\":").append(seed).append(",\"game\":").append(g)
                  .append(",\"status\":\"").append(status).append('"')
                  .append(",\"winner\":").append(winner == null ? "null" : "\"" + winner + "\"")
                  .append(",\"turns\":").append(turns)
                  .append(",\"ms\":").append(ms)
                  .append(",\"on_play\":").append(tracker.firstPlayer == null ? "null" : "\"" + tracker.firstPlayer + "\"")
                  .append(",\"players\":{");
                String[][] seats = {{"A", a}, {"B", b}};
                for (int i = 0; i < 2; i++) {
                    String p = seats[i][0];
                    if (i > 0) sb.append(',');
                    sb.append('"').append(p).append("\":{\"deck\":\"").append(seats[i][1]).append('"')
                      .append(",\"opening\":").append(jsonList(tracker.openingHand.get(p)))
                      .append(",\"drawn\":").append(jsonList(tracker.drawn.get(p)))
                      .append('}');
                }
                sb.append("}}");
                pw.println(sb);
                pw.flush();
                done++;

                if (done % 25 == 0) {
                    double rate = done * 3600_000.0 / (System.currentTimeMillis() - t0);
                    System.out.printf("%d/%d games, %.0f games/h, %d draws/timeouts, %d errors%n",
                            done, numGames, rate, draws, errors);
                }
            }
        }
        System.out.printf("Done: %d games in %d s, %d draws/timeouts, %d errors%n",
                done, (System.currentTimeMillis() - t0) / 1000, draws, errors);
        System.exit(0);
    }

    private static String jsonList(List<String> xs) {
        if (xs == null) return "[]";
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < xs.size(); i++) {
            if (i > 0) sb.append(',');
            sb.append('"').append(xs.get(i).replace("\\", "\\\\").replace("\"", "\\\"")).append('"');
        }
        return sb.append(']').toString();
    }
}

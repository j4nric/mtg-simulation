import forge.GuiDesktop;
import forge.deck.CardPool;
import forge.deck.Deck;
import forge.deck.DeckSection;
import forge.deck.io.DeckSerializer;
import forge.gamemodes.limited.AllAiBoosterDraft;
import forge.gamemodes.limited.LimitedPlayer;
import forge.gamemodes.limited.LimitedPlayerAI;
import forge.gui.GuiBase;
import forge.item.PaperCard;
import forge.model.CardBlock;
import forge.model.FModel;

import java.io.File;

/**
 * Runs N fully-AI 8-player booster drafts of one set and writes each seat's
 * 40-card deck as a .dck file (the rest of the pool goes to the sideboard).
 *
 * Usage: DraftSim <SETCODE> <numDrafts> <outDir>
 * Must be started with the forge-gui directory as working directory (for res/).
 */
public class DraftSim {
    public static void main(String[] args) {
        String setCode = args[0];
        int numDrafts = Integer.parseInt(args[1]);
        File outDir = new File(args[2]);
        outDir.mkdirs();

        GuiBase.setInterface(new GuiDesktop());
        FModel.initialize(null, null);

        CardBlock block = null;
        for (CardBlock b : FModel.getBlocks()) {
            if (b.getSets().stream().anyMatch(e -> e.getCode().equals(setCode))) {
                block = b;
                break;
            }
        }
        if (block == null) throw new IllegalArgumentException("No block for " + setCode);

        long t0 = System.currentTimeMillis();
        int written = 0;
        for (int d = 0; d < numDrafts; d++) {
            AllAiBoosterDraft draft = AllAiBoosterDraft.create(block, setCode, 3, 8);
            LimitedPlayerAI seat0 = (LimitedPlayerAI) draft.getHumanPlayer();

            while (draft.hasNextChoice()) {
                CardPool pack = draft.nextChoice();
                if (pack == null) break;
                PaperCard pick = seat0.chooseCard();
                if (pick == null) { draft.skipChoice(); continue; }
                draft.setChoice(pick, DeckSection.Sideboard);
            }

            int seat = 0;
            for (LimitedPlayer p : draft.getAllPlayers()) {
                int poolSize = p.getDeck().getOrCreate(DeckSection.Sideboard).countAll();
                Deck deck = ((LimitedPlayerAI) p).buildDeck(setCode);
                String name = String.format("d%04d_s%d", d, seat++);
                deck.setName(name);
                DeckSerializer.writeDeck(deck, new File(outDir, name + ".dck"));
                if (poolSize < 39) System.err.println("WARN " + name + " pool only " + poolSize);
                written++;
            }
        }
        System.out.printf("Wrote %d decks from %d drafts in %d ms%n",
                written, numDrafts, System.currentTimeMillis() - t0);
        System.exit(0);
    }
}

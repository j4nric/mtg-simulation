package forge.gamemodes.limited;

import forge.card.CardEdition;
import forge.model.CardBlock;
import forge.model.FModel;

import java.util.Set;

/**
 * A booster draft in which every seat, including seat 0, is an AI drafter.
 *
 * Forge's own factory deals the packs before seats can be reassigned, so the
 * reassigned seat 0 would hold no packs of its own. This factory makes all
 * seats AI first and only then opens the boosters.
 */
public class AllAiBoosterDraft extends BoosterDraft {

    private AllAiBoosterDraft(int podSize) {
        super(LimitedPoolType.Block, podSize);
    }

    public static AllAiBoosterDraft create(CardBlock block, String setCode, int rounds, int podSize) {
        return create(block, setCode, rounds, podSize, null);
    }

    /**
     * @param customRankings ranking file to draft and build decks by instead of
     *                       Forge's own, or null. Forge resolves it relative to res/draft/.
     */
    public static AllAiBoosterDraft create(CardBlock block, String setCode, int rounds, int podSize,
                                           String customRankings) {
        AllAiBoosterDraft draft = new AllAiBoosterDraft(podSize);
        draft.setHumanSeats(Set.of());

        CardEdition edition = FModel.getMagicDb().getEditions().get(setCode);
        if (edition != null) {
            draft.setDoublePick(edition.getDraftOptions().getDoublePick());
        }
        for (int i = 0; i < rounds; i++) {
            draft.product.add(block.getBooster(setCode));
        }
        IBoosterDraft.LAND_SET_CODE[0] = block.getLandSet();
        IBoosterDraft.CUSTOM_RANKINGS_FILE[0] = customRankings;

        draft.initializeBoosters();
        return draft;
    }
}

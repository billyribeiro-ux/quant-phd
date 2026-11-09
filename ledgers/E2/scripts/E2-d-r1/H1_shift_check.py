# H1: per-auction check of E2-c136 ("the winner's profit rises by 1334 cents in every auction") and E2-c102 totals,
# re-running the L08 Lab 1 auction loop (same seed, same draw order) for shade 0 and shade 1334.
import random
AUCTIONS, SEED, V_LOW, V_HIGH, HALF_WIDTH, BIDDERS = 20000, 20261028, 5000, 15000, 2000, 5
def run(shade, rng):
    profits = []; diffs_ok = 0
    for _ in range(AUCTIONS):
        value = rng.randint(V_LOW, V_HIGH)
        signals = [value + rng.randint(-HALF_WIDTH, HALF_WIDTH) for _ in range(BIDDERS)]
        bids = [s - shade for s in signals]
        winner = max(range(BIDDERS), key=lambda i: (bids[i], -i))
        profits.append(value - bids[winner])
    return profits
naive = run(0, random.Random(SEED))
shaded = run(1334, random.Random(SEED))
d = [s - n for s, n in zip(shaded, naive)]
print("auctions:", len(d), "per-auction differences all 1334:", all(x == 1334 for x in d))
print("naive total:", sum(naive), " shaded total:", sum(shaded), " shaded - naive:", sum(shaded) - sum(naive))
print("20000 * 1334 =", 20000 * 1334, " 59282 - (-26620718) =", 59282 - (-26620718))
print("c102 difference 59282 - 6669 =", 59282 - 6669, " 52613/79810 =", round(52613 / 79810, 4))

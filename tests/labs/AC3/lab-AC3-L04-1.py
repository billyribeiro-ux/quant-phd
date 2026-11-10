"""AC3 lab L04: post-earnings-announcement drift (PEAD) and delayed price response.

SIMULATED: the cross-section of 100 firms, their SUE surprises, post-announcement returns,
and subsequent announcement returns at lags t+1 to t+4 are generated under the Bernard & Thomas (1989)
autocorrelation structure. All calculations use standard library float and math.
"""

from __future__ import annotations

import random

SEED = 20261110
N_FIRMS = 100
N_DECILES = 10


def simulate_pead_cross_section(
    seed: int,
) -> tuple[list[float], list[float], list[list[float]]]:
    """Simulate SUE scores, 60-day post-announcement CAR, and 4 subsequent announcement reactions.

    Returns (sue_scores, car_60, subsequent_announcements).
    """
    rng = random.Random(seed)
    sue_scores: list[float] = []
    car_60: list[float] = []
    subsequent_announcements: list[list[float]] = []

    # Bernard & Thomas (1989) typical autocorrelations:
    # rho_1 = +0.34, rho_2 = +0.19, rho_3 = +0.06, rho_4 = -0.24
    lag_weights = [0.34, 0.19, 0.06, -0.24]

    for _ in range(N_FIRMS):
        sue = rng.gauss(0.0, 1.0)
        sue_scores.append(sue)

        # 60-day post-announcement drift CAR[+2, +60]:
        # Drift sensitivity ~ 2.5% per SUE unit, plus firm-specific noise
        drift = 0.025 * sue + rng.gauss(0.0, 0.04)
        car_60.append(drift)

        # 3-day abnormal return at subsequent announcements t+1, t+2, t+3, t+4
        sub_reactions: list[float] = []
        for rho in lag_weights:
            # Expected reaction proportional to unexpected seasonal change
            rxn = 0.015 * (rho * sue) + rng.gauss(0.0, 0.015)
            sub_reactions.append(rxn)
        subsequent_announcements.append(sub_reactions)

    return sue_scores, car_60, subsequent_announcements


def assign_deciles(scores: list[float]) -> list[int]:
    """Assign observations to 10 deciles (1..10) based on ranking.

    Ties broken by index. Decile 1 = lowest SUE, Decile 10 = highest SUE.
    """
    n = len(scores)
    indexed = sorted(range(n), key=lambda i: (scores[i], i))
    deciles = [0] * n
    for rank, idx in enumerate(indexed):
        d = min(N_DECILES, (rank * N_DECILES) // n + 1)
        deciles[idx] = d
    return deciles


def main() -> None:
    sue_scores, car_60, subsequent = simulate_pead_cross_section(SEED)
    deciles = assign_deciles(sue_scores)

    print(f"seed {SEED} firms {N_FIRMS} deciles {N_DECILES}")
    print(f"{'Decile':7s} | {'Count':5s} | {'Mean_SUE':9s} | {'Drift_CAR_60':13s} | {'t+1_Rxn':8s} | {'t+4_Rxn':8s}")
    print("-" * 65)

    decile_drift: dict[int, float] = {}
    decile_t1: dict[int, float] = {}
    decile_t4: dict[int, float] = {}

    for d in range(1, N_DECILES + 1):
        idxs = [i for i in range(N_FIRMS) if deciles[i] == d]
        count = len(idxs)
        mean_sue = sum(sue_scores[i] for i in idxs) / count
        mean_drift = sum(car_60[i] for i in idxs) / count
        mean_t1 = sum(subsequent[i][0] for i in idxs) / count
        mean_t4 = sum(subsequent[i][3] for i in idxs) / count

        decile_drift[d] = mean_drift
        decile_t1[d] = mean_t1
        decile_t4[d] = mean_t4

        print(f"{d:7d} | {count:5d} | {mean_sue:+9.3f} | {mean_drift:+13.4f} | {mean_t1:+8.4f} | {mean_t4:+8.4f}")

    gross_spread = decile_drift[10] - decile_drift[1]
    t1_spread = decile_t1[10] - decile_t1[1]
    t4_spread = decile_t4[10] - decile_t4[1]

    print("-" * 65)
    print(f"gross_drift_spread_decile_10_minus_1: {gross_spread:+.4f}")
    print(f"subsequent_t+1_announcement_spread: {t1_spread:+.4f}")
    print(f"subsequent_t+4_announcement_spread: {t4_spread:+.4f}")

    # Bernard & Thomas signature: t+1 spread has same sign as surprise, t+4 has opposite sign
    print(f"bernard_thomas_t1_positive: {t1_spread > 0}")
    print(f"bernard_thomas_t4_reversal: {t4_spread < 0}")

    # Net-of-cost drift under varying execution costs (round-trip bps)
    costs_bps = [0.0, 15.0, 30.0, 60.0]
    print("\nnet_of_cost_evaluation:")
    for cost in costs_bps:
        # Long decile 10, short decile 1 -> 2 legs * cost
        net_spread = gross_spread - 2.0 * (cost / 10000.0)
        print(f"cost_bps {cost:4.1f} : net_hedge_spread {net_spread:+.4f} | profitable {net_spread > 0}")


main()

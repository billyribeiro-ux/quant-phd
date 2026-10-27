"""AC2 L05 lab 1: an accrual-sorted portfolio study on a SIMULATED universe. It checks the mechanics only.

SIMULATED: every return in this lab is generated from the model below. No market data is read and no
published return is reproduced. The planted effect BETA is chosen by the author, so the spread this
lab recovers is the spread the generator put in. The lab shows how the sort, the spread and the
t-statistic behave when the effect is known. It says nothing about the size of the accruals effect
in real stock returns, and it does not reproduce Sloan (1996).

Model, per month t and firm i (units: monthly simple return, so 0.01 is one percent):
    z[t, i]   standardized accrual signal, the sort variable (known exactly here)
    r[t, i]   = BASE + BETA * z[t, i] + SIGMA * eps[t, i],  eps iid N(0, 1)
Each month the firms are sorted on z into quintiles of equal size. The strategy is long the lowest-accrual
quintile and short the highest, equal-weighted. The monthly spread is r_low - r_high.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

F64 = NDArray[np.float64]

N_FIRMS = 500
N_MONTHS = 120  # ten years of monthly spreads
SIGMA = 0.08  # idiosyncratic monthly volatility of each simulated stock
BASE = 0.005  # simulated mean monthly return of the universe
BETA = -0.0008  # the planted effect: a one-SD higher accrual lowers the monthly return by 8 basis points
N_SEEDS = 200
QUINTILE = N_FIRMS // 5
CRITICAL = 1.96  # normal approximation to the 5% two-sided critical value for |t|


def simulate(seed: int, beta: float, n_firms: int = N_FIRMS) -> tuple[F64, F64]:
    """Monthly spreads (long low-accrual, short high-accrual) and the realised z-gap for one seeded universe.

    Each month sorts n_firms firms into quintiles of n_firms // 5 firms, so the z-gap is the realised gap of that sort.
    """
    quintile = n_firms // 5
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((N_MONTHS, n_firms))
    eps = rng.standard_normal((N_MONTHS, n_firms))
    r = BASE + beta * z + SIGMA * eps
    order = np.argsort(z, axis=1, kind="stable")
    low = order[:, :quintile]
    high = order[:, -quintile:]
    r_low = np.take_along_axis(r, low, axis=1).mean(axis=1)
    r_high = np.take_along_axis(r, high, axis=1).mean(axis=1)
    z_low = np.take_along_axis(z, low, axis=1).mean(axis=1)
    z_high = np.take_along_axis(z, high, axis=1).mean(axis=1)
    return r_low - r_high, z_low - z_high


def t_stat(x: F64) -> float:
    """Mean over its standard error, with n - 1 degrees of freedom in the standard deviation."""
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(x.size)))


def main() -> None:
    null_t: list[float] = []
    effect_t: list[float] = []
    effect_means: list[float] = []
    gaps: list[float] = []
    for seed in range(N_SEEDS):
        spread0, _ = simulate(seed, 0.0)
        spread1, gap = simulate(seed, BETA)
        null_t.append(t_stat(spread0))
        effect_t.append(t_stat(spread1))
        effect_means.append(float(spread1.mean()))
        gaps.append(float(gap.mean()))

    null = np.array(null_t)
    effect = np.array(effect_t)
    planted = BETA * float(np.mean(gaps))  # expected monthly spread: BETA times the mean z-gap of the quintiles

    print(f"seeds {N_SEEDS} months {N_MONTHS} firms {N_FIRMS} sigma {SIGMA} beta {BETA}")
    print(f"mean_z_gap_simulated {float(np.mean(gaps)):.4f}")
    print(f"planted_monthly_spread {planted:.5f}")
    sd_theory = SIGMA * np.sqrt(2.0 / QUINTILE)  # sd of a two-leg spread: each leg averages QUINTILE firms
    print(f"spread_sd_theory {sd_theory:.5f}")
    print(f"expected_t_at_planted {planted / (sd_theory / np.sqrt(N_MONTHS)):.3f}")
    print(f"recovered_mean_monthly_spread {float(np.mean(effect_means)):.5f}")
    print(f"null_mean_t {float(null.mean()):.3f} null_sd_t {float(null.std(ddof=1)):.3f}")
    print(f"null_false_positive_rate {float(np.mean(np.abs(null) > CRITICAL)):.3f}")
    print(f"effect_rejection_rate_power {float(np.mean(np.abs(effect) > CRITICAL)):.3f}")
    print(f"effect_median_t {float(np.median(effect)):.3f}")
    print(f"seed0_spread_mean {float(effect_means[0]):.5f} seed0_t {effect_t[0]:.3f}")
    # The realised gap of the sort depends on how many firms are sorted each month (20 seeds at each size).
    for n_firms in (500, 5000):
        gap_n = [simulate(seed, 0.0, n_firms)[1].mean() for seed in range(20)]
        print(f"mean_z_gap_firms_{n_firms}_seeds_20 {float(np.mean(gap_n)):.4f}")


main()

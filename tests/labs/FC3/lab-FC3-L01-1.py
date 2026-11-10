"""Lab FC3-L01-1: Fair-game conditional expectation check.

SIMULATED return series to test the fair-game property:
E[r_{t+1} | past information] = E[r_{t+1}].
"""

from __future__ import annotations

import math
import random


def main() -> None:
    """Run fair-game simulation and compare conditional to unconditional mean."""
    rng = random.Random(42)
    n_periods = 20000
    mu = 0.008
    sigma = 0.040

    # SIMULATED: Seeded fair-game return series
    returns = [rng.gauss(mu, sigma) for _ in range(n_periods)]

    # Conditioning on sign of prior month return: r_{t-1} > 0 vs <= 0
    r_pos_next = [returns[t] for t in range(1, n_periods) if returns[t - 1] > 0]
    r_neg_next = [returns[t] for t in range(1, n_periods) if returns[t - 1] <= 0]

    mean_uncond = sum(returns) / n_periods
    mean_pos = sum(r_pos_next) / len(r_pos_next)
    mean_neg = sum(r_neg_next) / len(r_neg_next)

    diff_pos = abs(mean_pos - mean_uncond)
    diff_neg = abs(mean_neg - mean_uncond)

    # 99% Monte Carlo critical bound: 2.576 * sigma / sqrt(n_cond)
    tol_pos = 2.576 * sigma / math.sqrt(len(r_pos_next))
    tol_neg = 2.576 * sigma / math.sqrt(len(r_neg_next))

    print(f"Unconditional mean: {mean_uncond:.6f}")
    print(f"Conditional mean (r_t > 0): {mean_pos:.6f}")
    print(f"Conditional mean (r_t <= 0): {mean_neg:.6f}")
    print(f"Difference (|cond - uncond|): {diff_pos:.6f}")
    print(f"Monte Carlo tolerance: {tol_pos:.6f}")
    print(f"Fair-game property satisfied: {diff_pos < tol_pos and diff_neg < tol_neg}")


main()

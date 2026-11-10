"""Lab FC3-L03-1: Luck versus skill in fund performance.

SIMULATED universe of N=1000 zero-skill funds, testing the number of funds
exhibiting significant positive t-statistics by chance alone across seeds 0 to 9.
"""

from __future__ import annotations

import math
import random


def normal_quantile(p: float, tol: float = 1e-12) -> float:
    """Compute normal quantile via bisection on math.erf."""
    low, high = -10.0, 10.0
    target = 2.0 * p - 1.0
    while high - low > tol:
        mid = (low + high) / 2.0
        val = math.erf(mid / math.sqrt(2.0))
        if val < target:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def main() -> None:
    """Evaluate false positive counts across 10 random seeds."""
    n_funds = 1000
    n_months = 60
    level = 0.05
    crit = normal_quantile(1.0 - level)
    expected_count = n_funds * level

    print(f"Universe: N={n_funds} funds, T={n_months} months, zero true alpha (SIMULATED)")
    print(f"One-sided level: {level:.2f}, Normal critical value: {crit:.6f}")
    print(f"Expected false positives under null: {expected_count:.1f}")
    print("Seed | False Positives | Excess Over Expected")
    print("-----+-----------------+---------------------")

    counts: list[int] = []
    for seed in range(10):
        rng = random.Random(seed)
        factor = [rng.gauss(0.007, 0.045) for _ in range(n_months)]
        mean_f = sum(factor) / n_months
        s_ff = sum((f - mean_f) ** 2 for f in factor)

        cnt = 0
        for _ in range(n_funds):
            beta = 0.8 + 0.4 * rng.random()
            # True alpha is zero: r_it = beta * f_t + noise
            r = [beta * factor[t] + rng.gauss(0.0, 0.020) for t in range(n_months)]
            mean_r = sum(r) / n_months
            s_fr = sum((factor[t] - mean_f) * (r[t] - mean_r) for t in range(n_months))
            b = s_fr / s_ff
            a = mean_r - b * mean_f
            rss = sum((r[t] - (a + b * factor[t])) ** 2 for t in range(n_months))
            s2 = rss / (n_months - 2)
            se_a = math.sqrt(s2 * (1.0 / n_months + (mean_f**2) / s_ff))
            t_stat = a / se_a
            if t_stat > crit:
                cnt += 1
        counts.append(cnt)
        print(f"{seed:4d} | {cnt:15d} | {cnt - expected_count:+19.1f}")

    avg_cnt = sum(counts) / len(counts)
    print("-----+-----------------+---------------------")
    print(f"Mean false positives across 10 seeds: {avg_cnt:.2f} (expected {expected_count:.1f})")


main()

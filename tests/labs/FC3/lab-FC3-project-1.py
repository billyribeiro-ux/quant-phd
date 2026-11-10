"""Lab FC3-project-1: Project Rung 1 worked example.

SIMULATED 6-fund universe with T=24 months and one planted skilled fund (Fund 2).
Performs OLS regression, chance count, expected count, and bootstrap skill detection.
"""

from __future__ import annotations

import math
import random


def alpha_and_t(returns: list[float], factor: list[float]) -> tuple[float, float]:
    """Compute OLS alpha and t-statistic."""
    n_months = len(returns)
    mean_f = sum(factor) / n_months
    mean_r = sum(returns) / n_months

    s_ff = sum((f - mean_f) ** 2 for f in factor)
    s_fr = sum((factor[t] - mean_f) * (returns[t] - mean_r) for t in range(n_months))
    beta = s_fr / s_ff
    alpha = mean_r - beta * mean_f

    rss = sum((returns[t] - (alpha + beta * factor[t])) ** 2 for t in range(n_months))
    s2 = rss / (n_months - 2)
    var_a = s2 * (1.0 / n_months + (mean_f**2) / s_ff)
    se_a = math.sqrt(var_a)
    t_stat = alpha / se_a
    return alpha, t_stat


def main() -> None:
    """Run fully worked 6-fund performance analysis."""
    rng = random.Random(101)
    n_funds = 6
    n_months = 24
    planted_fund = 2

    # SIMULATED: Benchmark factor
    factor = [rng.gauss(0.008, 0.040) for _ in range(n_months)]

    # Returns for 6 funds: Fund 2 has planted monthly alpha of +0.015 (150 bps)
    returns: list[list[float]] = []
    for i in range(n_funds):
        alpha = 0.015 if i == planted_fund else 0.000
        beta = 0.9 + 0.2 * rng.random()
        r_i = [alpha + beta * factor[t] + rng.gauss(0.0, 0.015) for t in range(n_months)]
        returns.append(r_i)

    # Step 1: OLS estimation for all funds
    alphas: list[float] = []
    t_stats: list[float] = []
    print("Fund | Alpha (monthly) | t-statistic | Planted Status")
    print("-----+-----------------+-------------+---------------")
    for i in range(n_funds):
        a_i, t_i = alpha_and_t(returns[i], factor)
        alphas.append(a_i)
        t_stats.append(t_i)
        status = "Skilled (planted)" if i == planted_fund else "Zero-skill"
        print(f"{i:4d} | {a_i:15.5f} | {t_i:11.3f} | {status}")

    # Step 2: Naive count at one-sided 5% level
    crit_val = 1.644854
    naive_flagged = [i for i, t in enumerate(t_stats) if t > crit_val]
    expected_chance = n_funds * 0.05

    print("-----+-----------------+-------------+---------------")
    print(f"Naive flagged count (t > {crit_val:.4f}): {len(naive_flagged)} (Funds {naive_flagged})")
    print(f"Expected false positives by chance alone: {expected_chance:.2f}")

    # Step 3: Bootstrap threshold
    n_boot = 200
    boot_rng = random.Random(42)
    mean_f = sum(factor) / n_months
    s_ff = sum((f - mean_f) ** 2 for f in factor)

    slopes = [
        sum((factor[t] - mean_f) * (returns[i][t] - sum(returns[i]) / n_months) for t in range(n_months)) / s_ff
        for i in range(n_funds)
    ]
    residuals = [[returns[i][t] - (alphas[i] + slopes[i] * factor[t]) for t in range(n_months)] for i in range(n_funds)]

    max_t_boot: list[float] = []
    for _ in range(n_boot):
        tau = [boot_rng.randrange(n_months) for _ in range(n_months)]
        m_k = -1e9
        for i in range(n_funds):
            r_null = [slopes[i] * factor[t] + residuals[i][tau[t]] for t in range(n_months)]
            _, t_boot = alpha_and_t(r_null, factor)
            if t_boot > m_k:
                m_k = t_boot
        max_t_boot.append(m_k)

    max_t_boot.sort()
    idx = math.ceil((1.0 - 0.05) * n_boot) - 1
    boot_thresh = max_t_boot[idx]
    boot_flagged = [i for i, t in enumerate(t_stats) if t > boot_thresh]

    print(f"Bootstrap 95% max-t threshold: {boot_thresh:.4f}")
    print(f"Bootstrap recovered skilled funds: {boot_flagged}")
    print(f"Planted fund recovered successfully: {boot_flagged == [planted_fund]}")


main()

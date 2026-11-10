"""Lab S1-L10-1: Bootstrap vs. asymptotic confidence intervals for a Sharpe ratio.

Curriculum lab (yaml:653): computes asymptotic and percentile bootstrap 95% confidence intervals
for a per-period Sharpe ratio on i.i.d. returns, and checks empirical coverage over replications.
SIMULATED: all returns are generated with random.Random(1010).
Standard library only. No external imports.
"""

from __future__ import annotations

import math
import random
import statistics


def main() -> None:
    seed = 1010
    rng = random.Random(seed)
    t_periods = 120  # 10 years of monthly returns
    mu = 0.01  # 1% per period
    sigma = 0.04  # 4% per period
    true_sr = mu / sigma  # 0.25 per period

    z95 = statistics.NormalDist().inv_cdf(0.975)

    # 1. Primary sample analysis
    sample = [rng.gauss(mu, sigma) for _ in range(t_periods)]
    m = math.fsum(sample) / t_periods
    v = math.fsum((x - m) ** 2 for x in sample) / (t_periods - 1)
    s = math.sqrt(v)
    hsr = m / s

    # Asymptotic standard error under i.i.d. normality: sqrt((1 + hSR^2 / 2) / T)
    se_asy = math.sqrt((1.0 + (hsr**2) / 2.0) / t_periods)
    ci_asy_lo = hsr - z95 * se_asy
    ci_asy_hi = hsr + z95 * se_asy

    # Percentile bootstrap interval with B = 1000 resamples
    b = 1000
    boot_srs: list[float] = []
    for _ in range(b):
        res = [sample[rng.randrange(t_periods)] for _ in range(t_periods)]
        rm = math.fsum(res) / t_periods
        rv = math.fsum((x - rm) ** 2 for x in res) / (t_periods - 1)
        boot_srs.append(rm / math.sqrt(rv))

    boot_srs.sort()
    ci_boot_lo = boot_srs[int(0.025 * b)]
    ci_boot_hi = boot_srs[int(0.975 * b)]

    print(f"sample periods T: {t_periods}, true Sharpe ratio SR: {true_sr:.4f}")
    print(f"sample Sharpe ratio hSR: {hsr:.4f}")
    print(f"asymptotic standard error se(hSR): {se_asy:.4f}")
    print(f"asymptotic 95% CI: [{ci_asy_lo:.4f}, {ci_asy_hi:.4f}] (width: {ci_asy_hi - ci_asy_lo:.4f})")
    print(f"bootstrap 95% CI (B = {b}): [{ci_boot_lo:.4f}, {ci_boot_hi:.4f}] (width: {ci_boot_hi - ci_boot_lo:.4f})")

    # 2. Empirical coverage check over 100 seeded replications
    n_replications = 100
    covered_asy = 0
    covered_boot = 0
    b_coverage = 500

    for _ in range(n_replications):
        rep_sample = [rng.gauss(mu, sigma) for _ in range(t_periods)]
        rm = math.fsum(rep_sample) / t_periods
        rv = math.fsum((x - rm) ** 2 for x in rep_sample) / (t_periods - 1)
        rhs = rm / math.sqrt(rv)
        r_se = math.sqrt((1.0 + (rhs**2) / 2.0) / t_periods)

        if rhs - z95 * r_se <= true_sr <= rhs + z95 * r_se:
            covered_asy += 1

        b_s: list[float] = []
        for _ in range(b_coverage):
            b_res = [rep_sample[rng.randrange(t_periods)] for _ in range(t_periods)]
            bm = math.fsum(b_res) / t_periods
            bv = math.fsum((x - bm) ** 2 for x in b_res) / (t_periods - 1)
            b_s.append(bm / math.sqrt(bv))
        b_s.sort()
        if b_s[int(0.025 * b_coverage)] <= true_sr <= b_s[int(0.975 * b_coverage)]:
            covered_boot += 1

    rate_asy = covered_asy / n_replications
    rate_boot = covered_boot / n_replications

    print(f"coverage over {n_replications} replications (seed = {seed}):")
    print(f"asymptotic CI empirical coverage: {rate_asy:.2%}")
    print(f"bootstrap CI empirical coverage: {rate_boot:.2%}")


main()

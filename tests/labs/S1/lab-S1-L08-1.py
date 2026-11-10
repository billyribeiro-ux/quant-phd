"""Lab S1-L08-1: Percentile bootstrap confidence interval for a mean.

Generates a seeded skewed sample and compares normal asymptotic and bootstrap percentile 95% intervals.
SIMULATED: sample and resamples generated with random.Random(801).
Standard library only. No external imports.
"""

from __future__ import annotations

import math
import random
import statistics


def main() -> None:
    seed = 801
    rng = random.Random(seed)
    n = 30

    # Draw n observations from a lognormal distribution exp(Normal(0, 0.6^2))
    sample = [math.exp(rng.gauss(0.0, 0.6)) for _ in range(n)]

    sample_mean = math.fsum(sample) / n
    sample_var = math.fsum((x - sample_mean) ** 2 for x in sample) / (n - 1)
    se_mean = math.sqrt(sample_var / n)

    # 1. Asymptotic normal 95% confidence interval
    z95 = statistics.NormalDist().inv_cdf(0.975)
    ci_norm_lo = sample_mean - z95 * se_mean
    ci_norm_hi = sample_mean + z95 * se_mean

    # 2. Percentile bootstrap interval with B = 2000 resamples
    b = 2000
    boot_means: list[float] = []
    for _ in range(b):
        # Sample with replacement
        resample = [sample[rng.randrange(n)] for _ in range(n)]
        boot_means.append(math.fsum(resample) / n)

    boot_means.sort()
    # 2.5% and 97.5% quantiles of the bootstrap distribution
    idx_lo = int(0.025 * b)
    idx_hi = int(0.975 * b)
    ci_boot_lo = boot_means[idx_lo]
    ci_boot_hi = boot_means[idx_hi]

    boot_se = math.sqrt(math.fsum((x - sample_mean) ** 2 for x in boot_means) / (b - 1))

    print(f"sample size n: {n}, bootstrap resamples B: {b}, seed: {seed}")
    print(f"sample mean: {sample_mean:.4f}, sample standard error: {se_mean:.4f}")
    print(f"bootstrap standard error: {boot_se:.4f}")
    print(f"asymptotic normal 95% CI: [{ci_norm_lo:.4f}, {ci_norm_hi:.4f}] (width: {ci_norm_hi - ci_norm_lo:.4f})")
    print(f"percentile bootstrap 95% CI: [{ci_boot_lo:.4f}, {ci_boot_hi:.4f}] (width: {ci_boot_hi - ci_boot_lo:.4f})")


main()

"""Lab S1-L06-1: The t-statistic and the likelihood-ratio test.

Computes the Student t-statistic on a seeded normal sample,
evaluates the likelihood-ratio statistic -2 ln Lambda on a sample,
and checks the asymptotic chi-square null rejection rate via simulation.
SIMULATED: normal sample uses random.Random(601); simulation uses random.Random(602).
"""

from __future__ import annotations

import math
import random


def main() -> None:
    # Part 1: One-sample t-statistic on seeded normal sample (SIMULATED)
    n = 25
    mu0 = 0.0
    seed1 = 601
    rng1 = random.Random(seed1)

    # Draws from Normal(0, 1)
    sample = [rng1.gauss(0.0, 1.0) for _ in range(n)]
    sample_mean = math.fsum(sample) / n
    sample_var = math.fsum((x - sample_mean) ** 2 for x in sample) / (n - 1)
    sample_sd = math.sqrt(sample_var)
    se_mean = sample_sd / math.sqrt(n)

    t_stat = (sample_mean - mu0) / se_mean

    print(f"t-statistic sample size n: {n}, null mean mu0: {mu0:.1f}")
    print(f"sample mean: {sample_mean:.6f}, sample standard deviation: {sample_sd:.6f}")
    print(f"standard error of the mean: {se_mean:.6f}")
    print(f"computed t-statistic: {t_stat:.6f}")

    # Part 2: Bernoulli likelihood-ratio test statistic: -2 ln Lambda
    # H0: p = p0 vs H1: p != p0
    n_lr = 50
    k_obs = 32  # 32 successes in 50 trials
    p0 = 0.50
    p_hat = k_obs / n_lr

    # -2 ln Lambda = 2 * [ ell(p_hat) - ell(p0) ]
    # = 2 * [ k * ln(p_hat / p0) + (n - k) * ln((1 - p_hat) / (1 - p0)) ]
    term1 = k_obs * math.log(p_hat / p0)
    term2 = (n_lr - k_obs) * math.log((1.0 - p_hat) / (1.0 - p0))
    lr_stat = 2.0 * (term1 + term2)
    crit_chi2 = 3.8414588  # 95th percentile of chi-square with 1 degree of freedom

    print(f"likelihood-ratio test: n = {n_lr}, observed k = {k_obs}, p_hat = {p_hat:.4f}")
    print(f"log-likelihood difference: {term1 + term2:.6f}")
    print(f"likelihood-ratio statistic -2 ln Lambda: {lr_stat:.6f}")
    print(f"chi-square(1) 95% critical value: {crit_chi2:.6f}")
    print(f"reject H0 at alpha = 0.05: {lr_stat >= crit_chi2}")

    # Part 3: Seeded simulation of LR statistic under H0 (SIMULATED)
    n_sims = 10_000
    seed2 = 602
    rng2 = random.Random(seed2)

    rejections = 0
    for _ in range(n_sims):
        k = sum(1 for _ in range(n_lr) if rng2.random() < p0)
        if k == 0 or k == n_lr:
            continue
        ph = k / n_lr
        stat = 2.0 * (k * math.log(ph / p0) + (n_lr - k) * math.log((1.0 - ph) / (1.0 - p0)))
        if stat >= crit_chi2:
            rejections += 1

    sim_size = rejections / n_sims
    print(f"simulated null rejection rate (N = {n_sims}, seed = {seed2}): {sim_size:.4f}")


main()

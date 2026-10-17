"""Per-learner instances for the S7 / Atlas A8 autograder.

make_instance(seed) is deterministic, produces only valid instances, and
changes the answers (not just labels) from seed to seed: the numbers of
hypotheses and trials, the sample lengths, the signal strengths, the
skewness of the selected strategy, the CSCV block count and the share of
true discoveries all vary with the seed. All data are SIMULATED.
"""

from __future__ import annotations

from statistics import NormalDist
from typing import Any

import numpy as np

_PHI = NormalDist()


def make_instance(seed: int) -> dict[str, Any]:
    rng = np.random.default_rng([7, 8, seed])

    # Multiple testing: m one-sided p-values, m1 of them from true effects.
    m = int(rng.integers(40, 121))
    m1 = int(rng.integers(5, m // 3))
    nulls = rng.random(m - m1)
    effects = rng.uniform(2.0, 4.5, m1) + rng.normal(0.0, 1.0, m1)
    alternatives = np.array([1.0 - _PHI.cdf(float(z)) for z in effects])
    pvalues = rng.permutation(np.concatenate([nulls, alternatives]))
    if rng.random() < 0.5:
        pvalues = np.round(pvalues, 3)  # rounded reports create ties
    q = float(rng.choice([0.01, 0.05, 0.10]))

    # The proposed strategy: daily excess returns with a skewed jump component.
    n_obs = int(rng.integers(500, 1501))
    daily_sr = float(rng.uniform(0.02, 0.12))
    sigma = float(rng.uniform(0.005, 0.02))
    jump_sign = float(rng.choice([-1.0, 1.0]))
    jumps = (rng.random(n_obs) < rng.uniform(0.01, 0.04)) * jump_sign * rng.exponential(3.0 * sigma, n_obs)
    returns = rng.normal(0.0, sigma, n_obs) + jumps
    returns = returns - returns.mean() + daily_sr * returns.std(ddof=1)  # sample Sharpe ratio is exactly daily_sr

    # Sharpe ratios of every trial the researcher ran before choosing it.
    n_trials = int(rng.integers(20, 201))
    trial_sharpes = rng.normal(0.0, 1.0 / np.sqrt(n_obs), n_trials) * rng.uniform(0.8, 1.6)

    # A backtest matrix for CSCV: n_strategies configurations, a few with genuine drift.
    n_blocks = int(rng.choice([6, 8, 10]))
    n_strategies = int(rng.integers(8, 31))
    periods = n_blocks * int(rng.integers(40, 81)) + int(rng.integers(0, n_blocks))
    performance = rng.normal(0.0, 0.01, (periods, n_strategies))
    planted = rng.choice(n_strategies, size=int(rng.integers(0, 4)), replace=False)
    performance[:, planted] += rng.uniform(0.0005, 0.003, planted.size)

    # Performance differentials against a benchmark, with a common factor and serial correlation.
    k = int(rng.integers(6, 16))
    t_len = int(rng.integers(300, 601))
    common = rng.normal(0.0, 1.0, t_len)
    shocks = rng.normal(0.0, 1.0, (t_len, k))
    for t in range(1, t_len):
        shocks[t] += 0.2 * shocks[t - 1]
    differentials = 0.5 * common[:, None] + shocks
    kinds = rng.choice(["strong", "negative", "null"], size=k, p=[0.3, 0.3, 0.4])
    kinds[0], kinds[1] = "strong", "negative"
    differentials += np.where(kinds == "strong", 0.45, np.where(kinds == "negative", -0.45, 0.0))

    return {
        "seed": seed,
        "pvalues": pvalues,
        "q": q,
        "returns": returns,
        "trial_sharpes": trial_sharpes,
        "n_trials": n_trials,
        "performance": performance,
        "n_blocks": n_blocks,
        "differentials": differentials,
        "kinds": kinds,
        "periods_per_year": 252,
    }

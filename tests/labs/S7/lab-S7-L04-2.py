from statistics import NormalDist

import numpy as np
from numpy.typing import NDArray

# SIMULATED universe: 50 strategies' daily performance differentials against a benchmark,
# sharing a common component. "null": no strategy beats the benchmark; "alpha": strategy 0 does.
rng = np.random.default_rng(2000)
n_obs, n_strategies, n_boot, mean_block = 1000, 50, 1000, 10.0


def stationary_counts(n: int, mean_block: float, draws: int) -> NDArray[np.float64]:
    """How often each period appears in each stationary-bootstrap resample (draws x n)."""
    starts = rng.integers(0, n, size=(draws, n))
    new_block = rng.random((draws, n)) < 1.0 / mean_block
    new_block[:, 0] = True
    pos = np.arange(n)
    block_start = np.maximum.accumulate(np.where(new_block, pos, 0), axis=1)
    rows = np.arange(draws)[:, None]
    idx = (starts[rows, block_start] + pos - block_start) % n
    counts = np.zeros((draws, n))
    np.add.at(counts, (np.repeat(np.arange(draws), n), idx.ravel()), 1.0)
    return counts


def normal_sf(z: float) -> float:
    return 1.0 - NormalDist().cdf(z)


counts = stationary_counts(n_obs, mean_block, n_boot)
common = rng.standard_normal((n_obs, 1))
noise = rng.standard_normal((n_obs, n_strategies))
base = np.sqrt(0.3) * common + np.sqrt(0.7) * noise  # unit variance, pairwise correlation 0.3

print("case  best  V  naive_p_of_best  reality_check_p")
for case in ("null", "alpha"):
    d = base.copy()
    if case == "alpha":
        d[:, 0] += 4.0 / np.sqrt(n_obs)  # true mean worth a t-statistic of about 4
    means = d.mean(axis=0)
    v = np.sqrt(n_obs) * means.max()  # White's statistic: max_k sqrt(T) * mean_k
    v_star = np.sqrt(n_obs) * ((counts @ d) / n_obs - means).max(axis=1)  # recentred at the sample means
    p_rc = float(np.mean(v_star >= v))
    k = int(np.argmax(means))
    t_best = np.sqrt(n_obs) * means[k] / d[:, k].std(ddof=1)
    print(f"{case} {k} {v:.3f} {normal_sf(float(t_best)):.4f} {p_rc:.3f}")

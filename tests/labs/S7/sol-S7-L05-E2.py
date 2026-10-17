import numpy as np
from numpy.typing import NDArray

# SIMULATED null AR(1) differentials, phi = 0.3: how often does a one-sided 5% bootstrap
# test of H0: mean <= 0 reject, as a function of the stationary bootstrap's mean block length?
rng = np.random.default_rng(52)
phi, n_obs, n_boot, n_reps, alpha = 0.3, 500, 299, 300, 0.05


def stationary_indices(n: int, mean_block: float, draws: int) -> NDArray[np.int64]:
    """draws x n stationary-bootstrap index vectors (Lesson 4, Definition 3.1)."""
    starts = rng.integers(0, n, size=(draws, n))
    new_block = rng.random((draws, n)) < 1.0 / mean_block
    new_block[:, 0] = True
    pos = np.arange(n)
    block_start = np.maximum.accumulate(np.where(new_block, pos, 0), axis=1)
    idx = (starts[np.arange(draws)[:, None], block_start] + pos - block_start) % n
    return np.asarray(idx, dtype=np.int64)


print("mean_block  rejection_rate")
for mean_block in (1.0, 5.0, 20.0):
    rejections = 0
    for _ in range(n_reps):
        e = rng.standard_normal(n_obs + 100)
        d = np.empty_like(e)
        d[0] = e[0]
        for t in range(1, e.size):
            d[t] = phi * d[t - 1] + e[t]
        d = d[100:]  # burn-in
        t_obs = d.mean() / (d.std(ddof=1) / np.sqrt(n_obs))
        sample = d[stationary_indices(n_obs, mean_block, n_boot)]
        t_star = (sample.mean(axis=1) - d.mean()) / (sample.std(axis=1, ddof=1) / np.sqrt(n_obs))
        critical = np.sort(t_star)[int(np.ceil((1 - alpha) * n_boot)) - 1]
        rejections += int(t_obs > critical)
    print(f"{mean_block:.0f} {rejections / n_reps:.3f}")

import numpy as np
from numpy.typing import NDArray

# SIMULATED universe: model 0 has a true edge (t-statistic about 3), nine models are null,
# and P "poor" models with strongly negative mean differentials (t near -7.9) are added to the search.
rng = np.random.default_rng(2005)
n_obs, n_boot, mean_block = 1000, 2000, 10.0


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


counts = stationary_counts(n_obs, mean_block, n_boot)  # the same resamples for every universe below
good_and_null = rng.standard_normal((n_obs, 10))
good_and_null[:, 0] += 3.0 / np.sqrt(n_obs)
poor_pool = rng.standard_normal((n_obs, 100)) - 0.25

recentred_nulls: list[tuple[int, float]] = []
base_v = 0.0
print("poor_models_added  reality_check_p  spa_style_p")
for n_poor in (0, 20, 100):
    d = np.hstack([good_and_null, poor_pool[:, :n_poor]])
    means = d.mean(axis=0)
    sd = d.std(axis=0, ddof=1)
    boot_means = (counts @ d) / n_obs

    # Reality Check: raw sqrt(T)-scaled means, every model recentred at the least favourable point.
    v = np.sqrt(n_obs) * means.max()
    p_rc = np.mean((np.sqrt(n_obs) * (boot_means - means)).max(axis=1) >= v)

    # SPA-style: studentized statistics; a model whose mean lies below -A_k keeps its own
    # (negative) mean in the bootstrap, so it cannot drive the maximum.
    threshold = sd * np.sqrt(2.0 * np.log(np.log(n_obs)) / n_obs)
    centre = np.where(means <= -threshold, means, 0.0)
    t_obs = max(float((np.sqrt(n_obs) * means / sd).max()), 0.0)
    t_star = np.maximum((np.sqrt(n_obs) * (boot_means - means + centre) / sd).max(axis=1), 0.0)
    p_spa = np.mean(t_star >= t_obs)
    print(f"{n_poor} {p_rc:.3f} {p_spa:.3f}")
    if n_poor == 0:  # null strategies the SPA-style rule recentres although their true mean is zero
        base_v = float(v)
        recentred_nulls = [(int(k), float(np.sqrt(n_obs) * means[k] / sd[k])) for k in np.flatnonzero(centre < 0.0)]
listed = ", ".join(f"strategy {k} (t = {t:.2f})" for k, t in recentred_nulls)
print(f"null strategies recentred in the base universe: {listed}")
print(f"Reality Check statistic V_K in the base universe: {base_v:.3f}")

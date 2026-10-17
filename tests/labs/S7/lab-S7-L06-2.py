from statistics import NormalDist

import numpy as np
from numpy.typing import NDArray

# SIMULATED null world: 60 assets with iid monthly returns and no predictability.
# A researcher searches 36 cross-sectional momentum specifications in each world:
# 3 universes x 4 lookbacks x 3 choices of how many recent months to skip.
rng = np.random.default_rng(606)
n_assets, n_months, n_worlds = 60, 240, 300
lookbacks, skips = (3, 6, 9, 12), (0, 1, 2)
universes = (slice(0, 30), slice(30, 60), slice(0, 60))
start = max(lookbacks) + max(skips)  # common first month, so every specification uses the same sample
phi = NormalDist()


def strategy(r: NDArray[np.float64], c: NDArray[np.float64], lookback: int, skip: int) -> NDArray[np.float64]:
    """Monthly returns of long-short momentum held one month: weights rank each asset's return over
    months t-lookback-skip .. t-1-skip against the cross-sectional mean, one dollar per side.
    c holds cumulative returns with a leading row of zeros, so c[t] sums months 0..t-1."""
    t = np.arange(start, r.shape[0])
    past = c[t - skip] - c[t - skip - lookback]
    w = past - past.mean(axis=1, keepdims=True)
    w = w / np.abs(w).sum(axis=1, keepdims=True) * 2.0
    return np.asarray(np.sum(w * r[start:], axis=1))


def two_sided_p(x: NDArray[np.float64]) -> float:
    """p-value of the mean monthly return (non-overlapping holdings, so the iid t-test applies)."""
    t = x.mean() / (x.std(ddof=1) / np.sqrt(x.size))
    return 2.0 * (1.0 - phi.cdf(abs(float(t))))


smallest = np.empty(n_worlds)
single = np.empty(n_worlds)
for world in range(n_worlds):
    r = rng.standard_normal((n_months, n_assets)) * 0.05
    c = np.vstack([np.zeros((1, n_assets)), np.cumsum(r, axis=0)])
    pvals = [two_sided_p(strategy(r[:, u], c[:, u], k, s)) for u in universes for k in lookbacks for s in skips]
    smallest[world] = min(pvals)
    single[world] = pvals[-2]  # the one pre-specified test: all assets, 12-month lookback, skip 1 month

share = float(np.mean(smallest < 0.05))
print(f"specifications searched: {len(universes) * len(lookbacks) * len(skips)}")
print(f"false-positive rate of one pre-specified test: {np.mean(single < 0.05):.3f}")
print(f"false-positive rate of the best of the search: {share:.3f}")
print(f"median smallest p-value: {np.median(smallest):.4f}")
print(f"effective number of independent tests: {np.log(1 - share) / np.log(0.95):.1f}")

import numpy as np
from numpy.typing import NDArray

# SIMULATED AR(1) series: x_t = phi * x_{t-1} + e_t with unit-variance shocks.
rng = np.random.default_rng(404)
phi, n_obs, n_series, n_boot = 0.5, 500, 40, 400


def ar1(count: int, n: int) -> NDArray[np.float64]:
    """count independent AR(1) paths of length n, one per row."""
    e = rng.standard_normal((count, n + 200))
    x = np.empty_like(e)
    x[:, 0] = e[:, 0]
    for t in range(1, e.shape[1]):
        x[:, t] = phi * x[:, t - 1] + e[:, t]
    return x[:, 200:]  # drop the burn-in so each path starts near stationarity


def stationary_indices(n: int, mean_block: float, draws: int) -> NDArray[np.intp]:
    """Stationary-bootstrap index matrix (draws x n): new block w.p. 1/mean_block, else step +1 mod n."""
    starts = rng.integers(0, n, size=(draws, n))
    new_block = rng.random((draws, n)) < 1.0 / mean_block
    new_block[:, 0] = True
    pos = np.arange(n)
    block_start = np.maximum.accumulate(np.where(new_block, pos, 0), axis=1)
    rows = np.arange(draws)[:, None]
    idx: NDArray[np.intp] = (starts[rows, block_start] + pos - block_start) % n
    return idx


def exact_bootstrap_sd(x: NDArray[np.float64], mean_block: float) -> float:
    """Theorem 3.3: Var*(mean) = (1/n)[c(0) + 2 sum_h (1 - h/n)(1 - p)^h c(h)], c = circular autocovariance."""
    n, p = x.size, 1.0 / mean_block
    dev = x - x.mean()
    c = np.array([np.mean(dev * np.roll(dev, -h)) for h in range(n)])
    h = np.arange(1, n)
    return float(np.sqrt((c[0] + 2.0 * np.sum((1 - h / n) * (1 - p) ** h * c[1:])) / n))


long_run_sd = 1.0 / (1.0 - phi) / np.sqrt(n_obs)  # sd of the sample mean implied by the long-run variance
monte_carlo_sd = np.std(ar1(4000, n_obs).mean(axis=1), ddof=1)
series = ar1(n_series, n_obs)

print("method  sd_of_sample_mean")
print(f"long-run_theory {long_run_sd:.4f}")
print(f"monte_carlo {monte_carlo_sd:.4f}")
iid = np.mean([np.std(s[rng.integers(0, n_obs, size=(n_boot, n_obs))].mean(axis=1), ddof=1) for s in series])
print(f"iid_bootstrap {iid:.4f}")
for block in (5.0, 20.0, 50.0):
    sb = np.mean([np.std(s[stationary_indices(n_obs, block, n_boot)].mean(axis=1), ddof=1) for s in series])
    print(f"stationary_bootstrap_block_{block:.0f} {sb:.4f}")

first = series[0]
draws = first[stationary_indices(n_obs, 20.0, 4000)].mean(axis=1)
print(f"one_series_block_20_formula {exact_bootstrap_sd(first, 20.0):.4f}")
print(f"one_series_block_20_resampled {np.std(draws, ddof=1):.4f}")

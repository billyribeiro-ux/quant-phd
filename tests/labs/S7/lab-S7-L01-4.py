import math

import numpy as np
from numpy.typing import NDArray

# SIMULATED daily returns, monitored every day for ten years. Each day's return is divided by a
# volatility known in advance, so the standardized return is N(SR, 1) with SR the daily Sharpe ratio.
alpha, kappa, horizon, batch = 0.05, 252.0, 2520, 500
z_crit = 1.959963984540054  # two-sided 5% critical value of the standard normal
days = np.arange(1, horizon + 1)
naive_line = z_crit * np.sqrt(days)  # the fixed-level z-test rejects on day t when |S_t| >= this line
boundary = np.sqrt((days + kappa) * (2 * math.log(1 / alpha) + np.log1p(days / kappa)))  # b_t, equation (5)


def first_rejection_days(
    rng: np.random.Generator, daily_sharpe: float, n_paths: int
) -> tuple[NDArray[np.int64], NDArray[np.int64]]:
    """Trading day of the first rejection by the naive daily z-test and by the monitor (horizon + 1: never)."""
    naive = np.empty(n_paths, dtype=np.int64)
    monitor = np.empty(n_paths, dtype=np.int64)
    for start in range(0, n_paths, batch):
        size = min(batch, n_paths - start)
        cum = np.abs(np.cumsum(rng.standard_normal((size, horizon)) + daily_sharpe, axis=1))  # |S_t|
        for out, line in ((naive, naive_line), (monitor, boundary)):
            crossed = cum >= line
            out[start : start + size] = np.where(crossed.any(axis=1), crossed.argmax(axis=1) + 1, horizon + 1)
    return naive, monitor


rng = np.random.default_rng(20261018)
naive, monitor = first_rejection_days(rng, 0.0, 10000)
print("skill-free strategies: share rejected at least once in the first n daily looks")
print("looks  naive_z_test  anytime_valid_monitor")
for looks in (1, 2, 5, 12, 36, 252, 756, 2520):
    print(f"{looks} {np.mean(naive <= looks):.3f} {np.mean(monitor <= looks):.4f}")

print("skilled strategies: monitor detection time against one pre-planned test")
print("annual_sharpe  median_years  share_by_3y  share_by_10y  half_power_years_one_test")
for annual_sharpe in (1.0, 2.0):
    daily_sharpe = annual_sharpe / math.sqrt(252)
    _, detect = first_rejection_days(rng, daily_sharpe, 2000)
    half_power_days = (z_crit / daily_sharpe) ** 2  # a z-test at day T has power 1/2 when SR * sqrt(T) = z_crit
    print(
        f"{annual_sharpe:.1f} {np.median(detect) / 252:.2f} {np.mean(detect <= 756):.3f} "
        f"{np.mean(detect <= horizon):.3f} {half_power_days / 252:.2f}"
    )

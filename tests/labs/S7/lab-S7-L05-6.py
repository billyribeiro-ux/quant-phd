import csv
import math
from pathlib import Path
from statistics import NormalDist

import numpy as np
from numpy.typing import NDArray

# Daily spot rates, USD per unit of foreign currency (Federal Reserve H.10 noon buying rates in New York).
with (Path("data") / "fx_daily.csv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.reader(handle))
currencies, days = rows[0][1:], [row[0] for row in rows[1:]]
prices = np.array([[float(v) for v in row[1:]] for row in rows[1:]])
print(f"fx_daily.csv: {len(days)} days from {days[0]} to {days[-1]}, {len(currencies)} currencies")

# The universe, fixed before running: on day t a rule is long (short) the currency when the previous day's rate
# lies above (below) its moving average over the previous n days. Benchmark: cash, so each differential is the
# rule's spot return; the interest differential and trading costs are not in the data.
windows = (10, 20, 50, 100, 200)
t = np.arange(max(windows), len(days))  # the first day on which every rule has a signal, to the last
spot = prices[t] / prices[t - 1] - 1.0
running = np.vstack([np.zeros((1, len(currencies))), np.cumsum(prices, axis=0)])
names, columns = [], []
for c, currency in enumerate(currencies):
    for n in windows:
        average = (running[t, c] - running[t - n, c]) / n  # mean rate over days t - n .. t - 1
        columns.append(np.sign(prices[t - 1, c] - average) * spot[:, c])
        names.append(f"{currency}-MA{n}")
d = np.column_stack(columns)
n_obs, n_rules = d.shape
corr = np.corrcoef(d, rowvar=False)[~np.eye(n_rules, dtype=bool)].mean()
print(f"{n_rules} rules over {n_obs} days from {days[t[0]]} to {days[-1]}, mean pairwise correlation {corr:.3f}")

means, se = d.mean(axis=0), d.std(axis=0, ddof=1) / math.sqrt(n_obs)
t_obs = means / se
print("t-statistics of the rules' mean spot returns (rows: currency; columns: moving-average days)")
print("currency " + " ".join(f"MA{n}" for n in windows))
for c, currency in enumerate(currencies):
    print(currency + " " + " ".join(f"{x:.3f}" for x in t_obs[c * len(windows) : (c + 1) * len(windows)]))

rng = np.random.default_rng(507)
n_boot, alpha, chunk = 1000, 0.05, 100
rank = math.ceil((1 - alpha) * n_boot)
cells = n_obs * np.arange(chunk)[:, None]  # offsets that place draw b's dates in row b of a (chunk, T) table


def stationary_indices(mean_block: float) -> NDArray[np.int64]:
    """`chunk` x T stationary-bootstrap index vectors (Lesson 4, Definition 3.1), one per draw."""
    starts = rng.integers(0, n_obs, size=(chunk, n_obs))
    new_block = rng.random((chunk, n_obs)) < 1.0 / mean_block
    new_block[:, 0] = True
    pos = np.arange(n_obs)
    block_start = np.maximum.accumulate(np.where(new_block, pos, 0), axis=1)
    return np.asarray((starts[np.arange(chunk)[:, None], block_start] + pos - block_start) % n_obs, dtype=np.int64)


def joint_bootstrap(mean_block: float) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Resampled means and s*/sqrt(T) of every rule, B x K, from whole dates shared by all rules."""
    boot_mean, boot_se = np.empty((n_boot, n_rules)), np.empty((n_boot, n_rules))
    for b in range(0, n_boot, chunk):
        dates = stationary_indices(mean_block)
        weight = np.bincount((dates + cells).ravel(), minlength=chunk * n_obs).reshape(chunk, n_obs) / n_obs
        boot_mean[b : b + chunk] = weight @ d
        boot_se[b : b + chunk] = np.sqrt((weight @ (d * d) - boot_mean[b : b + chunk] ** 2) / (n_obs - 1))
    return boot_mean, boot_se


def stepm(t_star: NDArray[np.float64]) -> tuple[NDArray[np.bool_], float, int]:
    """StepM (Definition 1.2): rejections, the first step's critical value, and the number of steps run."""
    rejected = np.zeros(n_rules, dtype=bool)
    critical: list[float] = []
    while not rejected.all():
        active = ~rejected
        critical.append(float(np.sort(t_star[:, active].max(axis=1))[rank - 1]))
        new = active & (t_obs > critical[-1])
        if not new.any():
            break
        rejected |= new
    return rejected, critical[0], len(critical)


def reality_check(boot_mean: NDArray[np.float64]) -> float:
    """White's Reality Check p-value (Lesson 4, Definition 4.1)."""
    v_star = math.sqrt(n_obs) * (boot_mean - means).max(axis=1)
    return float(np.mean(v_star >= math.sqrt(n_obs) * means.max()))


def spa_style(boot_mean: NDArray[np.float64]) -> tuple[float, int]:
    """SPA-style p-value (Lesson 4, Definition 6.1), with omega_k the bootstrap sd of sqrt(T) * mean*_k."""
    omega = math.sqrt(n_obs) * boot_mean.std(axis=0, ddof=1)
    centre = np.where(means <= -omega * math.sqrt(2.0 * math.log(math.log(n_obs)) / n_obs), means, 0.0)
    observed = max(float((math.sqrt(n_obs) * means / omega).max()), 0.0)
    v_star = np.maximum((math.sqrt(n_obs) * (boot_mean - means + centre) / omega).max(axis=1), 0.0)
    return float(np.mean(v_star >= observed)), int((centre < 0).sum())


boot_mean, boot_se = joint_bootstrap(10.0)
t_star = (boot_mean - means) / boot_se
rejected, c_first, steps = stepm(t_star)
c_band = float(np.sort(np.abs(t_star).max(axis=1))[rank - 1])
per_rule, holm_first = NormalDist().inv_cdf(1 - alpha), NormalDist().inv_cdf(1 - alpha / n_rules)
print(f"one-sided 5% critical values: per rule {per_rule:.3f} Holm's first step {holm_first:.3f}")
print(f"StepM first step {c_first:.3f} two-sided sup-t band {c_band:.3f}")
print(f"rejections: per rule {int((t_obs > per_rule).sum())} StepM {int(rejected.sum())} after {steps} step(s)")
p_spa, recentred = spa_style(boot_mean)
print(f"Reality Check p {reality_check(boot_mean):.3f} SPA-style p {p_spa:.3f} with {recentred} rules recentred")
low, high = (means - c_band * se) * 252 * 100, (means + c_band * se) * 252 * 100
best = int(np.argmax(t_obs))
print(f"95% sup-t band in percent per year: best rule {names[best]} mean {means[best] * 252 * 100:.2f}", end=" ")
print(f"from {low[best]:.2f} to {high[best]:.2f}")
print(f"band half-widths from {(high - low).min() / 2:.2f} to {(high - low).max() / 2:.2f} percent per year")
print(f"bands above zero {int((low > 0).sum())} below zero {int((high < 0).sum())}")
for mean_block in (5.0, 20.0):
    boot_mean, boot_se = joint_bootstrap(mean_block)
    rejected, c_first, _ = stepm((boot_mean - means) / boot_se)
    print(f"mean block {mean_block:.0f}: StepM first step {c_first:.3f} rejects {int(rejected.sum())}", end=" ")
    print(f"Reality Check p {reality_check(boot_mean):.3f}")

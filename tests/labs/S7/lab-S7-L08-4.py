import csv
import itertools
import math
from pathlib import Path
from statistics import NormalDist

import numpy as np
from numpy.typing import NDArray

# Month-end spot rates, USD per unit of foreign currency (Federal Reserve H.10 noon buying rates in New York).
with (Path("data") / "fx_monthly.csv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.reader(handle))
currencies, months = rows[0][1:], [row[0] for row in rows[1:]]
prices = np.array([[float(v) if v else math.nan for v in row[1:]] for row in rows[1:]])
start = int(np.argmax(~np.isnan(prices).any(axis=1)))  # the first month in which every currency has a rate
print(f"fx_monthly.csv: {len(months)} months from {months[0]} to {months[-1]}")
print(f"all {len(currencies)} currencies have a rate from {months[start]}")

months, log_p = months[start:], np.log(prices[start:])
spot = np.exp(np.diff(log_p, axis=0)) - 1.0  # spot[t - 1]: simple spot return over month t, long the currency
grid = list(itertools.product((1, 3, 6, 9, 12), (1, 3, 6, 12), (0, 1)))  # lookback, holding, skip, in months
first = max(h for _, h, _ in grid) + max(s for _, _, s in grid) + max(lb for lb, _, _ in grid)


def tsmom(lookback: int, hold: int, skip: int) -> NDArray[np.float64]:
    """Monthly spot return, months first..last, of time-series momentum: each currency is held long (short) when
    its lookback-month log change, ending `skip` months before formation, is positive (negative); positions formed
    at each of the last `hold` month-ends are averaged, and currencies are equally weighted."""
    t = np.arange(first, len(months))
    weight = np.zeros((t.size, len(currencies)))
    for h in range(1, hold + 1):
        end = t - h - skip  # the signal formed at the end of month t - h uses prices up to month t - h - skip
        weight += np.sign(log_p[end] - log_p[end - lookback])
    return np.asarray((weight / hold * spot[t - 1]).mean(axis=1))


def sharpe(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Per-column Sharpe ratio of per-period returns."""
    return np.asarray(x.mean(axis=0) / x.std(axis=0, ddof=1))


def pbo(m: NDArray[np.float64], n_blocks: int) -> float:
    """CSCV estimate of the probability of backtest overfitting (Sharpe ratio as the metric)."""
    m = m[m.shape[0] % n_blocks :]
    blocks = np.split(m, n_blocks)
    n = m.shape[1]
    logits = []
    for combo in itertools.combinations(range(n_blocks), n_blocks // 2):
        train = np.vstack([blocks[i] for i in combo])
        test = np.vstack([blocks[i] for i in range(n_blocks) if i not in combo])
        best = int(np.argmax(sharpe(train)))
        oos = sharpe(test)
        rank = 1 + np.sum(oos < oos[best]) + 0.5 * (np.sum(oos == oos[best]) - 1)
        omega = rank / (n + 1)
        logits.append(math.log(omega / (1 - omega)))
    return float(np.mean(np.array(logits) <= 0))


phi, gamma_e = NormalDist(), 0.5772156649015329


def expected_max_z(n: float) -> float:
    """The bracket of approximation (3) of Lesson 1: the expected maximum of n independent standard normals."""
    return (1 - gamma_e) * phi.inv_cdf(1 - 1 / n) + gamma_e * phi.inv_cdf(1 - 1 / (n * math.e))


def moments(r: NDArray[np.float64]) -> tuple[float, float, float]:
    """Sharpe ratio (ddof=1), skewness and kurtosis (moment estimators), per period."""
    c = r - r.mean()
    m2, m3, m4 = (float(np.mean(c**k)) for k in (2, 3, 4))
    return float(r.mean() / r.std(ddof=1)), m3 / m2**1.5, m4 / m2**2


def psr(r: NDArray[np.float64], benchmark: float) -> float:
    """Probabilistic Sharpe ratio of `r` against a per-period benchmark Sharpe ratio (Lesson 7)."""
    sr, g3, g4 = moments(r)
    return phi.cdf((sr - benchmark) / math.sqrt((1.0 - g3 * sr + (g4 - 1.0) / 4.0 * sr**2) / (r.size - 1)))


trials = np.column_stack([tsmom(*spec) for spec in grid])
n_obs, n_trials = trials.shape
srs = sharpe(trials)
pick = int(np.argmax(srs))
selected = trials[:, pick]
sr, g3, g4 = moments(selected)
yearly = math.sqrt(12)
print(f"evaluation window: {months[first]} to {months[-1]}, {n_obs} months, {n_trials} trials")
print(f"annualized trial Sharpe ratios: min {srs.min() * yearly:.3f} median {np.median(srs) * yearly:.3f}")
print(f"in-sample best: L{grid[pick][0]}-H{grid[pick][1]}-skip{grid[pick][2]}")
print(f"  monthly SR {sr:.4f} annualized {sr * yearly:.3f} skewness {g3:.3f} kurtosis {g4:.3f}")
print(f"  PSR against zero: {psr(selected, 0.0):.4f}")
spread = math.sqrt(float(np.var(srs, ddof=1)))
sr0 = spread * expected_max_z(n_trials)
print(f"raw N {n_trials} and cross-sectional sd {spread:.4f}", end=" ")
print(f"give SR0 {sr0:.4f} per month and DSR {psr(selected, sr0):.4f}")

corr = np.corrcoef(trials, rowvar=False)
rho = float(corr[~np.eye(n_trials, dtype=bool)].mean())
eigenvalues = np.linalg.eigvalsh(corr)
participation = float(eigenvalues.sum() ** 2 / (eigenvalues**2).sum())
target = math.sqrt(1 - rho) * expected_max_z(n_trials)
lo, hi = 1.0 + 1e-9, float(n_trials)
for _ in range(60):  # bisection (Lesson 7, Lab 3): the bracket at N_eff is sqrt(1 - rho) times the bracket at N
    mid = 0.5 * (lo + hi)
    lo, hi = (mid, hi) if expected_max_z(mid) < target else (lo, mid)
n_eff = 0.5 * (lo + hi)
print(f"mean pairwise correlation {rho:.3f} participation ratio {participation:.2f} matching N_eff {n_eff:.2f}")
print(f"cross-sectional sd expected of skill-free trials, sqrt((1 - rho) / T): {math.sqrt((1 - rho) / n_obs):.4f}")
sr0_eff = expected_max_z(n_eff) / math.sqrt(n_obs)
print(f"N_eff {n_eff:.2f} and variance 1/T give SR0 {sr0_eff:.4f} per month and DSR {psr(selected, sr0_eff):.4f}")
for n_blocks in (8, 10, 16):
    print(f"PBO with S = {n_blocks} ({math.comb(n_blocks, n_blocks // 2)} splits): {pbo(trials, n_blocks):.4f}")

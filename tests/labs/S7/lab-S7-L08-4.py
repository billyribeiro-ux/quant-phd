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


def sign_rule(lookback: int, hold: int, skip: int) -> NDArray[np.float64]:
    """Monthly spot return, months first..last, of one sign rule: each currency is held long (short) when its
    lookback-month log change, ending `skip` months before formation, is positive (negative); positions formed at
    each of the last `hold` month-ends are averaged, and currencies are equally weighted."""
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


trials = np.column_stack([sign_rule(*spec) for spec in grid])
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
pbo_by_blocks = {n_blocks: pbo(trials, n_blocks) for n_blocks in (8, 10)}  # S = 16 comes from pbo_fast() below


# This grid's own null. Theorem 4.1 assumes exchangeable trials and independent months, and neither holds here:
# the rules differ in lookback, holding and skip, and overlapping cohorts tie each month to the ones before it.
# So resample whole months of the ten currencies' log changes with replacement, which keeps their joint spread
# and tails but removes every dependence across months (no rule can have an edge), rebuild the price paths and
# all 40 rules, and recompute the PBO with S = 16 and the in-sample best's DSR. The functions below give the same
# numbers as sign_rule() and pbo() faster: signals are summed by cumulative sums, and each split's Sharpe ratios are
# built from per-block sums. pbo() would take 12,870 passes over the data for S = 16, so the 16-block PBO, observed
# and null, comes from pbo_fast(), checked against pbo() at S = 8 and 10 here and at S = 16 by the course's tests.
def grid_fast(path: NDArray[np.float64]) -> NDArray[np.float64]:
    """All 40 trials on a log-price path, in grid order, as sign_rule() builds them."""
    t = np.arange(first, len(path))
    moves = np.exp(np.diff(path, axis=0)) - 1.0
    totals = {}  # running sums of the signals, one per lookback (the grid has five)
    for lookback in sorted({lb for lb, _, _ in grid}):
        signal = np.zeros_like(path)
        signal[lookback:] = np.sign(path[lookback:] - path[:-lookback])  # signal[s] compares months s and s - L
        totals[lookback] = np.cumsum(signal, axis=0)
    out = np.empty((t.size, len(grid)))
    for k, (lookback, hold, skip) in enumerate(grid):
        total = totals[lookback]
        held = total[t - 1 - skip] - total[t - 1 - skip - hold]  # signals formed at months t - h - skip, h = 1..H
        out[:, k] = (held / hold * moves[t - 1]).mean(axis=1)
    return out


def halves(n_blocks: int) -> tuple[NDArray[np.float64], NDArray[np.intp], NDArray[np.intp], NDArray[np.intp]]:
    """CSCV splits in itertools order, for pbo_fast(). A half is half of the blocks from the first half of them and
    the rest from the second; it is described by those two subsets (rows `low` and `high` of `subsets`, which lists
    every subset of n_blocks / 2 blocks), and `mirror` gives the row of each split's complementary split."""
    half = n_blocks // 2
    combos = list(itertools.combinations(range(n_blocks), half))
    subsets = np.array([[(mask >> b) & 1 for b in range(half)] for mask in range(1 << half)], dtype=np.float64)
    low = np.array([sum(1 << b for b in combo if b < half) for combo in combos])
    high = np.array([sum(1 << (b - half) for b in combo if b >= half) for combo in combos])
    index = {combo: row for row, combo in enumerate(combos)}
    mirror = np.array([index[tuple(b for b in range(n_blocks) if b not in combo)] for combo in combos])
    return subsets, low, high, mirror


def pbo_fast(
    m: NDArray[np.float64],
    subsets: NDArray[np.float64],
    low: NDArray[np.intp],
    high: NDArray[np.intp],
    mirror: NDArray[np.intp],
) -> float:
    """pbo() from per-block sums. A half's sums are a subset sum of the first half of the blocks plus one of the
    second, so every half comes from two small matrix products; a split's out-of-sample half is its mirror's
    in-sample half (Proposition 3.2); ranks need only the order of the Sharpe ratios, which mean * |mean| /
    variance keeps; and a logit is at most zero exactly when rank <= (N + 1) / 2."""
    half = subsets.shape[1]
    n_blocks = 2 * half
    m = m[m.shape[0] % n_blocks :]
    size, n = m.shape[0] // n_blocks, m.shape[1]
    rows = size * half
    block_sum = m.reshape(n_blocks, size, n).sum(axis=1)
    block_sq = (m * m).reshape(n_blocks, size, n).sum(axis=1)
    mean = (subsets @ block_sum[:half])[low] + (subsets @ block_sum[half:])[high]
    mean /= rows
    spread = (subsets @ block_sq[:half])[low] + (subsets @ block_sq[half:])[high]
    spread -= rows * np.square(mean)  # the half's sum of squared deviations
    half_sharpe = mean * np.abs(mean)
    half_sharpe /= spread  # same order as the Sharpe ratio
    oos = half_sharpe[mirror]
    mine = oos[np.arange(len(low)), np.argmax(half_sharpe, axis=1)][:, None]
    rank = 1 + (oos < mine).sum(axis=1) + 0.5 * ((oos == mine).sum(axis=1) - 1)
    return float(np.mean(rank <= (n + 1) / 2))


sixteen = halves(16)
pbo_by_blocks[16] = pbo_fast(trials, *sixteen)
for n_blocks, value in pbo_by_blocks.items():
    print(f"PBO with S = {n_blocks} ({math.comb(n_blocks, n_blocks // 2)} splits): {value:.4f}")


observed_pbo, observed_dsr = pbo_by_blocks[16], psr(selected, sr0)
same = np.array_equal(grid_fast(log_p), trials) and all(
    pbo_fast(trials, *halves(b)) == pbo_by_blocks[b] for b in (8, 10)
)
print(f"fast builders reproduce the grid and its 8- and 10-block PBOs exactly: {same}")
rng = np.random.default_rng(4008)
changes, n_null = np.diff(log_p, axis=0), 100
null_pbo, null_dsr = np.empty(n_null), np.empty(n_null)
for b in range(n_null):
    draw = changes[rng.integers(0, len(changes), size=len(changes))]
    resampled = grid_fast(np.vstack([log_p[:1], log_p[0] + np.cumsum(draw, axis=0)]))
    null_srs = sharpe(resampled)
    hurdle = math.sqrt(float(np.var(null_srs, ddof=1))) * expected_max_z(n_trials)
    null_pbo[b] = pbo_fast(resampled, *sixteen)
    null_dsr[b] = psr(resampled[:, int(np.argmax(null_srs))], hurdle)
print(
    f"null from {n_null} grids on resampled months: PBO mean {null_pbo.mean():.3f} sd {null_pbo.std(ddof=1):.3f}",
    end=" ",
)
tail = float(np.mean(null_pbo >= observed_pbo))
print(f"share at or above {observed_pbo:.4f}: {tail:.3f}", end=" ")
print(f"(Monte Carlo standard error {math.sqrt(tail * (1 - tail) / n_null):.3f})")
print(f"  DSR of the in-sample best: median {np.median(null_dsr):.3f}", end=" ")
print(f"share at or above {observed_dsr:.4f}: {np.mean(null_dsr >= observed_dsr):.3f}")

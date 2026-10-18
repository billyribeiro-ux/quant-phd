import csv
import itertools
import math
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

# The memo's trial set: Lesson 8, Lab 4's grid, rebuilt from the same file with the same code.
# Month-end spot rates, USD per unit of foreign currency (Federal Reserve H.10 noon buying rates in New York).
with (Path("data") / "fx_monthly.csv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.reader(handle))
currencies, months = rows[0][1:], [row[0] for row in rows[1:]]
prices = np.array([[float(v) if v else math.nan for v in row[1:]] for row in rows[1:]])
start = int(np.argmax(~np.isnan(prices).any(axis=1)))  # the first month in which every currency has a rate
print(f"fx_monthly.csv: {len(months)} months from {months[0]} to {months[-1]}")

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


trials = np.column_stack([sign_rule(*spec) for spec in grid])  # (T, N): the TrialSet's returns, column n = grid[n]
n_obs, n_trials = trials.shape
labels = [f"L{lb}-H{h}-skip{s}" for lb, h, s in grid]
sharpe = trials.mean(axis=0) / trials.std(axis=0, ddof=1)
pick = int(np.argmax(sharpe))  # the TrialSet's `selected`: the highest full-sample Sharpe ratio
print(f"prices from {months[0]}; returns from {months[first]} to {months[-1]}")
print(f"trial matrix: {n_obs} months x {n_trials} trials, columns in grid order (lookback, holding, skip)")
print(f"checksums: sum {trials.sum():.10f} sum of squares {(trials**2).sum():.10f}")
print("annualized Sharpe ratio by lookback (rows) and holding period, skip 0 then skip 1 (columns)")
print("lookback " + " ".join(f"H{h}s{s}" for s in (0, 1) for h in (1, 3, 6, 12)))
for lookback in (1, 3, 6, 9, 12):
    cells = [sharpe[grid.index((lookback, h, s))] * math.sqrt(12) for s in (0, 1) for h in (1, 3, 6, 12)]
    print(f"L{lookback} " + " ".join(f"{x:.3f}" for x in cells))
print(f"selected: column {pick}, {labels[pick]}")

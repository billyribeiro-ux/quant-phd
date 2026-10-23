import csv
import math
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

# Nine one-month currency payoffs (DKK left out, Lesson 1), each costing one dollar: p = 1.
with (Path("data") / "fx_monthly.csv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.reader(handle))
currencies, months = rows[0][1:], [row[0] for row in rows[1:]]
prices = np.array([[float(v) if v else math.nan for v in row[1:]] for row in rows[1:]])
start = int(np.argmax(~np.isnan(prices).any(axis=1)))
keep = [i for i, c in enumerate(currencies) if c != "DKK"]
x = prices[start + 1 :, keep] / prices[start:-1, keep]
ends = months[start + 1 :]
p = np.ones(x.shape[1])
half = x.shape[0] // 2
train, test = x[:half], x[half:]
print(f"train {ends[0]} to {ends[half - 1]} ({half} months); test {ends[half]} to {ends[-1]} ({len(test)} months)")


def weights(sample: NDArray[np.float64], lam: float) -> NDArray[np.float64]:
    """Ridge x* weights: (E_T[x x'] + lam I)^{-1} p; lam = 0 is the sample x* (Proposition 4.2)."""
    return np.asarray(np.linalg.solve(sample.T @ sample / len(sample) + lam * np.eye(sample.shape[1]), p))


def rms_bp(sample: NDArray[np.float64], b: NDArray[np.float64]) -> float:
    """Root-mean-square pricing error E_T[m x] - p, in basis points of the one-dollar price."""
    return float(1e4 * np.sqrt(np.mean((sample.T @ (sample @ b) / len(sample) - p) ** 2)))


# Choose lam on the training sample only: fit on its first three quarters, validate on its last quarter.
fit, valid = train[: 3 * half // 4], train[3 * half // 4 :]
grid = [0.0, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
scores = [rms_bp(valid, weights(fit, lam)) for lam in grid]
chosen = grid[int(np.argmin(scores))]
print("lam      validation rms (bp)")
for lam, score in zip(grid, scores, strict=True):
    print(f"{lam:7.0e}  {score:8.1f}")
for label, lam in (("sample x*", 0.0), (f"ridge, lam = {chosen:.0e}", chosen)):
    b = weights(train, lam)
    m_test = test @ b
    print(
        f"{label}: train rms {rms_bp(train, b):.2f} bp, test rms {rms_bp(test, b):.1f} bp, "
        f"test s.d. of m {m_test.std():.4f}, test min of m {m_test.min():.4f}"
    )
# Benchmark: the constant SDF m = 1 prices each payoff at its test-sample mean.
print(f"constant m = 1: test rms {1e4 * np.sqrt(np.mean((test.mean(axis=0) - p) ** 2)):.1f} bp")

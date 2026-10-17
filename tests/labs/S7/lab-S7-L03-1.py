import math

import numpy as np
from numpy.typing import NDArray

# SIMULATED one-sided z-tests: nulls have mean 0, true effects have mean 3.
rng = np.random.default_rng(303)
m, q, effect = 200, 0.10, 3.0
upper_tail = np.frompyfunc(lambda z: 0.5 * math.erfc(z / math.sqrt(2.0)), 1, 1)


def bh_count(p: NDArray[np.float64], level: float) -> NDArray[np.int64]:
    """Number of BH rejections in each row of p (rows are replications)."""
    ordered = np.sort(p, axis=1)
    lines = level * np.arange(1, p.shape[1] + 1) / p.shape[1]
    passing = ordered <= lines
    last = p.shape[1] - np.argmax(passing[:, ::-1], axis=1)
    return np.where(passing.any(axis=1), last, 0)


print("m1  realized_FDR  bound_m0q/m  power  P(R=0)")
for m1, n_reps in ((0, 10000), (40, 2000)):
    mu = np.zeros(m)
    mu[:m1] = effect
    z = rng.standard_normal((n_reps, m)) + mu
    p = upper_tail(z).astype(float)
    r = bh_count(p, q)
    threshold = q * r / m
    rejected = p <= threshold[:, None]
    false = rejected[:, m1:].sum(axis=1)
    fdp = false / np.maximum(r, 1)
    power = rejected[:, :m1].sum(axis=1).mean() / m1 if m1 else 0.0
    print(f"{m1} {fdp.mean():.4f} {(m - m1) * q / m:.4f} {power:.4f} {np.mean(r == 0):.4f}")

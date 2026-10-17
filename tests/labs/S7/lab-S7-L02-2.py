from statistics import NormalDist

import numpy as np
from numpy.typing import NDArray

# Harvey, Liu and Zhu's hypothetical ten-test example (their Table 4, panel A, p. 18):
# the reported t-statistics and the reported two-sided p-values in percent.
t_stats = np.array([1.99, 2.63, 2.21, 3.43, 2.17, 2.64, 4.56, 5.34, 2.75, 2.49])
reported_p = np.array([4.66, 0.85, 2.71, 0.05, 3.00, 0.84, 0.00, 0.00, 0.60, 1.28]) / 100
alpha = 0.05
m = t_stats.size


def holm_adjusted(p: NDArray[np.float64]) -> NDArray[np.float64]:
    """Holm-adjusted p-values: running maximum of (m - j + 1) * p_(j), capped at 1."""
    order = np.argsort(p, kind="stable")
    scaled = (m - np.arange(m)) * p[order]
    adjusted = np.empty(m)
    adjusted[order] = np.minimum(np.maximum.accumulate(scaled), 1.0)
    return adjusted


phi = NormalDist()
recomputed_p = np.array([2 * (1 - phi.cdf(float(t))) for t in t_stats])
print("reported p (%):  ", " ".join(f"{100 * p:.2f}" for p in reported_p))
print("recomputed p (%):", " ".join(f"{100 * p:.2f}" for p in recomputed_p))
for label, p in (("reported", reported_p), ("recomputed", recomputed_p)):
    bonferroni = np.flatnonzero(p <= alpha / m) + 1
    holm = np.flatnonzero(holm_adjusted(p) <= alpha) + 1
    print(f"{label} p-values: Bonferroni rejects tests {bonferroni.tolist()}, Holm rejects tests {holm.tolist()}")
print("test 6: reported p = 0.84%, recomputed p = " + f"{100 * recomputed_p[5]:.4f}%")
print("Holm threshold at the fifth step = " + f"{100 * alpha / (m + 1 - 5):.4f}%")

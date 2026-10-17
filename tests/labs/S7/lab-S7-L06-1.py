from statistics import NormalDist

import numpy as np
from numpy.typing import NDArray

# SIMULATED literatures: M two-sided tests, 20% of them true effects with t ~ N(3, 1).
# A procedure's t-statistic hurdle is the critical value it applies at the step where it stops,
# converted to |t| with the normal approximation.
rng = np.random.default_rng(62)
phi = NormalDist()
alpha, q, reps = 0.05, 0.05, 40


def to_t(p: float) -> float:
    """|t| whose two-sided normal p-value equals p."""
    return phi.inv_cdf(1.0 - p / 2.0)


def hurdles(t: NDArray[np.float64]) -> tuple[float, float, float]:
    """Bonferroni and Holm hurdles at FWER alpha, and the BHY hurdle at FDR q, for one set of tests."""
    m = t.size
    p = np.sort([2.0 * (1.0 - phi.cdf(abs(float(x)))) for x in t])
    ranks = np.arange(1, m + 1)
    holm_fail = np.nonzero(p > alpha / (m - ranks + 1))[0]
    k = int(holm_fail[0]) + 1 if holm_fail.size else m  # Holm stops at its first failure
    c_m = float(np.sum(1.0 / ranks))
    bhy_pass = np.nonzero(p <= ranks * q / (m * c_m))[0]
    k_star = int(bhy_pass[-1]) + 1 if bhy_pass.size else 1  # BHY's cutoff sits at its last rejection
    return to_t(alpha / m), to_t(alpha / (m - k + 1)), to_t(k_star * q / (m * c_m))


print("M  bonferroni  holm  bhy")
for m in (10, 100, 316, 1000, 10000):
    rows = []
    for _ in range(reps):
        effect = rng.random(m) < 0.2
        t = rng.standard_normal(m) + np.where(effect, 3.0, 0.0)
        rows.append(hurdles(t))
    mean = np.mean(np.array(rows), axis=0)
    print(f"{m} {mean[0]:.2f} {mean[1]:.2f} {mean[2]:.2f}")

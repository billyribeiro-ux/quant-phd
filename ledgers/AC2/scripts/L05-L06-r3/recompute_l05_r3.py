"""Independent re-derivation of the L05 z-gap numbers (own code, written from the lab's spec in its docstring).

Model: z ~ N(0,1) iid per firm-month, sorted each month into quintiles of n//5 firms (lowest z = low leg).
gap = mean z over low leg minus mean z over high leg. Draw order mirrors the lab: z first, then eps.
"""

import math

import numpy as np
from scipy.stats import norm  # noqa: F401  (not used; kept out of the computation)


def phi(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


q = -0.8416212335729143  # Phi^{-1}(0.2), computed below without scipy
# Phi^{-1}(0.2) by bisection on erf
lo, hi = -5.0, 5.0
for _ in range(200):
    mid = (lo + hi) / 2
    if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < 0.2:
        lo = mid
    else:
        hi = mid
q = (lo + hi) / 2
analytic = -2 * phi(q) / 0.2
print(f"analytic_gap_exact {analytic:.5f} q {q:.6f} phi_q {phi(q):.6f}")


def gap_for(seed: int, n: int, months: int = 120) -> np.ndarray:
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((months, n))
    _eps = rng.standard_normal((months, n))  # drawn to keep the stream aligned with the lab; unused here
    k = n // 5
    s = np.sort(z, axis=1)
    return s[:, :k].mean(axis=1) - s[:, -k:].mean(axis=1)


def summary(n: int, seeds: range) -> tuple[float, float, float]:
    per_seed = np.array([gap_for(sd, n).mean() for sd in seeds])
    return float(per_seed.mean()), float(per_seed.std(ddof=1) / math.sqrt(len(per_seed))), float(per_seed.std(ddof=1))


for n, seeds in [(500, range(20)), (5000, range(20)), (500, range(200)), (5000, range(200))]:
    m, se, sd = summary(n, seeds)
    print(f"n {n} seeds {len(seeds)} mean_gap {m:.4f} se_over_seeds {se:.4f} sd_per_seed {sd:.4f} minus_analytic {m - analytic:.4f}")

# Does the 20-seed mean at 500 differ from the 200-seed mean at 500 by more than its sampling error?
m20, se20, _ = summary(500, range(20))
m200, se200, _ = summary(500, range(200))
print(f"diff_20_minus_200 at 500: {m20 - m200:.4f}  se20 {se20:.4f}")

# Finite-sort bias check at 500 and 5000 with many more seeds (the mean of realised gaps)
for n in (50, 100, 500, 5000):
    m, se, _ = summary(n, range(400))
    print(f"n {n} seeds 400 mean_gap {m:.4f} se {se:.4f} minus_analytic {m - analytic:.4f}")

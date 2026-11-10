"""PM1 project lab 2 (rung 2, completion): benchmarking completion problem.

SIMULATED: a private equity fund cash flow schedule to evaluate with KS-PME, Direct Alpha,
and Long-Nickels index replication.
Standard library, NumPy, and SciPy only; fully deterministic.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


def main() -> None:
    times = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    calls = np.array([50.0, 30.0, 20.0, 0.0, 0.0, 0.0])
    distributions = np.array([0.0, 0.0, 10.0, 30.0, 50.0, 60.0])
    nav = 0.0
    benchmark_prices = np.array([100.0, 108.0, 116.64, 125.97, 136.05, 146.93])

    # 1. Kaplan & Schoar (2005) KS-PME
    disc_calls = float(np.sum(calls / benchmark_prices))
    disc_dist = float(np.sum(distributions / benchmark_prices) + (nav / benchmark_prices[-1]))
    ks_pme = disc_dist / disc_calls
    print(f"KS-PME: {ks_pme:.4f}")

    # 2. Direct Alpha
    flows = (distributions - calls) / benchmark_prices

    def npv_alpha(alpha: float) -> float:
        return float(np.sum(flows * np.exp(-alpha * times)) + (nav / benchmark_prices[-1]) * np.exp(-alpha * times[-1]))

    direct_alpha = float(brentq(npv_alpha, -0.5, 0.5, xtol=1e-8))
    print(f"Direct Alpha: {direct_alpha * 100:.2f}%")

    # 3. Long & Nickels (1996) Index Replication
    n = len(times)
    v = np.zeros(n)
    v[0] = calls[0] - distributions[0]
    for i in range(1, n):
        v[i] = v[i - 1] * (benchmark_prices[i] / benchmark_prices[i - 1]) + calls[i] - distributions[i]

    went_short = bool(np.any(v < -1e-6))
    print(f"LN Terminal NAV: {v[-1]:.2f}")
    print(f"LN Went Short: {went_short}")


main()

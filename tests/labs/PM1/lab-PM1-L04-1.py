"""Lab 1 for PM1 L04: Long-Nickels PME, Direct Alpha, and the Taylor Duration Approximation.

SIMULATED: a private equity fund evaluated under Long-Nickels PME and Direct Alpha.
Tests:
1. Exact continuous Direct Alpha via Brent root-finding.
2. The first-order Taylor approximation: alpha_approx = ln(KS-PME) / duration.
3. Long-Nickels synthetic NAV tracking and identification of the short-index threshold.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq


def main() -> None:
    times = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    calls = np.array([40.0, 30.0, 20.0, 0.0, 0.0, 0.0])
    distributions = np.array([0.0, 0.0, 10.0, 25.0, 40.0, 50.0])
    nav = 5.0
    # Public market index: 8% steady geometric growth
    prices = 100.0 * (1.08) ** times

    # 1. KS-PME
    disc_calls = float(np.sum(calls / prices))
    disc_dist = float(np.sum(distributions / prices) + (nav / prices[-1]))
    ks_pme = disc_dist / disc_calls

    # 2. Exact Direct Alpha
    flows = (distributions - calls) / prices

    def npv_alpha(alpha: float) -> float:
        return float(np.sum(flows * np.exp(-alpha * times)) + (nav / prices[-1]) * np.exp(-alpha * times[-1]))

    alpha_exact = float(brentq(npv_alpha, -0.5, 0.5, xtol=1e-8))

    # 3. Taylor Duration Approximation: alpha ~ ln(KS-PME) / duration
    # Capital-weighted call duration and distribution duration
    call_duration = float(np.sum(times * (calls / prices)) / disc_calls)
    dist_duration = float(np.sum(times * (distributions / prices)) + times[-1] * (nav / prices[-1])) / disc_dist
    fund_duration = dist_duration - call_duration
    alpha_approx = math.log(ks_pme) / fund_duration

    # 4. Long-Nickels Synthetic NAV Tracking
    n = len(times)
    v = np.zeros(n)
    v[0] = calls[0] - distributions[0]
    for i in range(1, n):
        v[i] = v[i - 1] * (prices[i] / prices[i - 1]) + calls[i] - distributions[i]
    went_short = bool(np.any(v < -1e-6))

    print(f"Kaplan-Schoar PME: {ks_pme:.4f}")
    print(f"Exact Direct Alpha (continuous): {alpha_exact * 100:.2f}%")
    print(f"Fund Cash Flow Duration: {fund_duration:.2f} years")
    print(f"Taylor Approx Direct Alpha: {alpha_approx * 100:.2f}%")
    print(f"Approximation Error: {abs(alpha_exact - alpha_approx) * 10000:.1f} bps")
    print(f"Long-Nickels Terminal NAV: ${v[-1]:.2f}M, Went Short: {went_short}")


main()

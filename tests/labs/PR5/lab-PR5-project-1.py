"""Lab PR5-project-1: Project Rung 1 Worked Example Twin.

SIMULATED: Analytical checks for expected MDD, Grossman-Zhou cushion, and pod drawdown tracking.
"""

from __future__ import annotations

import math

import numpy as np


def main() -> None:
    print("Project Rung 1 · Worked Example: Drawdown Analytics & Cushion Policy")
    print("=" * 68)

    # 1. Magdon-Ismail zero-drift expected MDD
    sigma = 0.20
    t_years = 1.0
    theo_mdd = sigma * math.sqrt(math.pi * t_years / 2.0)
    print(f"1. Magdon-Ismail Zero-Drift MDD: sigma={sigma:.2f}, T={t_years:.1f} yr")
    print(f"   Theoretical E[MDD(T)] = sigma * sqrt(pi*T/2) = {theo_mdd:.4f} (25.07%)")

    # 2. Grossman-Zhou cushion allocation
    wealth = 100.0
    peak = 110.0
    alpha = 0.85
    m_multiplier = 2.5
    floor = alpha * peak
    cushion = max(0.0, wealth - floor)
    dollar_alloc = m_multiplier * cushion
    print("\n2. Grossman-Zhou Floor Protection:")
    print(f"   Wealth W = {wealth:.1f}, Peak M = {peak:.1f}, Floor alpha = {alpha:.2f}")
    print(f"   Floor F = alpha * M = {floor:.2f}")
    print(f"   Cushion C = max(0, W - F) = {cushion:.2f}")
    print(f"   Risky Dollar Allocation = m* * C = {dollar_alloc:.2f}")

    # 3. Pod drawdown tracking
    w_series = [100.0, 108.0, 102.0, 96.0, 105.0]
    peaks = [float(p) for p in np.maximum.accumulate(w_series)]
    dds = [float((p - w) / p) for p, w in zip(peaks, w_series, strict=False)]
    mdd = max(dds)
    print("\n3. Discrete Wealth Path Drawdown Tracking:")
    print(f"   Wealth path:  {w_series}")
    print(f"   Peak path:    {peaks}")
    print(f"   Drawdown:     {[round(d, 4) for d in dds]}")
    print(f"   Maximum DD:   {mdd:.4f} (11.11%)")


main()

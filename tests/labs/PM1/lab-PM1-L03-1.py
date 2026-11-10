"""Lab 1 for PM1 L03: The Public Market Equivalent (KS-PME) and IRR Distortions.

SIMULATED: compares two private equity funds across bull and bear public market regimes.
Demonstrates why Internal Rate of Return (IRR) can mislead limited partners:
- Fund A: Operates in a raging bull market (index surges). Generates 25% IRR, but KS-PME < 1.0.
- Fund B: Operates in a bear market (index crashes 30%). Generates 10% IRR, but KS-PME = 2.09.
Computes exact MOIC, IRR, and Kaplan-Schoar PME.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


def main() -> None:
    times = np.array([0.0, 1.0, 2.0, 3.0, 4.0])

    # Fund A: Invests $100M at t=0, exits at t=4 for $244.14M (IRR = 25.0%)
    # Public market index surges: 100 -> 130 -> 170 -> 220 -> 280 (180% gain, ~29.4% annualized)
    calls_a = np.array([100.0, 0.0, 0.0, 0.0, 0.0])
    dist_a = np.array([0.0, 0.0, 0.0, 0.0, 244.14])
    prices_bull = np.array([100.0, 130.0, 170.0, 220.0, 280.0])

    # Fund B: Invests $100M at t=0, exits at t=4 for $146.41M (IRR = 10.0%)
    # Public market index collapses: 100 -> 90 -> 80 -> 75 -> 70 (-30% loss)
    calls_b = np.array([100.0, 0.0, 0.0, 0.0, 0.0])
    dist_b = np.array([0.0, 0.0, 0.0, 0.0, 146.41])
    prices_bear = np.array([100.0, 90.0, 80.0, 75.0, 70.0])

    # 1. Evaluate Fund A
    def npv_a(r: float) -> float:
        return float(np.sum((dist_a - calls_a) * (1.0 + r) ** (-times)))

    irr_a = float(brentq(npv_a, -0.5, 2.0))
    pme_a = float(np.sum(dist_a / prices_bull)) / float(np.sum(calls_a / prices_bull))

    # 2. Evaluate Fund B
    def npv_b(r: float) -> float:
        return float(np.sum((dist_b - calls_b) * (1.0 + r) ** (-times)))

    irr_b = float(brentq(npv_b, -0.5, 2.0))
    pme_b = float(np.sum(dist_b / prices_bear)) / float(np.sum(calls_b / prices_bear))

    print("--- Fund A (Bull Market Regime) ---")
    print(f"Annualized IRR: {irr_a * 100:.2f}%")
    print(f"Kaplan-Schoar PME: {pme_a:.4f} (Result: {'Outperformed' if pme_a >= 1.0 else 'Underperformed'})")

    print("\n--- Fund B (Bear Market Regime) ---")
    print(f"Annualized IRR: {irr_b * 100:.2f}%")
    print(f"Kaplan-Schoar PME: {pme_b:.4f} (Result: {'Outperformed' if pme_b >= 1.0 else 'Underperformed'})")


main()

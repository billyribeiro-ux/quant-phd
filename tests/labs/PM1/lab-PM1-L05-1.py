"""Lab 1 for PM1 L05: IRR Manipulation with a Subscription Line of Credit.

Curriculum lab: "IRR manipulation with a subscription line."
SIMULATED: a private equity fund evaluating 3 capital funding structures on an identical $100M acquisition:
- Scenario 1 (No Facility): LP funds $100M at t=0.0; exited at t=5.0 for $200.0M (2.0x MOIC).
- Scenario 2 (1-Year Line): Subscription line funds $100M at t=0.0 at 5.0% interest. LP funds $105.0M at t=1.0.
- Scenario 3 (2-Year Line): Subscription line funds $100M at t=0.0 at 5.0% compounded. LP funds $110.25M at t=2.0.
Calculates annualized LP IRR, MOIC/TVPI, KS-PME, and Direct Alpha against an 8% public benchmark.
Demonstrates holding period compression: IRR increases while TVPI decreases.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


def evaluate_scenario(
    times: np.ndarray, calls: np.ndarray, dist: np.ndarray, prices: np.ndarray
) -> tuple[float, float, float, float]:
    # 1. MOIC
    tvpi = float(np.sum(dist)) / float(np.sum(calls))

    # 2. IRR
    def npv_irr(r: float) -> float:
        return float(np.sum((dist - calls) * (1.0 + r) ** (-times)))

    irr = float(brentq(npv_irr, -0.5, 2.0))

    # 3. KS-PME
    disc_c = float(np.sum(calls / prices))
    disc_d = float(np.sum(dist / prices))
    ks_pme = disc_d / disc_c

    # 4. Direct Alpha
    def npv_a(a: float) -> float:
        flows = (dist - calls) / prices
        return float(np.sum(flows * np.exp(-a * times)))

    da = float(brentq(npv_a, -0.5, 0.5))

    return irr, tvpi, ks_pme, da


def main() -> None:
    # 5-year evaluation horizon (annual points)
    times = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    prices = 100.0 * (1.08) ** times  # 8% annual market growth

    # All scenarios exit at t=5 for $200.0M
    dist = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 200.0])

    # Scenario 1: Standard capital call at t=0
    calls_1 = np.array([100.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    irr_1, tvpi_1, pme_1, da_1 = evaluate_scenario(times, calls_1, dist, prices)

    # Scenario 2: 1-year subscription facility (LP funds $105M at t=1)
    calls_2 = np.array([0.0, 105.0, 0.0, 0.0, 0.0, 0.0])
    irr_2, tvpi_2, pme_2, da_2 = evaluate_scenario(times, calls_2, dist, prices)

    # Scenario 3: 2-year subscription facility (LP funds $110.25M at t=2)
    calls_3 = np.array([0.0, 0.0, 110.25, 0.0, 0.0, 0.0])
    irr_3, tvpi_3, pme_3, da_3 = evaluate_scenario(times, calls_3, dist, prices)

    print("--- Scenario 1: Direct LP Capital Call (No Facility) ---")
    print(f"Annualized LP IRR: {irr_1 * 100:.2f}%")
    print(f"TVPI / MOIC: {tvpi_1:.4f}x")
    print(f"Kaplan-Schoar PME: {pme_1:.4f}")
    print(f"Direct Alpha: {da_1 * 100:.2f}%")

    print("\n--- Scenario 2: 1-Year Subscription Line (5% Borrowing Rate) ---")
    print(f"Annualized LP IRR: {irr_2 * 100:.2f}% (Spread: +{(irr_2 - irr_1) * 10000:.0f} bps)")
    print(f"TVPI / MOIC: {tvpi_2:.4f}x (Erosion: -{(tvpi_1 - tvpi_2):.4f}x)")
    print(f"Kaplan-Schoar PME: {pme_2:.4f}")
    print(f"Direct Alpha: {da_2 * 100:.2f}%")

    print("\n--- Scenario 3: 2-Year Subscription Line (5% Borrowing Rate) ---")
    print(f"Annualized LP IRR: {irr_3 * 100:.2f}% (Spread: +{(irr_3 - irr_1) * 10000:.0f} bps)")
    print(f"TVPI / MOIC: {tvpi_3:.4f}x (Erosion: -{(tvpi_1 - tvpi_3):.4f}x)")
    print(f"Kaplan-Schoar PME: {pme_3:.4f}")
    print(f"Direct Alpha: {da_3 * 100:.2f}%")


main()

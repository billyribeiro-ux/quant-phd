"""PM1 project lab 1 (rung 1, worked example): private equity benchmarking engine.

SIMULATED: a representative 10-year private equity fund with semi-annual cash flows.
Computes MOIC (DPI, RVPI, TVPI), IRR, Kaplan-Schoar PME, Direct Alpha, and Long-Nickels PME.
Standard library, NumPy, and SciPy only; fully deterministic.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


def main() -> None:
    # 1. Cash flow schedule over 5 years (semi-annual dates)
    times = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    calls = np.array([30.0, 25.0, 20.0, 15.0, 10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    distributions = np.array([0.0, 0.0, 0.0, 0.0, 5.0, 15.0, 25.0, 35.0, 40.0, 30.0, 20.0])
    nav = 10.0  # Remaining unrealized NAV at horizon T=5.0

    # Public benchmark index prices (annualized ~8% geometric drift)
    benchmark_prices = np.array([100.0, 103.92, 108.00, 112.24, 116.64, 121.22, 125.97, 130.91, 136.05, 141.38, 146.93])

    # 2. MOIC Decomposition
    total_calls = float(np.sum(calls))
    total_dist = float(np.sum(distributions))
    dpi = total_dist / total_calls
    rvpi = nav / total_calls
    tvpi = dpi + rvpi
    print(f"Step 1: MOIC metrics -> DPI={dpi:.4f}, RVPI={rvpi:.4f}, TVPI={tvpi:.4f}")

    # 3. Net Cash Flows and IRR
    net_cf = distributions - calls
    net_cf[-1] += nav

    def npv(r: float) -> float:
        return float(np.sum(net_cf * (1.0 + r) ** (-times)))

    irr = float(brentq(npv, -0.5, 2.0, xtol=1e-8))
    print(f"Step 2: Annualized IRR -> {irr * 100:.2f}%")

    # 4. Kaplan & Schoar (2005) KS-PME
    disc_calls = float(np.sum(calls / benchmark_prices))
    disc_dist = float(np.sum(distributions / benchmark_prices) + (nav / benchmark_prices[-1]))
    ks_pme = disc_dist / disc_calls
    print(f"Step 3: Kaplan-Schoar PME -> {ks_pme:.4f}")

    # 5. Direct Alpha (Gredil, Griffiths & Stucke 2014)
    def npv_alpha(alpha: float) -> float:
        flows = (distributions - calls) / benchmark_prices
        return float(np.sum(flows * np.exp(-alpha * times)) + (nav / benchmark_prices[-1]) * np.exp(-alpha * times[-1]))

    direct_alpha = float(brentq(npv_alpha, -0.5, 0.5, xtol=1e-8))
    print(f"Step 4: Direct Alpha (continuous annualized) -> {direct_alpha * 100:.2f}%")

    # 6. Long & Nickels (1996) Index Replication
    n = len(times)
    v = np.zeros(n)
    v[0] = calls[0] - distributions[0]
    for i in range(1, n):
        v[i] = v[i - 1] * (benchmark_prices[i] / benchmark_prices[i - 1]) + calls[i] - distributions[i]

    went_short = bool(np.any(v < -1e-6))
    print(f"Step 5: Long-Nickels Terminal NAV -> {v[-1]:.2f}, Went Short -> {went_short}")

    if not went_short and v[-1] >= 0:
        ln_cf = distributions - calls
        ln_cf[-1] += v[-1]

        def npv_ln(r: float) -> float:
            return float(np.sum(ln_cf * (1.0 + r) ** (-times)))

        ln_irr = float(brentq(npv_ln, -0.5, 2.0, xtol=1e-8))
        print(f"Step 6: Long-Nickels Benchmark IRR -> {ln_irr * 100:.2f}%")
        print(f"Step 7: Excess IRR Spread (PE IRR - LN IRR) -> {(irr - ln_irr) * 100:.2f}%")


main()

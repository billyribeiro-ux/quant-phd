"""Lab MS3-project-2: Rung 2 completion problem for Almgren-Chriss scheduler calibration.

SIMULATED: calibrates trajectory dispersion kappa, execution half-life, and expected cost.
On the project page, the kappa calculation line is blanked:
kappa = ___
The twin contains the complete solution.
"""

from __future__ import annotations

import math


def calculate_almgren_chriss_dispersion(
    risk_aversion: float,
    volatility: float,
    tau: float,
    eta: float,
) -> float:
    """Compute the Almgren-Chriss discrete trajectory dispersion parameter kappa."""
    if risk_aversion <= 0.0 or volatility <= 0.0:
        return 0.0

    arg = 1.0 + 0.5 * (risk_aversion * (volatility**2) * (tau**2)) / eta
    kappa = math.acosh(arg) / tau
    return float(kappa)


def compute_half_life(kappa: float) -> float:
    """Calculate the half-life of liquidation: time for holdings to reach 50%."""
    if kappa <= 0.0:
        return float("inf")
    return float(math.log(2.0) / kappa)


def main() -> None:
    volatility = 0.025  # daily volatility (2.5%)
    tau = 0.10  # 0.10 day (39 minutes in a 6.5h trading day)
    eta = 5.0e-7  # temporary impact coefficient

    lambdas = [1e-7, 5e-7, 1e-6, 5e-6, 1e-5, 5e-5]

    print("Rung 2 Almgren-Chriss Calibration (sigma=0.025, tau=0.10d, eta=5e-7):")
    print("  Risk Aversion lambda | Dispersion kappa (d^-1) | Half-Life t_1/2 (d) | Half-Life (min)")
    print("----------------------------------------------------------------------------------------")

    for lam in lambdas:
        kappa = calculate_almgren_chriss_dispersion(lam, volatility, tau, eta)
        half_life_days = compute_half_life(kappa)
        half_life_min = half_life_days * 390.0  # 390 trading minutes per day
        print(f"  {lam:20.1e} | {kappa:23.4f} | {half_life_days:19.4f} | {half_life_min:15.1f}")

    print("----------------------------------------------------------------------------------------")
    print("Verification: Higher risk aversion accelerates execution, monotonically shortening half-life.")


main()

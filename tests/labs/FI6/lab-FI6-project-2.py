"""Lab FI6-project-2: Project Rung 2 Completion Problem Twin.

SIMULATED: Solution twin for SABR implied volatility evaluation,
Breeden-Litzenberger risk-neutral density extraction, and butterfly arbitrage checking.
"""

from __future__ import annotations

import math

from scipy.stats import norm


def compute_sabr_density_and_arbitrage(
    fwd: float,
    texp: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
    test_strikes: list[float],
) -> tuple[list[float], list[float], bool]:
    """Calculate SABR Black volatilities, Breeden-Litzenberger densities, and verify absence of arbitrage."""
    vols: list[float] = []
    densities: list[float] = []
    is_arbitrage_free = True
    dk = 1e-4

    def single_vol(k: float) -> float:
        if abs(fwd - k) < 1e-8:
            t1 = alpha / (fwd ** (1.0 - beta))
            g1 = (1.0 - beta) ** 2 / 24.0 * (alpha**2 / (fwd ** (2.0 - 2.0 * beta)))
            g2 = rho * beta * nu * alpha / (4.0 * (fwd ** (1.0 - beta)))
            g3 = (2.0 - 3.0 * rho**2) / 24.0 * (nu**2)
            return float(t1 * (1.0 + (g1 + g2 + g3) * texp))

        log_fk = math.log(fwd / k)
        denom_base = (fwd * k) ** ((1.0 - beta) / 2.0)
        denom_exp = 1.0 + ((1.0 - beta) ** 2 / 24.0) * (log_fk**2) + ((1.0 - beta) ** 4 / 1920.0) * (log_fk**4)
        denom = denom_base * denom_exp

        # Hagan z variable
        z = (nu / alpha) * denom_base * log_fk
        if abs(z) < 1e-6:
            z_over_xz = 1.0 - 0.5 * rho * z + (1.0 / 12.0) * (2.0 - 3.0 * rho**2) * (z**2)
        else:
            rad = max(1.0 - 2.0 * rho * z + z**2, 0.0)
            xz = math.log((math.sqrt(rad) + z - rho) / (1.0 - rho))
            z_over_xz = z / xz

        t_term = (
            ((1.0 - beta) ** 2 / 24.0) * (alpha**2 / ((fwd * k) ** (1.0 - beta)))
            + (rho * beta * nu * alpha) / (4.0 * denom_base)
            + ((2.0 - 3.0 * rho**2) / 24.0) * (nu**2)
        )
        return float((alpha / denom) * z_over_xz * (1.0 + t_term * texp))

    def black_price(k: float, v: float) -> float:
        std = v * math.sqrt(texp)
        d1 = (math.log(fwd / k) + 0.5 * std**2) / std
        d2 = d1 - std
        return float(fwd * norm.cdf(d1) - k * norm.cdf(d2))

    for k in test_strikes:
        vol = single_vol(k)
        vols.append(vol)

        c_mid = black_price(k, vol)
        c_up = black_price(k + dk, single_vol(k + dk))
        c_dn = black_price(k - dk, single_vol(k - dk))

        density = (c_up - 2.0 * c_mid + c_dn) / (dk**2)
        densities.append(density)

        if density < 0.0:
            is_arbitrage_free = False

    return vols, densities, is_arbitrage_free


def run_lab() -> None:
    print("=== Rung 2: SABR Volatility & Breeden-Litzenberger Density Solution ===")

    fwd = 0.0400
    texp = 2.0
    alpha = 0.038
    beta = 0.5
    rho = -0.15
    nu = 0.45
    strikes = [0.025, 0.030, 0.035, 0.040, 0.045, 0.050, 0.055]

    vols, densities, arb_free = compute_sabr_density_and_arbitrage(fwd, texp, alpha, beta, rho, nu, strikes)

    print(f"{'Strike':<10} {'SABR Vol':<12} {'Density q(K)':<14} {'Non-Negative':<12}")
    for k, v, q in zip(strikes, vols, densities, strict=False):
        print(f"{k * 100.0:<9.2f}% {v * 100.0:<11.2f}% {q:<13.4f} {'PASS' if q >= 0.0 else 'FAIL'}")

    print()
    print(f"Surface Arbitrage-Free   : {arb_free}")
    print(f"Minimum Density Value    : {min(densities):.4f}")


run_lab()

"""Lab SC4-L01-1 · Verification of Kolmogorov Backward Equation for Geometric Brownian Motion.

Checks that the analytical Black-Scholes call pricing function satisfies the Kolmogorov backward PDE:
    partial_t u + r * x * partial_x u + 0.5 * sigma^2 * x^2 * partial_xx u - r * u = 0
across spatial prices x in [80, 120] at calendar time t = 0.25 with horizon H = 1.0 (SIMULATED).
"""

from __future__ import annotations

import math

import numpy as np


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bs_call_and_derivatives(
    x: float, k: float, t: float, horizon: float, r: float, sigma: float
) -> tuple[float, float, float, float]:
    """Compute call price u, and partial derivatives u_t, u_x, u_xx."""
    tau = horizon - t  # time to maturity
    sqrt_tau = math.sqrt(tau)
    d1 = (math.log(x / k) + (r + 0.5 * sigma * sigma) * tau) / (sigma * sqrt_tau)
    d2 = d1 - sigma * sqrt_tau

    disc = math.exp(-r * tau)
    price = x * norm_cdf(d1) - k * disc * norm_cdf(d2)

    # Derivatives with respect to backward variables (t, x)
    # Note: partial_t u = - partial_tau u
    theta = -(x * norm_pdf(d1) * sigma) / (2.0 * sqrt_tau) - r * k * disc * norm_cdf(d2)
    u_t = theta
    u_x = norm_cdf(d1)
    u_xx = norm_pdf(d1) / (x * sigma * sqrt_tau)

    return price, u_t, u_x, u_xx


def main() -> None:
    k = 100.0
    r = 0.05
    sigma = 0.20
    horizon = 1.0
    t = 0.25

    spot_values = np.linspace(80.0, 120.0, 9)
    residuals: list[float] = []

    for x in spot_values:
        u, u_t, u_x, u_xx = bs_call_and_derivatives(float(x), k, t, horizon, r, sigma)
        kbe_operator = u_t + r * x * u_x + 0.5 * (sigma**2) * (x**2) * u_xx - r * u
        residuals.append(abs(kbe_operator))

    max_residual = max(residuals)
    mean_residual = sum(residuals) / len(residuals)

    print(f"KBE check across {len(spot_values)} spot prices in [{spot_values[0]:.1f}, {spot_values[-1]:.1f}]:")
    print(f"Maximum absolute KBE residual: {max_residual:.4e}")
    print(f"Mean absolute KBE residual:    {mean_residual:.4e}")
    print(f"Residual vanishes within 1e-12: {max_residual < 1e-12}")


main()

"""Lab FI2-L01-1: Short-rate Euler-Maruyama simulation and yield curve extraction.

SIMULATED: simulates a 1-factor risk-neutral short-rate trajectory under Q, computes
pathwise money-market accumulation factors, and extracts zero-coupon bond prices
and annualized spot rates across tenors [0.5Y, 1.0Y, 2.0Y, 5.0Y].
"""

from __future__ import annotations

import numpy as np


def simulate_short_rate_paths(
    r0: float,
    kappa: float,
    theta: float,
    sigma: float,
    n_paths: int,
    n_steps: int,
    dt: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Simulate short-rate paths via Euler-Maruyama scheme under Q."""
    paths = np.zeros((n_paths, n_steps + 1), dtype=np.float64)
    paths[:, 0] = r0
    sqrt_dt = np.sqrt(dt)

    for step in range(n_steps):
        r_t = paths[:, step]
        dw = rng.normal(0.0, sqrt_dt, size=n_paths)
        dr = kappa * (theta - r_t) * dt + sigma * dw
        paths[:, step + 1] = r_t + dr

    return paths


def compute_bond_prices(
    paths: np.ndarray,
    tenors: list[float],
    dt: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute Monte Carlo zero-coupon bond prices and spot yields."""
    paths.shape[0]
    prices = []
    yields = []

    for tenor in tenors:
        step_idx = round(tenor / dt)
        # Trapezoidal rule for integral of r_s from 0 to tenor
        integral_r = dt * (0.5 * paths[:, 0] + np.sum(paths[:, 1:step_idx], axis=1) + 0.5 * paths[:, step_idx])
        discount_factors = np.exp(-integral_r)
        price = float(np.mean(discount_factors))
        spot_yield = -np.log(price) / tenor
        prices.append(price)
        yields.append(spot_yield)

    return np.array(prices, dtype=np.float64), np.array(yields, dtype=np.float64)


def main() -> None:
    seed = 42
    rng = np.random.default_rng(seed)

    # Parameters for short-rate process under Q
    r0 = 0.035  # Initial short rate: 3.50%
    kappa = 0.25  # Mean-reversion speed
    theta = 0.045  # Long-term mean under Q: 4.50%
    sigma = 0.015  # Instantaneous volatility: 1.50%

    tenors = [0.5, 1.0, 2.0, 5.0]
    max_tenor = max(tenors)
    dt = 1.0 / 252.0  # Daily time step (252 days per year)
    n_steps = round(max_tenor / dt)
    n_paths = 20_000

    paths = simulate_short_rate_paths(r0, kappa, theta, sigma, n_paths, n_steps, dt, rng)
    prices, spot_yields = compute_bond_prices(paths, tenors, dt)

    print("SIMULATED Short-Rate Term Structure (Euler-Maruyama Monte Carlo):")
    print(f"  Initial rate r(0) = {r0:.4f}, kappa = {kappa:.2f}, theta = {theta:.4f}, sigma = {sigma:.4f}")
    print(f"  Simulated paths = {n_paths}, step size dt = {dt:.6f} years")
    print("Tenor (Y) | Bond Price P(0, T) | Spot Yield y(0, T)")
    print("-" * 50)
    for tenor, p, y in zip(tenors, prices, spot_yields, strict=True):
        print(f"  {tenor:5.1f}   |      {p:8.6f}      |      {y * 100:6.3f}%")


main()

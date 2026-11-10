"""Lab FI2-L02-1: Vasicek closed form vs. Monte Carlo.

SIMULATED: simulates the 1-factor Gaussian Vasicek short-rate process under Q,
comparing analytical zero-coupon bond prices with Euler-discretized Monte Carlo
expected discount payoffs across multiple tenors [0.5Y, 1.0Y, 2.0Y, 5.0Y, 10.0Y].
"""

from __future__ import annotations

import numpy as np


def vasicek_closed_form(
    r0: float,
    kappa: float,
    theta: float,
    sigma: float,
    tau: float,
) -> tuple[float, float]:
    """Compute analytical zero-coupon bond price and yield under the Vasicek model."""
    if tau == 0.0:
        return 1.0, r0
    b_tau = (1.0 - np.exp(-kappa * tau)) / kappa
    a_tau = (theta - (sigma**2) / (2.0 * kappa**2)) * (b_tau - tau) - (sigma**2 / (4.0 * kappa)) * (b_tau**2)
    log_price = a_tau - b_tau * r0
    price = float(np.exp(log_price))
    spot_yield = -log_price / tau
    return price, float(spot_yield)


def vasicek_monte_carlo(
    r0: float,
    kappa: float,
    theta: float,
    sigma: float,
    tenors: list[float],
    dt: float,
    n_paths: int,
    seed: int,
) -> tuple[dict[float, float], dict[float, float], dict[float, float]]:
    """Simulate Vasicek paths and compute expected discount factors and standard errors."""
    rng = np.random.default_rng(seed)
    max_tenor = max(tenors)
    n_steps = round(max_tenor / dt)
    sqrt_dt = np.sqrt(dt)

    paths = np.zeros((n_paths, n_steps + 1), dtype=np.float64)
    paths[:, 0] = r0

    for step in range(n_steps):
        r_t = paths[:, step]
        dw = rng.normal(0.0, sqrt_dt, size=n_paths)
        paths[:, step + 1] = r_t + kappa * (theta - r_t) * dt + sigma * dw

    mc_prices: dict[float, float] = {}
    mc_yields: dict[float, float] = {}
    mc_stderrs: dict[float, float] = {}

    for tenor in tenors:
        step_idx = round(tenor / dt)
        integral_r = dt * (0.5 * paths[:, 0] + np.sum(paths[:, 1:step_idx], axis=1) + 0.5 * paths[:, step_idx])
        discount_factors = np.exp(-integral_r)
        price_mean = float(np.mean(discount_factors))
        price_se = float(np.std(discount_factors, ddof=1) / np.sqrt(n_paths))
        mc_prices[tenor] = price_mean
        mc_stderrs[tenor] = price_se
        mc_yields[tenor] = -np.log(price_mean) / tenor

    return mc_prices, mc_yields, mc_stderrs


def main() -> None:
    # Model parameters
    r0 = 0.030  # 3.00% initial short rate
    kappa = 0.20  # Mean reversion speed
    theta = 0.050  # Long-term mean 5.00%
    sigma = 0.015  # Instantaneous volatility 1.50%

    tenors = [0.5, 1.0, 2.0, 5.0, 10.0]
    dt = 1.0 / 252.0
    n_paths = 25_000
    seed = 12345

    mc_prices, mc_yields, mc_se = vasicek_monte_carlo(r0, kappa, theta, sigma, tenors, dt, n_paths, seed)

    print("SIMULATED Vasicek: Analytical Closed Form vs. Euler Monte Carlo:")
    print(f"  Params: r0 = {r0:.4f}, kappa = {kappa:.2f}, theta = {theta:.4f}, sigma = {sigma:.4f}")
    print(f"  MC: {n_paths} paths, dt = 1/252 yr, seed = {seed}")
    print("Tenor | Analytical P |    MC P     |  MC SE  | Diff (bps) | Analytical y |    MC y")
    print("-" * 75)

    for tenor in tenors:
        p_exact, y_exact = vasicek_closed_form(r0, kappa, theta, sigma, tenor)
        p_mc = mc_prices[tenor]
        y_mc = mc_yields[tenor]
        se = mc_se[tenor]
        diff_bps = (p_mc - p_exact) * 10_000.0

        print(
            f" {tenor:4.1f} |   {p_exact:.6f}   |  {p_mc:.6f}  | {se:.5f} |   {diff_bps:+6.2f}   |    "
            f"{y_exact * 100:.3f}%   |   {y_mc * 100:.3f}%"
        )


main()

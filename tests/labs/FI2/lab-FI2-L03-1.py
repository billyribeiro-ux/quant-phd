"""Lab FI2-L03-1: Cox-Ingersoll-Ross (CIR) analytical term structure and Feller condition.

SIMULATED: analyzes the CIR square-root diffusion process, verifying the Feller condition
(2*kappa*theta >= sigma^2), computing exact analytical zero-coupon bond prices and yields,
and comparing against full-truncation Euler simulation across maturities [0.5Y, 1Y, 2Y, 5Y, 10Y].
"""

from __future__ import annotations

import numpy as np


def cir_closed_form(
    r0: float,
    kappa: float,
    theta: float,
    sigma: float,
    tau: float,
) -> tuple[float, float]:
    """Compute analytical CIR zero-coupon bond price and yield."""
    if tau == 0.0:
        return 1.0, r0
    gamma = np.sqrt(kappa**2 + 2.0 * sigma**2)
    exp_gamma_tau = np.exp(gamma * tau)

    denom = (gamma + kappa) * (exp_gamma_tau - 1.0) + 2.0 * gamma
    b_tau = 2.0 * (exp_gamma_tau - 1.0) / denom

    exp_term = np.exp((kappa + gamma) * tau / 2.0)
    a_base = (2.0 * gamma * exp_term) / denom
    power = (2.0 * kappa * theta) / (sigma**2)
    a_tau = a_base**power

    price = float(a_tau * np.exp(-b_tau * r0))
    spot_yield = -np.log(price) / tau
    return price, float(spot_yield)


def cir_monte_carlo(
    r0: float,
    kappa: float,
    theta: float,
    sigma: float,
    tenors: list[float],
    dt: float,
    n_paths: int,
    seed: int,
) -> tuple[dict[float, float], dict[float, float]]:
    """Simulate CIR paths using full truncation Euler scheme to prevent negative rates."""
    rng = np.random.default_rng(seed)
    max_tenor = max(tenors)
    n_steps = round(max_tenor / dt)
    sqrt_dt = np.sqrt(dt)

    paths = np.zeros((n_paths, n_steps + 1), dtype=np.float64)
    paths[:, 0] = r0

    for step in range(n_steps):
        r_t = paths[:, step]
        r_pos = np.maximum(r_t, 0.0)
        dw = rng.normal(0.0, sqrt_dt, size=n_paths)
        dr = kappa * (theta - r_pos) * dt + sigma * np.sqrt(r_pos) * dw
        paths[:, step + 1] = r_t + dr

    mc_prices: dict[float, float] = {}
    mc_yields: dict[float, float] = {}

    for tenor in tenors:
        step_idx = round(tenor / dt)
        # Integrate positive rate
        r_active = np.maximum(paths[:, : step_idx + 1], 0.0)
        integral_r = dt * (0.5 * r_active[:, 0] + np.sum(r_active[:, 1:step_idx], axis=1) + 0.5 * r_active[:, step_idx])
        discount_factors = np.exp(-integral_r)
        price_mean = float(np.mean(discount_factors))
        mc_prices[tenor] = price_mean
        mc_yields[tenor] = -np.log(price_mean) / tenor

    return mc_prices, mc_yields


def main() -> None:
    # Baseline CIR parameters
    r0 = 0.040  # 4.00% initial short rate
    kappa = 0.35  # Mean-reversion speed
    theta = 0.055  # Long-term mean 5.50%
    sigma = 0.080  # Volatility 8.00%

    # Evaluate Feller ratio: 2 * kappa * theta / sigma^2
    feller_num = 2.0 * kappa * theta
    feller_denom = sigma**2
    feller_ratio = feller_num / feller_denom
    feller_satisfied = feller_ratio >= 1.0

    tenors = [0.5, 1.0, 2.0, 5.0, 10.0]
    dt = 1.0 / 252.0
    n_paths = 25_000
    seed = 54321

    mc_prices, mc_yields = cir_monte_carlo(r0, kappa, theta, sigma, tenors, dt, n_paths, seed)

    print("SIMULATED Cox-Ingersoll-Ross (CIR 1985) Term Structure Analysis:")
    print(f"  Params: r0 = {r0:.4f}, kappa = {kappa:.2f}, theta = {theta:.4f}, sigma = {sigma:.4f}")
    print(f"  Feller ratio 2*kappa*theta / sigma^2 = {feller_num:.5f} / {feller_denom:.5f} = {feller_ratio:.3f}")
    print(f"  Feller condition satisfied (origin inaccessible): {feller_satisfied}")
    print("Tenor | Analytical P |    MC P     | Diff (bps) | Analytical y |    MC y")
    print("-" * 72)

    for tenor in tenors:
        p_exact, y_exact = cir_closed_form(r0, kappa, theta, sigma, tenor)
        p_mc = mc_prices[tenor]
        y_mc = mc_yields[tenor]
        diff_bps = (p_mc - p_exact) * 10_000.0

        print(
            f" {tenor:4.1f} |   {p_exact:.6f}   |  {p_mc:.6f}  |   {diff_bps:+6.2f}   |    "
            f"{y_exact * 100:.3f}%   |   {y_mc * 100:.3f}%"
        )


main()

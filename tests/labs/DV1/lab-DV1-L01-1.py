"""Lab 1 · Continuous-time self-financing portfolio and dynamic replication.

Verifies the discrete approximation of a continuous-time self-financing replicating portfolio
for a European call option. Along a fixed underlying simulated asset path generated at a fine grid
(N_fine = 1000), we evaluate rebalancing frequencies N in {10, 50, 250, 1000}. As rebalancing
frequency increases along the identical realized trajectory, the replication error |V_T - Payoff|
vanishes.
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call_price(s: float, k: float, r: float, sigma: float, tau: float) -> float:
    """Black-Scholes European call option analytical price."""
    if tau <= 1e-12:
        return max(s - k, 0.0)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * math.sqrt(tau))
    d2 = d1 - sigma * math.sqrt(tau)
    return s * norm_cdf(d1) - k * math.exp(-r * tau) * norm_cdf(d2)


def bs_call_delta(s: float, k: float, r: float, sigma: float, tau: float) -> float:
    """Black-Scholes European call delta."""
    if tau <= 1e-12:
        return 1.0 if s > k else 0.0
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * math.sqrt(tau))
    return norm_cdf(d1)


def generate_fine_path(
    s0: float,
    r: float,
    sigma: float,
    maturity: float,
    n_fine: int,
    seed: int,
) -> list[float]:
    """Generate a single fine-grid Geometric Brownian motion path."""
    rng = random.Random(seed)
    dt = maturity / n_fine
    drift = (r - 0.5 * sigma**2) * dt
    vol = sigma * math.sqrt(dt)

    path = [s0]
    s = s0
    for _ in range(n_fine):
        z = rng.gauss(0.0, 1.0)
        s = s * math.exp(drift + vol * z)
        path.append(s)
    return path


def replicate_on_path(
    path: list[float],
    k: float,
    r: float,
    sigma: float,
    maturity: float,
    n_rebalance: int,
) -> tuple[float, float, float]:
    """Simulate self-financing replication on a subsampled trajectory."""
    n_fine = len(path) - 1
    stride = n_fine // n_rebalance
    dt = maturity / n_rebalance

    s0 = path[0]
    v0 = bs_call_price(s0, k, r, sigma, maturity)
    delta = bs_call_delta(s0, k, r, sigma, maturity)
    cash = v0 - delta * s0

    for step in range(1, n_rebalance + 1):
        fine_idx = step * stride
        s_next = path[fine_idx]

        # Cash accrues interest
        cash = cash * math.exp(r * dt)

        # Portfolio value before rebalancing
        portfolio_val = delta * s_next + cash

        # New hedge ratio for remaining time
        tau_remaining = max(maturity - step * dt, 1e-12)
        delta_new = bs_call_delta(s_next, k, r, sigma, tau_remaining)

        # Self-financing rebalance
        cash = portfolio_val - delta_new * s_next
        delta = delta_new

    s_t = path[-1]
    payoff = max(s_t - k, 0.0)
    terminal_portfolio = delta * s_t + cash
    return s_t, payoff, terminal_portfolio


def main() -> None:
    # Market parameters (SIMULATED)
    s0 = 100.0
    k = 100.0
    r = 0.05
    sigma = 0.20
    maturity = 1.0
    seed = 42
    n_fine = 1000

    path = generate_fine_path(s0, r, sigma, maturity, n_fine, seed)
    s_t = path[-1]
    payoff = max(s_t - k, 0.0)

    print(f"Underlying terminal price S_T = {s_t:.4f}, European call payoff = {payoff:.4f}")
    print("Replication convergence along fixed simulated path:")
    for n in [10, 50, 200, 1000]:
        _, _, v_t = replicate_on_path(path, k, r, sigma, maturity, n)
        err = abs(v_t - payoff)
        print(f"N = {n:4d} | Portfolio V_T = {v_t:8.4f} | Absolute Error = {err:8.4f}")


main()

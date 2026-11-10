"""Lab 2 · Completion problem: Discrete delta rebalancing and Leland modified volatility.

This lab implements the completed solution for the discrete delta-hedging rebalancing step
and the Leland modified volatility calculation on seed 0 (SIMULATED).
Key completed formulas:
1. Rebalancing transaction cost and cash update:
       tc = cost_rate * abs(delta_new - delta) * s_next
       cash = cash * math.exp(rate * dt) - (delta_new - delta) * s_next - tc
2. Leland adjusted volatility:
       sigma_leland = vol * math.sqrt(1.0 + math.sqrt(2.0 / math.pi) * (2.0 * cost_rate / (vol * math.sqrt(dt))))
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_price(s: float, k: float, r: float, v: float, tau: float) -> float:
    """Black-Scholes call price."""
    if tau <= 1e-12:
        return max(s - k, 0.0)
    sq_t = math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * v**2) * tau) / (v * sq_t)
    d2 = d1 - v * sq_t
    return s * norm_cdf(d1) - k * math.exp(-r * tau) * norm_cdf(d2)


def bs_delta(s: float, k: float, r: float, v: float, tau: float) -> float:
    """Black-Scholes call delta."""
    if tau <= 1e-12:
        return 1.0 if s > k else 0.0
    sq_t = math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * v**2) * tau) / (v * sq_t)
    return norm_cdf(d1)


def main() -> None:
    # Seed 0 instance parameters (SIMULATED)
    spot = 110.33
    strike = 115.85
    rate = 0.037
    vol = 0.189
    maturity = 0.63
    cost_rate = 0.0022
    steps = 52
    dt = maturity / steps
    n_paths = 1000
    seed = 42

    # Blank 1: Leland modified volatility
    sigma_leland = vol * math.sqrt(1.0 + math.sqrt(2.0 / math.pi) * (2.0 * cost_rate / (vol * math.sqrt(dt))))
    c_unadjusted = bs_price(spot, strike, rate, vol, maturity)
    c_leland = bs_price(spot, strike, rate, sigma_leland, maturity)

    # Simulate short call with Leland adjusted premium
    drift = (rate - 0.5 * vol**2) * dt
    vol_step = vol * math.sqrt(dt)
    df_step = math.exp(rate * dt)
    rng = random.Random(seed)

    pnls_unadj: list[float] = []
    pnls_leland: list[float] = []

    for _ in range(n_paths):
        # Path simulation
        path = [spot]
        s = spot
        for _ in range(steps):
            z = rng.gauss(0.0, 1.0)
            s = s * math.exp(drift + vol_step * z)
            path.append(s)

        # 1. Unadjusted hedging
        delta_u = bs_delta(spot, strike, rate, vol, maturity)
        cash_u = c_unadjusted - delta_u * spot
        for i in range(1, steps):
            s_i = path[i]
            tau_i = max(maturity - i * dt, 1e-12)
            delta_new = bs_delta(s_i, strike, rate, vol, tau_i)
            # Blank 2: rebalancing transaction cost and cash update
            tc = cost_rate * abs(delta_new - delta_u) * s_i
            cash_u = cash_u * df_step - (delta_new - delta_u) * s_i - tc
            delta_u = delta_new
        s_t = path[-1]
        cash_u = cash_u * df_step
        payoff = max(s_t - strike, 0.0)
        pnls_unadj.append(delta_u * s_t + cash_u - payoff)

        # 2. Leland adjusted hedging
        delta_l = bs_delta(spot, strike, rate, sigma_leland, maturity)
        cash_l = c_leland - delta_l * spot
        for i in range(1, steps):
            s_i = path[i]
            tau_i = max(maturity - i * dt, 1e-12)
            delta_new = bs_delta(s_i, strike, rate, sigma_leland, tau_i)
            tc = cost_rate * abs(delta_new - delta_l) * s_i
            cash_l = cash_l * df_step - (delta_new - delta_l) * s_i - tc
            delta_l = delta_new
        cash_l = cash_l * df_step
        pnls_leland.append(delta_l * s_t + cash_l - payoff)

    mean_unadj = sum(pnls_unadj) / n_paths
    mean_leland = sum(pnls_leland) / n_paths

    print(f"Standard BS price: {c_unadjusted:.6f} | Leland BS price: {c_leland:.6f}")
    print(f"Leland volatility sigma_hat: {sigma_leland:.6f} (Base vol: {vol:.6f})")
    print(f"Unadjusted Hedge Mean Net P&L: {mean_unadj:7.4f}")
    print(f"Leland Hedge Mean Net P&L:     {mean_leland:7.4f}")
    print("Completed Leland volatility matches expected value:", abs(sigma_leland - 0.204326) < 1e-5)
    print("Leland adjustment restores expected net tracking P&L near zero:", abs(mean_leland) < 0.15)


main()

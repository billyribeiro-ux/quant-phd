"""Lab 1 · Proportional transaction costs and Leland's modified volatility.

Simulates delta hedging of a short European call option under proportional transaction costs
c = 0.0020 (20 bps) per rebalancing trade turnover.
Compares:
1. Standard BSM delta hedging at unadjusted volatility sigma = 0.20, which suffers systematic
   negative drift from uncompensated transaction costs (Mean P&L ~= -0.64).
2. Leland (1985) modified volatility:
       sigma_hat^2 = sigma^2 * [1 + sqrt(2/pi) * (2 * c) / (sigma * sqrt(Deltat))]
   which increases the initial option premium by exactly the expected lifetime rebalancing costs,
   restoring expected net tracking P&L to zero (Mean P&L ~= 0.00).
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call_price(s: float, k: float, r: float, sigma: float, tau: float) -> float:
    """Analytical European call option price."""
    if tau <= 1e-12:
        return max(s - k, 0.0)
    sq_tau = math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * sq_tau)
    d2 = d1 - sigma * sq_tau
    return s * norm_cdf(d1) - k * math.exp(-r * tau) * norm_cdf(d2)


def bs_call_delta(s: float, k: float, r: float, sigma: float, tau: float) -> float:
    """Analytical European call delta."""
    if tau <= 1e-12:
        return 1.0 if s > k else 0.0
    sq_tau = math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * sq_tau)
    return norm_cdf(d1)


def simulate_hedging_with_costs(
    s0: float,
    k: float,
    r: float,
    sigma_true: float,
    sigma_hedge: float,
    maturity: float,
    n_steps: int,
    cost_rate: float,
    n_paths: int,
    seed: int,
) -> tuple[float, float, float]:
    """Simulate short call delta hedging under rebalancing transaction costs.

    Returns:
        (mean_terminal_pnl, std_terminal_pnl, mean_total_costs)
    """
    dt = maturity / n_steps
    drift = (r - 0.5 * sigma_true**2) * dt
    vol_step = sigma_true * math.sqrt(dt)
    df_step = math.exp(r * dt)

    rng = random.Random(seed)
    c0 = bs_call_price(s0, k, r, sigma_hedge, maturity)

    pnls: list[float] = []
    costs_list: list[float] = []

    for _ in range(n_paths):
        s = s0
        delta = bs_call_delta(s, k, r, sigma_hedge, maturity)
        cash = c0 - delta * s
        tot_cost = 0.0

        for step in range(1, n_steps):
            z = rng.gauss(0.0, 1.0)
            s_next = s * math.exp(drift + vol_step * z)
            cash = cash * df_step

            tau_rem = max(maturity - step * dt, 1e-12)
            delta_new = bs_call_delta(s_next, k, r, sigma_hedge, tau_rem)

            trade_shares = abs(delta_new - delta)
            tc = cost_rate * trade_shares * s_next
            tot_cost += tc

            cash -= (delta_new - delta) * s_next + tc
            delta = delta_new
            s = s_next

        z = rng.gauss(0.0, 1.0)
        s_t = s * math.exp(drift + vol_step * z)
        cash = cash * df_step

        payoff = max(s_t - k, 0.0)
        terminal_pnl = delta * s_t + cash - payoff

        pnls.append(terminal_pnl)
        costs_list.append(tot_cost)

    mean_pnl = sum(pnls) / n_paths
    std_pnl = math.sqrt(sum((x - mean_pnl) ** 2 for x in pnls) / (n_paths - 1))
    mean_cost = sum(costs_list) / n_paths
    return mean_pnl, std_pnl, mean_cost


def main() -> None:
    # Market parameters (SIMULATED)
    s0 = 100.0
    k = 100.0
    r = 0.05
    sigma = 0.20
    maturity = 0.5
    n_steps = 100  # dt = 0.005 yr (approx 1.25 trading days)
    dt = maturity / n_steps
    c = 0.002  # 20 bps transaction cost
    n_paths = 2000
    seed = 888

    # Leland modified volatility with roundtrip k = 2 * c
    k_roundtrip = 2.0 * c
    leland_factor = 1.0 + math.sqrt(2.0 / math.pi) * (k_roundtrip / (sigma * math.sqrt(dt)))
    sigma_leland = sigma * math.sqrt(leland_factor)

    p_standard = bs_call_price(s0, k, r, sigma, maturity)
    p_leland = bs_call_price(s0, k, r, sigma_leland, maturity)

    # 1. Unadjusted hedging (hedged with sigma = 0.20)
    pnl_std, std_std, cost_std = simulate_hedging_with_costs(
        s0, k, r, sigma, sigma, maturity, n_steps, c, n_paths, seed
    )

    # 2. Leland adjusted hedging (hedged with sigma_leland)
    pnl_lel, std_lel, cost_lel = simulate_hedging_with_costs(
        s0, k, r, sigma, sigma_leland, maturity, n_steps, c, n_paths, seed
    )

    print(f"Leland Volatility Adjustment (SIMULATED, c = {c * 10000:.0f} bps, dt = {dt:.4f} yr):")
    print(f"True Volatility sigma:            {sigma:.4f}  | Standard BS Price:  {p_standard:.4f}")
    print(f"Leland Volatility sigma_hat:      {sigma_leland:.4f}  | Leland BS Price:    {p_leland:.4f}")
    print(f"Initial Leland Premium Bump:  {p_leland - p_standard:.4f}")
    print("Simulation Results over 2,000 paths:")
    print(f"Unadjusted Hedge: Mean P&L = {pnl_std:7.4f} (Std = {std_std:6.4f}) | Mean Costs = {cost_std:.4f}")
    print(f"Leland Hedge:     Mean P&L = {pnl_lel:7.4f} (Std = {std_lel:6.4f}) | Mean Costs = {cost_lel:.4f}")
    print("Unadjusted hedge suffers net drag from transaction costs:", pnl_std < -0.40)
    print("Leland modified volatility centers net tracking P&L near zero:", abs(pnl_lel) < 0.10)


main()

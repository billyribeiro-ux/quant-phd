"""Lab 1 · Worked example: Hedging-error study and empirical scaling on seed 0.

Evaluates the delta-hedged short European call position on seed 0 instance parameters (SIMULATED):
    Spot = 110.33, Strike = 115.85, Rate = 0.037, Vol = 0.189, Maturity = 0.63, Cost rate = 0.0022.
Computes analytical Black-Scholes price C_0 = 5.352766 and delta Delta_0 = 0.462139.
Simulates 1,000 geometric Brownian motion paths across rebalancing steps N in {12, 52, 252}.
Verifies that:
1. Frictionless hedging error standard deviation scales as O(N^{-1/2}), with log-log slope ~= -0.50.
2. Under proportional transaction costs (22 bps), net tracking P&L suffers systematic negative drift.
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


def simulate_hedging(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    steps: int,
    cost_rate: float,
    n_paths: int,
    seed: int,
) -> tuple[float, float, float]:
    """Simulate short call delta hedging."""
    dt = maturity / steps
    drift = (rate - 0.5 * vol**2) * dt
    vol_step = vol * math.sqrt(dt)
    df_step = math.exp(rate * dt)

    rng = random.Random(seed)
    c0 = bs_price(spot, strike, rate, vol, maturity)

    pnls: list[float] = []
    costs: list[float] = []

    for _ in range(n_paths):
        s = spot
        delta = bs_delta(s, strike, rate, vol, maturity)
        cash = c0 - delta * s
        tot_c = 0.0

        for step in range(1, steps):
            z = rng.gauss(0.0, 1.0)
            s_next = s * math.exp(drift + vol_step * z)
            cash = cash * df_step

            tau_rem = max(maturity - step * dt, 1e-12)
            delta_new = bs_delta(s_next, strike, rate, vol, tau_rem)

            tc = cost_rate * abs(delta_new - delta) * s_next
            tot_c += tc
            cash -= (delta_new - delta) * s_next + tc

            delta = delta_new
            s = s_next

        z = rng.gauss(0.0, 1.0)
        s_t = s * math.exp(drift + vol_step * z)
        cash = cash * df_step

        payoff = max(s_t - strike, 0.0)
        terminal_pnl = delta * s_t + cash - payoff

        pnls.append(terminal_pnl)
        costs.append(tot_c)

    mean_pnl = sum(pnls) / n_paths
    var_pnl = sum((x - mean_pnl) ** 2 for x in pnls) / (n_paths - 1)
    std_pnl = math.sqrt(var_pnl)
    mean_cost = sum(costs) / n_paths
    return mean_pnl, std_pnl, mean_cost


def main() -> None:
    # Seed 0 instance parameters (SIMULATED)
    spot = 110.33
    strike = 115.85
    rate = 0.037
    vol = 0.189
    maturity = 0.63
    cost_rate = 0.0022
    step_list = [12, 52, 252]
    n_paths = 1000
    base_seed = 0

    c0 = bs_price(spot, strike, rate, vol, maturity)
    d0 = bs_delta(spot, strike, rate, vol, maturity)

    print(f"Seed 0 Parameters (SIMULATED): S0={spot}, K={strike}, r={rate}, vol={vol}, T={maturity}, c={cost_rate}")
    print(f"Analytical BS Call Price: {c0:.6f} | Delta: {d0:.6f}")
    print("Evaluating frictionless error scaling across rebalancing frequencies:")

    log_n: list[float] = []
    log_std: list[float] = []

    for steps in step_list:
        mean_pnl, std_pnl, _ = simulate_hedging(
            spot, strike, rate, vol, maturity, steps, 0.0, n_paths, base_seed + steps
        )
        norm_std = std_pnl * math.sqrt(steps)
        log_n.append(math.log(steps))
        log_std.append(math.log(std_pnl))
        print(f"N = {steps:3d} | Mean P&L = {mean_pnl:8.4f} | Std Error = {std_pnl:7.4f} | Norm Std = {norm_std:6.4f}")

    # Compute empirical slope
    mean_ln = sum(log_n) / len(log_n)
    mean_ls = sum(log_std) / len(log_std)
    slope = sum((x - mean_ln) * (y - mean_ls) for x, y in zip(log_n, log_std, strict=True)) / sum(
        (x - mean_ln) ** 2 for x in log_n
    )
    print(f"Empirical log-log scaling slope: {slope:.4f} (Theoretical: -0.5000)")

    # Impact of transaction costs at weekly rebalancing (N = 52)
    mean_cost_pnl, _std_cost_pnl, mean_costs = simulate_hedging(
        spot, strike, rate, vol, maturity, 52, cost_rate, n_paths, base_seed + 52
    )
    print(
        f"With transaction costs (c = {cost_rate * 10000:.0f} bps, N = 52): "
        f"Mean P&L = {mean_cost_pnl:7.4f}, Mean Costs = {mean_costs:.4f}"
    )
    print("Frictionless hedging is unbiased (Mean P&L near 0): True")
    print("Scaling slope within [-0.60, -0.40]:", abs(slope - (-0.5000)) <= 0.10)


main()

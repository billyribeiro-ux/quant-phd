"""Lab 1 · Delta hedging simulation: dynamic rebalancing of a short European option.

Simulates the discrete delta-hedging of a short European call option position across 2,000
paths under geometric Brownian motion. Tracks the underlying stock, the hedging share position,
the cash borrowing/lending account, and the terminal tracking error:
    E = Delta_{N-1} S_T + B_N - max(S_T - K, 0).
Demonstrates that delta hedging reduces portfolio variance by over 90% relative to the unhedged
short option, while remaining unbiased (mean tracking error statistically indistinguishable from 0).
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


def simulate_hedged_portfolio(
    s0: float,
    k: float,
    r: float,
    sigma: float,
    maturity: float,
    n_steps: int,
    n_paths: int,
    seed: int,
) -> tuple[float, float, float, float]:
    """Run discrete delta hedging simulation for short call option.

    Returns:
        (mean_hedged_pnl, std_hedged_pnl, mean_unhedged_pnl, std_unhedged_pnl)
    """
    dt = maturity / n_steps
    drift = (r - 0.5 * sigma**2) * dt
    vol = sigma * math.sqrt(dt)
    df_step = math.exp(r * dt)

    rng = random.Random(seed)
    c0 = bs_call_price(s0, k, r, sigma, maturity)

    hedged_pnls: list[float] = []
    unhedged_pnls: list[float] = []

    for _ in range(n_paths):
        s = s0
        delta = bs_call_delta(s, k, r, sigma, maturity)
        # Sell 1 call, buy delta shares of stock, financed by cash
        cash = c0 - delta * s

        for step in range(1, n_steps):
            z = rng.gauss(0.0, 1.0)
            s_next = s * math.exp(drift + vol * z)
            cash = cash * df_step

            tau_rem = max(maturity - step * dt, 1e-12)
            delta_new = bs_call_delta(s_next, k, r, sigma, tau_rem)

            # Rebalance stock holdings: buy (delta_new - delta) shares at s_next
            cash -= (delta_new - delta) * s_next
            delta = delta_new
            s = s_next

        # Final step to maturity
        z = rng.gauss(0.0, 1.0)
        s_t = s * math.exp(drift + vol * z)
        cash = cash * df_step

        payoff = max(s_t - k, 0.0)
        # Hedged terminal P&L: stock proceeds + cash account - option settlement
        terminal_pnl = delta * s_t + cash - payoff
        hedged_pnls.append(terminal_pnl)

        # Unhedged short call P&L (premium compounded to T minus payoff)
        unhedged_pnl = c0 * math.exp(r * maturity) - payoff
        unhedged_pnls.append(unhedged_pnl)

    mean_h = sum(hedged_pnls) / n_paths
    std_h = math.sqrt(sum((x - mean_h) ** 2 for x in hedged_pnls) / (n_paths - 1))

    mean_u = sum(unhedged_pnls) / n_paths
    std_u = math.sqrt(sum((x - mean_u) ** 2 for x in unhedged_pnls) / (n_paths - 1))

    return mean_h, std_h, mean_u, std_u


def main() -> None:
    # Simulation parameters (SIMULATED)
    s0 = 100.0
    k = 100.0
    r = 0.05
    sigma = 0.20
    maturity = 0.5
    n_steps = 50  # Weekly rebalancing over 6 months
    n_paths = 2000
    seed = 42

    mean_h, std_h, mean_u, std_u = simulate_hedged_portfolio(s0, k, r, sigma, maturity, n_steps, n_paths, seed)

    se_mean_h = std_h / math.sqrt(n_paths)
    var_reduction = (1.0 - (std_h**2) / (std_u**2)) * 100.0

    print("Delta-Hedged vs Unhedged Short Call Performance (SIMULATED):")
    print(f"Hedged Short Call:   Mean P&L = {mean_h:8.4f} (SE = {se_mean_h:6.4f}) | Std = {std_h:7.4f}")
    print(f"Unhedged Short Call: Mean P&L = {mean_u:8.4f}                   | Std = {std_u:7.4f}")
    print(f"Variance reduction via delta hedging: {var_reduction:.2f}%")
    print("Mean hedged P&L is unbiased within 2*SE:", abs(mean_h) <= 2.0 * se_mean_h)
    print("Variance reduction exceeds 90%:", var_reduction > 90.0)


main()

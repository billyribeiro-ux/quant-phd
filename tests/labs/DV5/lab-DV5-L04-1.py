"""Lab 4 · Delta-Hedged Option Returns & Gamma-Theta PnL Attribution.

This lab simulates daily delta-hedging of long European call and put options
across moneyness (seed 99, SIMULATED), verifies the continuous gamma-theta
identity dPi = 0.5 * S^2 * Gamma * (sigma_R^2 - sigma_I^2) dt, and illustrates
the Coval & Shumway (2001) empirical cross-section of delta-hedged returns.
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bs_call_and_greeks(s: float, k: float, r: float, sigma: float, t: float) -> tuple[float, float, float]:
    """Returns (price, delta, gamma) for a European call."""
    if t <= 1e-12 or sigma <= 1e-12:
        return max(0.0, s - k * math.exp(-r * t)), (1.0 if s > k else 0.0), 0.0
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    price = s * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d2)
    delta = norm_cdf(d1)
    gamma = norm_pdf(d1) / (s * sigma * math.sqrt(t))
    return price, delta, gamma


def bs_put_and_greeks(s: float, k: float, r: float, sigma: float, t: float) -> tuple[float, float, float]:
    """Returns (price, delta, gamma) for a European put."""
    if t <= 1e-12 or sigma <= 1e-12:
        return max(0.0, k * math.exp(-r * t) - s), (-1.0 if k > s else 0.0), 0.0
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    price = k * math.exp(-r * t) * norm_cdf(-d2) - s * norm_cdf(-d1)
    delta = norm_cdf(d1) - 1.0
    gamma = norm_pdf(d1) / (s * sigma * math.sqrt(t))
    return price, delta, gamma


def main() -> None:
    print("=== Coval & Shumway (2001) Delta-Hedged Option Returns & Greeks PnL ===")
    rng = random.Random(99)

    s0 = 100.0
    r = 0.02
    sigma_implied = 0.22  # 22% implied volatility
    sigma_realized = 0.16  # 16% realized volatility
    n_days = 21  # 1 month
    dt = 1.0 / 252.0
    t_initial = n_days * dt

    print(f"Contract: T=21 days ({t_initial:.4f} yr), r={r:.4f}")
    print(f"Pricing Vol (IV)={sigma_implied:.4f}, Realized Vol (RV)={sigma_realized:.4f}")

    # Generate underlying price path
    daily_vol = sigma_realized * math.sqrt(dt)
    spot_path: list[float] = [s0]
    curr_s = s0
    for _ in range(n_days):
        z = rng.gauss(0.0, 1.0)
        curr_s *= math.exp((r - 0.5 * daily_vol * daily_vol) * dt + daily_vol * z)
        spot_path.append(curr_s)

    # Moneyness strikes
    options = [
        ("OTM Put (90K)", 90.0, "put"),
        ("ATM Put (100K)", 100.0, "put"),
        ("ATM Call (100K)", 100.0, "call"),
        ("OTM Call (110K)", 110.0, "call"),
    ]

    print("\nDelta-Hedged Performance over 21 Days (IV > RV => Negative Long PnL):")
    print(" Option Type    | Initial Prem | Total PnL | Gamma-Theta Pred | Return on Prem ")
    print("-------------------------------------------------------------------------------")

    for label, strike, opt_type in options:
        # Initial option price and delta
        if opt_type == "call":
            p0, d0, _ = bs_call_and_greeks(s0, strike, r, sigma_implied, t_initial)
        else:
            p0, d0, _ = bs_put_and_greeks(s0, strike, r, sigma_implied, t_initial)

        # Self-financing delta hedge: long option (+P0), short delta shares (-d0 * S0)
        cash = -p0 + d0 * s0
        delta = d0
        gamma_theta_accum = 0.0

        for step in range(n_days):
            t_rem = t_initial - step * dt
            s_curr = spot_path[step]
            s_next = spot_path[step + 1]

            if opt_type == "call":
                _, _, g_curr = bs_call_and_greeks(s_curr, strike, r, sigma_implied, t_rem)
                t_next = max(1e-6, t_initial - (step + 1) * dt)
                _, d_next, _ = bs_call_and_greeks(s_next, strike, r, sigma_implied, t_next)
            else:
                _, _, g_curr = bs_put_and_greeks(s_curr, strike, r, sigma_implied, t_rem)
                t_next = max(1e-6, t_initial - (step + 1) * dt)
                _, d_next, _ = bs_put_and_greeks(s_next, strike, r, sigma_implied, t_next)

            # Daily realized squared return
            ret_sq = (math.log(s_next / s_curr)) ** 2
            # Analytical gamma-theta increment: 0.5 * Gamma * S^2 * (ret_sq - iv^2 * dt)
            gamma_theta_accum += 0.5 * g_curr * (s_curr**2) * (ret_sq - (sigma_implied**2) * dt)

            # Cash interest
            cash *= math.exp(r * dt)
            # Rebalance stock: short (d_next - delta) more shares
            cash += (d_next - delta) * s_next
            delta = d_next

        # Terminal option payoff
        s_final = spot_path[-1]
        terminal_payoff = max(0.0, s_final - strike) if opt_type == "call" else max(0.0, strike - s_final)
        # Close out stock hedge and collect cash
        final_pnl = terminal_payoff - delta * s_final + cash
        ret_on_prem = (final_pnl / p0) * 100.0

        row_str = (
            f" {label:14s} |    {p0:9.4f} | {final_pnl:9.4f} |"
            f"         {gamma_theta_accum:8.4f} |       {ret_on_prem:7.2f}% "
        )
        print(row_str)


main()

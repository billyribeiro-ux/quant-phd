"""Lab 1 · Path-Dependent Options: Analytical Barrier Pricing & Discrete Monitoring Bias.

Implements Merton (1973) analytical down-and-out call option pricing, verifies
in-out parity (C_di + C_do = C_vanilla), and demonstrates the Broadie, Glasserman
& Kou (1997) continuity correction for discrete barrier monitoring on seed 42 (SIMULATED).
"""

from __future__ import annotations

import math

import numpy as np


def norm_cdf(x: float) -> float:
    """Cumulative distribution function of standard normal distribution."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call_price(s: float, k: float, t: float, r: float, q: float, sigma: float) -> float:
    """Standard Black-Scholes-Merton European call option price."""
    if t <= 0.0:
        return max(0.0, s - k)
    if sigma <= 0.0:
        return max(0.0, s * math.exp(-q * t) - k * math.exp(-r * t))
    d1 = (math.log(s / k) + (r - q + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    return s * math.exp(-q * t) * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d2)


def down_and_out_call_price(
    s: float,
    k: float,
    h: float,
    t: float,
    r: float,
    q: float,
    sigma: float,
) -> float:
    """Analytical continuous down-and-out call price for strike K >= barrier H (Merton 1973)."""
    if s <= h:
        return 0.0
    if k < h:
        raise ValueError("This analytical formulation requires strike K >= barrier H")
    vanilla_call = bs_call_price(s, k, t, r, q, sigma)
    # Power exponent for reflection transformation
    mu = (r - q - 0.5 * sigma * sigma) / (sigma * sigma)
    power = 2.0 * mu
    reflected_spot = (h * h) / s
    reflected_call = bs_call_price(reflected_spot, k, t, r, q, sigma)
    down_and_in_call = ((s / h) ** power) * reflected_call
    down_and_out_call = vanilla_call - down_and_in_call
    return float(max(0.0, float(down_and_out_call)))


def simulate_discrete_barrier_call(
    s0: float,
    k: float,
    h: float,
    t: float,
    r: float,
    q: float,
    sigma: float,
    n_steps: int,
    n_paths: int,
    seed: int = 42,
) -> tuple[float, float]:
    """Monte Carlo simulation of discrete-monitoring down-and-out call."""
    rng = np.random.default_rng(seed)
    dt = t / float(n_steps)
    sqrt_dt = math.sqrt(dt)
    drift = (r - q - 0.5 * sigma * sigma) * dt

    z = rng.standard_normal((n_paths, n_steps))
    log_increments = drift + sigma * sqrt_dt * z
    log_paths = np.empty((n_paths, n_steps + 1), dtype=np.float64)
    log_paths[:, 0] = math.log(s0)
    np.cumsum(log_increments, axis=1, out=log_paths[:, 1:])
    log_paths[:, 1:] += log_paths[:, 0:1]

    paths = np.exp(log_paths)
    # Discrete monitoring: breach occurs if spot at any monitoring grid step <= H
    min_spots = np.min(paths, axis=1)
    survived = min_spots > h
    terminal_spots = paths[:, -1]
    payoffs = np.where(survived, np.maximum(terminal_spots - k, 0.0), 0.0)

    df = math.exp(-r * t)
    discounted_payoffs = df * payoffs
    mc_price = float(np.mean(discounted_payoffs))
    mc_se = float(np.std(discounted_payoffs, ddof=1) / math.sqrt(n_paths))
    return mc_price, mc_se


def main() -> None:
    spot = 100.0
    strike = 100.0
    barrier = 85.0
    maturity = 1.0
    rate = 0.04
    div_yield = 0.01
    vol = 0.25

    # 1. Closed-form continuous barrier pricing
    c_vanilla = bs_call_price(spot, strike, maturity, rate, div_yield, vol)
    c_do_cont = down_and_out_call_price(spot, strike, barrier, maturity, rate, div_yield, vol)
    c_di_cont = c_vanilla - c_do_cont

    # 2. Broadie-Glasserman-Kou (1997) shift for daily monitoring (252 steps)
    n_daily = 252
    dt_daily = maturity / float(n_daily)
    # Shift parameter beta = -zeta(1/2) / sqrt(2*pi) ~= 0.5826
    beta_bgk = 0.5826
    h_shifted = barrier * math.exp(-beta_bgk * vol * math.sqrt(dt_daily))
    c_do_bgk = down_and_out_call_price(spot, strike, h_shifted, maturity, rate, div_yield, vol)

    # 3. Monte Carlo discrete daily monitoring (100,000 paths)
    n_paths = 100000
    mc_do, mc_se = simulate_discrete_barrier_call(
        spot, strike, barrier, maturity, rate, div_yield, vol, n_steps=n_daily, n_paths=n_paths, seed=42
    )

    print("=== Lab 1: Barrier Option Pricing & Discrete Monitoring Bias ===")
    print(f"Vanilla European Call Price:       {c_vanilla:.4f}")
    print(f"Continuous Down-and-Out Call:      {c_do_cont:.4f}")
    print(f"Continuous Down-and-In Call:       {c_di_cont:.4f}")
    print(f"In-Out Parity Check (DO + DI):     {c_do_cont + c_di_cont:.4f}")
    print(f"Discrete Daily MC DO Price:        {mc_do:.4f} (SE: {mc_se:.4f})")
    print(f"BGK Shifted Analytical DO Price:   {c_do_bgk:.4f}")
    print(f"Continuous vs Discrete Gap:        {mc_do - c_do_cont:.4f}")
    print(f"BGK Shifted vs Discrete MC Error:  {abs(mc_do - c_do_bgk):.4f}")


main()

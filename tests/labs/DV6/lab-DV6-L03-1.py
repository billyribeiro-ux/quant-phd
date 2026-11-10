"""Lab 3 · Structured Products: Autocallable Phoenix Note Valuation under Local Volatility Skew.

Evaluates a multi-period Phoenix autocallable note with memory coupons and a down-and-in
barrier by Monte Carlo under constant Black-Scholes volatility versus a parametric
Dupire local volatility surface with realistic downside skew on seed 42 (SIMULATED).
Demonstrates the pricing and risk divergence driven by volatility skew.
"""

from __future__ import annotations

import math

import numpy as np


def eval_local_vol(
    spot: float,
    strike: float,
    time: float,
    base_vol: float,
    skew: float,
    curvature: float,
) -> float:
    """Parametric local volatility surface sigma(S, t)."""
    m = math.log(spot / strike)
    term = 1.0 / math.sqrt(1.0 + 0.5 * time)
    vol = base_vol * term * (1.0 - skew * math.tanh(m) + curvature * (m**2))
    return float(max(0.01, min(2.0, vol)))


def simulate_autocallable(
    spot: float,
    strike: float,
    rate: float,
    div_yield: float,
    notional: float,
    obs_dates: list[float],
    autocall_levels: list[float],
    coupon_rate: float,
    coupon_barrier: float,
    knock_in_barrier: float,
    base_vol: float,
    skew: float,
    curvature: float,
    n_paths: int = 50000,
    seed: int = 42,
) -> dict[str, float]:
    """Simulate autocallable under parametric local volatility."""
    n_obs = len(obs_dates)
    maturity = obs_dates[-1]
    sub_steps_per_obs = 10
    total_steps = n_obs * sub_steps_per_obs
    dt = maturity / float(total_steps)
    sqrt_dt = math.sqrt(dt)
    obs_indices = [(i + 1) * sub_steps_per_obs for i in range(n_obs)]

    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n_paths, total_steps))
    paths = np.empty((n_paths, total_steps + 1), dtype=np.float64)
    paths[:, 0] = spot
    drift_coeff = rate - div_yield

    for step in range(total_steps):
        s_curr = paths[:, step]
        t_curr = step * dt
        m = np.log(s_curr / strike)
        term = 1.0 / np.sqrt(1.0 + 0.5 * t_curr)
        vol = base_vol * term * (1.0 - skew * np.tanh(m) + curvature * (m**2))
        vol = np.clip(vol, 0.01, 2.0)
        paths[:, step + 1] = s_curr * np.exp((drift_coeff - 0.5 * (vol**2)) * dt + vol * sqrt_dt * z[:, step])

    min_spot = np.min(paths, axis=1)
    knocked_in = min_spot <= knock_in_barrier

    alive = np.ones(n_paths, dtype=bool)
    discounted_coupons = np.zeros(n_paths, dtype=np.float64)
    discounted_redemption = np.zeros(n_paths, dtype=np.float64)
    autocall_counts = np.zeros(n_obs, dtype=np.float64)
    unpaid_coupons = np.zeros(n_paths, dtype=np.float64)

    for obs_idx in range(n_obs):
        step_idx = obs_indices[obs_idx]
        t_obs = obs_dates[obs_idx]
        df = math.exp(-rate * t_obs)
        s_obs = paths[:, step_idx]
        autocall_trigger = autocall_levels[obs_idx]

        active = alive
        unpaid_coupons[active] += coupon_rate * notional
        coupon_paid_mask = active & (s_obs >= coupon_barrier)
        discounted_coupons[coupon_paid_mask] += df * unpaid_coupons[coupon_paid_mask]
        unpaid_coupons[coupon_paid_mask] = 0.0

        if obs_idx < n_obs - 1:
            autocall_mask = active & (s_obs >= autocall_trigger)
            discounted_redemption[autocall_mask] += df * notional
            autocall_counts[obs_idx] += float(np.sum(autocall_mask))
            alive[autocall_mask] = False
        else:
            autocall_mask = active & (s_obs >= autocall_trigger)
            discounted_redemption[autocall_mask] += df * notional
            autocall_counts[obs_idx] += float(np.sum(autocall_mask))

            non_autocall_active = active & (~autocall_mask)
            safe_mask = non_autocall_active & (~knocked_in)
            discounted_redemption[safe_mask] += df * notional

            loss_mask = non_autocall_active & knocked_in
            discounted_redemption[loss_mask] += df * notional * (s_obs[loss_mask] / strike)
            alive[:] = False

    coupon_pv = float(np.mean(discounted_coupons))
    redemption_pv = float(np.mean(discounted_redemption))
    total_price = coupon_pv + redemption_pv
    prob_autocall_total = float(np.sum(autocall_counts) / n_paths)
    prob_knock_in = float(np.mean(knocked_in))

    return {
        "price": total_price,
        "coupon_pv": coupon_pv,
        "redemption_pv": redemption_pv,
        "autocall_prob": prob_autocall_total,
        "knock_in_prob": prob_knock_in,
    }


def main() -> None:
    spot = 100.0
    strike = 100.0
    rate = 0.03
    div_yield = 0.015
    notional = 1000.0
    obs_dates = [0.5, 1.0, 1.5, 2.0]
    autocall_levels = [100.0, 98.0, 96.0, 94.0]
    coupon_rate = 0.03  # 3% per semi-annual (6% p.a.)
    coupon_barrier = 80.0
    knock_in_barrier = 65.0
    base_vol = 0.22

    # 1. Flat Black-Scholes Model (skew = 0, curvature = 0)
    flat_res = simulate_autocallable(
        spot,
        strike,
        rate,
        div_yield,
        notional,
        obs_dates,
        autocall_levels,
        coupon_rate,
        coupon_barrier,
        knock_in_barrier,
        base_vol,
        skew=0.0,
        curvature=0.0,
        n_paths=50000,
        seed=42,
    )

    # 2. Local Volatility Model with Downside Skew (skew = 0.16, curvature = 0.05)
    skew_res = simulate_autocallable(
        spot,
        strike,
        rate,
        div_yield,
        notional,
        obs_dates,
        autocall_levels,
        coupon_rate,
        coupon_barrier,
        knock_in_barrier,
        base_vol,
        skew=0.16,
        curvature=0.05,
        n_paths=50000,
        seed=42,
    )

    print("=== Lab 3: Autocallable Valuation: Flat Vol vs Local Vol Skew ===")
    print(f"Flat Vol Note Price:               {flat_res['price']:.2f} USD")
    print(f"  Coupon PV:                       {flat_res['coupon_pv']:.2f} USD")
    print(f"  Redemption PV:                   {flat_res['redemption_pv']:.2f} USD")
    print(f"  Autocall Probability:            {flat_res['autocall_prob'] * 100.0:.2f}%")
    print(f"  Knock-In Barrier Breach Rate:    {flat_res['knock_in_prob'] * 100.0:.2f}%")
    print(f"\nLocal Vol Skew Note Price:         {skew_res['price']:.2f} USD")
    print(f"  Coupon PV:                       {skew_res['coupon_pv']:.2f} USD")
    print(f"  Redemption PV:                   {skew_res['redemption_pv']:.2f} USD")
    print(f"  Autocall Probability:            {skew_res['autocall_prob'] * 100.0:.2f}%")
    print(f"  Knock-In Barrier Breach Rate:    {skew_res['knock_in_prob'] * 100.0:.2f}%")
    print(f"\nModel Skew Value Impact:           {skew_res['price'] - flat_res['price']:.2f} USD")
    print(f"Knock-In Probability Increase:     +{(skew_res['knock_in_prob'] - flat_res['knock_in_prob']) * 100.0:.2f}%")


main()

"""Lab Project 1 · Worked Example: Multi-Period Autocallable Pricing & Dealer Hedging.

Demonstrates the complete quantitative pipeline on Seed 0 (SIMULATED):
1. Parametric local volatility surface calibration.
2. Phoenix autocallable Monte Carlo pricing with memory coupons and knock-in barriers.
3. Finite-difference Greeks (Delta, Gamma, Vega).
4. Dealer gamma exposure profile across spot levels and barrier cliff identification.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def eval_local_vol(
    spot: float,
    strike: float,
    time: float,
    base_vol: float,
    skew: float,
    curvature: float,
) -> float:
    """Evaluate parametric local volatility sigma(S, t)."""
    m = math.log(spot / strike)
    term = 1.0 / math.sqrt(1.0 + 0.5 * time)
    skew_effect = -skew * math.tanh(m)
    smile_effect = curvature * (m**2)
    vol = base_vol * term * (1.0 + skew_effect + smile_effect)
    return float(max(0.01, min(2.0, vol)))


def price_autocallable(
    params: dict[str, Any],
    n_paths: int = 3000,
    seed: int = 42,
) -> dict[str, Any]:
    """Price a multi-period Phoenix autocallable note by Monte Carlo under local volatility."""
    spot = float(params["spot"])
    strike = float(params["strike"])
    rate = float(params["rate"])
    div_yield = float(params["div_yield"])
    notional = float(params["notional"])
    obs_dates: list[float] = list(params["observation_dates"])
    autocall_levels: list[float] = list(params["autocall_levels"])
    coupon_rate = float(params["coupon_rate"])
    coupon_barrier = float(params["coupon_barrier"])
    memory_coupon = bool(params.get("memory_coupon", True))
    knock_in_barrier = float(params["knock_in_barrier"])
    barrier_type = str(params.get("barrier_type", "continuous"))
    base_vol = float(params["base_vol"])
    skew = float(params.get("skew", 0.15))
    curvature = float(params.get("curvature", 0.05))

    n_obs = len(obs_dates)
    maturity = obs_dates[-1]

    sub_steps_per_obs = 10
    total_steps = n_obs * sub_steps_per_obs
    dt = maturity / float(total_steps)

    obs_indices = [(i + 1) * sub_steps_per_obs for i in range(n_obs)]

    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n_paths, total_steps))

    paths = np.empty((n_paths, total_steps + 1), dtype=np.float64)
    paths[:, 0] = spot

    sqrt_dt = math.sqrt(dt)
    drift_coeff = rate - div_yield

    for step in range(total_steps):
        s_curr = paths[:, step]
        t_curr = step * dt

        m = np.log(s_curr / strike)
        term = 1.0 / np.sqrt(1.0 + 0.5 * t_curr)
        skew_term = -skew * np.tanh(m)
        smile_term = curvature * (m**2)
        vol = base_vol * term * (1.0 + skew_term + smile_term)
        vol = np.clip(vol, 0.01, 2.0)

        log_increment = (drift_coeff - 0.5 * (vol**2)) * dt + vol * sqrt_dt * z[:, step]
        paths[:, step + 1] = s_curr * np.exp(log_increment)

    if barrier_type == "continuous":
        min_spot = np.min(paths, axis=1)
        knocked_in = min_spot <= knock_in_barrier
    else:
        knocked_in = paths[:, -1] <= knock_in_barrier

    alive = np.ones(n_paths, dtype=bool)
    discounted_coupons = np.zeros(n_paths, dtype=np.float64)
    discounted_redemption = np.zeros(n_paths, dtype=np.float64)
    autocall_counts = np.zeros(n_obs, dtype=np.float64)
    termination_times = np.full(n_paths, maturity, dtype=np.float64)
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
        if memory_coupon:
            discounted_coupons[coupon_paid_mask] += df * unpaid_coupons[coupon_paid_mask]
            unpaid_coupons[coupon_paid_mask] = 0.0
        else:
            discounted_coupons[coupon_paid_mask] += df * (coupon_rate * notional)
            unpaid_coupons[active] = 0.0

        if obs_idx < n_obs - 1:
            autocall_mask = active & (s_obs >= autocall_trigger)
            discounted_redemption[autocall_mask] += df * notional
            autocall_counts[obs_idx] += float(np.sum(autocall_mask))
            termination_times[autocall_mask] = t_obs
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
    autocall_probs = [float(c / n_paths) for c in autocall_counts]
    knock_in_prob = float(np.mean(knocked_in))
    expected_tenor = float(np.mean(termination_times))

    return {
        "price": total_price,
        "coupon_pv": coupon_pv,
        "redemption_pv": redemption_pv,
        "autocall_probs": autocall_probs,
        "knock_in_prob": knock_in_prob,
        "expected_tenor": expected_tenor,
    }


def compute_autocallable_greeks(
    params: dict[str, Any],
    spot_bump_pct: float = 0.01,
    vol_bump: float = 0.01,
    n_paths: int = 3000,
    seed: int = 42,
) -> dict[str, float]:
    """Compute Delta, Gamma, and Vega using common random numbers (CRN)."""
    spot = float(params["spot"])
    base_vol = float(params["base_vol"])

    h = spot * spot_bump_pct
    params_up = dict(params, spot=spot + h)
    params_down = dict(params, spot=spot - h)
    params_vol_up = dict(params, base_vol=base_vol + vol_bump)

    p0 = price_autocallable(params, n_paths=n_paths, seed=seed)["price"]
    p_up = price_autocallable(params_up, n_paths=n_paths, seed=seed)["price"]
    p_down = price_autocallable(params_down, n_paths=n_paths, seed=seed)["price"]
    p_vol = price_autocallable(params_vol_up, n_paths=n_paths, seed=seed)["price"]

    delta = (p_up - p_down) / (2.0 * h)
    gamma = (p_up - 2.0 * p0 + p_down) / (h**2)
    vega = (p_vol - p0) / vol_bump

    return {
        "delta": float(delta),
        "gamma": float(gamma),
        "vega": float(vega),
    }


def analyze_dealer_hedging_profile(
    params: dict[str, Any],
    spot_grid: list[float],
    n_paths: int = 1500,
    seed: int = 42,
) -> list[dict[str, float]]:
    """Evaluate note pricing and dealer hedging profile across spot levels."""
    notional = float(params["notional"])
    profile: list[dict[str, float]] = []

    for s in spot_grid:
        p_eval = dict(params, spot=s)
        h = max(0.5, s * 0.01)

        p0 = price_autocallable(p_eval, n_paths=n_paths, seed=seed)["price"]
        p_up = price_autocallable(dict(p_eval, spot=s + h), n_paths=n_paths, seed=seed)["price"]
        p_down = price_autocallable(dict(p_eval, spot=s - h), n_paths=n_paths, seed=seed)["price"]

        client_delta = (p_up - p_down) / (2.0 * h)
        client_gamma = (p_up - 2.0 * p0 + p_down) / (h**2)

        dealer_delta = -client_delta
        dealer_gamma = -client_gamma
        dealer_gamma_exposure = dealer_gamma * s * (notional / s)

        profile.append(
            {
                "spot": float(s),
                "note_price": float(p0),
                "delta": float(client_delta),
                "gamma": float(client_gamma),
                "dealer_delta": float(dealer_delta),
                "dealer_gamma": float(dealer_gamma),
                "dealer_gamma_exposure": float(dealer_gamma_exposure),
            }
        )

    return profile


def simulate_hedging_pnl_impact(
    params: dict[str, Any],
    spot_shock_pct: float,
    rebalancing_friction_bps: float,
) -> dict[str, float]:
    """Calculate dealer delta rebalancing flow and transaction cost friction under a spot move."""
    spot = float(params["spot"])
    notional = float(params["notional"])
    greeks_0 = compute_autocallable_greeks(params, n_paths=2000, seed=42)

    s_shocked = spot * (1.0 + spot_shock_pct)
    greeks_shocked = compute_autocallable_greeks(dict(params, spot=s_shocked), n_paths=2000, seed=42)

    dealer_delta_0 = -greeks_0["delta"]
    dealer_delta_shocked = -greeks_shocked["delta"]

    delta_shares_change = (dealer_delta_shocked - dealer_delta_0) * (notional / spot)
    trading_volume_usd = abs(delta_shares_change) * s_shocked
    rebalance_friction = trading_volume_usd * (rebalancing_friction_bps / 10000.0)

    delta_s = s_shocked - spot
    gamma_pnl = 0.5 * (-greeks_0["gamma"]) * (delta_s**2) * (notional / spot)

    return {
        "spot_initial": spot,
        "spot_shocked": s_shocked,
        "delta_initial": dealer_delta_0,
        "delta_shocked": dealer_delta_shocked,
        "rebalance_shares": float(delta_shares_change),
        "trading_volume_usd": float(trading_volume_usd),
        "rebalance_friction": float(rebalance_friction),
        "gamma_pnl": float(gamma_pnl),
    }


def main() -> None:
    print("=== DV6 Project Rung 1: Worked Example (Seed 0) ===")
    instance: dict[str, Any] = {
        "spot": 107.67,
        "strike": 107.67,
        "rate": 0.0427,
        "div_yield": 0.0184,
        "notional": 1000.0,
        "observation_dates": [0.5, 1.0, 1.5, 2.0],
        "autocall_levels": [107.67, 107.13, 106.59, 106.05],
        "coupon_rate": 0.0327,
        "coupon_barrier": 82.93,
        "memory_coupon": True,
        "knock_in_barrier": 71.35,
        "barrier_type": "continuous",
        "base_vol": 0.2043,
        "skew": 0.1381,
        "curvature": 0.0533,
        "n_steps": 40,
        "spot_grid": [59.22, 66.76, 73.22, 80.75, 91.52, 102.29, 107.67, 113.05, 123.82, 134.59],
    }

    spot = float(instance["spot"])
    strike = float(instance["strike"])
    rate = float(instance["rate"])
    div_yield = float(instance["div_yield"])
    notional = float(instance["notional"])
    base_vol = float(instance["base_vol"])
    skew = float(instance["skew"])
    curvature = float(instance["curvature"])
    knock_in_b = float(instance["knock_in_barrier"])

    print("Contract Specification (Seed 0):")
    print(f"  Spot: ${spot:.2f} | Strike: ${strike:.2f} | Notional: ${notional:.2f}")
    print(f"  Risk-Free Rate: {rate * 100.0:.2f}% | Dividend Yield: {div_yield * 100.0:.2f}%")
    print(f"  Knock-In Barrier: ${knock_in_b:.2f} ({knock_in_b / spot * 100.0:.1f}% of spot)")
    cp_rate = instance["coupon_rate"] * 100.0
    print(f"  Coupon Rate: {cp_rate:.2f}% semi-annual | Coupon Barrier: ${instance['coupon_barrier']:.2f}")
    print(f"  Autocall Schedule: {instance['observation_dates']} yrs @ levels {instance['autocall_levels']}")

    # 1. Local Volatility Evaluation
    vol_atm = eval_local_vol(spot, strike, 0.5, base_vol, skew, curvature)
    vol_down = eval_local_vol(spot * 0.85, strike, 0.5, base_vol, skew, curvature)
    vol_up = eval_local_vol(spot * 1.15, strike, 0.5, base_vol, skew, curvature)
    print("\n1. Local Volatility Surface Check (t = 0.5 yr):")
    print(f"  ATM Vol (S={spot:.1f}):   {vol_atm * 100.0:.2f}%")
    print(f"  Downside Vol (85% S): {vol_down * 100.0:.2f}%")
    print(f"  Upside Vol (115% S):  {vol_up * 100.0:.2f}%")
    print(f"  Downside Skew Spread: +{(vol_down - vol_up) * 100.0:.2f}%")

    # 2. Monte Carlo Pricing
    price_res = price_autocallable(instance, n_paths=5000, seed=42)
    print("\n2. Phoenix Autocallable Pricing Results:")
    print(f"  Total Note Value:     ${price_res['price']:.2f} USD")
    print(f"  Coupon PV Component:  ${price_res['coupon_pv']:.2f} USD")
    print(f"  Redemption PV:        ${price_res['redemption_pv']:.2f} USD")
    print(f"  Knock-In Breach Prob: {price_res['knock_in_prob'] * 100.0:.2f}%")
    print(f"  Expected Tenor:       {price_res['expected_tenor']:.3f} years")
    for t, p in zip(instance["observation_dates"], price_res["autocall_probs"], strict=False):
        print(f"    Autocall Prob (t={t:.1f}y): {p * 100.0:.2f}%")

    # 3. Greek Sensitivities
    greeks = compute_autocallable_greeks(instance, n_paths=5000, seed=42)
    print("\n3. Client & Dealer Greek Sensitivities:")
    print(f"  Client Delta:         {greeks['delta']:.4f}")
    print(f"  Dealer Delta:         {-greeks['delta']:.4f}")
    print(f"  Client Gamma:         {greeks['gamma']:.6f}")
    print(f"  Dealer Gamma:         {-greeks['gamma']:.6f}")
    print(f"  Vega (per 1% vol):    ${greeks['vega'] * 0.01:.2f} USD")

    # 4. Dealer Gamma Profile Across Spot Grid
    profile = analyze_dealer_hedging_profile(instance, instance["spot_grid"], n_paths=2000, seed=42)
    print("\n4. Dealer Gamma Exposure Profile Across Spot:")
    print(f"  {'Spot':>7} | {'Note Price':>10} | {'Client Delta':>12} | {'Dealer Gamma':>12} | {'Dealer GEX ($)':>14}")
    print(f"  {'-' * 7}-+-{'-' * 10}-+-{'-' * 12}-+-{'-' * 12}-+-{'-' * 14}")
    for row in profile:
        s, np_val, d = row["spot"], row["note_price"], row["delta"]
        dg, gex = row["dealer_gamma"], row["dealer_gamma_exposure"]
        print(f"  {s:7.2f} | {np_val:10.2f} | {d:12.4f} | {dg:12.6f} | {gex:14.2f}")

    # 5. Stress Shock Rebalancing Impact
    shock = simulate_hedging_pnl_impact(instance, spot_shock_pct=-0.05, rebalancing_friction_bps=5.0)
    print("\n5. Dealer Rebalancing Flow Under -5% Market Selloff:")
    print(f"  Initial Spot:         ${shock['spot_initial']:.2f} -> Shocked Spot: ${shock['spot_shocked']:.2f}")
    print(f"  Dealer Delta Move:    {shock['delta_initial']:.4f} -> {shock['delta_shocked']:.4f}")
    print(f"  Rebalancing Shares:   {shock['rebalance_shares']:.2f} shares")
    print(f"  Rebalancing Turnover: ${shock['trading_volume_usd']:,.2f} USD")
    print(f"  Execution Friction:   ${shock['rebalance_friction']:.2f} USD")
    print(f"  Gamma PnL Impact:     ${shock['gamma_pnl']:.2f} USD")


main()

"""Mutant 3: Flips dealer delta and gamma signs to match client position rather than dealer short position."""

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
    if spot <= 0.0 or strike <= 0.0 or time < 0.0 or base_vol <= 0.0 or curvature < 0.0:
        raise ValueError("Invalid parameters")
    m = math.log(spot / strike)
    term = 1.0 / math.sqrt(1.0 + 0.5 * time)
    vol = base_vol * term * (1.0 - skew * math.tanh(m) + curvature * (m**2))
    return float(max(0.01, min(2.0, vol)))


def _validate_params(params: dict[str, Any]) -> None:
    spot = float(params.get("spot", 0.0))
    strike = float(params.get("strike", 0.0))
    notional = float(params.get("notional", 0.0))
    base_vol = float(params.get("base_vol", 0.0))
    obs_dates = list(params.get("observation_dates", []))
    autocall_levels = list(params.get("autocall_levels", []))
    if spot <= 0.0 or strike <= 0.0 or notional <= 0.0 or base_vol <= 0.0:
        raise ValueError("Invalid parameters")
    if not obs_dates or len(obs_dates) != len(autocall_levels):
        raise ValueError("Schedule mismatch")


def price_autocallable(
    params: dict[str, Any],
    n_paths: int = 3000,
    seed: int = 42,
) -> dict[str, Any]:
    _validate_params(params)
    spot = float(params["spot"])
    strike = float(params["strike"])
    rate = float(params["rate"])
    div_yield = float(params["div_yield"])
    notional = float(params["notional"])
    obs_dates = list(params["observation_dates"])
    autocall_levels = list(params["autocall_levels"])
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
        vol = base_vol * term * (1.0 - skew * np.tanh(m) + curvature * (m**2))
        vol = np.clip(vol, 0.01, 2.0)
        paths[:, step + 1] = s_curr * np.exp((drift_coeff - 0.5 * (vol**2)) * dt + vol * sqrt_dt * z[:, step])

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
    return {
        "price": coupon_pv + redemption_pv,
        "coupon_pv": coupon_pv,
        "redemption_pv": redemption_pv,
        "autocall_probs": [float(c / n_paths) for c in autocall_counts],
        "knock_in_prob": float(np.mean(knocked_in)),
        "expected_tenor": float(np.mean(termination_times)),
    }


def compute_autocallable_greeks(
    params: dict[str, Any],
    spot_bump_pct: float = 0.01,
    vol_bump: float = 0.01,
    n_paths: int = 3000,
    seed: int = 42,
) -> dict[str, float]:
    spot = float(params["spot"])
    base_vol = float(params["base_vol"])
    h = spot * spot_bump_pct
    p0 = price_autocallable(params, n_paths=n_paths, seed=seed)["price"]
    p_up = price_autocallable(dict(params, spot=spot + h), n_paths=n_paths, seed=seed)["price"]
    p_down = price_autocallable(dict(params, spot=spot - h), n_paths=n_paths, seed=seed)["price"]
    p_vol = price_autocallable(dict(params, base_vol=base_vol + vol_bump), n_paths=n_paths, seed=seed)["price"]
    return {
        "delta": float((p_up - p_down) / (2.0 * h)),
        "gamma": float((p_up - 2.0 * p0 + p_down) / (h**2)),
        "vega": float((p_vol - p0) / vol_bump),
    }


def analyze_dealer_hedging_profile(
    params: dict[str, Any],
    spot_grid: list[float],
    n_paths: int = 1500,
    seed: int = 42,
) -> list[dict[str, float]]:
    notional = float(params["notional"])
    profile: list[dict[str, float]] = []
    for s in spot_grid:
        p_eval = dict(params, spot=s)
        h = max(0.5, s * 0.01)
        p0 = price_autocallable(p_eval, n_paths=n_paths, seed=seed)["price"]
        p_up = price_autocallable(dict(p_eval, spot=s + h), n_paths=n_paths, seed=seed)["price"]
        p_down = price_autocallable(dict(p_eval, spot=s - h), n_paths=n_paths, seed=seed)["price"]
        cd = (p_up - p_down) / (2.0 * h)
        cg = (p_up - 2.0 * p0 + p_down) / (h**2)
        # DEFECT: Fails to negate Greeks for dealer, assuming dealer is long the note
        profile.append(
            {
                "spot": float(s),
                "note_price": float(p0),
                "delta": float(cd),
                "gamma": float(cg),
                "dealer_delta": float(cd),
                "dealer_gamma": float(cg),
                "dealer_gamma_exposure": float(cg * s * (notional / s)),
            }
        )
    return profile


def simulate_hedging_pnl_impact(
    params: dict[str, Any],
    spot_shock_pct: float,
    rebalancing_friction_bps: float,
) -> dict[str, float]:
    spot = float(params["spot"])
    notional = float(params["notional"])
    g0 = compute_autocallable_greeks(params, n_paths=2000, seed=42)
    s_shocked = spot * (1.0 + spot_shock_pct)
    g1 = compute_autocallable_greeks(dict(params, spot=s_shocked), n_paths=2000, seed=42)
    d_shares = (g1["delta"] - g0["delta"]) * (notional / spot)
    vol_usd = abs(d_shares) * s_shocked
    fric = vol_usd * (rebalancing_friction_bps / 10000.0)
    delta_s = s_shocked - spot
    pnl = 0.5 * (g0["gamma"]) * (delta_s**2) * (notional / spot)
    return {
        "spot_initial": spot,
        "spot_shocked": s_shocked,
        "delta_initial": g0["delta"],
        "delta_shocked": g1["delta"],
        "rebalance_shares": float(d_shares),
        "trading_volume_usd": float(vol_usd),
        "rebalance_friction": float(fric),
        "gamma_pnl": float(pnl),
    }

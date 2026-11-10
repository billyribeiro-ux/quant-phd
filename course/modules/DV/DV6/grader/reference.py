"""Reference implementation for DV6: Exotics, Structured Products & Dealer Hedging.

Provides institutional-grade pricing and risk analytics for autocallable structured notes:
1. Parametric local volatility surface evaluation.
2. Monte Carlo path simulation under continuous local volatility.
3. Multi-period Phoenix autocallable pricing with memory coupons and knock-in barriers.
4. Finite-difference Greek computation (Delta, Gamma, Vega) using common random numbers (CRN).
5. Dealer gamma positioning and hedging flow impact across spot levels.
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
    if spot <= 0.0:
        raise ValueError(f"Spot price must be strictly positive, got {spot}")
    if strike <= 0.0:
        raise ValueError(f"Strike price must be strictly positive, got {strike}")
    if time < 0.0:
        raise ValueError(f"Time to maturity must be non-negative, got {time}")
    if base_vol <= 0.0:
        raise ValueError(f"Base volatility must be strictly positive, got {base_vol}")
    if curvature < 0.0:
        raise ValueError(f"Curvature parameter must be non-negative, got {curvature}")

    # Log-moneyness relative to strike
    m = math.log(spot / strike)
    # Term structure decay
    term = 1.0 / math.sqrt(1.0 + 0.5 * time)
    # Skew and smile curvature
    skew_effect = -skew * math.tanh(m)
    smile_effect = curvature * (m**2)
    vol = base_vol * term * (1.0 + skew_effect + smile_effect)
    # Clamp to realistic volatility bounds [1.0%, 200.0%]
    return float(max(0.01, min(2.0, vol)))


def _validate_params(params: dict[str, Any]) -> None:
    """Validate structure and bounds of autocallable contract parameters."""
    spot = float(params.get("spot", 0.0))
    strike = float(params.get("strike", 0.0))
    rate = float(params.get("rate", 0.0))
    div_yield = float(params.get("div_yield", 0.0))
    notional = float(params.get("notional", 0.0))
    obs_dates: list[float] = list(params.get("observation_dates", []))
    autocall_levels: list[float] = list(params.get("autocall_levels", []))
    coupon_rate = float(params.get("coupon_rate", 0.0))
    coupon_barrier = float(params.get("coupon_barrier", 0.0))
    knock_in_barrier = float(params.get("knock_in_barrier", 0.0))
    base_vol = float(params.get("base_vol", 0.0))

    if spot <= 0.0:
        raise ValueError(f"Spot must be strictly positive, got {spot}")
    if strike <= 0.0:
        raise ValueError(f"Strike must be strictly positive, got {strike}")
    if notional <= 0.0:
        raise ValueError(f"Notional must be strictly positive, got {notional}")
    if base_vol <= 0.0:
        raise ValueError(f"Base volatility must be strictly positive, got {base_vol}")
    if rate < -0.05 or rate > 0.50:
        raise ValueError(f"Interest rate out of reasonable bounds, got {rate}")
    if div_yield < 0.0 or div_yield > 0.50:
        raise ValueError(f"Dividend yield out of reasonable bounds, got {div_yield}")
    if not obs_dates:
        raise ValueError("Observation dates list cannot be empty")
    if len(obs_dates) != len(autocall_levels):
        raise ValueError(
            f"Observation dates ({len(obs_dates)}) and autocall levels ({len(autocall_levels)}) must have equal length"
        )
    if any(obs_dates[i] >= obs_dates[i + 1] for i in range(len(obs_dates) - 1)):
        raise ValueError("Observation dates must be strictly strictly increasing")
    if any(t <= 0.0 for t in obs_dates):
        raise ValueError("Observation dates must be strictly positive")
    if coupon_rate < 0.0:
        raise ValueError(f"Coupon rate cannot be negative, got {coupon_rate}")
    if coupon_barrier <= 0.0:
        raise ValueError(f"Coupon barrier must be strictly positive, got {coupon_barrier}")
    if knock_in_barrier <= 0.0:
        raise ValueError(f"Knock-in barrier must be strictly positive, got {knock_in_barrier}")


def price_autocallable(
    params: dict[str, Any],
    n_paths: int = 3000,
    seed: int = 42,
) -> dict[str, Any]:
    """Price a multi-period Phoenix autocallable note by Monte Carlo under local volatility."""
    _validate_params(params)
    if n_paths <= 0:
        raise ValueError(f"Number of paths must be strictly positive, got {n_paths}")

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

    # Grid discretization: at least 10 sub-steps per observation period
    sub_steps_per_obs = 10
    total_steps = n_obs * sub_steps_per_obs
    dt = maturity / float(total_steps)

    # Observation step indices
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

        # Vectorized local volatility evaluation
        m = np.log(s_curr / strike)
        term = 1.0 / np.sqrt(1.0 + 0.5 * t_curr)
        skew_term = -skew * np.tanh(m)
        smile_term = curvature * (m**2)
        vol = base_vol * term * (1.0 + skew_term + smile_term)
        vol = np.clip(vol, 0.01, 2.0)

        # Log-Euler step
        log_increment = (drift_coeff - 0.5 * (vol**2)) * dt + vol * sqrt_dt * z[:, step]
        paths[:, step + 1] = s_curr * np.exp(log_increment)

    # Knock-in barrier tracking
    if barrier_type == "continuous":
        # Check minimum along full path
        min_spot = np.min(paths, axis=1)
        knocked_in = min_spot <= knock_in_barrier
    elif barrier_type == "maturity_only":
        knocked_in = paths[:, -1] <= knock_in_barrier
    else:
        raise ValueError(f"Unknown barrier_type: {barrier_type}")

    # Track lifecycle states
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

        # Accumulate period coupon
        active = alive
        unpaid_coupons[active] += coupon_rate * notional

        # Coupon payment condition
        coupon_paid_mask = active & (s_obs >= coupon_barrier)
        if memory_coupon:
            discounted_coupons[coupon_paid_mask] += df * unpaid_coupons[coupon_paid_mask]
            unpaid_coupons[coupon_paid_mask] = 0.0
        else:
            discounted_coupons[coupon_paid_mask] += df * (coupon_rate * notional)
            unpaid_coupons[active] = 0.0

        # Check early autocall redemption
        if obs_idx < n_obs - 1:
            autocall_mask = active & (s_obs >= autocall_trigger)
            discounted_redemption[autocall_mask] += df * notional
            autocall_counts[obs_idx] += float(np.sum(autocall_mask))
            termination_times[autocall_mask] = t_obs
            alive[autocall_mask] = False
        else:
            # Final maturity settlement
            autocall_mask = active & (s_obs >= autocall_trigger)
            discounted_redemption[autocall_mask] += df * notional
            autocall_counts[obs_idx] += float(np.sum(autocall_mask))

            # Not autocalled: check knock-in status
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

    # Shares of underlying delta to rebalance per note
    delta_shares_change = (dealer_delta_shocked - dealer_delta_0) * (notional / spot)
    trading_volume_usd = abs(delta_shares_change) * s_shocked
    rebalance_friction = trading_volume_usd * (rebalancing_friction_bps / 10000.0)

    # Gamma PnL contribution: 0.5 * Dealer_Gamma * (Delta S)^2
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

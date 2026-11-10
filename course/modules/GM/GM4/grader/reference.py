"""Reference solution for Atlas A20: macro trade-construction engine (atlas.strategy)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class MacroView:
    """Specification of a macroeconomic view."""

    view_id: str
    asset_ids: list[str]
    view_type: str  # "directional", "curve_steepener", "curve_flattener", "relative_value", "volatility"
    expected_move_bps: float
    confidence: float  # (0, 1]
    horizon_days: int  # > 0

    def __post_init__(self) -> None:
        if not self.view_id:
            msg = "view_id cannot be empty"
            raise ValueError(msg)
        if not self.asset_ids:
            msg = "asset_ids cannot be empty"
            raise ValueError(msg)
        valid_types = {
            "directional",
            "curve_steepener",
            "curve_flattener",
            "relative_value",
            "volatility",
        }
        if self.view_type not in valid_types:
            msg = f"Invalid view_type: {self.view_type}"
            raise ValueError(msg)
        if not (0.0 < self.confidence <= 1.0):
            msg = "confidence must be in (0, 1]"
            raise ValueError(msg)
        if self.horizon_days <= 0:
            msg = "horizon_days must be positive"
            raise ValueError(msg)


def compute_dv01_hedge_ratio(dv01_leg1: float, dv01_leg2: float) -> float:
    """Calculate duration-neutral hedge ratio: units of leg 2 per unit of leg 1."""
    if not isinstance(dv01_leg1, (int, float)) or not isinstance(dv01_leg2, (int, float)):
        msg = "DV01 inputs must be numeric"
        raise TypeError(msg)
    if dv01_leg1 <= 0.0 or dv01_leg2 <= 0.0:
        msg = "DV01 values must be strictly positive"
        raise ValueError(msg)
    return float(dv01_leg1 / dv01_leg2)


def construct_curve_spread(
    notional_leg1: float,
    dv01_leg1: float,
    dv01_leg2: float,
    direction: str = "steepener",
) -> tuple[float, float]:
    """Calculate signed notional positions (N1, N2) for a duration-neutral curve trade."""
    if notional_leg1 <= 0.0:
        msg = "notional_leg1 must be strictly positive"
        raise ValueError(msg)
    if dv01_leg1 <= 0.0 or dv01_leg2 <= 0.0:
        msg = "DV01 values must be strictly positive"
        raise ValueError(msg)
    if direction not in ("steepener", "flattener"):
        msg = f"Invalid curve direction: {direction}"
        raise ValueError(msg)

    ratio = compute_dv01_hedge_ratio(dv01_leg1, dv01_leg2)
    hedge_notional = notional_leg1 * ratio

    if direction == "steepener":
        # Steepener: Long front-end (leg1), Short back-end (leg2)
        return float(notional_leg1), float(-hedge_notional)
    # Flattener: Short front-end (leg1), Long back-end (leg2)
    return float(-notional_leg1), float(hedge_notional)


def evaluate_carry_and_rolldown(
    spot_yield: float,
    duration: float,
    roll_down_bps: float,
    repo_rate: float,
    horizon_years: float,
) -> dict[str, float]:
    """Compute gross carry, roll-down gain, repo financing drag, and net carry."""
    if duration <= 0.0 or horizon_years <= 0.0:
        msg = "Duration and horizon_years must be strictly positive"
        raise ValueError(msg)

    gross_carry = spot_yield * horizon_years
    roll_down = (roll_down_bps * 1e-4) * duration * horizon_years
    repo_drag = repo_rate * horizon_years
    net_carry = gross_carry + roll_down - repo_drag
    net_carry_bps = net_carry * 10_000.0

    return {
        "gross_carry": float(gross_carry),
        "roll_down": float(roll_down),
        "repo_drag": float(repo_drag),
        "net_carry": float(net_carry),
        "net_carry_bps": float(net_carry_bps),
    }


def _bsm_d1_d2(s: float, k: float, v: float, t: float, r: float) -> tuple[float, float]:
    """Helper for d1 and d2."""
    sqt = v * math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * v * v) * t) / sqt
    d2 = d1 - sqt
    return d1, d2


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def compute_expression_convexity(
    spot: float,
    strikes: np.ndarray,
    vols: np.ndarray,
    expiry: float,
    rate: float,
    weights: np.ndarray,
    is_call: np.ndarray,
) -> dict[str, float]:
    """Compute aggregate Greeks (delta, gamma, vega, theta) for an options/delta-one portfolio."""
    if spot <= 0.0 or expiry <= 0.0:
        msg = "spot and expiry must be strictly positive"
        raise ValueError(msg)
    n = len(strikes)
    if not (len(vols) == n and len(weights) == n and len(is_call) == n):
        msg = "Mismatched dimensions in option vectors"
        raise ValueError(msg)

    net_delta = 0.0
    net_gamma = 0.0
    net_vega = 0.0
    net_theta = 0.0

    for i in range(n):
        k = float(strikes[i])
        v = float(vols[i])
        w = float(weights[i])
        call = bool(is_call[i])

        if k <= 0.0 or v <= 0.0:
            msg = "Strike and vol must be positive"
            raise ValueError(msg)

        d1, d2 = _bsm_d1_d2(spot, k, v, expiry, rate)
        pdf_d1 = _norm_pdf(d1)
        cdf_d1 = _norm_cdf(d1)
        cdf_d2 = _norm_cdf(d2)

        if call:
            delta = cdf_d1
            theta = -(spot * pdf_d1 * v) / (2.0 * math.sqrt(expiry)) - rate * k * math.exp(-rate * expiry) * cdf_d2
        else:
            delta = cdf_d1 - 1.0
            theta = -(spot * pdf_d1 * v) / (2.0 * math.sqrt(expiry)) + rate * k * math.exp(-rate * expiry) * _norm_cdf(
                -d2
            )

        gamma = pdf_d1 / (spot * v * math.sqrt(expiry))
        vega = spot * pdf_d1 * math.sqrt(expiry)

        net_delta += w * delta
        net_gamma += w * gamma
        net_vega += w * vega
        net_theta += w * theta

    convexity_score = float(net_gamma * (spot**2) / 100.0)

    return {
        "delta": float(net_delta),
        "gamma": float(net_gamma),
        "vega": float(net_vega),
        "theta": float(net_theta),
        "convexity_score": convexity_score,
    }


def compute_asymmetry_ratio(pnl_distribution: np.ndarray) -> float:
    """Compute ratio of expected upside to expected downside from a scenario P&L distribution."""
    if pnl_distribution.ndim != 1 or len(pnl_distribution) == 0:
        msg = "pnl_distribution must be non-empty 1D array"
        raise ValueError(msg)

    upside = np.maximum(0.0, pnl_distribution)
    downside = np.maximum(0.0, -pnl_distribution)

    mu_up = float(np.mean(upside))
    mu_down = float(np.mean(downside))

    if mu_down > 1e-12:
        return float(mu_up / mu_down)
    if mu_up > 1e-12:
        return float("inf")
    return 0.0


def size_trade_fractional_kelly(
    expected_excess_return: float,
    variance: float,
    fraction: float = 0.25,
    max_leverage: float = 5.0,
) -> float:
    """Calculate fractional Kelly portfolio weight subject to maximum leverage cap."""
    if variance <= 0.0:
        msg = "variance must be strictly positive"
        raise ValueError(msg)
    if not (0.0 < fraction <= 1.0):
        msg = "fraction must be in (0, 1.0]"
        raise ValueError(msg)
    if max_leverage <= 0.0:
        msg = "max_leverage must be strictly positive"
        raise ValueError(msg)

    unconstrained = expected_excess_return / variance
    sized = fraction * unconstrained

    if sized > max_leverage:
        return float(max_leverage)
    if sized < -max_leverage:
        return float(-max_leverage)
    return float(sized)


def _bsm_price(s: float, k: float, v: float, t: float, r: float, is_call: bool) -> float:
    """Analytical BSM price."""
    if t <= 1e-6:
        return max(0.0, s - k) if is_call else max(0.0, k - s)
    d1, d2 = _bsm_d1_d2(s, k, v, t, r)
    if is_call:
        return s * _norm_cdf(d1) - k * math.exp(-r * t) * _norm_cdf(d2)
    return k * math.exp(-r * t) * _norm_cdf(-d2) - s * _norm_cdf(-d1)


def scenario_pnl_grid(
    spot_shocks: np.ndarray,
    vol_shocks: np.ndarray,
    base_spot: float,
    base_vols: np.ndarray,
    strikes: np.ndarray,
    expiry: float,
    rate: float,
    weights: np.ndarray,
    is_call: np.ndarray,
    holding_period: float = 0.0,
) -> np.ndarray:
    """Compute 2D grid of scenario P&L across spot shocks (columns) and vol shocks (rows)."""
    if base_spot <= 0.0 or expiry <= 0.0:
        msg = "base_spot and expiry must be positive"
        raise ValueError(msg)

    n_options = len(strikes)
    # Compute initial portfolio value
    v0 = 0.0
    for i in range(n_options):
        k = float(strikes[i])
        v = float(base_vols[i])
        w = float(weights[i])
        call = bool(is_call[i])
        v0 += w * _bsm_price(base_spot, k, v, expiry, rate, call)

    grid = np.zeros((len(vol_shocks), len(spot_shocks)), dtype=np.float64)
    remaining_t = max(1e-6, expiry - holding_period)

    for j, dv in enumerate(vol_shocks):
        for k_idx, ds in enumerate(spot_shocks):
            s_scen = base_spot * (1.0 + float(ds))
            v_scen = 0.0
            for i in range(n_options):
                k = float(strikes[i])
                vol_scen = max(0.01, float(base_vols[i]) + float(dv))
                w = float(weights[i])
                call = bool(is_call[i])
                v_scen += w * _bsm_price(s_scen, k, vol_scen, remaining_t, rate, call)
            grid[j, k_idx] = v_scen - v0

    return grid


class MacroTradeEngine:
    """End-to-end macro trade construction engine (Milestone A20)."""

    def __init__(self, risk_free_rate: float = 0.045) -> None:
        self.risk_free_rate = float(risk_free_rate)

    def construct_trade(
        self,
        view: MacroView,
        leg1_params: dict[str, float],
        leg2_params: dict[str, float] | None = None,
        sizing_budget: float = 1_000_000.0,
        kelly_fraction: float = 0.25,
        max_leverage: float = 4.0,
    ) -> dict[str, Any]:
        """Construct full trade package: sizing, carry attribution, Greeks, asymmetry, and scenario P&L."""
        if leg2_params is not None and "dv01" in leg1_params and "dv01" in leg2_params:
            # Curve / relative value trade
            dv01_1 = leg1_params["dv01"]
            dv01_2 = leg2_params["dv01"]
            direction = "steepener" if view.view_type == "curve_steepener" else "flattener"
            n1, n2 = construct_curve_spread(sizing_budget, dv01_1, dv01_2, direction=direction)

            # Carry for leg 1 and leg 2
            carry_1 = evaluate_carry_and_rolldown(
                leg1_params["spot_yield"],
                leg1_params["duration"],
                leg1_params.get("roll_down_bps", 0.0),
                self.risk_free_rate,
                view.horizon_days / 365.0,
            )
            carry_2 = evaluate_carry_and_rolldown(
                leg2_params["spot_yield"],
                leg2_params["duration"],
                leg2_params.get("roll_down_bps", 0.0),
                self.risk_free_rate,
                view.horizon_days / 365.0,
            )

            # Net carry: weighted by signed notional
            total_notional = abs(n1) + abs(n2)
            w1 = n1 / total_notional
            w2 = n2 / total_notional
            net_carry_bps = w1 * carry_1["net_carry_bps"] + w2 * carry_2["net_carry_bps"]

            # Kelly sizing based on view expected return and duration risk
            expected_return = (view.expected_move_bps * 1e-4) * view.confidence
            est_vol = 0.08
            kelly_w = size_trade_fractional_kelly(
                expected_return, est_vol**2, fraction=kelly_fraction, max_leverage=max_leverage
            )

            return {
                "view_id": view.view_id,
                "trade_type": view.view_type,
                "leg1_notional": n1,
                "leg2_notional": n2,
                "hedge_ratio": compute_dv01_hedge_ratio(dv01_1, dv01_2),
                "net_dv01": n1 * dv01_1 * 1e-4 + n2 * dv01_2 * 1e-4,
                "net_carry_bps": net_carry_bps,
                "kelly_weight": kelly_w,
                "allocated_capital": sizing_budget * abs(kelly_w),
            }

        # Directional or outright trade
        return {
            "view_id": view.view_id,
            "trade_type": view.view_type,
            "leg1_notional": sizing_budget,
            "kelly_weight": 1.0,
            "allocated_capital": sizing_budget,
        }

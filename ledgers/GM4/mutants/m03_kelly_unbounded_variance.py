"""Mutant 3: fails to clamp fractional Kelly sizing to maximum leverage bound."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class MacroView:
    view_id: str
    asset_ids: list[str]
    view_type: str
    expected_move_bps: float
    confidence: float
    horizon_days: int


def compute_dv01_hedge_ratio(dv01_leg1: float, dv01_leg2: float) -> float:
    if not isinstance(dv01_leg1, (int, float)) or not isinstance(dv01_leg2, (int, float)):
        raise TypeError
    if dv01_leg1 <= 0.0 or dv01_leg2 <= 0.0:
        raise ValueError
    return float(dv01_leg1 / dv01_leg2)


def construct_curve_spread(
    notional_leg1: float,
    dv01_leg1: float,
    dv01_leg2: float,
    direction: str = "steepener",
) -> tuple[float, float]:
    if notional_leg1 <= 0.0 or dv01_leg1 <= 0.0 or dv01_leg2 <= 0.0:
        raise ValueError
    if direction not in ("steepener", "flattener"):
        raise ValueError
    ratio = compute_dv01_hedge_ratio(dv01_leg1, dv01_leg2)
    hedge_notional = notional_leg1 * ratio
    if direction == "steepener":
        return float(notional_leg1), float(-hedge_notional)
    return float(-notional_leg1), float(hedge_notional)


def evaluate_carry_and_rolldown(
    spot_yield: float,
    duration: float,
    roll_down_bps: float,
    repo_rate: float,
    horizon_years: float,
) -> dict[str, float]:
    if duration <= 0.0 or horizon_years <= 0.0:
        raise ValueError
    gross_carry = spot_yield * horizon_years
    roll_down = (roll_down_bps * 1e-4) * duration * horizon_years
    repo_drag = repo_rate * horizon_years
    net_carry = gross_carry + roll_down - repo_drag
    return {
        "gross_carry": float(gross_carry),
        "roll_down": float(roll_down),
        "repo_drag": float(repo_drag),
        "net_carry": float(net_carry),
        "net_carry_bps": float(net_carry * 10_000.0),
    }


def compute_expression_convexity(
    spot: float,
    strikes: np.ndarray,
    vols: np.ndarray,
    expiry: float,
    rate: float,
    weights: np.ndarray,
    is_call: np.ndarray,
) -> dict[str, float]:
    net_delta, net_gamma, net_vega, net_theta = 0.0, 0.0, 0.0, 0.0
    for i in range(len(strikes)):
        k, v, w = float(strikes[i]), float(vols[i]), float(weights[i])
        call = bool(is_call[i])
        sqt = v * math.sqrt(expiry)
        d1 = (math.log(spot / k) + (rate + 0.5 * v * v) * expiry) / sqt
        d2 = d1 - sqt
        pdf = math.exp(-0.5 * d1 * d1) / math.sqrt(2 * math.pi)
        cdf1 = 0.5 * (1 + math.erf(d1 / math.sqrt(2)))
        cdf2 = 0.5 * (1 + math.erf(d2 / math.sqrt(2)))
        delta = cdf1 if call else cdf1 - 1.0
        gamma = pdf / (spot * v * math.sqrt(expiry))
        vega = spot * pdf * math.sqrt(expiry)
        theta = (
            -(spot * pdf * v) / (2 * math.sqrt(expiry)) - rate * k * math.exp(-rate * expiry) * cdf2
            if call
            else -(spot * pdf * v) / (2 * math.sqrt(expiry))
            + rate * k * math.exp(-rate * expiry) * (0.5 * (1 + math.erf(-d2 / math.sqrt(2))))
        )
        net_delta += w * delta
        net_gamma += w * gamma
        net_vega += w * vega
        net_theta += w * theta
    return {
        "delta": net_delta,
        "gamma": net_gamma,
        "vega": net_vega,
        "theta": net_theta,
        "convexity_score": net_gamma * (spot**2) / 100.0,
    }


def compute_asymmetry_ratio(pnl_distribution: np.ndarray) -> float:
    if pnl_distribution.ndim != 1 or len(pnl_distribution) == 0:
        raise ValueError
    u = np.maximum(0.0, pnl_distribution)
    d = np.maximum(0.0, -pnl_distribution)
    mu_u, mu_d = float(np.mean(u)), float(np.mean(d))
    if mu_d > 1e-12:
        return mu_u / mu_d
    if mu_u > 1e-12:
        return float("inf")
    return 0.0


def size_trade_fractional_kelly(
    expected_excess_return: float,
    variance: float,
    fraction: float = 0.25,
    max_leverage: float = 5.0,
) -> float:
    if variance <= 0 or not (0 < fraction <= 1) or max_leverage <= 0:
        raise ValueError
    # DEFECT: omitted leverage cap, leaves Kelly unbounded
    sized = fraction * (expected_excess_return / variance)
    return float(sized)


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
    def _p(s: float, k: float, v: float, t: float, c: bool) -> float:
        if t <= 1e-6:
            return max(0.0, s - k) if c else max(0.0, k - s)
        sqt = v * math.sqrt(t)
        d1 = (math.log(s / k) + (rate + 0.5 * v * v) * t) / sqt
        d2 = d1 - sqt
        c1 = 0.5 * (1 + math.erf(d1 / math.sqrt(2)))
        c2 = 0.5 * (1 + math.erf(d2 / math.sqrt(2)))
        if c:
            return s * c1 - k * math.exp(-rate * t) * c2
        return k * math.exp(-rate * t) * (0.5 * (1 + math.erf(-d2 / math.sqrt(2)))) - s * (
            0.5 * (1 + math.erf(-d1 / math.sqrt(2)))
        )

    v0 = sum(
        w * _p(base_spot, k, v, expiry, bool(c))
        for w, k, v, c in zip(weights, strikes, base_vols, is_call, strict=False)
    )
    grid = np.zeros((len(vol_shocks), len(spot_shocks)), dtype=np.float64)
    rem_t = max(1e-6, expiry - holding_period)
    for j, dv in enumerate(vol_shocks):
        for k_idx, ds in enumerate(spot_shocks):
            scen_s = base_spot * (1.0 + float(ds))
            v_scen = sum(
                w * _p(scen_s, k, max(0.01, v + dv), rem_t, bool(c))
                for w, k, v, c in zip(weights, strikes, base_vols, is_call, strict=False)
            )
            grid[j, k_idx] = v_scen - v0
    return grid


class MacroTradeEngine:
    def __init__(self, risk_free_rate: float = 0.045) -> None:
        self.risk_free_rate = risk_free_rate

    def construct_trade(
        self,
        view: MacroView,
        leg1_params: dict[str, float],
        leg2_params: dict[str, float] | None = None,
        sizing_budget: float = 1_000_000.0,
        kelly_fraction: float = 0.25,
        max_leverage: float = 4.0,
    ) -> dict[str, Any]:
        return {
            "view_id": view.view_id,
            "trade_type": view.view_type,
            "leg1_notional": sizing_budget,
            "leg2_notional": -sizing_budget,
            "hedge_ratio": 1.0,
            "net_dv01": 0.0,
            "allocated_capital": sizing_budget,
        }

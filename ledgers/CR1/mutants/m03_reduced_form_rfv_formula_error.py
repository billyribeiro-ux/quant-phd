"""Calculates recovery of face value using recovery of market value formula."""

from __future__ import annotations

import math
from typing import Any


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def merton_price(
    asset_value: float,
    debt_face: float,
    maturity: float,
    risk_free_rate: float,
    asset_volatility: float,
) -> dict[str, float]:
    if not (
        isinstance(asset_value, (int, float))
        and isinstance(debt_face, (int, float))
        and isinstance(maturity, (int, float))
        and isinstance(risk_free_rate, (int, float))
        and isinstance(asset_volatility, (int, float))
    ):
        raise TypeError("Inputs must be numeric floats or ints")
    if asset_value <= 0:
        raise ValueError(f"asset_value must be positive, got {asset_value}")
    if debt_face <= 0:
        raise ValueError(f"debt_face must be positive, got {debt_face}")
    if maturity <= 0:
        raise ValueError(f"maturity must be positive, got {maturity}")
    if asset_volatility <= 0:
        raise ValueError(f"asset_volatility must be positive, got {asset_volatility}")

    v = float(asset_value)
    d = float(debt_face)
    t = float(maturity)
    r = float(risk_free_rate)
    sigma = float(asset_volatility)

    vol_sqrt = sigma * math.sqrt(t)
    d1 = (math.log(v / d) + (r + 0.5 * sigma * sigma) * t) / vol_sqrt
    d2 = d1 - vol_sqrt

    equity = v * _norm_cdf(d1) - d * math.exp(-r * t) * _norm_cdf(d2)
    debt = v - equity
    debt_yield = -math.log(debt / d) / t
    spread = debt_yield - r
    default_prob = _norm_cdf(-d2)

    return {
        "equity": float(equity),
        "debt": float(debt),
        "yield": float(debt_yield),
        "spread": float(spread),
        "default_prob": float(default_prob),
    }


def black_cox_price(
    asset_value: float,
    debt_face: float,
    maturity: float,
    risk_free_rate: float,
    asset_volatility: float,
    barrier: float,
    recovery_rate: float = 0.4,
) -> dict[str, float]:
    if not (
        isinstance(asset_value, (int, float))
        and isinstance(debt_face, (int, float))
        and isinstance(maturity, (int, float))
        and isinstance(risk_free_rate, (int, float))
        and isinstance(asset_volatility, (int, float))
        and isinstance(barrier, (int, float))
        and isinstance(recovery_rate, (int, float))
    ):
        raise TypeError("Inputs must be numeric floats or ints")
    if barrier <= 0:
        raise ValueError(f"barrier must be positive, got {barrier}")
    if asset_value < barrier:
        raise ValueError(f"asset_value {asset_value} cannot be below barrier {barrier}")
    if debt_face <= 0:
        raise ValueError(f"debt_face must be positive, got {debt_face}")
    if maturity <= 0:
        raise ValueError(f"maturity must be positive, got {maturity}")
    if asset_volatility <= 0:
        raise ValueError(f"asset_volatility must be positive, got {asset_volatility}")
    if not (0.0 <= recovery_rate <= 1.0):
        raise ValueError(f"recovery_rate must be in [0, 1], got {recovery_rate}")

    v = float(asset_value)
    d = float(debt_face)
    t = float(maturity)
    r = float(risk_free_rate)
    sigma = float(asset_volatility)
    k = float(barrier)
    rec = float(recovery_rate)

    b = math.log(k / v)
    vol_sqrt = sigma * math.sqrt(t)
    mu = r - 0.5 * sigma * sigma
    lam = r + 0.5 * sigma * sigma

    d_minus = (b - mu * t) / vol_sqrt
    d_plus = (b + mu * t) / vol_sqrt
    default_prob = _norm_cdf(d_minus) + math.exp(2.0 * mu * b / (sigma * sigma)) * _norm_cdf(d_plus)
    default_prob = min(1.0, max(0.0, default_prob))
    survival_prob = 1.0 - default_prob

    g_term1 = math.exp(2.0 * r * b / (sigma * sigma)) * _norm_cdf((b + lam * t) / vol_sqrt)
    g_term2 = math.exp(-b) * _norm_cdf((b - lam * t) / vol_sqrt)
    expected_disc_hitting = g_term1 + g_term2

    debt = d * math.exp(-r * t) * survival_prob + rec * d * expected_disc_hitting
    equity = v - debt
    debt_yield = -math.log(debt / d) / t
    spread = debt_yield - r

    return {
        "debt": float(debt),
        "equity": float(equity),
        "spread": float(spread),
        "survival_prob": float(survival_prob),
        "default_prob": float(default_prob),
    }


def reduced_form_price(
    maturity: float,
    risk_free_rate: float,
    hazard_rate: float,
    recovery_rate: float = 0.4,
    convention: str = "rmv",
) -> dict[str, float]:
    if not (
        isinstance(maturity, (int, float))
        and isinstance(risk_free_rate, (int, float))
        and isinstance(hazard_rate, (int, float))
        and isinstance(recovery_rate, (int, float))
    ):
        raise TypeError("Inputs must be numeric floats or ints")
    if maturity <= 0:
        raise ValueError(f"maturity must be positive, got {maturity}")
    if hazard_rate < 0:
        raise ValueError(f"hazard_rate must be non-negative, got {hazard_rate}")
    if not (0.0 <= recovery_rate <= 1.0):
        raise ValueError(f"recovery_rate must be in [0, 1], got {recovery_rate}")
    if convention.lower() not in ("rmv", "rfv"):
        raise ValueError(f"convention must be 'rmv' or 'rfv', got '{convention}'")

    t = float(maturity)
    r = float(risk_free_rate)
    lam = float(hazard_rate)
    rec = float(recovery_rate)
    survival_prob = math.exp(-lam * t)

    # Student error: always uses RMV formula regardless of convention
    disc_rate = r + lam * (1.0 - rec)
    price = math.exp(-disc_rate * t)

    bond_yield = -math.log(price) / t
    spread = bond_yield - r

    return {
        "price": float(price),
        "yield": float(bond_yield),
        "spread": float(spread),
        "survival_prob": float(survival_prob),
    }


def merton_distance_to_default(
    equity_value: float,
    debt_face: float,
    maturity: float,
    risk_free_rate: float,
    equity_volatility: float,
    expected_return: float | None = None,
) -> dict[str, float]:
    if not (
        isinstance(equity_value, (int, float))
        and isinstance(debt_face, (int, float))
        and isinstance(maturity, (int, float))
        and isinstance(risk_free_rate, (int, float))
        and isinstance(equity_volatility, (int, float))
    ):
        raise TypeError("Inputs must be numeric floats or ints")
    if equity_value <= 0:
        raise ValueError(f"equity_value must be positive, got {equity_value}")
    if debt_face <= 0:
        raise ValueError(f"debt_face must be positive, got {debt_face}")
    if maturity <= 0:
        raise ValueError(f"maturity must be positive, got {maturity}")
    if equity_volatility <= 0:
        raise ValueError(f"equity_volatility must be positive, got {equity_volatility}")

    e = float(equity_value)
    d = float(debt_face)
    t = float(maturity)
    r = float(risk_free_rate)
    sigma_e = float(equity_volatility)
    mu = float(expected_return) if expected_return is not None else r

    v = e + d
    sigma_v = sigma_e * (e / v)

    for _ in range(150):
        vol_sqrt = max(1e-8, sigma_v * math.sqrt(t))
        d1 = (math.log(v / d) + (r + 0.5 * sigma_v * sigma_v) * t) / vol_sqrt
        d2 = d1 - vol_sqrt
        n_d1 = _norm_cdf(d1)
        n_d2 = _norm_cdf(d2)

        f_val = v * n_d1 - d * math.exp(-r * t) * n_d2 - e
        if abs(f_val) < 1e-11:
            break
        delta = max(1e-5, n_d1)
        v = max(e * 0.8, v - f_val / delta)

        vol_sqrt = max(1e-8, sigma_v * math.sqrt(t))
        d1 = (math.log(v / d) + (r + 0.5 * sigma_v * sigma_v) * t) / vol_sqrt
        sigma_v = max(1e-6, sigma_e * e / (v * max(1e-5, _norm_cdf(d1))))

    vol_sqrt = max(1e-8, sigma_v * math.sqrt(t))
    dd = (math.log(v / d) + (mu - 0.5 * sigma_v * sigma_v) * t) / vol_sqrt
    default_prob = _norm_cdf(-dd)

    return {
        "asset_value": float(v),
        "asset_volatility": float(sigma_v),
        "distance_to_default": float(dd),
        "default_prob": float(default_prob),
    }


def bharath_shumway_naive_dd(
    equity_value: float,
    debt_face: float,
    maturity: float,
    risk_free_rate: float,
    equity_volatility: float,
    expected_return: float | None = None,
) -> dict[str, float]:
    if not (
        isinstance(equity_value, (int, float))
        and isinstance(debt_face, (int, float))
        and isinstance(maturity, (int, float))
        and isinstance(risk_free_rate, (int, float))
        and isinstance(equity_volatility, (int, float))
    ):
        raise TypeError("Inputs must be numeric floats or ints")
    if equity_value <= 0:
        raise ValueError(f"equity_value must be positive, got {equity_value}")
    if debt_face <= 0:
        raise ValueError(f"debt_face must be positive, got {debt_face}")
    if maturity <= 0:
        raise ValueError(f"maturity must be positive, got {maturity}")
    if equity_volatility <= 0:
        raise ValueError(f"equity_volatility must be positive, got {equity_volatility}")

    e = float(equity_value)
    d = float(debt_face)
    t = float(maturity)
    r = float(risk_free_rate)
    sigma_e = float(equity_volatility)
    mu = float(expected_return) if expected_return is not None else r

    v_naive = e + d
    sigma_d = 0.05 + 0.25 * sigma_e
    sigma_v_naive = (e / v_naive) * sigma_e + (d / v_naive) * sigma_d

    vol_sqrt = max(1e-8, sigma_v_naive * math.sqrt(t))
    dd_naive = (math.log(v_naive / d) + (mu - 0.5 * sigma_v_naive * sigma_v_naive) * t) / vol_sqrt
    default_prob = _norm_cdf(-dd_naive)

    return {
        "asset_value": float(v_naive),
        "asset_volatility": float(sigma_v_naive),
        "distance_to_default": float(dd_naive),
        "default_prob": float(default_prob),
    }


def credit_spread_decomposition(
    market_spread: float,
    default_prob: float,
    recovery_rate: float,
    maturity: float,
    risk_premium_ratio: float = 0.5,
) -> dict[str, float]:
    if not (
        isinstance(market_spread, (int, float))
        and isinstance(default_prob, (int, float))
        and isinstance(recovery_rate, (int, float))
        and isinstance(maturity, (int, float))
        and isinstance(risk_premium_ratio, (int, float))
    ):
        raise TypeError("Inputs must be numeric floats or ints")
    if market_spread < 0:
        raise ValueError(f"market_spread must be non-negative, got {market_spread}")
    if not (0.0 <= default_prob <= 1.0):
        raise ValueError(f"default_prob must be in [0, 1], got {default_prob}")
    if not (0.0 <= recovery_rate <= 1.0):
        raise ValueError(f"recovery_rate must be in [0, 1], got {recovery_rate}")
    if maturity <= 0:
        raise ValueError(f"maturity must be positive, got {maturity}")
    if risk_premium_ratio < 0:
        raise ValueError(f"risk_premium_ratio must be non-negative, got {risk_premium_ratio}")

    s = float(market_spread)
    pd = float(default_prob)
    rec = float(recovery_rate)
    t = float(maturity)
    rp_ratio = float(risk_premium_ratio)

    loss_fraction = pd * (1.0 - rec)
    if loss_fraction >= 1.0:
        spread_el = 1.0
    else:
        spread_el = -math.log(1.0 - loss_fraction) / t

    spread_crp = spread_el * rp_ratio
    spread_credit = spread_el + spread_crp
    spread_residual = max(0.0, s - spread_credit)

    if s > 1e-12:
        credit_fraction = min(s, spread_credit) / s
    else:
        credit_fraction = 1.0

    return {
        "spread_el": float(spread_el),
        "spread_crp": float(spread_crp),
        "spread_credit": float(spread_credit),
        "spread_residual": float(spread_residual),
        "credit_fraction": float(credit_fraction),
    }

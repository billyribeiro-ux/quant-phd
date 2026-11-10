"""Reference solution for the CF2 cost of capital engine (wacc_engine.py).

Standard library only. All rates and parameters are decimals unless specified in cents.
All validation errors raise ValueError.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from decimal import ROUND_HALF_UP, Decimal


def _is_finite_number(val: object) -> bool:
    return isinstance(val, (int, float)) and not isinstance(val, bool) and math.isfinite(val)


def beta_ols(firm: Sequence[float], market: Sequence[float]) -> float:
    """Sample beta: sample covariance over sample variance, with Bessel correction (n - 1).

    Raises ValueError if lengths differ, if n < 2, or if market variance is zero.
    """
    n = len(firm)
    if n != len(market):
        raise ValueError("firm and market return series must have the same length")
    if n < 2:
        raise ValueError("sample beta requires at least 2 return periods")
    if not all(_is_finite_number(x) for x in firm) or not all(_is_finite_number(y) for y in market):
        raise ValueError("return series must contain finite numbers")

    mean_m = sum(market) / n
    mean_f = sum(firm) / n

    cov_fm = sum((f - mean_f) * (m - mean_m) for f, m in zip(firm, market, strict=True)) / (n - 1)
    var_m = sum((m - mean_m) ** 2 for m in market) / (n - 1)

    if var_m <= 1e-15:
        raise ValueError("market returns must have non-zero variance")

    return cov_fm / var_m


def unlever_beta(beta_levered: float, debt_cents: int, equity_cents: int, tax_rate: float) -> float:
    """Unlevered asset beta under the assumption of debt beta zero (Hamada formula).

    beta_U = beta_L / (1 + (1 - tau_c) * D / E).
    Raises ValueError if D < 0, E <= 0, or tax_rate not in [0, 1).
    """
    if isinstance(debt_cents, bool) or isinstance(equity_cents, bool):
        raise ValueError("debt and equity must be integers, not booleans")
    if debt_cents < 0:
        raise ValueError("debt must be non-negative")
    if equity_cents <= 0:
        raise ValueError("equity must be strictly positive")
    if not _is_finite_number(tax_rate) or not (0.0 <= tax_rate < 1.0):
        raise ValueError("corporate tax rate must be in [0, 1)")
    if not _is_finite_number(beta_levered):
        raise ValueError("levered beta must be a finite number")

    de_ratio = debt_cents / equity_cents
    return beta_levered / (1.0 + (1.0 - tax_rate) * de_ratio)


def relever_beta(beta_unlevered: float, debt_cents: int, equity_cents: int, tax_rate: float) -> float:
    """Relevered equity beta from unlevered asset beta (Hamada formula inverse).

    beta_L = beta_U * (1 + (1 - tau_c) * D / E).
    Raises ValueError if D < 0, E <= 0, or tax_rate not in [0, 1).
    """
    if isinstance(debt_cents, bool) or isinstance(equity_cents, bool):
        raise ValueError("debt and equity must be integers, not booleans")
    if debt_cents < 0:
        raise ValueError("debt must be non-negative")
    if equity_cents <= 0:
        raise ValueError("equity must be strictly positive")
    if not _is_finite_number(tax_rate) or not (0.0 <= tax_rate < 1.0):
        raise ValueError("corporate tax rate must be in [0, 1)")
    if not _is_finite_number(beta_unlevered):
        raise ValueError("unlevered beta must be a finite number")

    de_ratio = debt_cents / equity_cents
    return beta_unlevered * (1.0 + (1.0 - tax_rate) * de_ratio)


def cost_of_equity(risk_free: float, beta: float, erp: float) -> float:
    """CAPM cost of equity: r_E = r_f + beta * ERP."""
    if not (_is_finite_number(risk_free) and _is_finite_number(beta) and _is_finite_number(erp)):
        raise ValueError("all inputs to cost of equity must be finite numbers")
    return risk_free + beta * erp


def cost_of_debt(risk_free: float, spread: float) -> float:
    """Pre-tax cost of debt: r_D = r_f + spread."""
    if not (_is_finite_number(risk_free) and _is_finite_number(spread)):
        raise ValueError("all inputs to cost of debt must be finite numbers")
    return risk_free + spread


def wacc(debt_cents: int, equity_cents: int, cost_equity: float, cost_debt: float, tax_rate: float) -> float:
    """Weighted average cost of capital: r_WACC = (E/V) r_E + (D/V) r_D (1 - tau_c).

    Raises ValueError if D < 0, E < 0, D + E <= 0, or tax_rate not in [0, 1).
    """
    if isinstance(debt_cents, bool) or isinstance(equity_cents, bool):
        raise ValueError("debt and equity must be integers, not booleans")
    if debt_cents < 0 or equity_cents < 0:
        raise ValueError("debt and equity values must be non-negative")
    total = debt_cents + equity_cents
    if total <= 0:
        raise ValueError("total firm enterprise value (D + E) must be strictly positive")
    if not _is_finite_number(tax_rate) or not (0.0 <= tax_rate < 1.0):
        raise ValueError("corporate tax rate must be in [0, 1)")
    if not (_is_finite_number(cost_equity) and _is_finite_number(cost_debt)):
        raise ValueError("costs of capital must be finite numbers")

    w_e = equity_cents / total
    w_d = debt_cents / total
    return w_e * cost_equity * (1.0 - tax_rate) + w_d * cost_debt


def wacc_delta_variance(
    debt_cents: int,
    equity_cents: int,
    beta: float,
    erp: float,
    var_beta: float,
    var_erp: float,
    cov_beta_erp: float,
    var_spread: float,
    tax_rate: float,
) -> float:
    """Delta-method linearised variance of WACC with weights and tax rate treated as fixed.

    w_E^2 * [ERP^2 * Var(beta) + beta^2 * Var(ERP) + 2 * beta * ERP * Cov(beta, ERP)]
    + [w_D * (1 - tau_c)]^2 * Var(spread).

    Raises ValueError if variances are negative, if covariance matrix is not positive semi-definite
    (var_beta * var_erp < cov_beta_erp^2), if capital weights are non-positive, or if tax_rate not in [0, 1).
    """
    if isinstance(debt_cents, bool) or isinstance(equity_cents, bool):
        raise ValueError("debt and equity must be integers, not booleans")
    if debt_cents < 0 or equity_cents < 0:
        raise ValueError("debt and equity must be non-negative")
    total = debt_cents + equity_cents
    if total <= 0:
        raise ValueError("total capital must be strictly positive")
    if not _is_finite_number(tax_rate) or not (0.0 <= tax_rate < 1.0):
        raise ValueError("corporate tax rate must be in [0, 1)")

    for name, v in [("var_beta", var_beta), ("var_erp", var_erp), ("var_spread", var_spread)]:
        if not _is_finite_number(v) or v < 0.0:
            raise ValueError(f"{name} must be a non-negative finite number")

    if not _is_finite_number(cov_beta_erp):
        raise ValueError("cov_beta_erp must be a finite number")

    if var_beta * var_erp < cov_beta_erp**2 - 1e-15:
        raise ValueError("covariance matrix of beta and ERP must be positive semi-definite")

    w_e = equity_cents / total
    w_d = debt_cents / total

    term_equity = (w_e**2) * (erp**2 * var_beta + beta**2 * var_erp + 2.0 * beta * erp * cov_beta_erp)
    term_debt = (w_d * (1.0 - tax_rate)) ** 2 * var_spread

    return term_equity + term_debt


def valuation_range(
    cash_flow_cents: int,
    growth: float,
    wacc_mid: float,
    wacc_se: float,
    k: float = 1.0,
) -> tuple[int, int]:
    """Valuation range [V_low, V_high] in integer cents using growing perpetuity C_1 / (r - g).

    Evaluated at endpoint discount rates r = wacc_mid +/- k * wacc_se.
    Higher discount rate r_high gives low valuation V_low.
    Lower discount rate r_low gives high valuation V_high.
    Both endpoints are rounded half-up to integer cents on exact decimal values.

    Raises ValueError if cash_flow_cents is not a positive integer, if k < 0,
    if wacc_se < 0, or if either endpoint rate is at or below growth.
    """
    if isinstance(cash_flow_cents, bool) or not isinstance(cash_flow_cents, int) or cash_flow_cents <= 0:
        raise ValueError("cash_flow_cents must be a positive integer number of cents")
    if not _is_finite_number(k) or k < 0.0:
        raise ValueError("k must be a non-negative number")
    if not _is_finite_number(wacc_se) or wacc_se < 0.0:
        raise ValueError("wacc_se must be a non-negative number")
    if not (_is_finite_number(growth) and _is_finite_number(wacc_mid)):
        raise ValueError("growth and wacc_mid must be finite numbers")

    # Use exact Decimal arithmetic from string representation to avoid float binary artifacts
    d_mid = Decimal(str(wacc_mid))
    d_se = Decimal(str(wacc_se))
    d_k = Decimal(str(k))
    d_g = Decimal(str(growth))
    d_cf = Decimal(cash_flow_cents)

    r_low = d_mid - d_k * d_se
    r_high = d_mid + d_k * d_se

    if r_low <= d_g:
        raise ValueError("lower discount rate bound must strictly exceed growth rate")
    if r_high <= d_g:
        raise ValueError("upper discount rate bound must strictly exceed growth rate")

    val_low = (d_cf / (r_high - d_g)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    val_high = (d_cf / (r_low - d_g)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    return int(val_low), int(val_high)

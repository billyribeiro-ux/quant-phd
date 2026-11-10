"""Starter template for the CF2 cost of capital engine (wacc_engine.py).

Implement each function according to the specification on project.html.
All validation errors must raise ValueError.
"""

from __future__ import annotations

from collections.abc import Sequence


def beta_ols(firm: Sequence[float], market: Sequence[float]) -> float:
    """Sample beta: sample covariance over sample variance, with Bessel correction (n - 1)."""
    raise NotImplementedError("beta_ols is not yet implemented")


def unlever_beta(beta_levered: float, debt_cents: int, equity_cents: int, tax_rate: float) -> float:
    """Unlevered asset beta under the assumption of debt beta zero (Hamada formula)."""
    raise NotImplementedError("unlever_beta is not yet implemented")


def relever_beta(beta_unlevered: float, debt_cents: int, equity_cents: int, tax_rate: float) -> float:
    """Relevered equity beta from unlevered asset beta (Hamada formula inverse)."""
    raise NotImplementedError("relever_beta is not yet implemented")


def cost_of_equity(risk_free: float, beta: float, erp: float) -> float:
    """CAPM cost of equity: r_E = r_f + beta * ERP."""
    raise NotImplementedError("cost_of_equity is not yet implemented")


def cost_of_debt(risk_free: float, spread: float) -> float:
    """Pre-tax cost of debt: r_D = r_f + spread."""
    raise NotImplementedError("cost_of_debt is not yet implemented")


def wacc(debt_cents: int, equity_cents: int, cost_equity: float, cost_debt: float, tax_rate: float) -> float:
    """Weighted average cost of capital: r_WACC = (E/V) r_E + (D/V) r_D (1 - tau_c)."""
    raise NotImplementedError("wacc is not yet implemented")


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
    """Delta-method linearised variance of WACC with weights and tax rate treated as fixed."""
    raise NotImplementedError("wacc_delta_variance is not yet implemented")


def valuation_range(
    cash_flow_cents: int,
    growth: float,
    wacc_mid: float,
    wacc_se: float,
    k: float = 1.0,
) -> tuple[int, int]:
    """Valuation range [V_low, V_high] in integer cents using growing perpetuity C_1 / (r - g)."""
    raise NotImplementedError("valuation_range is not yet implemented")

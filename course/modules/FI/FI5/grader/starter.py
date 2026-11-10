"""Starter code stub for FI5 Inflation-Expectations Decomposition project."""

from __future__ import annotations


def breakeven_yield(nominal_yield: float, real_yield: float) -> float:
    """Compute the breakeven inflation rate as the yield spread between nominal and real bonds."""
    raise NotImplementedError


def tips_cash_flows(
    base_cpi: float,
    ref_cpi: float,
    coupon_rate: float,
    maturity_years: int,
    face_value: float = 100.0,
) -> dict[str, float]:
    """Compute TIPS indexation, adjusted coupon, and deflation-floor protected principal."""
    raise NotImplementedError


def replicate_synthetic_treasury(real_yield: float, swap_rate: float) -> float:
    """Replicate synthetic nominal Treasury yield via compounding Fisher replication."""
    raise NotImplementedError


def fleckenstein_puzzle_basis(
    cash_nominal_price: float,
    synthetic_price: float,
    mod_duration: float,
) -> dict[str, float]:
    """Compute the Fleckenstein, Longstaff, and Lustig (2014) mispricing puzzle basis."""
    raise NotImplementedError


def decompose_breakeven(
    nominal_yield: float,
    real_yield: float,
    survey_expected_inflation: float,
    tips_liquidity_proxy: float,
    beta_liquidity: float = 1.0,
) -> dict[str, float]:
    """Perform tripartite decomposition of breakeven inflation into expectations, IRP, and TLP."""
    raise NotImplementedError

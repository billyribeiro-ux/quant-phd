"""Mutant 3: Subtracts TIPS liquidity premium instead of adding it in breakeven decomposition."""

from __future__ import annotations


def breakeven_yield(nominal_yield: float, real_yield: float) -> float:
    return nominal_yield - real_yield


def tips_cash_flows(
    base_cpi: float,
    ref_cpi: float,
    coupon_rate: float,
    maturity_years: int,
    face_value: float = 100.0,
) -> dict[str, float]:
    if base_cpi <= 0.0 or ref_cpi <= 0.0:
        raise ValueError("CPI values must be strictly positive")
    if face_value <= 0.0:
        raise ValueError("Face value must be strictly positive")
    if maturity_years <= 0:
        raise ValueError("Maturity years must be positive")
    if coupon_rate < 0.0:
        raise ValueError("Coupon rate cannot be negative")

    index_ratio = ref_cpi / base_cpi
    adjusted_coupon = face_value * (coupon_rate / 2.0) * index_ratio
    adjusted_principal = face_value * max(1.0, index_ratio)
    deflation_floor_benefit = face_value * max(0.0, 1.0 - index_ratio)
    total_maturity_cash_flow = adjusted_coupon + adjusted_principal

    return {
        "index_ratio": index_ratio,
        "adjusted_coupon": adjusted_coupon,
        "adjusted_principal": adjusted_principal,
        "deflation_floor_benefit": deflation_floor_benefit,
        "total_maturity_cash_flow": total_maturity_cash_flow,
    }


def replicate_synthetic_treasury(real_yield: float, swap_rate: float) -> float:
    return (1.0 + real_yield) * (1.0 + swap_rate) - 1.0


def fleckenstein_puzzle_basis(
    cash_nominal_price: float,
    synthetic_price: float,
    mod_duration: float,
) -> dict[str, float]:
    if cash_nominal_price <= 0.0 or mod_duration <= 0.0:
        raise ValueError("Cash price and modified duration must be strictly positive")

    price_basis = cash_nominal_price - synthetic_price
    yield_basis_bps = (price_basis / (cash_nominal_price * mod_duration)) * 10_000.0

    return {
        "price_basis": price_basis,
        "yield_basis_bps": yield_basis_bps,
    }


def decompose_breakeven(
    nominal_yield: float,
    real_yield: float,
    survey_expected_inflation: float,
    tips_liquidity_proxy: float,
    beta_liquidity: float = 1.0,
) -> dict[str, float]:
    bei = nominal_yield - real_yield
    tlp = beta_liquidity * tips_liquidity_proxy
    # Error: subtracted TLP instead of adding TLP
    irp = bei - survey_expected_inflation - tlp

    return {
        "bei": bei,
        "expected_inflation": survey_expected_inflation,
        "tips_liquidity_premium": tlp,
        "inflation_risk_premium": irp,
    }

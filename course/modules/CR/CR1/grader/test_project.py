"""Acceptance suite for the CR1 credit engine (atlas/credit.py).

Runs identically in the browser (Pyodide) and locally:
    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import math
import os
from typing import Any

import pytest
from atlas import credit as sol  # type: ignore[attr-defined]
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)

ASSET_VALUE = float(INST["asset_value"])
DEBT_FACE = float(INST["debt_face"])
MATURITY = float(INST["maturity"])
RISK_FREE_RATE = float(INST["risk_free_rate"])
ASSET_VOLATILITY = float(INST["asset_volatility"])
BARRIER = float(INST["barrier"])
RECOVERY_RATE = float(INST["recovery_rate"])
HAZARD_RATE = float(INST["hazard_rate"])
EQUITY_VALUE = float(INST["equity_value"])
EQUITY_VOLATILITY = float(INST["equity_volatility"])
EXPECTED_RETURN = float(INST["expected_return"])
MARKET_SPREAD = float(INST["market_spread"])
DEFAULT_PROB = float(INST["default_prob"])
RISK_PREMIUM_RATIO = float(INST["risk_premium_ratio"])


# ============================================================================
# 1. Merton (1974) Model Tests
# ============================================================================


def test_merton_balance_sheet_identity() -> None:
    """Equity + Debt must equal total firm Asset Value (articulation)."""
    res = sol.merton_price(ASSET_VALUE, DEBT_FACE, MATURITY, RISK_FREE_RATE, ASSET_VOLATILITY)
    assert abs(res["equity"] + res["debt"] - ASSET_VALUE) < 1e-7, "Equity + Debt != Asset Value"
    assert res["equity"] > 0.0, "Equity must be strictly positive"
    assert res["debt"] > 0.0, "Debt must be strictly positive"


def test_merton_spread_and_yield_consistency() -> None:
    """Spread must equal yield minus risk-free rate, and spread must be non-negative."""
    res = sol.merton_price(ASSET_VALUE, DEBT_FACE, MATURITY, RISK_FREE_RATE, ASSET_VOLATILITY)
    assert abs(res["yield"] - (RISK_FREE_RATE + res["spread"])) < 1e-9, "Spread != yield - risk-free rate"
    assert res["spread"] >= -1e-9, "Credit spread cannot be negative"
    assert 0.0 <= res["default_prob"] <= 1.0, "Default probability must lie in [0, 1]"


def test_merton_volatility_comparative_statics() -> None:
    """Higher asset volatility increases equity (call option) and decreases risky debt."""
    low_vol = sol.merton_price(ASSET_VALUE, DEBT_FACE, MATURITY, RISK_FREE_RATE, 0.10)
    high_vol = sol.merton_price(ASSET_VALUE, DEBT_FACE, MATURITY, RISK_FREE_RATE, 0.40)
    assert high_vol["equity"] > low_vol["equity"], "Equity must increase with asset volatility"
    assert high_vol["debt"] < low_vol["debt"], "Debt must decrease with asset volatility"
    assert high_vol["spread"] > low_vol["spread"], "Spread must increase with asset volatility"


def test_merton_safe_firm_limit() -> None:
    """For an overwhelmingly solvent firm (V >> D), credit spread vanishes to 0."""
    res = sol.merton_price(1000.0, 10.0, 1.0, 0.05, 0.20)
    assert res["spread"] < 1e-4, "Spread must approach zero for extremely solvent firms"
    assert res["default_prob"] < 1e-4, "Default probability must approach zero"


# ============================================================================
# 2. Black-Cox (1976) First-Passage Model Tests
# ============================================================================


def test_black_cox_balance_sheet_identity() -> None:
    """Black-Cox debt + equity must equal asset value."""
    res = sol.black_cox_price(
        ASSET_VALUE, DEBT_FACE, MATURITY, RISK_FREE_RATE, ASSET_VOLATILITY, BARRIER, RECOVERY_RATE
    )
    assert abs(res["debt"] + res["equity"] - ASSET_VALUE) < 1e-7, "Debt + Equity != Asset Value"
    assert 0.0 <= res["default_prob"] <= 1.0, "Default prob must be in [0, 1]"
    assert abs(res["default_prob"] + res["survival_prob"] - 1.0) < 1e-7, "Survival + Default != 1"


def test_black_cox_recovery_sensitivity() -> None:
    """Higher recovery rate strictly increases debt value and decreases credit spread."""
    res_low_rec = sol.black_cox_price(ASSET_VALUE, DEBT_FACE, MATURITY, RISK_FREE_RATE, ASSET_VOLATILITY, BARRIER, 0.20)
    res_high_rec = sol.black_cox_price(
        ASSET_VALUE, DEBT_FACE, MATURITY, RISK_FREE_RATE, ASSET_VOLATILITY, BARRIER, 0.80
    )
    assert res_high_rec["debt"] >= res_low_rec["debt"] - 1e-9, "Higher recovery must increase debt value"
    assert res_high_rec["spread"] <= res_low_rec["spread"] + 1e-9, "Higher recovery must decrease spread"


def test_black_cox_boundary_default() -> None:
    """When asset value touches the barrier, default probability is 1.0."""
    res = sol.black_cox_price(BARRIER, DEBT_FACE, MATURITY, RISK_FREE_RATE, ASSET_VOLATILITY, BARRIER, RECOVERY_RATE)
    assert abs(res["default_prob"] - 1.0) < 1e-4, "Touching barrier must produce default prob 1.0"
    assert abs(res["survival_prob"]) < 1e-4, "Touching barrier must produce survival prob 0.0"


def test_black_cox_stochastic_discounting() -> None:
    """Black-Cox debt must properly discount early default recovery at r > 0."""
    res = sol.black_cox_price(
        asset_value=100.0,
        debt_face=80.0,
        maturity=3.0,
        risk_free_rate=0.06,
        asset_volatility=0.25,
        barrier=75.0,
        recovery_rate=0.40,
    )
    undiscounted_debt_recovery = 0.40 * 80.0 * res["default_prob"]
    promised_discounted = 80.0 * math.exp(-0.06 * 3.0) * res["survival_prob"]
    max_undiscounted_debt = promised_discounted + undiscounted_debt_recovery
    assert res["debt"] < max_undiscounted_debt - 1e-4, "Early recovery must be discounted under risk-free rate"


# ============================================================================
# 3. Reduced-Form (Intensity-Based) Model Tests
# ============================================================================


def test_reduced_form_rmv_formula() -> None:
    """RMV convention must exactly match Duffie-Singleton analytical formula exp(-(r + lambda*(1-R))*T)."""
    res = sol.reduced_form_price(MATURITY, RISK_FREE_RATE, HAZARD_RATE, RECOVERY_RATE, convention="rmv")
    expected_price = math.exp(-(RISK_FREE_RATE + HAZARD_RATE * (1.0 - RECOVERY_RATE)) * MATURITY)
    assert abs(res["price"] - expected_price) < 1e-9, "RMV price differs from Duffie-Singleton formula"
    expected_spread = HAZARD_RATE * (1.0 - RECOVERY_RATE)
    assert abs(res["spread"] - expected_spread) < 1e-9, "RMV spread differs from lambda*(1-R)"


def test_reduced_form_rfv_bounds() -> None:
    """RFV bond price must lie strictly between zero-recovery price and risk-free price, and match RFV formula."""
    t = MATURITY
    r = RISK_FREE_RATE
    lam = HAZARD_RATE
    rec = RECOVERY_RATE
    res_rfv = sol.reduced_form_price(t, r, lam, rec, convention="rfv")
    p_rfv = res_rfv["price"]
    p_zero_rec = math.exp(-(r + lam) * t)
    p_riskfree = math.exp(-r * t)
    assert p_zero_rec <= p_rfv <= p_riskfree + 1e-9, "RFV price must lie between zero recovery and risk-free bond"

    # Exact RFV Duffie-Singleton formula
    expected_rfv = math.exp(-(r + lam) * t) + rec * (lam / (r + lam)) * (1.0 - math.exp(-(r + lam) * t))
    assert abs(p_rfv - expected_rfv) < 1e-7, "RFV price must match Duffie-Singleton RFV formula"

    # RFV price must strictly differ from RMV price when recovery > 0
    res_rmv = sol.reduced_form_price(t, r, lam, rec, convention="rmv")
    assert abs(p_rfv - res_rmv["price"]) > 1e-6, "RFV price must differ from RMV price"


def test_reduced_form_zero_hazard_limit() -> None:
    """When hazard rate is 0, bond price equals risk-free bond price and spread is 0."""
    res = sol.reduced_form_price(MATURITY, RISK_FREE_RATE, 0.0, RECOVERY_RATE, convention="rmv")
    assert abs(res["price"] - math.exp(-RISK_FREE_RATE * MATURITY)) < 1e-9, "Zero hazard must equal risk-free price"
    assert abs(res["spread"]) < 1e-9, "Zero hazard must give zero spread"


# ============================================================================
# 4. Distance to Default Tests
# ============================================================================


def test_merton_distance_to_default_inversion() -> None:
    """The inverted asset value and volatility must reconstruct the observable equity value and volatility."""
    res = sol.merton_distance_to_default(
        EQUITY_VALUE, DEBT_FACE, MATURITY, RISK_FREE_RATE, EQUITY_VOLATILITY, EXPECTED_RETURN
    )
    v_est = res["asset_value"]
    sigma_v_est = res["asset_volatility"]

    # Reconstruct Merton equity
    vol_sqrt = sigma_v_est * math.sqrt(MATURITY)
    d1 = (math.log(v_est / DEBT_FACE) + (RISK_FREE_RATE + 0.5 * sigma_v_est**2) * MATURITY) / vol_sqrt
    d2 = d1 - vol_sqrt
    n_d1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    n_d2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    reconstructed_e = v_est * n_d1 - DEBT_FACE * math.exp(-RISK_FREE_RATE * MATURITY) * n_d2
    assert abs(reconstructed_e - EQUITY_VALUE) < 1e-5, "Reconstructed equity differs from observed equity"

    reconstructed_sigma_e = (v_est * n_d1 / EQUITY_VALUE) * sigma_v_est
    assert abs(reconstructed_sigma_e - EQUITY_VOLATILITY) < 1e-4, "Reconstructed equity vol differs from observed"

    expected_dd = (math.log(v_est / DEBT_FACE) + (EXPECTED_RETURN - 0.5 * sigma_v_est**2) * MATURITY) / vol_sqrt
    assert abs(res["distance_to_default"] - expected_dd) < 1e-6, "Merton distance to default formula mismatch"


def test_bharath_shumway_naive_dd_properties() -> None:
    """Naive predictor must equal analytical Bharath & Shumway formulas."""
    res = sol.bharath_shumway_naive_dd(
        EQUITY_VALUE, DEBT_FACE, MATURITY, RISK_FREE_RATE, EQUITY_VOLATILITY, EXPECTED_RETURN
    )
    expected_v = EQUITY_VALUE + DEBT_FACE
    expected_sigma_d = 0.05 + 0.25 * EQUITY_VOLATILITY
    expected_sigma_v = (EQUITY_VALUE / expected_v) * EQUITY_VOLATILITY + (DEBT_FACE / expected_v) * expected_sigma_d
    assert abs(res["asset_value"] - expected_v) < 1e-9, "Naive asset value != E + D"
    assert abs(res["asset_volatility"] - expected_sigma_v) < 1e-9, "Naive asset volatility formula mismatch"
    assert 0.0 <= res["default_prob"] <= 1.0, "Naive default prob must lie in [0, 1]"


# ============================================================================
# 5. Credit Spread Decomposition Tests
# ============================================================================


def test_credit_spread_decomposition_identities() -> None:
    """Spread decomposition components must satisfy summation and positivity identities."""
    res = sol.credit_spread_decomposition(MARKET_SPREAD, DEFAULT_PROB, RECOVERY_RATE, MATURITY, RISK_PREMIUM_RATIO)
    assert abs(res["spread_credit"] - (res["spread_el"] + res["spread_crp"])) < 1e-9, "spread_credit != el + crp"
    assert res["spread_el"] >= 0.0, "Expected loss spread must be non-negative"
    assert res["spread_crp"] >= 0.0, "Credit risk premium must be non-negative"
    assert res["spread_residual"] >= 0.0, "Non-credit residual cannot be negative"
    assert 0.0 <= res["credit_fraction"] <= 1.0, "Credit fraction must lie in [0, 1]"
    # Articulation: when market spread >= spread_credit, credit + residual == market spread
    if res["spread_credit"] <= MARKET_SPREAD:
        assert abs(res["spread_credit"] + res["spread_residual"] - MARKET_SPREAD) < 1e-9, "Spread articulation failed"


def test_credit_spread_decomposition_clamping() -> None:
    """When modeled credit spread exceeds market spread, residual spread must be clamped to 0.0."""
    res = sol.credit_spread_decomposition(
        market_spread=0.0050,  # 50 bps market spread
        default_prob=0.10,  # high default prob -> spread_el + spread_crp > 50 bps
        recovery_rate=0.40,
        maturity=5.0,
        risk_premium_ratio=0.5,
    )
    assert res["spread_residual"] >= 0.0, "Residual spread must never be negative (non-negative clamping)"
    assert res["spread_residual"] == 0.0, "When credit risk exceeds market spread, residual must be exactly 0.0"


# ============================================================================
# 6. Input Validation & Error Handling
# ============================================================================


def test_invalid_merton_inputs() -> None:
    """Invalid parameter values must raise ValueError."""
    with pytest.raises(ValueError):
        sol.merton_price(-100.0, 80.0, 1.0, 0.05, 0.20)
    with pytest.raises(ValueError):
        sol.merton_price(100.0, -80.0, 1.0, 0.05, 0.20)
    with pytest.raises(ValueError):
        sol.merton_price(100.0, 80.0, -1.0, 0.05, 0.20)
    with pytest.raises(ValueError):
        sol.merton_price(100.0, 80.0, 1.0, 0.05, -0.20)


def test_invalid_black_cox_barrier() -> None:
    """Asset value below barrier must raise ValueError."""
    with pytest.raises(ValueError):
        sol.black_cox_price(50.0, 80.0, 1.0, 0.05, 0.20, barrier=60.0)


def test_invalid_reduced_form_inputs() -> None:
    """Invalid convention must raise ValueError."""
    with pytest.raises(ValueError):
        sol.reduced_form_price(1.0, 0.05, 0.02, 0.40, convention="invalid_convention")
    with pytest.raises(ValueError):
        sol.reduced_form_price(1.0, 0.05, -0.01, 0.40, convention="rmv")


def test_invalid_type_inputs() -> None:
    """Non-numeric inputs must raise TypeError."""
    with pytest.raises(TypeError):
        sol.merton_price("100", 80.0, 1.0, 0.05, 0.20)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        sol.reduced_form_price(1.0, "0.05", 0.02, 0.40)  # type: ignore[arg-type]

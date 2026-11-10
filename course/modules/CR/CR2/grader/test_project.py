"""Acceptance test suite for CR2: Credit Derivatives & Correlation.

Runs identically in Pyodide and native pytest:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import math
import os
from typing import Any

import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]
from reference import (  # type: ignore[import-not-found, unused-ignore]
    base_correlation_and_skew_analysis,
    bootstrap_hazard_curve,
    cds_bond_basis_analysis,
    cds_valuation,
    one_factor_gaussian_copula_loss,
    price_cdo_tranche,
)

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)

TENORS: list[float] = list(INST["tenors"])
SPREADS_BPS: list[float] = list(INST["spreads_bps"])
RECOVERY_RATE: float = float(INST["recovery_rate"])
RISK_FREE_RATE: float = float(INST["risk_free_rate"])
EVAL_TENOR: float = float(INST["eval_tenor"])
RUNNING_COUPON_BPS: float = float(INST["running_coupon_bps"])
BOND_CASH_SPREAD_BPS: float = float(INST["bond_cash_spread_bps"])
REPO_RATE: float = float(INST["repo_rate"])
FUNDING_RATE: float = float(INST["funding_rate"])
NUM_NAMES: int = int(INST["num_names"])
PORTFOLIO_PD_5Y: float = float(INST["portfolio_pd_5y"])
RHO: float = float(INST["rho"])
STUDENT_T_DF: int = int(INST["student_t_df"])
TEST_ATTACHMENT: float = float(INST["test_attachment"])
TEST_DETACHMENT: float = float(INST["test_detachment"])


# ============================================================================
# 1. Single-Name CDS Hazard Rate Bootstrapping Tests
# ============================================================================


def test_bootstrap_output_structure() -> None:
    """Bootstrapper must return required dictionary keys and matching list lengths."""
    res = bootstrap_hazard_curve(TENORS, SPREADS_BPS, recovery=RECOVERY_RATE, r=RISK_FREE_RATE)
    assert "tenors" in res and "hazard_rates" in res and "survival_probs" in res
    assert len(res["hazard_rates"]) == len(TENORS), "Hazard rates count != tenors count"
    assert len(res["survival_probs"]) == len(TENORS), "Survival probs count != tenors count"


def test_bootstrap_hazard_rate_positivity() -> None:
    """All bootstrapped default intensities (hazard rates) must be strictly positive."""
    res = bootstrap_hazard_curve(TENORS, SPREADS_BPS, recovery=RECOVERY_RATE, r=RISK_FREE_RATE)
    for idx, lam in enumerate(res["hazard_rates"]):
        assert lam > 0.0, f"Hazard rate at tenor {TENORS[idx]} must be positive, got {lam}"
        assert lam < 2.0, f"Hazard rate unreasonably high: {lam}"


def test_bootstrap_survival_probabilities_monotonicity() -> None:
    """Cumulative survival probability Q(T) must be strictly decreasing: 1 > Q(T1) > Q(T2) > 0."""
    res = bootstrap_hazard_curve(TENORS, SPREADS_BPS, recovery=RECOVERY_RATE, r=RISK_FREE_RATE)
    q_vals = res["survival_probs"]
    assert 0.0 < q_vals[0] < 1.0, f"Q(T1) must be in (0, 1), got {q_vals[0]}"
    for i in range(len(q_vals) - 1):
        assert q_vals[i] > q_vals[i + 1], (
            f"Survival probability must strictly decrease: "
            f"Q({TENORS[i]})={q_vals[i]} <= Q({TENORS[i + 1]})={q_vals[i + 1]}"
        )


def test_bootstrap_par_spread_reproduction() -> None:
    """Bootstrapped hazard curve must re-price input par CDS quotes to high numerical accuracy."""
    res = bootstrap_hazard_curve(TENORS, SPREADS_BPS, recovery=RECOVERY_RATE, r=RISK_FREE_RATE)
    model_spreads = res["model_spreads_bps"]
    for i, target_s in enumerate(SPREADS_BPS):
        diff = abs(model_spreads[i] - target_s)
        assert diff < 1e-3, (
            f"Repriced spread at tenor {TENORS[i]} ({model_spreads[i]:.4f} bp) diverges from quote ({target_s:.4f} bp)"
        )


# ============================================================================
# 2. Mark-to-Market CDS Valuation and Risky PV01 Tests
# ============================================================================


def test_cds_valuation_par_spread_consistency() -> None:
    """When running coupon equals the break-even par spread, upfront fee must equal zero."""
    boot = bootstrap_hazard_curve(TENORS, SPREADS_BPS, recovery=RECOVERY_RATE, r=RISK_FREE_RATE)
    par_5y = SPREADS_BPS[3]
    val = cds_valuation(
        5.0,
        par_5y,
        boot["hazard_rates"],
        TENORS,
        recovery=RECOVERY_RATE,
        r=RISK_FREE_RATE,
    )
    assert abs(val["upfront_fee"]) < 1e-4, f"Upfront fee at par spread must be ~0, got {val['upfront_fee']}"
    assert abs(val["par_spread_bps"] - par_5y) < 1e-3, "Calculated par spread != input 5Y spread"


def test_cds_valuation_pv01_positivity() -> None:
    """Risky PV01 must be positive and bounded above by the risk-free annuity."""
    boot = bootstrap_hazard_curve(TENORS, SPREADS_BPS, recovery=RECOVERY_RATE, r=RISK_FREE_RATE)
    val = cds_valuation(
        EVAL_TENOR,
        RUNNING_COUPON_BPS,
        boot["hazard_rates"],
        TENORS,
        recovery=RECOVERY_RATE,
        r=RISK_FREE_RATE,
    )
    pv01 = val["risky_pv01"]
    rf_annuity = (1.0 - math.exp(-RISK_FREE_RATE * EVAL_TENOR)) / RISK_FREE_RATE * 0.0001
    assert 0.0 < pv01 < rf_annuity, f"Risky PV01 ({pv01}) must be in (0, {rf_annuity})"


# ============================================================================
# 3. CDS-Bond Basis Analytics Tests
# ============================================================================


def test_cds_bond_basis_sign_and_arbitrage_direction() -> None:
    """Basis = CDS spread - Bond cash spread. Arbitrage actions must match sign."""
    cds_5y = SPREADS_BPS[3]
    res = cds_bond_basis_analysis(cds_5y, BOND_CASH_SPREAD_BPS, REPO_RATE, FUNDING_RATE)
    expected_basis = cds_5y - BOND_CASH_SPREAD_BPS
    assert abs(res["basis_bps"] - expected_basis) < 1e-7, "Basis != CDS - Cash spread"

    if expected_basis < 0.0:
        assert res["arbitrage_strategy"] == "negative_basis_trade"
        assert res["recommended_action"] == "buy_bond_buy_cds"
        assert res["gross_carry_bps"] > 0.0, "Negative basis must offer positive gross carry"
    elif expected_basis > 0.0:
        assert res["arbitrage_strategy"] == "positive_basis_trade"
        assert res["recommended_action"] == "short_bond_sell_cds"
        assert res["gross_carry_bps"] > 0.0


def test_cds_bond_basis_funding_drag() -> None:
    """Funding drag must accurately adjust gross carry to net carry."""
    cds_5y = SPREADS_BPS[3]
    res = cds_bond_basis_analysis(cds_5y, BOND_CASH_SPREAD_BPS, REPO_RATE, FUNDING_RATE)
    expected_drag = (REPO_RATE - FUNDING_RATE) * 10000.0
    assert abs(res["funding_drag_bps"] - expected_drag) < 1e-7
    if res["basis_bps"] < 0.0:
        assert abs(res["net_carry_bps"] - (res["gross_carry_bps"] - expected_drag)) < 1e-7


# ============================================================================
# 4. One-Factor Gaussian Copula Loss Distribution Tests
# ============================================================================


def test_gaussian_copula_expected_loss_unconditional_invariance() -> None:
    """Unconditional expected loss E[L] = (1 - R) * p must be invariant to correlation rho."""
    res = one_factor_gaussian_copula_loss(PORTFOLIO_PD_5Y, RECOVERY_RATE, RHO)
    theoretical_el = (1.0 - RECOVERY_RATE) * PORTFOLIO_PD_5Y
    assert abs(res["expected_loss"] - theoretical_el) < 1e-4, (
        f"Expected loss {res['expected_loss']} != theoretical {theoretical_el}"
    )


def test_gaussian_copula_variance_increases_with_rho() -> None:
    """Portfolio loss variance must be strictly higher for higher correlation."""
    res_low = one_factor_gaussian_copula_loss(PORTFOLIO_PD_5Y, RECOVERY_RATE, 0.05)
    res_high = one_factor_gaussian_copula_loss(PORTFOLIO_PD_5Y, RECOVERY_RATE, 0.45)
    assert res_high["loss_std"] > res_low["loss_std"] * 1.5, "Higher correlation must increase loss volatility"


def test_gaussian_copula_lhp_var_bounds() -> None:
    """99% Vasicek/LHP credit VaR must exceed expected loss and remain <= (1 - R)."""
    res = one_factor_gaussian_copula_loss(PORTFOLIO_PD_5Y, RECOVERY_RATE, RHO)
    var99 = res["lhp_var_99"]
    assert var99 > res["expected_loss"], f"99% VaR ({var99}) must exceed expected loss ({res['expected_loss']})"
    assert var99 <= (1.0 - RECOVERY_RATE) + 1e-9, f"99% VaR cannot exceed maximum possible loss {1.0 - RECOVERY_RATE}"


# ============================================================================
# 5. CDO Tranche Pricing & Student-t Tail Dependence Tests
# ============================================================================


def test_cdo_tranche_loss_bounds_and_partition() -> None:
    """Expected tranche loss fraction must be in [0, 1] and positive."""
    res = price_cdo_tranche(
        TEST_ATTACHMENT,
        TEST_DETACHMENT,
        PORTFOLIO_PD_5Y,
        RECOVERY_RATE,
        RHO,
        r=RISK_FREE_RATE,
        tenor=5.0,
    )
    el = res["expected_tranche_loss_final"]
    assert 0.0 <= el <= 1.0, f"Expected tranche loss {el} outside [0, 1]"
    assert res["premium_leg_pv"] > 0.0, "Premium leg PV must be positive"
    assert res["protection_leg_pv"] >= 0.0, "Protection leg PV must be non-negative"


def test_cdo_tranche_spread_monotonicity() -> None:
    """Equity tranche (0-3%) must have much higher spread than senior tranche (15-30%)."""
    res_eq = price_cdo_tranche(0.0, 0.03, PORTFOLIO_PD_5Y, RECOVERY_RATE, RHO, r=RISK_FREE_RATE)
    res_sn = price_cdo_tranche(0.15, 0.30, PORTFOLIO_PD_5Y, RECOVERY_RATE, RHO, r=RISK_FREE_RATE)
    assert res_eq["break_even_spread_bps"] > res_sn["break_even_spread_bps"] * 5.0, (
        "Equity tranche spread must significantly exceed senior tranche spread"
    )


def test_student_t_tail_dependence_spread_widening() -> None:
    """Under Student-t copula, senior tranche (15-30%) expected loss must exceed Gaussian copula."""
    res_gauss = price_cdo_tranche(
        0.15, 0.30, PORTFOLIO_PD_5Y, RECOVERY_RATE, RHO, r=RISK_FREE_RATE, copula_type="gaussian"
    )
    res_t = price_cdo_tranche(
        0.15,
        0.30,
        PORTFOLIO_PD_5Y,
        RECOVERY_RATE,
        RHO,
        r=RISK_FREE_RATE,
        copula_type="student_t",
        df_t=STUDENT_T_DF,
    )
    # Joint tail default clustering in Student-t copula increases senior tranche expected loss
    t_loss = res_t["expected_tranche_loss_final"]
    gauss_loss = res_gauss["expected_tranche_loss_final"]
    assert t_loss > gauss_loss * 1.5, f"Student-t senior loss ({t_loss}) should exceed Gaussian ({gauss_loss})"


def test_student_t_equity_tranche_loss_compression() -> None:
    """Under Student-t copula, equity tranche (0-3%) expected loss is compressed vs Gaussian."""
    res_gauss = price_cdo_tranche(
        0.0, 0.03, PORTFOLIO_PD_5Y, RECOVERY_RATE, RHO, r=RISK_FREE_RATE, copula_type="gaussian"
    )
    res_t = price_cdo_tranche(
        0.0,
        0.03,
        PORTFOLIO_PD_5Y,
        RECOVERY_RATE,
        RHO,
        r=RISK_FREE_RATE,
        copula_type="student_t",
        df_t=STUDENT_T_DF,
    )
    # Fat tails concentrate defaults into fewer massive crash states, lowering equity tranche expected loss
    t_eq = res_t["expected_tranche_loss_final"]
    gauss_eq = res_gauss["expected_tranche_loss_final"]
    assert t_eq < gauss_eq, f"Student-t equity loss ({t_eq}) should be less than Gaussian ({gauss_eq})"


# ============================================================================
# 6. Correlation Skew and Base Correlation Curve Tests
# ============================================================================


def test_correlation_skew_base_correlation_monotonicity() -> None:
    """Base correlation curve must be monotonically increasing with detachment point (correlation skew)."""
    skew_res = base_correlation_and_skew_analysis(PORTFOLIO_PD_5Y, RECOVERY_RATE, r=RISK_FREE_RATE)
    base_rhos = skew_res["base_correlations"]
    assert len(base_rhos) >= 4, "Must compute base correlations for standard tranches"
    for i in range(len(base_rhos) - 1):
        assert base_rhos[i] <= base_rhos[i + 1] + 1e-6, (
            f"Base correlation must increase with strike: rho(K{i})={base_rhos[i]} > rho(K{i + 1})={base_rhos[i + 1]}"
        )
    assert skew_res["skew_slope"] > 0.0, "Base correlation skew slope must be strictly positive"

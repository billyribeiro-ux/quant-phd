"""Acceptance test suite for CF7: Financial Modeling & Reconciler.

Tests model structure, accounting articulation, debt schedule and revolver circularity,
DCF valuation, sensitivity analysis, and automated model integrity checks.
"""

from __future__ import annotations

import copy
import math
import os

import model_reconciler as learner  # type: ignore[import-not-found, unused-ignore]
import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INSTANCE = make_instance(SEED)


# -----------------------------------------------------------------------------
# 1. Input Validation Tests
# -----------------------------------------------------------------------------


def test_input_validation_tax_rate() -> None:
    bad = copy.deepcopy(INSTANCE)
    bad["operating_assumptions"]["tax_rate"] = 1.05
    with pytest.raises(ValueError, match="tax_rate"):
        learner.build_model(bad)


def test_input_validation_negative_growth() -> None:
    bad = copy.deepcopy(INSTANCE)
    bad["operating_assumptions"]["revenue_growth"][0] = -1.20
    with pytest.raises(ValueError, match="revenue_growth"):
        learner.build_model(bad)


def test_input_validation_wacc() -> None:
    bad = copy.deepcopy(INSTANCE)
    bad["valuation_assumptions"]["wacc"] = -0.05
    with pytest.raises(ValueError, match="wacc"):
        learner.build_model(bad)


def test_input_validation_terminal_growth_exceeds_wacc() -> None:
    bad = copy.deepcopy(INSTANCE)
    bad["valuation_assumptions"]["terminal_growth_rate"] = 0.15
    bad["valuation_assumptions"]["wacc"] = 0.10
    with pytest.raises(ValueError, match="terminal_growth_rate"):
        learner.build_model(bad)


def test_input_validation_negative_shares() -> None:
    bad = copy.deepcopy(INSTANCE)
    bad["valuation_assumptions"]["shares_outstanding"] = 0.0
    with pytest.raises(ValueError, match="shares_outstanding"):
        learner.build_model(bad)


# -----------------------------------------------------------------------------
# 2. Three-Statement Articulation & Accounting Invariants
# -----------------------------------------------------------------------------


def test_balance_sheet_balances() -> None:
    """Assets == Liabilities + Equity across all forecast periods to 1e-4 tolerance."""
    res = learner.build_model(INSTANCE)
    bs = res["balance_sheet"]
    assets = bs["total_assets"]
    liab = bs["total_liabilities"]
    equity = bs["total_equity"]

    assert len(assets) == INSTANCE["horizon"]
    for t in range(len(assets)):
        gap = abs(assets[t] - (liab[t] + equity[t]))
        assert gap < 1e-4, f"Balance sheet does not balance in period {t + 1}: gap={gap}"


def test_retained_earnings_corkscrew() -> None:
    """RE_t == RE_{t-1} + NI_t - Div_t."""
    res = learner.build_model(INSTANCE)
    re_list = res["balance_sheet"]["retained_earnings"]
    ni_list = res["income_statement"]["net_income"]
    div_list = res["cash_flow_statement"]["dividends"]

    prev_re = INSTANCE["historical_data"]["retained_earnings"]
    for t in range(len(re_list)):
        expected_re = prev_re + ni_list[t] - div_list[t]
        assert abs(re_list[t] - expected_re) < 1e-4, f"Retained earnings roll-forward failed in period {t + 1}"
        prev_re = re_list[t]


def test_net_ppe_corkscrew() -> None:
    """PP&E_t == PP&E_{t-1} + CapEx_t - Depr_t."""
    res = learner.build_model(INSTANCE)
    ppe_list = res["balance_sheet"]["net_ppe"]
    capex_list = res["cash_flow_statement"]["capex"]
    depr_list = res["income_statement"]["depreciation"]

    prev_ppe = INSTANCE["historical_data"]["net_ppe"]
    for t in range(len(ppe_list)):
        expected_ppe = prev_ppe + capex_list[t] - depr_list[t]
        assert abs(ppe_list[t] - expected_ppe) < 1e-4, f"Net PP&E roll-forward failed in period {t + 1}"
        prev_ppe = ppe_list[t]


def test_cash_flow_statement_tie_out() -> None:
    """Ending cash on Cash Flow Statement matches Balance Sheet cash exactly."""
    res = learner.build_model(INSTANCE)
    cfs_cash = res["cash_flow_statement"]["ending_cash"]
    bs_cash = res["balance_sheet"]["cash"]
    beg_cash = res["cash_flow_statement"]["beginning_cash"]
    net_flow = res["cash_flow_statement"]["net_change_in_cash"]

    prev = INSTANCE["historical_data"]["cash"]
    for t in range(len(cfs_cash)):
        assert abs(beg_cash[t] - prev) < 1e-4
        assert abs(cfs_cash[t] - (beg_cash[t] + net_flow[t])) < 1e-4
        assert abs(cfs_cash[t] - bs_cash[t]) < 1e-4
        prev = cfs_cash[t]


def test_cash_flow_from_operations_articulation() -> None:
    """CFO == Net Income + Depreciation - Delta AR - Delta Inv + Delta AP."""
    res = learner.build_model(INSTANCE)
    cfs = res["cash_flow_statement"]
    ni = cfs["net_income"]
    depr = cfs["depreciation"]
    d_ar = cfs["delta_ar"]
    d_inv = cfs["delta_inventory"]
    d_ap = cfs["delta_ap"]
    cfo = cfs["cash_from_operations"]

    for t in range(len(cfo)):
        expected_cfo = ni[t] + depr[t] - d_ar[t] - d_inv[t] + d_ap[t]
        assert abs(cfo[t] - expected_cfo) < 1e-4


# -----------------------------------------------------------------------------
# 3. Debt Schedule & Revolver Circularity
# -----------------------------------------------------------------------------


def test_revolver_closed_form_matches_fixed_point_iteration() -> None:
    """The closed form for revolver circularity matches iterative fixed-point convergence."""
    c_min = 25.0
    c_prev = 20.0
    r_prev = 15.0
    ebit = 40.0
    term_int = 4.0
    depr = 10.0
    delta_nwc = 5.0
    capex = 18.0
    term_amort = 6.0
    tax_rate = 0.25
    r_rate = 0.075
    c_rate = 0.02
    div_rate = 0.15
    max_rev = 100.0

    alpha = (1.0 - div_rate) * (1.0 - tax_rate)
    cf_core = alpha * (ebit - term_int) + depr - delta_nwc - capex - term_amort
    r_closed, c_closed, _d_closed = learner.solve_revolver_circularity(
        c_min=c_min,
        c_prev=c_prev,
        r_prev=r_prev,
        cf_core=cf_core,
        r_rate=r_rate,
        c_rate=c_rate,
        tax_rate=tax_rate,
        max_revolver=max_rev,
        div_rate=div_rate,
    )

    # Run iterative solver
    r_iter = r_prev
    for _ in range(50):
        r_bar = 0.5 * (r_prev + r_iter)
        c_bar = 0.5 * (c_prev + c_min)
        net_int = term_int + r_rate * r_bar - c_rate * c_bar
        ebt = ebit - net_int
        tax = tax_rate * max(0.0, ebt)
        ni = ebt - tax
        div = div_rate * ni
        cfo = ni + depr - delta_nwc
        cfi = -capex
        cff = -term_amort - div + (r_iter - r_prev)
        c_next = c_prev + cfo + cfi + cff
        # Update r_iter to restore c_next to c_min
        r_iter = r_iter + (c_min - c_next)

    assert abs(r_closed - r_iter) < 1e-6
    assert abs(c_closed - c_min) < 1e-6


def test_revolver_non_negative() -> None:
    """Revolver balance never drops below zero."""
    res = learner.build_model(INSTANCE)
    revolver_balances = res["balance_sheet"]["revolver_balance"]
    for r in revolver_balances:
        assert r >= -1e-8


def test_interest_expense_matches_average_debt() -> None:
    """Interest expense is calculated on average debt balances across the period."""
    res = learner.build_model(INSTANCE)
    term_rate = INSTANCE["debt_assumptions"]["term_debt_interest_rate"]
    revolver_rate = INSTANCE["debt_assumptions"]["revolver_interest_rate"]

    ds = res["debt_schedule"]
    term_beg = ds["term_debt_opening"]
    term_end = ds["term_debt_closing"]
    rev_beg = ds["revolver_opening"]
    rev_end = ds["revolver_closing"]
    int_exp = res["income_statement"]["interest_expense"]

    for t in range(len(int_exp)):
        term_avg = 0.5 * (term_beg[t] + term_end[t])
        rev_avg = 0.5 * (rev_beg[t] + rev_end[t])
        expected_int = term_avg * term_rate + rev_avg * revolver_rate
        assert abs(int_exp[t] - expected_int) < 1e-4, (
            f"Interest expense period {t + 1} did not match average debt calculation"
        )


# -----------------------------------------------------------------------------
# 4. DCF Valuation & Sensitivity Analysis
# -----------------------------------------------------------------------------


def test_fcff_calculation() -> None:
    """FCFF == EBIT*(1 - tax) + Depr - CapEx - Delta NWC."""
    res = learner.build_model(INSTANCE)
    is_stmt = res["income_statement"]
    cfs = res["cash_flow_statement"]
    dcf = res["dcf_valuation"]

    tax_rate = INSTANCE["operating_assumptions"]["tax_rate"]
    for t in range(len(dcf["fcff"])):
        nopat = is_stmt["ebit"][t] * (1.0 - tax_rate)
        delta_nwc = cfs["delta_ar"][t] + cfs["delta_inventory"][t] - cfs["delta_ap"][t]
        expected_fcff = nopat + is_stmt["depreciation"][t] - cfs["capex"][t] - delta_nwc
        assert abs(dcf["fcff"][t] - expected_fcff) < 1e-4


def test_enterprise_to_equity_bridge() -> None:
    """Equity Value == Enterprise Value - (Total Debt - Cash)."""
    res = learner.build_model(INSTANCE)
    dcf = res["dcf_valuation"]
    ev = dcf["enterprise_value"]
    net_debt = dcf["net_debt"]
    eq_val = dcf["equity_value"]
    shares = dcf["shares_outstanding"]
    eq_per_share = dcf["equity_value_per_share"]

    assert abs(eq_val - (ev - net_debt)) < 1e-4
    assert abs(eq_per_share - (eq_val / shares)) < 1e-4


def test_discount_factors_decay_monotonically() -> None:
    res = learner.build_model(INSTANCE)
    dfs = res["dcf_valuation"]["discount_factors"]
    for t in range(len(dfs) - 1):
        assert dfs[t] > dfs[t + 1]


def test_sensitivity_monotonicity() -> None:
    """Higher WACC decreases equity value; higher terminal g increases equity value."""
    res = learner.build_model(INSTANCE)
    sens = res["sensitivities"]
    matrix = sens["equity_value_per_share"]

    # Check along rows (increasing g for fixed WACC)
    for row in matrix:
        for j in range(len(row) - 1):
            if not math.isnan(row[j]) and not math.isnan(row[j + 1]):
                assert row[j + 1] > row[j], f"Valuation not strictly increasing in terminal growth: {row}"

    # Check along columns (increasing WACC for fixed g)
    for col_idx in range(len(matrix[0])):
        for i in range(len(matrix) - 1):
            val1 = matrix[i][col_idx]
            val2 = matrix[i + 1][col_idx]
            if not math.isnan(val1) and not math.isnan(val2):
                assert val2 < val1, (
                    f"Valuation not strictly decreasing in WACC: col={col_idx}, row {i}={val1}, row {i + 1}={val2}"
                )


# -----------------------------------------------------------------------------
# 5. Integrity & Reconciliation Audits
# -----------------------------------------------------------------------------


def test_model_integrity_flags_passed() -> None:
    res = learner.build_model(INSTANCE)
    integrity = res["integrity"]
    assert integrity["balance_check_passed"] is True
    assert integrity["cash_tie_out_passed"] is True
    assert integrity["max_bs_imbalance"] < 1e-4
    assert integrity["max_cash_discrepancy"] < 1e-4


def test_reconciliation_detects_mismatch() -> None:
    res = learner.build_model(INSTANCE)
    corrupted = copy.deepcopy(res)
    # Inject 5% discrepancy into period 1 net income
    corrupted["income_statement"]["net_income"][0] *= 1.05

    audit = learner.reconcile_sheets(corrupted, res, tolerance=1e-4)
    assert audit["passed"] is False
    assert len(audit["discrepancies"]) >= 1
    disc = audit["discrepancies"][0]
    assert disc["line_item"] == "net_income"


def test_hardcode_detection() -> None:
    clean_formulas = {
        "B5": "=B3*B4",
        "C5": "=C3*C4",
        "B10": "=(B8+B9)/2",
        "B12": "=B11*365",
    }
    violations_clean = learner.check_hardcodes(clean_formulas)
    assert len(violations_clean) == 0

    dirty_formulas = {
        "B5": "=B3*0.25",  # Hard-coded tax rate 0.25
        "C5": "=C3*1.08",  # Hard-coded growth rate 1.08
    }
    violations_dirty = learner.check_hardcodes(dirty_formulas)
    assert len(violations_dirty) == 2

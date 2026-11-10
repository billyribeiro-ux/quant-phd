"""Test suite for CAP0: Integrated Corporate Finance and Equity Case."""

from __future__ import annotations

import math
import os
from typing import Any, cast

import pytest
from capstone_engine import (
    audit_forensic_quality,
    compute_dynamic_dcf,
    design_hedging_program,
    forecast_three_statements,
    optimize_capital_and_liquidity,
    simulate_board_scenarios,
)
from instance import make_instance

SEED = int(os.environ.get("QF_SEED", "0"))


@pytest.fixture(scope="module")
def inst() -> dict[str, Any]:
    """Generate instance dataset for active seed."""
    return make_instance(SEED)


@pytest.fixture(scope="module")
def forecast(inst: dict[str, Any]) -> dict[str, Any]:
    """Reconstruct integrated three-statement financial forecast."""
    return cast(dict[str, Any], forecast_three_statements(inst))


@pytest.fixture(scope="module")
def dcf(inst: dict[str, Any], forecast: dict[str, Any]) -> dict[str, Any]:
    """Compute baseline discounted cash flow valuation."""
    return cast(dict[str, Any], compute_dynamic_dcf(inst, forecast))


def test_balance_sheet_articulation(forecast: dict[str, Any]) -> None:
    """Verify that balance sheet articulates with zero gap across all forecast years."""
    assert forecast["is_articulated"] is True
    gaps: list[float] = forecast["balance_sheet"]["articulation_gap"]
    assert len(gaps) == 5
    for t, gap in enumerate(gaps, start=1):
        assert abs(gap) < 1e-6, f"Balance sheet articulation violated in year {t} with gap {gap:.8f}"


def test_cash_flow_continuity(forecast: dict[str, Any]) -> None:
    """Verify that delta cash equals the sum of CFO, CFI, and CFF across all years."""
    cf: dict[str, list[float]] = forecast["cash_flow"]
    bs: dict[str, list[float]] = forecast["balance_sheet"]

    cfo = cf["cfo"]
    cfi = cf["cfi"]
    cff = cf["cff"]
    delta_cash = cf["delta_cash"]
    cash = bs["cash"]

    for t in range(len(delta_cash)):
        sum_components = cfo[t] + cfi[t] + cff[t]
        assert abs(delta_cash[t] - sum_components) < 1e-6, f"Cash flow continuity failure in year {t + 1}"

    for t in range(1, len(cash)):
        assert abs((cash[t] - cash[t - 1]) - delta_cash[t]) < 1e-6, (
            f"Cash balance roll-forward mismatch in year {t + 1}"
        )


def test_forensic_audit_and_beneish(inst: dict[str, Any]) -> None:
    """Verify Sloan accruals ratio and 8-variable Beneish M-Score calculations."""
    audit = audit_forensic_quality(inst)
    assert "sloan_accruals" in audit
    assert "sloan_ratio" in audit
    assert "beneish_m_score" in audit
    assert "manipulation_flag" in audit

    indices = audit["indices"]
    expected_keys = {"dsri", "gmi", "aqi", "sgi", "depi", "sgai", "lvgi", "tata"}
    assert set(indices.keys()) == expected_keys

    # Check that indices are strictly positive and finite
    for k, val in indices.items():
        assert isinstance(val, (int, float))
        assert not math.isnan(val), f"Index {k} is NaN"

    m_score = audit["beneish_m_score"]
    assert -10.0 < m_score < 10.0, f"Unreasonable Beneish M-Score: {m_score}"
    assert audit["manipulation_flag"] == (m_score > -1.78)


def test_dynamic_dcf_valuation(dcf: dict[str, Any], inst: dict[str, Any]) -> None:
    """Verify dynamic WACC, positive enterprise value, and coherent share price target."""
    ev = float(dcf["enterprise_value"])
    pv_explicit = float(dcf["pv_explicit"])
    pv_tv = float(dcf["pv_terminal_value"])
    eq_val = float(dcf["equity_value"])
    target_price = float(dcf["share_price_target"])

    assert ev > 0.0, "Enterprise value must be positive"
    assert abs(ev - (pv_explicit + pv_tv)) < 1e-6, "EV must equal PV(explicit) + PV(terminal)"
    assert eq_val > 0.0, "Equity value must be positive"
    assert target_price > 0.0, "Target share price must be positive"

    # WACC and Beta invariants
    beta_u = float(inst["beta_u"])
    beta_l_series: list[float] = dcf["beta_levered_series"]
    assert all(b >= beta_u for b in beta_l_series), (
        "Levered beta must strictly exceed or equal unlevered beta for levered firm"
    )

    wacc_series: list[float] = dcf["wacc_series"]
    assert all(0.04 <= w <= 0.18 for w in wacc_series), "WACC path out of reasonable corporate bounds"


def test_capital_structure_optimization_and_liquidity(inst: dict[str, Any], forecast: dict[str, Any]) -> None:
    """Verify trade-off theory concave optimum and debt covenant compliance."""
    cs = optimize_capital_and_liquidity(inst, forecast)
    assert 0.10 <= cs["optimal_leverage"] <= 0.75, "Optimal leverage must lie in interior range"
    assert cs["max_levered_value"] >= cs["unlevered_value"], "Levered value must exceed or equal unlevered value"
    assert cs["trade_off_gain"] >= 0.0, "Tax shield gain net of distress must be non-negative"

    # Covenant and liquidity metrics
    assert cs["year1_icr"] > 0.0, "ICR must be positive"
    assert cs["min_cash_buffer"] > 0.0, "Precautionary cash buffer must be positive"
    assert 0.0 <= cs["max_ebitda_drawdown_pct"] <= 1.0, "EBITDA drawdown fraction must be in [0, 1]"


def test_hedging_program_architecture(inst: dict[str, Any]) -> None:
    """Verify minimum-variance hedge ratio and ASC 815 effectiveness conditions."""
    h = design_hedging_program(inst)
    h_star = float(h["h_star"])
    r_squared = float(h["r_squared"])
    var_unhedged = float(h["unhedged_variance"])
    var_hedged = float(h["hedged_variance"])
    var_pct = float(h["variance_reduction_pct"])

    assert 0.50 <= h_star <= 1.50, f"Hedge ratio {h_star} out of expected range"
    assert 0.0 <= r_squared <= 1.0, f"R^2 must be in [0, 1], got {r_squared}"
    assert var_hedged <= var_unhedged, "Hedged variance cannot exceed unhedged variance"
    assert abs(var_pct - r_squared) < 1e-4, "Variance reduction percentage must equal R^2"
    assert h["var_reduction_dollar"] > 0.0, "Hedging must deliver positive dollar VaR savings"


def test_board_scenario_monotonicity(inst: dict[str, Any], dcf: dict[str, Any]) -> None:
    """Verify monotonicity of scenario targets: Bull > Base > Bear."""
    scenarios = simulate_board_scenarios(inst, dcf)
    p_bull = float(scenarios["bull_target_price"])
    p_base = float(scenarios["base_target_price"])
    p_bear = float(scenarios["bear_target_price"])
    p_weighted = float(scenarios["weighted_target_price"])

    assert p_bull > p_base > p_bear, f"Scenario monotonicity violated: Bull {p_bull} > Base {p_base} > Bear {p_bear}"
    assert p_bear <= p_weighted <= p_bull, "Weighted target must lie between Bear and Bull"
    assert scenarios["margin_of_safety_pct"] >= 0.0, "Margin of safety cannot be negative"

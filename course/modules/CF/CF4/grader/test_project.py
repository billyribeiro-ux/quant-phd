"""Acceptance test suite for Atlas A16 Valuation Engine (atlas.valuation).

Tests exact financial identities, DCF monotonicity, Ohlson residual income,
bridge consistency, and sensitivity grids across seeded test cases.
"""

from __future__ import annotations

import math
import os
from collections.abc import Sequence
from typing import Any, cast

import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]

try:
    from atlas.valuation import (  # type: ignore[import-not-found, unused-ignore]
        calculate_fcff,
        dcf_enterprise_value,
        enterprise_to_equity_bridge,
        multiples_valuation,
        residual_income_valuation,
        scenario_valuation,
        sensitivity_grid_2d,
    )
except ImportError:
    try:
        from valuation import (  # type: ignore[import-not-found, unused-ignore]
            calculate_fcff,
            dcf_enterprise_value,
            enterprise_to_equity_bridge,
            multiples_valuation,
            residual_income_valuation,
            scenario_valuation,
            sensitivity_grid_2d,
        )
    except ImportError:
        from reference import (  # type: ignore[import-not-found, unused-ignore]
            calculate_fcff,
            dcf_enterprise_value,
            enterprise_to_equity_bridge,
            multiples_valuation,
            residual_income_valuation,
            scenario_valuation,
            sensitivity_grid_2d,
        )


@pytest.fixture(scope="module")
def seed() -> int:
    return int(os.environ.get("QF_SEED", "0"))


@pytest.fixture(scope="module")
def inst(seed: int) -> dict[str, Any]:
    return cast(dict[str, Any], make_instance(seed))


# --- 1. FCFF Tests ---


def test_fcff_hand_value() -> None:
    # EBIT = 200.0, tax = 0.25 -> NOPAT = 150.0
    # D&A = 40.0, CapEx = 60.0, Delta NWC = 15.0
    # FCFF = 150.0 + 40.0 - 60.0 - 15.0 = 115.0
    res = calculate_fcff(
        ebit=200.0,
        tax_rate=0.25,
        depreciation=40.0,
        capex=60.0,
        delta_nwc=15.0,
    )
    assert abs(res - 115.0) < 1e-9


def test_fcff_instance_matches(inst: dict[str, Any]) -> None:
    ebits = inst["ebits"]
    tax_rate = float(inst["tax_rate"])
    deprs = inst["depreciations"]
    capexs = inst["capexs"]
    dnwcs = inst["delta_nwcs"]
    expected_fcffs = cast(Sequence[Any], inst["fcffs"])

    fcff_computed = cast(Sequence[Any], calculate_fcff(ebits, tax_rate, deprs, capexs, dnwcs))
    for comp, exp in zip(list(fcff_computed), list(expected_fcffs), strict=True):
        assert abs(float(comp) - float(exp)) < 1e-4


def test_fcff_validation_errors() -> None:
    with pytest.raises(ValueError):
        calculate_fcff(100.0, tax_rate=-0.1, depreciation=10.0, capex=10.0, delta_nwc=5.0)
    with pytest.raises(ValueError):
        calculate_fcff(100.0, tax_rate=1.0, depreciation=10.0, capex=10.0, delta_nwc=5.0)
    with pytest.raises(ValueError):
        calculate_fcff(100.0, tax_rate=0.25, depreciation=-5.0, capex=10.0, delta_nwc=5.0)
    with pytest.raises(ValueError):
        calculate_fcff(100.0, tax_rate=0.25, depreciation=10.0, capex=-2.0, delta_nwc=5.0)


# --- 2. DCF Enterprise Value Tests ---


def test_dcf_hand_value_gordon() -> None:
    # 3 periods: FCFF = [100.0, 110.0, 120.0]
    # WACC = 10% (0.10), g = 2% (0.02)
    # df1 = 1/1.1 = 0.9090909
    # df2 = 1/1.21 = 0.8264463
    # df3 = 1/1.331 = 0.7513148
    # PV explicit = 100*0.9090909 + 110*0.8264463 + 120*0.7513148 = 90.90909 + 90.90909 + 90.15778 = 271.97596
    # TV3 = 120 * 1.02 / (0.10 - 0.02) = 122.4 / 0.08 = 1530.0
    # PV(TV3) = 1530.0 / 1.331 = 1149.51165
    # Total EV = 271.97596 + 1149.51165 = 1421.4876
    res = dcf_enterprise_value([100.0, 110.0, 120.0], wacc=0.10, terminal_method="gordon", terminal_growth=0.02)
    assert abs(res["pv_explicit"] - 271.9759579) < 1e-4
    assert abs(res["terminal_value"] - 1530.0) < 1e-4
    assert abs(res["pv_terminal"] - 1149.511645) < 1e-4
    assert abs(res["enterprise_value"] - 1421.48760) < 1e-4


def test_dcf_hand_value_exit_multiple() -> None:
    # Exit multiple = 10.0x on terminal metric (e.g. EBITDA = 150.0)
    # TV3 = 1500.0
    # PV(TV3) at 10% = 1500.0 / 1.331 = 1126.9722
    res = dcf_enterprise_value(
        [100.0, 110.0, 120.0],
        wacc=0.10,
        terminal_method="exit_multiple",
        exit_multiple=10.0,
        terminal_metric=150.0,
    )
    assert abs(res["terminal_value"] - 1500.0) < 1e-4
    assert abs(res["pv_terminal"] - 1126.9722) < 1e-4


def test_dcf_mid_year_higher_pv() -> None:
    cfs = [100.0, 110.0, 120.0, 130.0, 140.0]
    res_yearend = dcf_enterprise_value(cfs, wacc=0.09, terminal_growth=0.025, mid_year=False)
    res_midyear = dcf_enterprise_value(cfs, wacc=0.09, terminal_growth=0.025, mid_year=True)
    # Mid-year discounting discounts by (t - 0.5) instead of t, so PV of explicit cash flows must be strictly higher
    assert res_midyear["pv_explicit"] > res_yearend["pv_explicit"]
    # Ratio of explicit PVs should be approximately sqrt(1 + WACC) = sqrt(1.09) = 1.04403
    expected_ratio = math.sqrt(1.09)
    actual_ratio = res_midyear["pv_explicit"] / res_yearend["pv_explicit"]
    assert abs(actual_ratio - expected_ratio) < 1e-4


def test_dcf_monotonicity_wacc(inst: dict[str, Any]) -> None:
    fcffs = inst["fcffs"]
    g = float(inst["terminal_growth"])

    ev_low_wacc = dcf_enterprise_value(fcffs, wacc=0.08, terminal_growth=g)["enterprise_value"]
    ev_high_wacc = dcf_enterprise_value(fcffs, wacc=0.11, terminal_growth=g)["enterprise_value"]
    assert ev_low_wacc > ev_high_wacc


def test_dcf_monotonicity_growth(inst: dict[str, Any]) -> None:
    fcffs = inst["fcffs"]
    wacc = float(inst["wacc"])

    ev_low_g = dcf_enterprise_value(fcffs, wacc=wacc, terminal_growth=0.015)["enterprise_value"]
    ev_high_g = dcf_enterprise_value(fcffs, wacc=wacc, terminal_growth=0.025)["enterprise_value"]
    assert ev_high_g > ev_low_g


def test_dcf_growth_equals_or_exceeds_wacc_raises() -> None:
    with pytest.raises(ValueError):
        dcf_enterprise_value([100.0], wacc=0.05, terminal_growth=0.05)
    with pytest.raises(ValueError):
        dcf_enterprise_value([100.0], wacc=0.05, terminal_growth=0.06)


# --- 3. Enterprise to Equity Bridge Tests ---


def test_bridge_hand_values() -> None:
    # EV = 1000.0, Total Debt = 300.0, Cash = 50.0
    # Net Debt = 250.0
    # Minority interest = 20.0, Preferred = 30.0, Non-operating assets = 40.0
    # Equity Value = 1000.0 - 300.0 + 50.0 - 20.0 - 30.0 + 40.0 = 740.0
    # Shares = 74.0 -> Per share = 10.00
    res = enterprise_to_equity_bridge(
        enterprise_value=1000.0,
        total_debt=300.0,
        cash=50.0,
        minority_interest=20.0,
        preferred_stock=30.0,
        non_operating_assets=40.0,
        shares_outstanding=74.0,
    )
    assert abs(res["net_debt"] - 250.0) < 1e-9
    assert abs(res["equity_value"] - 740.0) < 1e-9
    assert abs(res["per_share_value"] - 10.00) < 1e-9


def test_bridge_negative_values_raise() -> None:
    with pytest.raises(ValueError):
        enterprise_to_equity_bridge(1000.0, total_debt=-10.0, cash=50.0)
    with pytest.raises(ValueError):
        enterprise_to_equity_bridge(1000.0, total_debt=100.0, cash=-5.0)
    with pytest.raises(ValueError):
        enterprise_to_equity_bridge(1000.0, total_debt=100.0, cash=50.0, shares_outstanding=0.0)


# --- 4. Residual Income Valuation Tests ---


def test_residual_income_hand_values() -> None:
    # B0 = 100.0, r_e = 10%
    # NI = [15.0, 18.0]
    # Div = [5.0, 6.0]
    # t=1: Normal return = 10% * 100 = 10.0 -> RI1 = 15.0 - 10.0 = 5.0
    #      PV(RI1) = 5.0 / 1.1 = 4.545455
    #      B1 = 100 + 15 - 5 = 110.0
    # t=2: Normal return = 10% * 110 = 11.0 -> RI2 = 18.0 - 11.0 = 7.0
    #      PV(RI2) = 7.0 / 1.21 = 5.785124
    #      B2 = 110 + 18 - 6 = 122.0
    # Explicit PV(RI) = 4.545455 + 5.785124 = 10.330579
    # With omega = 0.0 (terminal RI disappears):
    # Total Equity Value = B0 + PV(RI) = 100.0 + 10.330579 = 110.330579
    res = residual_income_valuation(
        initial_book_equity=100.0,
        net_income_forecast=[15.0, 18.0],
        dividends_forecast=[5.0, 6.0],
        cost_of_equity=0.10,
        omega=0.0,
    )
    assert abs(res["book_values"][0] - 100.0) < 1e-9
    assert abs(res["book_values"][1] - 110.0) < 1e-9
    assert abs(res["book_values"][2] - 122.0) < 1e-9
    assert abs(res["residual_income"][0] - 5.0) < 1e-9
    assert abs(res["residual_income"][1] - 7.0) < 1e-9
    assert abs(res["pv_residual_income"] - 10.330579) < 1e-4
    assert abs(res["equity_value"] - 110.330579) < 1e-4


def test_residual_income_clean_surplus_identity() -> None:
    # When terminal growth g and terminal payout articulate clean surplus,
    # dividend DCF must exactly equal Ohlson residual income.
    b0 = 200.0
    earnings = [30.0, 35.0, 40.0]
    dividends = [10.0, 12.0, 15.0]
    r_e = 0.10

    # Explicit calculation of dividends and residual income
    # t=1: b1 = 200 + 30 - 10 = 220, ri1 = 30 - 0.10*200 = 10.0
    # t=2: b2 = 220 + 35 - 12 = 243, ri2 = 35 - 0.10*220 = 13.0
    # t=3: b3 = 243 + 40 - 15 = 268, ri3 = 40 - 0.10*243 = 15.7
    res_ri = residual_income_valuation(b0, earnings, dividends, cost_of_equity=r_e, omega=0.0)
    assert abs(res_ri["book_values"][-1] - 268.0) < 1e-9

    # Finite horizon equivalence with liquidating dividend:
    # If the firm liquidates at t=3 paying out B3, dividend DCF equals:
    # PV(div1, div2, div3 + B3)
    pv_divs = 10.0 / 1.1 + 12.0 / (1.1**2) + (15.0 + 268.0) / (1.1**3)
    # Ohlson gives B0 + PV(RI1, RI2, RI3)
    pv_ri = 10.0 / 1.1 + 13.0 / (1.1**2) + 15.7 / (1.1**3)
    v_ohlson = b0 + pv_ri

    assert abs(pv_divs - v_ohlson) < 1e-6


# --- 5. Multiples Valuation Tests ---


def test_multiples_valuation_ev_ebitda() -> None:
    # EBITDA = 80.0, Multiple = 12.5x -> Implied EV = 1000.0
    # Net Debt = 250.0 -> Implied Equity = 750.0
    # Shares = 75.0 -> Per share = 10.00
    res = multiples_valuation(80.0, 12.5, multiple_type="ev_ebitda", net_debt=250.0, shares_outstanding=75.0)
    assert abs(res["implied_enterprise_value"] - 1000.0) < 1e-9
    assert abs(res["implied_equity_value"] - 750.0) < 1e-9
    assert abs(res["implied_per_share_value"] - 10.00) < 1e-9


def test_multiples_valuation_pe() -> None:
    # Net Income = 50.0, P/E Multiple = 20.0x -> Implied Equity = 1000.0
    # Net Debt = 200.0 -> Implied EV = 1200.0
    # Shares = 50.0 -> Per share = 20.00
    res = multiples_valuation(50.0, 20.0, multiple_type="pe", net_debt=200.0, shares_outstanding=50.0)
    assert abs(res["implied_equity_value"] - 1000.0) < 1e-9
    assert abs(res["implied_enterprise_value"] - 1200.0) < 1e-9
    assert abs(res["implied_per_share_value"] - 20.00) < 1e-9


# --- 6. Sensitivity Grid Tests ---


def test_sensitivity_grid_dimensions_and_properties(inst: dict[str, Any]) -> None:
    fcffs = inst["fcffs"]
    wacc_range = inst["wacc_range"]
    growth_range = inst["growth_range"]
    debt = float(inst["total_debt"])
    cash = float(inst["cash"])
    shares = float(inst["shares_outstanding"])

    res = sensitivity_grid_2d(
        fcffs,
        wacc_range,
        growth_range,
        total_debt=debt,
        cash=cash,
        shares_outstanding=shares,
    )

    grid = res["grid"]
    assert len(grid) == len(wacc_range)
    assert len(grid[0]) == len(growth_range)

    # Check monotonicity along column (higher WACC -> lower per share value)
    for col in range(len(growth_range)):
        for row in range(len(wacc_range) - 1):
            val_upper = grid[row][col]
            val_lower = grid[row + 1][col]
            if not math.isnan(val_upper) and not math.isnan(val_lower):
                assert val_upper > val_lower

    # Check monotonicity along row (higher growth -> higher per share value)
    for row in range(len(wacc_range)):
        for col in range(len(growth_range) - 1):
            val_left = grid[row][col]
            val_right = grid[row][col + 1]
            if not math.isnan(val_left) and not math.isnan(val_right):
                assert val_right > val_left


# --- 7. Scenario Valuation Tests ---


def test_scenario_valuation_expected_values(inst: dict[str, Any]) -> None:
    fcffs = inst["fcffs"]
    bear_fcff = inst["bear_fcff"]
    bull_fcff = inst["bull_fcff"]
    weights = inst["scenario_weights"]
    waccs = inst["scenario_waccs"]
    growths = inst["scenario_growths"]
    debt = float(inst["total_debt"])
    cash = float(inst["cash"])
    net_d = debt - cash
    shares = float(inst["shares_outstanding"])

    scenarios = {
        "bear": {
            "weight": weights[0],
            "fcff_forecast": bear_fcff,
            "wacc": waccs[0],
            "terminal_growth": growths[0],
            "net_debt": net_d,
            "shares_outstanding": shares,
        },
        "base": {
            "weight": weights[1],
            "fcff_forecast": fcffs,
            "wacc": waccs[1],
            "terminal_growth": growths[1],
            "net_debt": net_d,
            "shares_outstanding": shares,
        },
        "bull": {
            "weight": weights[2],
            "fcff_forecast": bull_fcff,
            "wacc": waccs[2],
            "terminal_growth": growths[2],
            "net_debt": net_d,
            "shares_outstanding": shares,
        },
    }
    res = scenario_valuation(scenarios)

    assert "scenario_results" in res
    assert "bear" in res["scenario_results"]
    assert "base" in res["scenario_results"]
    assert "bull" in res["scenario_results"]

    # Bull price target must exceed Base which must exceed Bear
    assert (
        res["scenario_results"]["bull"]["per_share_value"]
        > res["scenario_results"]["base"]["per_share_value"]
        > res["scenario_results"]["bear"]["per_share_value"]
    )

    # Expected value is weighted average
    expected_calc = (
        float(weights[0]) * res["scenario_results"]["bear"]["per_share_value"]
        + float(weights[1]) * res["scenario_results"]["base"]["per_share_value"]
        + float(weights[2]) * res["scenario_results"]["bull"]["per_share_value"]
    )
    assert abs(res["expected_per_share_value"] - expected_calc) < 1e-5


def test_scenario_valuation_bad_weights_raises() -> None:
    bad_scenarios = {
        "s1": {"weight": 0.4, "fcff_forecast": [10.0], "wacc": 0.08, "terminal_growth": 0.02},
        "s2": {"weight": 0.4, "fcff_forecast": [10.0], "wacc": 0.08, "terminal_growth": 0.02},
    }
    with pytest.raises(ValueError):
        scenario_valuation(bad_scenarios)

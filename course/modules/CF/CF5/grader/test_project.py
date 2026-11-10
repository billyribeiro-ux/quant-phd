"""Acceptance test suite for CF5 LBO Model.

Tests Sources & Uses identity, operating cash flow articulation, multi-tranche debt
schedules, cash sweep mechanics, covenant compliance, MOIC/IRR returns, and the
Kaplan-Strömberg value creation attribution identity across seeded instances.
"""

from __future__ import annotations

import os
from typing import Any, cast

import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]

try:
    from lbo_model import (  # type: ignore[import-not-found, unused-ignore]
        build_sources_and_uses,
        calculate_returns_and_attribution,
        evaluate_covenants,
        forecast_operations,
        run_debt_schedule,
        run_lbo_model,
    )
except ImportError:
    from reference import (  # type: ignore[import-not-found, unused-ignore]
        build_sources_and_uses,
        calculate_returns_and_attribution,
        evaluate_covenants,
        forecast_operations,
        run_debt_schedule,
        run_lbo_model,
    )


@pytest.fixture(scope="module")
def seed() -> int:
    return int(os.environ.get("QF_SEED", "0"))


@pytest.fixture(scope="module")
def inst(seed: int) -> dict[str, Any]:
    return cast(dict[str, Any], make_instance(seed))


# --- 1. Sources and Uses Tests ---


def test_sources_and_uses_hand_calc() -> None:
    # EBITDA = 100.0, multiple = 10.0 -> EV = 1000.0
    # existing_debt = 200.0, target_cash = 50.0 -> Equity purchase = 1000 - 200 + 50 = 850.0
    # TLA (3.0x) = 300.0, TLB (2.0x) = 200.0 -> Total debt = 500.0
    # txn_fee_rate = 0.02 -> 20.0, financing_fee_rate = 0.03 -> 15.0
    # min_cash = 25.0
    # Refinance debt = 200.0
    # Total Uses = 850 (equity) + 200 (debt refi) + 20 (txn fee) + 15 (fin fee) + 25 (min cash) = 1110.0
    # Sources: TLA 300 + TLB 200 + Target cash 50 + Rollover 0 = 550.0
    # Sponsor Equity = 1110.0 - 550.0 = 560.0
    # Total Sources = 560 + 550 = 1110.0
    su = build_sources_and_uses(
        ebitda_0=100.0,
        entry_multiple=10.0,
        existing_debt=200.0,
        min_cash=25.0,
        target_cash=50.0,
        txn_fee_rate=0.02,
        financing_fee_rate=0.03,
        tla_leverage=3.0,
        tlb_leverage=2.0,
        rollover_equity=0.0,
    )
    assert abs(su["purchase_enterprise_value"] - 1000.0) < 1e-4
    assert abs(su["equity_purchase_price"] - 850.0) < 1e-4
    assert abs(su["refinance_debt"] - 200.0) < 1e-4
    assert abs(su["total_fees"] - 35.0) < 1e-4
    assert abs(su["total_uses"] - 1110.0) < 1e-4
    assert abs(su["sponsor_equity"] - 560.0) < 1e-4
    assert abs(su["total_sources"] - 1110.0) < 1e-4
    assert abs(su["opening_cash"] - 25.0) < 1e-4
    assert abs(su["opening_net_debt"] - 475.0) < 1e-4


def test_sources_and_uses_identity(inst: dict[str, Any]) -> None:
    su = build_sources_and_uses(
        ebitda_0=inst["ebitda_0"],
        entry_multiple=inst["entry_multiple"],
        existing_debt=inst["existing_debt"],
        min_cash=inst["min_cash"],
        target_cash=inst["target_cash"],
        txn_fee_rate=inst["txn_fee_rate"],
        financing_fee_rate=inst["financing_fee_rate"],
        tla_leverage=inst["tla_leverage"],
        tlb_leverage=inst["tlb_leverage"],
        rollover_equity=inst["rollover_equity"],
    )
    assert abs(su["total_sources"] - su["total_uses"]) < 1e-4
    assert su["sponsor_equity"] > 0.0
    assert su["opening_cash"] == inst["min_cash"]
    assert abs(su["opening_net_debt"] - (su["total_debt_issued"] - su["opening_cash"])) < 1e-4


def test_sources_and_uses_validation() -> None:
    with pytest.raises(ValueError):
        build_sources_and_uses(
            ebitda_0=-10.0,
            entry_multiple=10.0,
            existing_debt=50.0,
            min_cash=10.0,
            target_cash=10.0,
            txn_fee_rate=0.02,
            financing_fee_rate=0.02,
            tla_leverage=3.0,
            tlb_leverage=2.0,
        )
    with pytest.raises(ValueError):
        build_sources_and_uses(
            ebitda_0=100.0,
            entry_multiple=-5.0,
            existing_debt=50.0,
            min_cash=10.0,
            target_cash=10.0,
            txn_fee_rate=0.02,
            financing_fee_rate=0.02,
            tla_leverage=3.0,
            tlb_leverage=2.0,
        )


# --- 2. Operating Forecast Tests ---


def test_forecast_operations_growth(inst: dict[str, Any]) -> None:
    ops = forecast_operations(
        revenue_0=inst["revenue_0"],
        growth_rates=inst["growth_rates"],
        ebitda_margins=inst["ebitda_margins"],
        capex_pcts=inst["capex_pcts"],
        da_pcts=inst["da_pcts"],
        nwc_pcts=inst["nwc_pcts"],
        tax_rate=inst["tax_rate"],
    )
    revs = ops["revenues"]
    assert len(revs) == 5
    for i in range(5):
        assert ops["ebitdas"][i] > 0.0
        assert ops["ebits"][i] == round(ops["ebitdas"][i] - ops["das"][i], 4)
        assert ops["unlevered_fcfs"][i] <= ops["ebitdas"][i]


# --- 3. Debt Schedule & Cash Sweep Tests ---


def test_interest_expense_beginning_balance() -> None:
    # 1 year, ebitda = 100, capex = 20, da = 15, delta_nwc = 5
    # TLA init = 200 at 8% -> interest = 16.0
    # TLB init = 100 at 10% -> interest = 10.0
    # Total interest = 26.0
    # EBIT = 100 - 15 = 85.0, EBT = 85 - 26 = 59.0, Tax (20%) = 11.8
    # CFADS = 100 - 20 - 5 - 26 - 11.8 = 37.2
    debt = run_debt_schedule(
        ebitda_forecast=[100.0],
        capex_forecast=[20.0],
        da_forecast=[15.0],
        delta_nwc_forecast=[5.0],
        tax_rate=0.20,
        tla_initial=200.0,
        tla_rate=0.08,
        tla_amort_rate=0.05,  # 10.0
        tlb_initial=100.0,
        tlb_rate=0.10,
        tlb_amort_rate=0.01,  # 1.0
        min_cash=10.0,
        initial_cash=10.0,
        sweep_pct=1.0,
        interest_method="beginning",
    )
    assert abs(debt["tla_interest"][0] - 16.0) < 1e-4
    assert abs(debt["tlb_interest"][0] - 10.0) < 1e-4
    assert abs(debt["total_interest"][0] - 26.0) < 1e-4
    assert abs(debt["taxes"][0] - 11.8) < 1e-4
    assert abs(debt["cfads"][0] - 37.2) < 1e-4
    assert abs(debt["tla_mand_amort"][0] - 10.0) < 1e-4
    assert abs(debt["tlb_mand_amort"][0] - 1.0) < 1e-4
    # Cash before sweep = 10.0 + 37.2 - 11.0 = 36.2
    # Excess cash = 36.2 - 10.0 = 26.2
    # Sweep TLA = 26.2
    assert abs(debt["tla_sweep"][0] - 26.2) < 1e-4
    assert abs(debt["tlb_sweep"][0] - 0.0) < 1e-4
    assert abs(debt["end_cash"][0] - 10.0) < 1e-4


def test_debt_schedule_minimum_cash_preserved(inst: dict[str, Any]) -> None:
    res = run_lbo_model(inst)
    debt = res["debt_schedule"]
    min_cash = float(inst["min_cash"])
    for cash in debt["end_cash"]:
        assert cash >= min_cash - 1e-4


def test_debt_schedule_amortization_priority(inst: dict[str, Any]) -> None:
    res = run_lbo_model(inst)
    debt = res["debt_schedule"]
    # TLA should amortize and sweep down
    for end_tla, end_tlb in zip(debt["end_tla"], debt["end_tlb"], strict=True):
        assert end_tla >= -1e-4
        assert end_tlb >= -1e-4


# --- 4. Covenant Tests ---


def test_covenant_evaluation() -> None:
    total_debt = [500.0, 420.0, 330.0, 220.0, 100.0]
    cash = [20.0, 20.0, 20.0, 20.0, 20.0]
    interest = [45.0, 38.0, 30.0, 20.0, 10.0]
    ebitda = [100.0, 110.0, 120.0, 130.0, 140.0]
    max_leverage = [5.5, 5.0, 4.5, 4.0, 3.5]
    min_cov = 2.0

    covs = evaluate_covenants(total_debt, cash, interest, ebitda, max_leverage, min_cov)
    assert covs["is_compliant"] is True
    assert not any(covs["leverage_breaches"])
    assert not any(covs["coverage_breaches"])

    # Test breach scenario
    tight_max_lev = [4.5, 4.0, 3.5, 3.0, 2.5]  # Period 0: 500/100 = 5.0 > 4.5 -> breach
    covs_breach = evaluate_covenants(total_debt, cash, interest, ebitda, tight_max_lev, min_cov)
    assert covs_breach["is_compliant"] is False
    assert covs_breach["leverage_breaches"][0] is True


# --- 5. Returns & Kaplan-Strömberg Value Creation Attribution Tests ---


def test_exit_equity_bridge() -> None:
    # exit_ebitda = 150.0, exit_mult = 11.0 -> exit_ev = 1650.0
    # exit_net_debt = 200.0 -> exit_equity = 1450.0
    # sponsor_equity_0 = 400.0, rollover = 0.0 -> sponsor exit = 1450.0
    # MOIC = 1450.0 / 400.0 = 3.625
    # IRR = (3.625)**(0.2) - 1.0 = 29.38%
    ret = calculate_returns_and_attribution(
        entry_ebitda=100.0,
        exit_ebitda=150.0,
        entry_multiple=10.0,
        exit_multiple=11.0,
        sponsor_equity_0=400.0,
        exit_net_debt=200.0,
        holding_period_years=5.0,
        rollover_equity_0=0.0,
    )
    assert abs(ret["exit_ev"] - 1650.0) < 1e-4
    assert abs(ret["exit_equity_total"] - 1450.0) < 1e-4
    assert abs(ret["moic"] - 3.625) < 1e-4
    assert abs(ret["irr"] - 0.2938) < 1e-3


def test_value_creation_attribution_identity(inst: dict[str, Any]) -> None:
    res = run_lbo_model(inst)
    ret = res["returns"]
    # Total equity gain must exactly equal sum of EBITDA growth, multiple expansion, and deleveraging
    sum_attrib = ret["delta_ebitda_growth"] + ret["delta_multiple_expansion"] + ret["delta_deleveraging"]
    assert abs(sum_attrib - ret["total_equity_gain"]) < 1e-3

    # Percentages must sum to 1.0
    pct_sum = ret["pct_ebitda_growth"] + ret["pct_multiple_expansion"] + ret["pct_deleveraging"]
    assert abs(pct_sum - 1.0) < 1e-3


def test_value_creation_hand_calc() -> None:
    # Entry EBITDA = 100, Entry Multiple = 10 -> Entry EV = 1000
    # Exit EBITDA = 140, Exit Multiple = 12 -> Exit EV = 1680
    # Total Entry Equity = 400 -> Implied Entry Net Debt = 1000 - 400 = 600
    # Exit Net Debt = 180 -> Exit Equity Total = 1680 - 180 = 1500
    # Total Equity Gain = 1500 - 400 = 1100
    #
    # 1. EBITDA Growth = (140 - 100) * 10 = 400
    # 2. Multiple Expansion = 140 * (12 - 10) = 280
    # 3. Deleveraging = 600 - 180 = 420
    # Sum = 400 + 280 + 420 = 1100!
    ret = calculate_returns_and_attribution(
        entry_ebitda=100.0,
        exit_ebitda=140.0,
        entry_multiple=10.0,
        exit_multiple=12.0,
        sponsor_equity_0=400.0,
        exit_net_debt=180.0,
        holding_period_years=5.0,
        rollover_equity_0=0.0,
    )
    assert abs(ret["delta_ebitda_growth"] - 400.0) < 1e-4
    assert abs(ret["delta_multiple_expansion"] - 280.0) < 1e-4
    assert abs(ret["delta_deleveraging"] - 420.0) < 1e-4
    assert abs(ret["total_equity_gain"] - 1100.0) < 1e-4
    assert abs(ret["pct_ebitda_growth"] - (400.0 / 1100.0)) < 1e-4
    assert abs(ret["pct_multiple_expansion"] - (280.0 / 1100.0)) < 1e-4
    assert abs(ret["pct_deleveraging"] - (420.0 / 1100.0)) < 1e-4


def test_moic_monotonic_in_exit_multiple(inst: dict[str, Any]) -> None:
    params_low = dict(inst)
    params_low["exit_multiple"] = float(inst["entry_multiple"]) - 1.0
    params_high = dict(inst)
    params_high["exit_multiple"] = float(inst["entry_multiple"]) + 2.0

    res_low = run_lbo_model(params_low)
    res_high = run_lbo_model(params_high)
    assert res_high["returns"]["moic"] > res_low["returns"]["moic"]
    assert res_high["returns"]["irr"] > res_low["returns"]["irr"]

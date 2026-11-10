"""Acceptance test suite for CF6: Raising Capital & Investment Banking (ipo_pricing.py).

Runs identically in Pyodide and native pytest:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import json
import math
import os
from collections.abc import Callable
from typing import Any

import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]
from ipo_pricing import (  # type: ignore[import-not-found, unused-ignore]
    bookbuilding_allocation,
    long_run_bhar,
    rock_equilibrium_price,
    seo_announcement_impact,
    syndicate_economics,
)

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def _assert_close(a: float, b: float, tol: float = 1e-5, msg: str = "") -> None:
    __tracebackhide__ = True
    if not math.isfinite(a) or abs(a - b) > tol:
        pytest.fail(f"Value mismatch: {a} vs {b} (diff={abs(a - b):.6e}, tol={tol}) {msg}")


def _must_raise(func: Callable[[], Any], condition_name: str) -> None:
    __tracebackhide__ = True
    try:
        func()
    except ValueError:
        return
    pytest.fail(f"Failed to raise ValueError for invalid condition: {condition_name}")


# -----------------------------------------------------------------------------
# 1. Rock (1986) Winner's Curse Equilibrium Tests
# -----------------------------------------------------------------------------


def test_rock_equilibrium_price_bounds() -> None:
    """Rock equilibrium offer price must strictly lie between v_low and E[v]."""
    v_l = INST["v_low"]
    v_h = INST["v_high"]
    p = INST["prob_high"]
    s = INST["s_shares"]
    i_dem = INST["informed_demand"]
    b_u = INST["uninformed_budget"]

    p_star, alpha_h, underpricing = rock_equilibrium_price(v_l, v_h, p, s, i_dem, b_u)
    e_v = (1.0 - p) * v_l + p * v_h

    assert v_l < p_star < e_v, f"P_star={p_star} must lie strictly in ({v_l}, {e_v})"
    assert underpricing > 0.0, f"Underpricing={underpricing} must be positive in Rock equilibrium"
    assert 0.0 < alpha_h <= 1.0, f"Rationing probability alpha_H={alpha_h} must be in (0, 1]"


def test_rock_uninformed_zero_profit_condition() -> None:
    """In Rock equilibrium, uninformed expected dollar return must equal zero."""
    v_l = INST["v_low"]
    v_h = INST["v_high"]
    p = INST["prob_high"]
    s = INST["s_shares"]
    i_dem = INST["informed_demand"]
    b_u = INST["uninformed_budget"]

    p_star, _alpha_h, _ = rock_equilibrium_price(v_l, v_h, p, s, i_dem, b_u)

    d_u = b_u / p_star
    alloc_l = min(d_u, float(s))
    alloc_h = (float(s) / (d_u + float(i_dem))) * d_u if (d_u + float(i_dem)) > float(s) else d_u
    expected_profit = (1.0 - p) * alloc_l * (v_l - p_star) + p * alloc_h * (v_h - p_star)

    _assert_close(expected_profit, 0.0, tol=1e-2, msg="Uninformed expected profit must be zero in equilibrium")


def test_rock_comparative_statics_informed_demand() -> None:
    """Higher informed demand intensifies the winner's curse, increasing underpricing."""
    v_l, v_h, p = 12.0, 26.0, 0.55
    s, b_u = 2_000_000, 50_000_000.0

    p_star_low_i, _, up_low_i = rock_equilibrium_price(v_l, v_h, p, s, 1_000_000, b_u)
    p_star_high_i, _, up_high_i = rock_equilibrium_price(v_l, v_h, p, s, 4_000_000, b_u)

    assert up_high_i > up_low_i, "Greater informed demand must worsen winner's curse and increase underpricing"
    assert p_star_high_i < p_star_low_i, "Greater informed demand must lower equilibrium offer price"


def test_rock_input_validation() -> None:
    """Rock function must validate parameter boundaries."""
    _must_raise(lambda: rock_equilibrium_price(-5.0, 20.0, 0.5, 1000, 1000, 10000.0), "negative v_low")
    _must_raise(lambda: rock_equilibrium_price(25.0, 20.0, 0.5, 1000, 1000, 10000.0), "v_low >= v_high")
    _must_raise(lambda: rock_equilibrium_price(10.0, 20.0, 1.5, 1000, 1000, 10000.0), "prob_high > 1")
    _must_raise(lambda: rock_equilibrium_price(10.0, 20.0, 0.5, 0, 1000, 10000.0), "zero shares")


# -----------------------------------------------------------------------------
# 2. Bookbuilding Allocation Tests
# -----------------------------------------------------------------------------


def test_bookbuilding_total_allocation_and_conservation() -> None:
    """Bookbuilding allocation must conserve shares and not exceed total offering."""
    bids = json.loads(str(INST["bids_json"]))
    total_shares = INST["total_shares_offered"]
    clearing_price = INST["clearing_price"]

    result = bookbuilding_allocation(bids, total_shares, clearing_price, rule="discretionary")
    alloc = result["allocations"]

    assert sum(alloc.values()) == result["total_allocated"]
    assert result["total_allocated"] <= total_shares

    # Bids below clearing price must receive exactly 0 shares
    for b in bids:
        if b["bid_price"] < clearing_price:
            assert alloc[b["bidder_id"]] == 0, f"Bidder {b['bidder_id']} below clearing price received shares"


def test_bookbuilding_discretionary_favors_positive_info() -> None:
    """Discretionary allocation prioritizes bidders who revealed positive private info."""
    bids = [
        {
            "bidder_id": "inst_pos",
            "bid_price": 22.0,
            "bid_shares": 1_000_000,
            "revealed_info": "positive",
            "investor_type": "institutional",
        },
        {
            "bidder_id": "inst_neu",
            "bid_price": 22.0,
            "bid_shares": 1_000_000,
            "revealed_info": "neutral",
            "investor_type": "institutional",
        },
        {
            "bidder_id": "ret_neu",
            "bid_price": 22.0,
            "bid_shares": 1_000_000,
            "revealed_info": "neutral",
            "investor_type": "retail",
        },
    ]
    total_shares = 1_500_000
    clearing_price = 20.0

    res = bookbuilding_allocation(bids, total_shares, clearing_price, rule="discretionary")
    alloc = res["allocations"]
    fulfill = res["fulfillment_rates"]

    assert alloc["inst_pos"] == 1_000_000, "Positive info bidder must receive full allocation when pos_demand <= total"
    assert fulfill["inst_pos"] == 1.0
    assert alloc["inst_neu"] == 250_000
    assert alloc["ret_neu"] == 250_000
    assert fulfill["inst_pos"] > fulfill["inst_neu"]


def test_bookbuilding_pro_rata_equal_rationing() -> None:
    """Pro-rata allocation must ration all qualifying bids equally."""
    bids = [
        {
            "bidder_id": "b1",
            "bid_price": 20.0,
            "bid_shares": 1_000_000,
            "revealed_info": "positive",
            "investor_type": "institutional",
        },
        {
            "bidder_id": "b2",
            "bid_price": 20.0,
            "bid_shares": 1_000_000,
            "revealed_info": "neutral",
            "investor_type": "institutional",
        },
    ]
    res = bookbuilding_allocation(bids, 1_000_000, 20.0, rule="pro_rata")
    assert res["allocations"]["b1"] == 500_000
    assert res["allocations"]["b2"] == 500_000
    _assert_close(res["fulfillment_rates"]["b1"], 0.5, tol=1e-6)
    _assert_close(res["fulfillment_rates"]["b2"], 0.5, tol=1e-6)


def test_bookbuilding_revenue_cents_articulation() -> None:
    """Gross revenue in cents must articulate with allocated shares and clearing price."""
    bids = json.loads(str(INST["bids_json"]))
    total_shares = INST["total_shares_offered"]
    clearing_price = INST["clearing_price"]

    res = bookbuilding_allocation(bids, total_shares, clearing_price, rule="discretionary")
    expected_cents = round(res["total_allocated"] * clearing_price * 100)
    assert res["total_revenue_cents"] == expected_cents


# -----------------------------------------------------------------------------
# 3. Myers-Majluf (1984) SEO Announcement Tests
# -----------------------------------------------------------------------------


def test_seo_announcement_decision_and_dilution() -> None:
    """Good firm issues equity if and only if project NPV exceeds adverse selection dilution."""
    res = seo_announcement_impact(
        v_assets_good=INST["v_assets_good"],
        v_assets_bad=INST["v_assets_bad"],
        prob_good=INST["prob_good"],
        project_cost=INST["project_cost"],
        project_npv=INST["project_npv"],
        slack_cash=INST["slack_cash"],
    )

    if INST["project_npv"] >= res["dilution_cost"]:
        assert res["good_firm_decision"] == "issue"
    else:
        assert res["good_firm_decision"] == "pass"

    _assert_close(res["dilution_cost"], res["npv_threshold"], tol=1e-5)


def test_seo_sufficient_slack_eliminates_dilution() -> None:
    """When internal cash slack covers project cost, no equity is issued and dilution is zero."""
    res = seo_announcement_impact(
        v_assets_good=200.0,
        v_assets_bad=100.0,
        prob_good=0.5,
        project_cost=30.0,
        project_npv=8.0,
        slack_cash=40.0,  # Slack exceeds cost
    )
    assert res["slack_sufficient"] is True
    assert res["good_firm_decision"] == "issue"
    assert res["dilution_cost"] == 0.0
    assert res["announcement_return"] == 0.0


def test_seo_information_asymmetry_comparative_statics() -> None:
    """Larger information asymmetry regarding assets in place increases dilution cost."""
    res_low_asym = seo_announcement_impact(160.0, 140.0, 0.5, 40.0, 10.0, 0.0)
    res_high_asym = seo_announcement_impact(220.0, 80.0, 0.5, 40.0, 10.0, 0.0)

    assert res_high_asym["dilution_cost"] > res_low_asym["dilution_cost"], "Higher asymmetry must increase dilution"


# -----------------------------------------------------------------------------
# 4. Long-Run BHAR and Wealth Relative Tests
# -----------------------------------------------------------------------------


def test_long_run_bhar_and_wealth_relative_math() -> None:
    """BHAR and Wealth Relative must match exact geometric compounding definitions."""
    f_rets = INST["firm_returns"]
    b_rets = INST["benchmark_returns"]

    res = long_run_bhar(f_rets, b_rets)

    prod_f = 1.0
    prod_b = 1.0
    for f, b in zip(f_rets, b_rets, strict=True):
        prod_f *= 1.0 + f
        prod_b *= 1.0 + b

    expected_bhar = prod_f - prod_b
    expected_wr = prod_f / prod_b

    _assert_close(res["bhar"], expected_bhar, tol=1e-9, msg="BHAR mismatch")
    _assert_close(res["wealth_relative"], expected_wr, tol=1e-9, msg="Wealth relative mismatch")
    _assert_close(res["firm_compounded"], prod_f - 1.0, tol=1e-9)
    _assert_close(res["benchmark_compounded"], prod_b - 1.0, tol=1e-9)


def test_long_run_bhar_identical_returns_identity() -> None:
    """When firm returns equal benchmark returns, BHAR is 0 and WR is 1.0."""
    same_rets = [0.01] * 24
    res = long_run_bhar(same_rets, same_rets)
    _assert_close(res["bhar"], 0.0, tol=1e-12)
    _assert_close(res["wealth_relative"], 1.0, tol=1e-12)
    _assert_close(res["annualized_abnormal"], 0.0, tol=1e-12)


# -----------------------------------------------------------------------------
# 5. Syndicate Economics & Gross Spread Tests
# -----------------------------------------------------------------------------


def test_syndicate_economics_exact_balance_articulation() -> None:
    """Syndicate fee accounting must articulate to the exact integer cent."""
    gross = INST["gross_proceeds_cents"]
    spread_bps = INST["spread_bps"]
    lead_s = INST["lead_manager_share"]
    co_s = INST["co_manager_share"]
    sell_s = INST["selling_group_share"]

    res = syndicate_economics(gross, spread_bps, lead_s, co_s, sell_s)

    # 1. Total spread + Net proceeds == Gross proceeds
    assert res["gross_proceeds_cents"] == res["total_spread_cents"] + res["net_proceeds_cents"]

    # 2. Syndicate tranche compensation sum == Total spread
    syndicate_sum = res["lead_manager_cents"] + res["co_manager_cents"] + res["selling_group_cents"]
    assert syndicate_sum == res["total_spread_cents"], f"Syndicate sum {syndicate_sum} != {res['total_spread_cents']}"

    # 3. Functional fee breakdown sum == Total spread
    fee_sum = res["management_fee_cents"] + res["underwriting_fee_cents"] + res["selling_concession_cents"]
    assert fee_sum == res["total_spread_cents"], f"Fee sum {fee_sum} != {res['total_spread_cents']}"


def test_syndicate_economics_7_percent_benchmark() -> None:
    """Standard $100M IPO at 700 bps produces exactly $7.0M gross spread and $93.0M net proceeds."""
    res = syndicate_economics(100_000_000_00, spread_bps=700)
    assert res["total_spread_cents"] == 7_000_000_00
    assert res["net_proceeds_cents"] == 93_000_000_00
    assert res["lead_manager_cents"] == 4_200_000_00  # 60%
    assert res["co_manager_cents"] == 2_100_000_00  # 30%
    assert res["selling_group_cents"] == 700_000_00  # 10%

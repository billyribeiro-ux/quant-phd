"""Acceptance test suite for PM2: Venture Capital (Term-Sheet Economics).

Runs identically in native pytest and in-browser Pyodide:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any

import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]
from reference import (  # type: ignore[import-not-found, unused-ignore]
    build_cap_table,
    calculate_exit_waterfall,
    compute_anti_dilution_price,
    evaluate_term_sheet,
)

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


# ============================================================================
# 1. Instance Structure and Determinism
# ============================================================================


def test_instance_structure() -> None:
    required_keys = {
        "seed",
        "founders_shares",
        "seniority",
        "round_names",
        "round_pre_money",
        "round_investments",
        "round_pools",
        "round_liquidation_multiples",
        "round_participations",
        "round_cap_multiples",
        "round_anti_dilutions",
        "test_exit_values",
    }
    assert required_keys.issubset(INST.keys()), f"Missing keys in instance: {required_keys - set(INST.keys())}"

    assert INST["founders_shares"] > 0
    assert INST["seniority"] in ("standard", "pari_passu")
    assert len(INST["round_names"]) == 3
    assert len(INST["test_exit_values"]) >= 5

    assert len(INST["round_pre_money"]) == 3
    assert len(INST["round_investments"]) == 3
    assert len(INST["round_pools"]) == 3


# ============================================================================
# 2. Anti-Dilution Formula Invariants
# ============================================================================


def test_anti_dilution_mechanics() -> None:
    old_cp = 2.00
    new_price = 1.00
    inv = 5_000_000.0
    fd_pre = 10_000_000.0
    cp_pre = 8_000_000.0

    # Invariant 1: Up-round never triggers anti-dilution
    assert compute_anti_dilution_price(old_cp, 3.00, inv, fd_pre, cp_pre, "broad_based") == old_cp
    assert compute_anti_dilution_price(old_cp, 3.00, inv, fd_pre, cp_pre, "full_ratchet") == old_cp

    # Invariant 2: Full Ratchet sets conversion price exactly to down-round issue price
    p_fr = compute_anti_dilution_price(old_cp, new_price, inv, fd_pre, cp_pre, "full_ratchet")
    assert abs(p_fr - 1.00) < 1e-9

    # Invariant 3: Broad-Based Weighted Average formula
    p_bb = compute_anti_dilution_price(old_cp, new_price, inv, fd_pre, cp_pre, "broad_based")
    assert abs(p_bb - 1.66666667) < 1e-6

    # Invariant 4: Narrow-Based Weighted Average formula
    p_nb = compute_anti_dilution_price(old_cp, new_price, inv, fd_pre, cp_pre, "narrow_based")
    assert abs(p_nb - 1.6153846) < 1e-6

    # Invariant 5: Mathematical hierarchy: Full Ratchet <= Narrow-Based <= Broad-Based <= Old Price
    assert new_price <= p_fr <= p_nb <= p_bb <= old_cp


# ============================================================================
# 3. Cap Table Evolution and Option Pool Shuffle
# ============================================================================


def test_cap_table_option_pool_shuffle() -> None:
    cap_table = build_cap_table(INST)

    # Invariant 1: Total shares equal sum of parts
    parts_sum = (
        cap_table["founders_shares"]
        + cap_table["options_shares"]
        + cap_table["series_a"]["shares"]
        + cap_table["series_b"]["shares"]
        + cap_table["series_c"]["shares"]
    )
    assert abs(cap_table["total_shares"] - parts_sum) < 1e-4, "Cap table total shares does not articulate"

    # Invariant 2: Series A option pool size on post-A closing
    round_a_test = {
        "founders_shares": 8_000_000,
        "seniority": "standard",
        "round_names": ["Series A", "Series B", "Series C"],
        "round_pre_money": [12_000_000.0, 20_000_000.0, 30_000_000.0],
        "round_investments": [4_000_000.0, 5_000_000.0, 10_000_000.0],
        "round_pools": [0.15, 0.0, 0.0],
        "round_liquidation_multiples": [1.0, 1.0, 1.0],
        "round_participations": ["non_participating", "non_participating", "non_participating"],
        "round_cap_multiples": [0.0, 0.0, 0.0],
        "round_anti_dilutions": ["broad_based", "broad_based", "broad_based"],
        "test_exit_values": [0.0, 10_000_000.0],
    }

    cap_test = build_cap_table(round_a_test)
    a_sh = cap_test["series_a"]["shares"]
    assert abs(a_sh - 3_333_333.33) < 1.0
    assert abs(cap_test["series_a"]["issue_price"] - 1.20) < 1e-4

    # Conversion ratios must be >= 1.0
    assert cap_table["series_a"]["conversion_ratio"] >= 1.0 - 1e-9
    assert cap_table["series_b"]["conversion_ratio"] >= 1.0 - 1e-9
    assert cap_table["series_c"]["conversion_ratio"] >= 1.0 - 1e-9


# ============================================================================
# 4. Waterfall Conservation of Value
# ============================================================================


def test_waterfall_conservation_of_value() -> None:
    cap_table = build_cap_table(INST)
    seniority = INST["seniority"]

    for exit_val in INST["test_exit_values"]:
        payoffs = calculate_exit_waterfall(float(exit_val), cap_table, seniority=seniority)
        total_payout = sum(payoffs.values())
        assert abs(total_payout - exit_val) < 1e-4, (
            f"Conservation of value violated at exit {exit_val}: sum={total_payout}"
        )
        for claimant, p in payoffs.items():
            assert p >= -1e-6, f"Negative payout to {claimant} at exit {exit_val}: {p}"


# ============================================================================
# 5. Waterfall Monotonicity Invariants
# ============================================================================


def test_waterfall_monotonicity() -> None:
    cap_table = build_cap_table(INST)
    seniority = INST["seniority"]

    exit_grid = [
        0.0,
        1_000_000.0,
        5_000_000.0,
        15_000_000.0,
        25_000_000.0,
        50_000_000.0,
        100_000_000.0,
        200_000_000.0,
    ]

    prev_payoffs: dict[str, float] | None = None
    for ev in exit_grid:
        cur_payoffs = calculate_exit_waterfall(ev, cap_table, seniority=seniority)
        if prev_payoffs is not None:
            for claimant in ["founders", "options", "series_a", "series_b", "series_c"]:
                assert cur_payoffs[claimant] >= prev_payoffs[claimant] - 1e-4, (
                    f"Monotonicity violated for {claimant}: {prev_payoffs[claimant]} -> {cur_payoffs[claimant]}"
                )
        prev_payoffs = cur_payoffs


# ============================================================================
# 6. Seniority and Preference Satisfaction
# ============================================================================


def test_waterfall_seniority_invariants() -> None:
    cap_table = build_cap_table(INST)

    pref_c = cap_table["series_c"]["liquidation_multiple"] * cap_table["series_c"]["investment"]
    pref_b = cap_table["series_b"]["liquidation_multiple"] * cap_table["series_b"]["investment"]
    pref_a = cap_table["series_a"]["liquidation_multiple"] * cap_table["series_a"]["investment"]

    low_exit = pref_c * 0.50
    pay_low = calculate_exit_waterfall(low_exit, cap_table, seniority="standard")
    assert abs(pay_low["series_c"] - low_exit) < 1e-4
    assert abs(pay_low["series_b"]) < 1e-4
    assert abs(pay_low["series_a"]) < 1e-4
    assert abs(pay_low["founders"]) < 1e-4

    tot_pref = pref_a + pref_b + pref_c
    pay_pari = calculate_exit_waterfall(low_exit, cap_table, seniority="pari_passu")
    assert abs(pay_pari["series_c"] - low_exit * (pref_c / tot_pref)) < 1e-4
    assert abs(pay_pari["series_b"] - low_exit * (pref_b / tot_pref)) < 1e-4
    assert abs(pay_pari["series_a"] - low_exit * (pref_a / tot_pref)) < 1e-4
    assert abs(pay_pari["founders"]) < 1e-4


# ============================================================================
# 7. Asymptotic Conversion and Complete Term-Sheet Evaluation
# ============================================================================


def test_asymptotic_conversion_and_evaluation() -> None:
    summary = evaluate_term_sheet(INST)
    assert "cap_table" in summary
    assert "waterfalls" in summary

    cap_table = summary["cap_table"]
    huge_exit = 500_000_000.0
    huge_pay = calculate_exit_waterfall(huge_exit, cap_table, seniority="standard")

    assert huge_pay["founders"] > 0.0
    assert huge_pay["options"] > 0.0
    assert huge_pay["founders"] > huge_pay["options"]
    pref_c = cap_table["series_c"]["investment"] * cap_table["series_c"]["liquidation_multiple"]
    assert huge_pay["series_c"] > pref_c * 2.0, "Preferred equity must convert to common at high exits"

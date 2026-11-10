"""Pytest acceptance test suite for CR4 Capital Structure Recovery Waterfall & Fulcrum Engine.

Tests strict APR conservation, priority monotonicity, fulcrum security uniqueness,
consensual carve-out conservation, POR distribution articulation, and investor IRR/MOIC metrics.
"""

from __future__ import annotations

import os
from typing import Any, cast

import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]

try:
    from waterfall import (  # type: ignore[import-not-found, unused-ignore]
        calculate_waterfall_strict,
        calculate_waterfall_with_carveout,
        evaluate_expected_returns,
        reorganization_equity_distribution,
        run_waterfall_engine,
    )
except ImportError:
    from reference import (  # type: ignore[import-not-found, unused-ignore]
        calculate_waterfall_strict,
        calculate_waterfall_with_carveout,
        evaluate_expected_returns,
        reorganization_equity_distribution,
        run_waterfall_engine,
    )


@pytest.fixture(scope="module")
def seed() -> int:
    return int(os.environ.get("QF_SEED", "0"))


@pytest.fixture(scope="module")
def inst(seed: int) -> dict[str, Any]:
    return make_instance(seed)


# --- 1. Determinism and Instance Properties ---


def test_instance_determinism(seed: int) -> None:
    i1 = make_instance(seed)
    i2 = make_instance(seed)
    assert i1["company_name"] == i2["company_name"]
    assert len(i1["tranches"]) == len(i2["tranches"])
    assert i1["holding_period_years"] == i2["holding_period_years"]


# --- 2. Conservation of Value under Strict APR ---


def test_waterfall_conservation_of_value(inst: dict[str, Any]) -> None:
    tranches = inst["tranches"]

    for scenario in inst["scenarios"]:
        ev = float(scenario["ev"])
        results = calculate_waterfall_strict(tranches, ev)
        total_allocated = sum(r["allocated"] for r in results)

        expected_total = ev  # since equity absorbs any excess if EV > total debt
        assert abs(total_allocated - expected_total) < 1e-4, (
            f"Value conservation violated in scenario '{scenario['name']}': "
            f"allocated {total_allocated} != EV {expected_total}"
        )


# --- 3. Strict Absolute Priority Monotonicity ---


def test_strict_absolute_priority_monotonicity(inst: dict[str, Any]) -> None:
    tranches = inst["tranches"]

    for scenario in inst["scenarios"]:
        ev = float(scenario["ev"])
        results = calculate_waterfall_strict(tranches, ev)

        for i in range(len(results) - 1):
            senior = results[i]
            junior = results[i + 1]

            if senior["claim"] > 0 and junior["allocated"] > 0:
                assert abs(senior["allocated"] - senior["claim"]) < 1e-5, (
                    f"APR violation in scenario '{scenario['name']}': "
                    f"junior tranche '{junior['name']}' received {junior['allocated']} "
                    f"while senior tranche '{senior['name']}' only received {senior['allocated']}/{senior['claim']}"
                )


# --- 4. Fulcrum Security Uniqueness and Logic ---


def test_fulcrum_security_identification(inst: dict[str, Any]) -> None:
    tranches = inst["tranches"]
    total_debt = sum(t["claim"] for t in tranches if t["claim"] > 0)

    for scenario in inst["scenarios"]:
        ev = float(scenario["ev"])
        results = calculate_waterfall_strict(tranches, ev)
        fulcrum_tranches = [r for r in results if r["is_fulcrum"]]

        if ev < total_debt:
            assert len(fulcrum_tranches) == 1, (
                f"Expected 1 fulcrum tranche in '{scenario['name']}', got {len(fulcrum_tranches)}"
            )
            f_item = fulcrum_tranches[0]
            assert f_item["claim"] > 0
            assert f_item["allocated"] <= f_item["claim"]
        else:
            # Fully solvent scenario: no debt tranche is fulcrum
            assert len(fulcrum_tranches) == 0, (
                f"Expected 0 fulcrum tranches in solvent '{scenario['name']}', got {len(fulcrum_tranches)}"
            )


# --- 5. Consensual Plan Carve-Out Conservation ---


def test_carveout_conservation_of_value(inst: dict[str, Any]) -> None:
    tranches = inst["tranches"]
    carveout = inst["carveout"]

    for scenario in inst["scenarios"]:
        ev = float(scenario["ev"])
        strict_res = calculate_waterfall_strict(tranches, ev)
        adj_res = calculate_waterfall_with_carveout(tranches, ev, carveout)

        total_strict = sum(r["allocated"] for r in strict_res)
        total_adj = sum(r["allocated"] for r in adj_res)

        assert abs(total_strict - total_adj) < 1e-5, (
            f"Carve-out leaked value: strict total {total_strict} != adjusted total {total_adj}"
        )


def test_carveout_transfer_mechanics(inst: dict[str, Any]) -> None:
    tranches = inst["tranches"]
    carveout = inst["carveout"]
    ev = float(inst["scenarios"][2]["ev"])  # Base scenario

    strict_res = calculate_waterfall_strict(tranches, ev)
    adj_res = calculate_waterfall_with_carveout(tranches, ev, carveout)

    src_name = carveout["source_tranche"]
    tgt_name = carveout["target_tranche"]
    pct = carveout["carveout_pct"]

    strict_src = next(r for r in strict_res if r["name"] == src_name)
    adj_src = next(r for r in adj_res if r["name"] == src_name)
    strict_tgt = next(r for r in strict_res if r["name"] == tgt_name)
    adj_tgt = next(r for r in adj_res if r["name"] == tgt_name)

    expected_transfer = round(strict_src["allocated"] * pct, 6)
    actual_deduction = round(strict_src["allocated"] - adj_src["allocated"], 6)
    actual_addition = round(adj_tgt["allocated"] - strict_tgt["allocated"], 6)

    assert abs(actual_deduction - expected_transfer) < 1e-4
    assert abs(actual_addition - expected_transfer) < 1e-4


# --- 6. Plan of Reorganization (POR) Articulation ---


def test_por_consideration_articulation(inst: dict[str, Any]) -> None:
    tranches = inst["tranches"]
    por = inst["por"]
    base_ev = next(s["ev"] for s in inst["scenarios"] if s["name"] == por["scenario_name"])

    dist = reorganization_equity_distribution(
        tranches,
        float(base_ev),
        float(por["new_debt_issued"]),
        float(por["cash_dist"]),
    )

    reorg_eq = dist["reorg_equity_value"]
    cash = dist["cash_distributed"]
    debt = dist["new_debt_distributed"]

    # Invariant: cash + debt + equity == base_ev
    assert abs(cash + debt + reorg_eq - base_ev) < 1e-4

    # Ownership percentages sum to 1.0 (or 0.0 if reorg_eq == 0)
    total_eq_pct = sum(t["equity_ownership_pct"] for t in dist["tranche_distributions"])
    if reorg_eq > 0:
        assert abs(total_eq_pct - 1.0) < 1e-4


# --- 7. Distressed Investor Return Properties ---


def test_expected_returns_mathematical_consistency(inst: dict[str, Any]) -> None:
    tranches = inst["tranches"]
    scenarios = inst["scenarios"]
    prices = inst["purchase_prices"]
    hp = inst["holding_period_years"]

    ret = evaluate_expected_returns(tranches, scenarios, prices, hp)

    assert ret["holding_period_years"] == hp
    assert ret["total_capital_invested"] > 0
    assert ret["total_expected_recovery"] >= 0

    if ret["total_capital_invested"] > 0:
        expected_moic = round(ret["total_expected_recovery"] / ret["total_capital_invested"], 6)
        assert abs(ret["portfolio_moic"] - expected_moic) < 1e-5

        if ret["portfolio_moic"] > 0:
            expected_irr = round((ret["portfolio_moic"] ** (1.0 / hp)) - 1.0, 6)
            assert abs(ret["portfolio_irr"] - expected_irr) < 1e-5

    for t_ret in ret["tranche_returns"]:
        name = t_ret["name"]
        if name in prices:
            assert t_ret["moic"] is not None
            assert t_ret["irr"] is not None
            if t_ret["moic"] > 0:
                calc_irr = (t_ret["moic"] ** (1.0 / hp)) - 1.0
                assert abs(t_ret["irr"] - calc_irr) < 1e-4


# --- 8. Boundary Cases and Edge Conditions ---


def test_zero_enterprise_value_edge_case(inst: dict[str, Any]) -> None:
    tranches = inst["tranches"]
    res = calculate_waterfall_strict(tranches, 0.0)

    for r in res:
        assert r["allocated"] == 0.0
        assert r["recovery_pct"] == 0.0
        if r["claim"] > 0:
            assert r["deficiency"] == r["claim"]

    # Top tranche should be marked fulcrum in zero EV
    assert res[0]["is_fulcrum"] is True
    assert sum(1 for r in res if r["is_fulcrum"]) == 1


def test_exact_cumulative_claim_boundary() -> None:
    tranches = [
        {"name": "Tranche A", "claim": 50.0, "seniority": 1},
        {"name": "Tranche B", "claim": 30.0, "seniority": 2},
        {"name": "Tranche C", "claim": 20.0, "seniority": 3},
    ]
    # EV exactly covers A and B
    ev = 80.0
    res = calculate_waterfall_strict(tranches, ev)

    assert res[0]["allocated"] == 50.0
    assert res[0]["recovery_pct"] == 1.0
    assert res[0]["is_fulcrum"] is False

    assert res[1]["allocated"] == 30.0
    assert res[1]["recovery_pct"] == 1.0
    assert res[1]["is_fulcrum"] is True  # exact boundary fulcrum

    assert res[2]["allocated"] == 0.0
    assert res[2]["recovery_pct"] == 0.0
    assert res[2]["is_fulcrum"] is False


def test_input_validation_exceptions(inst: dict[str, Any]) -> None:
    tranches = inst["tranches"]
    with pytest.raises(ValueError, match="Enterprise value must be non-negative"):
        calculate_waterfall_strict(tranches, -10.0)

    with pytest.raises(TypeError, match="tranches must be a list"):
        calculate_waterfall_strict(cast(Any, "invalid"), 100.0)


# --- 9. Full Engine Integration Run ---


def test_run_waterfall_engine_integration(inst: dict[str, Any]) -> None:
    output = run_waterfall_engine(inst)
    assert output["company_name"] == inst["company_name"]
    assert len(output["scenarios"]) == len(inst["scenarios"])
    assert "carveout_results" in output
    assert "por_distribution" in output
    assert "expected_returns" in output

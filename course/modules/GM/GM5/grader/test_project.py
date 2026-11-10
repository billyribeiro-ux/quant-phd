"""Autograder test suite for GM5: Crises as Mechanisms.

Runs identically in native pytest and Pyodide:
    pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import math
import os
from typing import Any

import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]
from reference import (  # type: ignore[import-not-found, unused-ignore]
    calculate_forced_sales,
    classify_crisis_regime,
    compute_margin_call,
    estimate_fire_sale_discount,
    evaluate_policy_intervention,
    simulate_liquidity_spiral,
)

pytestmark = pytest.mark.filterwarnings("error")


def _get_instance() -> dict[str, Any]:
    """Retrieve test instance seeded by environment SEED or fallback to 0."""
    seed_env = os.environ.get("SEED", "0")
    try:
        seed = int(seed_env)
    except ValueError:
        seed = 0
    return make_instance(seed)


def test_margin_call_invariants() -> None:
    """Property 1: Equity, leverage, and margin call deficit articulation."""
    inst = _get_instance()
    p0 = inst["p0"]
    q0 = inst["q0"]
    cash0 = inst["cash0"]
    debt0 = inst["debt0"]
    h0 = inst["haircut0"]

    res = compute_margin_call(q0, p0, cash0, debt0, h0)

    # Balance sheet articulation
    expected_asset_val = q0 * p0
    expected_equity = expected_asset_val + cash0 - debt0
    expected_required_margin = h0 * expected_asset_val
    expected_deficit = max(0.0, expected_required_margin - expected_equity)

    assert math.isclose(res["asset_value"], expected_asset_val, rel_tol=1e-7)
    assert math.isclose(res["equity"], expected_equity, rel_tol=1e-7)
    assert math.isclose(res["required_margin"], expected_required_margin, rel_tol=1e-7)
    assert math.isclose(res["margin_deficit"], expected_deficit, rel_tol=1e-7)

    # Leverage bounds
    if expected_equity > 0:
        assert math.isclose(res["current_leverage"], expected_asset_val / expected_equity, rel_tol=1e-7)
    else:
        assert math.isinf(res["current_leverage"])
    assert math.isclose(res["max_leverage"], 1.0 / h0, rel_tol=1e-7)

    # Monotonicity with respect to haircut
    res_higher_h = compute_margin_call(q0, p0, cash0, debt0, h0 + 0.05)
    assert res_higher_h["required_margin"] > res["required_margin"]
    assert res_higher_h["margin_deficit"] >= res["margin_deficit"]


def test_forced_sales_bounds_and_solvency() -> None:
    """Property 2: Forced liquidation volume conservation, bounds, and insolvency response."""
    inst = _get_instance()
    p0 = inst["p0"]
    q0 = inst["q0"]
    cash0 = inst["cash0"]
    debt0 = inst["debt0"]
    h0 = inst["haircut0"]

    # When balance sheet is well-capitalized (large cash, zero deficit)
    well_cap = calculate_forced_sales(q0, p0, cash=debt0 + 100.0, debt=debt0, haircut=h0)
    assert well_cap["forced_qty"] == 0.0, "Zero margin deficit must result in zero forced selling"
    assert math.isclose(well_cap["remaining_position"], q0, rel_tol=1e-7)

    # Under current instance
    forced = calculate_forced_sales(q0, p0, cash0, debt0, h0)
    assert 0.0 <= forced["forced_qty"] <= q0, "Forced quantity must be non-negative and bounded by position"
    assert math.isclose(forced["remaining_position"] + forced["forced_qty"], q0, rel_tol=1e-7)
    assert math.isclose(forced["forced_proceeds"], forced["forced_qty"] * p0, rel_tol=1e-7)

    # Under stressed price triggering margin deficit: post-sale margin deficit must be resolved
    p_stress = p0 * 0.88
    forced_stress = calculate_forced_sales(q0, p_stress, cash0, debt0, h0)
    assert forced_stress["forced_qty"] > 0.0, "Substantial price drop must trigger forced liquidation"
    assert forced_stress["forced_qty"] <= q0, "Forced liquidation cannot exceed total position"
    post_stress = compute_margin_call(
        forced_stress["remaining_position"], p_stress, cash0, forced_stress["post_sale_debt"], h0
    )
    assert post_stress["margin_deficit"] <= 1e-6, "Post-sale margin deficit must be eliminated"

    # Complete insolvency condition: debt vastly exceeds asset value
    insolvent = calculate_forced_sales(q0, p0, cash=0.0, debt=p0 * q0 * 2.0, haircut=h0)
    assert math.isclose(insolvent["forced_qty"], q0, rel_tol=1e-7), "Insolvent fund must liquidate entire position"
    assert insolvent["remaining_position"] == 0.0


def test_fire_sale_impact_monotonicity() -> None:
    """Property 3: Fire-sale price degradation monotonicity and Kyle's lambda scaling."""
    depth = 0.005
    perm_coef = 1e-6

    # Zero volume produces zero impact
    zero_impact = estimate_fire_sale_discount(0.0, depth, perm_coef)
    assert zero_impact["temporary_impact"] == 0.0
    assert zero_impact["permanent_impact"] == 0.0
    assert zero_impact["total_price_drop"] == 0.0

    # Monotonicity
    impact_small = estimate_fire_sale_discount(100.0, depth, perm_coef)
    impact_large = estimate_fire_sale_discount(300.0, depth, perm_coef)

    assert impact_large["temporary_impact"] > impact_small["temporary_impact"]
    assert impact_large["permanent_impact"] > impact_small["permanent_impact"]
    assert impact_large["total_price_drop"] > impact_small["total_price_drop"]
    assert math.isclose(
        impact_large["effective_discount"],
        0.5 * impact_large["temporary_impact"] + impact_large["permanent_impact"],
        rel_tol=1e-7,
    )


def test_liquidity_spiral_simulation_conservation_and_bounds() -> None:
    """Property 4: Full dynamic liquidity spiral state conservation and spiral amplification."""
    inst = _get_instance()
    p0 = inst["p0"]
    q0 = inst["q0"]
    cash0 = inst["cash0"]
    debt0 = inst["debt0"]
    h0 = inst["haircut0"]
    shocks = inst["exogenous_shocks"]
    lam = inst["lambda_impact"]
    h_sens = inst["haircut_sensitivity"]

    sim = simulate_liquidity_spiral(
        p0=p0,
        q0=q0,
        cash0=cash0,
        debt0=debt0,
        haircut0=h0,
        exogenous_shocks=shocks,
        lambda_impact=lam,
        haircut_sensitivity=h_sens,
        policy_backstop=None,
    )

    n_steps = len(shocks)
    assert len(sim["prices"]) <= n_steps + 1
    assert len(sim["positions"]) == len(sim["prices"])
    assert len(sim["equities"]) == len(sim["prices"])

    # Prices and positions must stay non-negative
    for p in sim["prices"]:
        assert p > 0.0, "Asset price must remain positive"
    for q in sim["positions"]:
        assert q >= 0.0, "Position must remain non-negative"

    # Liquidity spiral multiplier under negative shocks must be >= 1.0
    assert sim["spiral_multiplier"] >= 1.0, "Feedback spiral must strictly weakly amplify exogenous shock"
    assert math.isclose(sim["total_forced_volume"], sum(sim["forced_sales"]), rel_tol=1e-7)


def test_margin_spiral_amplification() -> None:
    """Property 5: Endogenous haircut spiral updates haircuts and amplifies forced selling."""
    inst = _get_instance()
    p0 = inst["p0"]
    q0 = inst["q0"]
    cash0 = inst["cash0"]
    debt0 = inst["debt0"]
    h0 = inst["haircut0"]
    shocks = inst["exogenous_shocks"]
    lam = inst["lambda_impact"]

    # Baseline with zero haircut sensitivity (loss spiral only)
    sim_loss_only = simulate_liquidity_spiral(
        p0=p0,
        q0=q0,
        cash0=cash0,
        debt0=debt0,
        haircut0=h0,
        exogenous_shocks=shocks,
        lambda_impact=lam,
        haircut_sensitivity=0.0,
        policy_backstop=None,
    )

    # Coupled loss and margin spiral (haircut sensitivity > 0)
    sim_coupled = simulate_liquidity_spiral(
        p0=p0,
        q0=q0,
        cash0=cash0,
        debt0=debt0,
        haircut0=h0,
        exogenous_shocks=shocks,
        lambda_impact=lam,
        haircut_sensitivity=inst["haircut_sensitivity"],
        policy_backstop=None,
    )

    # Haircut spiral must produce strictly increasing haircuts in response to volatility
    assert sim_coupled["haircuts"][1] > sim_loss_only["haircuts"][1]
    assert sim_coupled["haircuts"][-1] > sim_loss_only["haircuts"][-1]

    # Single-period margin shock amplification: higher haircut increases forced liquidation
    f_high = calculate_forced_sales(q0, p0 * 0.95, cash0, debt0, h0 + 0.05)
    f_base = calculate_forced_sales(q0, p0 * 0.95, cash0, debt0, h0)
    assert f_high["forced_qty"] >= f_base["forced_qty"]


def test_policy_backstop_efficacy() -> None:
    """Property 6: Central bank policy backstop halts fire-sale spiral and mitigates losses."""
    inst = _get_instance()
    p0 = inst["p0"]
    q0 = inst["q0"]
    cash0 = inst["cash0"]
    debt0 = inst["debt0"]
    h0 = inst["haircut0"]
    shocks = inst["exogenous_shocks"]
    lam = inst["lambda_impact"]
    h_sens = inst["haircut_sensitivity"]
    backstop = {
        "enabled": inst["policy_enabled"],
        "price_floor": inst["policy_price_floor"],
    }

    baseline = simulate_liquidity_spiral(
        p0=p0,
        q0=q0,
        cash0=cash0,
        debt0=debt0,
        haircut0=h0,
        exogenous_shocks=shocks,
        lambda_impact=lam,
        haircut_sensitivity=h_sens,
        policy_backstop=None,
    )

    backstopped = simulate_liquidity_spiral(
        p0=p0,
        q0=q0,
        cash0=cash0,
        debt0=debt0,
        haircut0=h0,
        exogenous_shocks=shocks,
        lambda_impact=lam,
        haircut_sensitivity=h_sens,
        policy_backstop=backstop,
    )

    eval_metrics = evaluate_policy_intervention(baseline, backstopped)

    # Backstop must preserve price and attenuate multiplier
    assert eval_metrics["price_preservation"] >= -1e-6, "Backstop must not worsen price drop"
    assert eval_metrics["multiplier_attenuation"] >= -1e-6, "Backstop must not increase spiral multiplier"
    assert eval_metrics["forced_volume_reduction"] >= -1e-6, "Backstop must not increase forced selling"


def test_regime_classification() -> None:
    """Property 7: Deterministic classification of crisis feedback severity."""
    assert classify_crisis_regime(2.0, 0.01, 1.1, defaulted=False) == "ORDERLY_ABSORPTION"
    assert classify_crisis_regime(5.0, 0.03, 1.8, defaulted=False) == "LOSS_SPIRAL"
    assert classify_crisis_regime(8.0, 0.12, 2.2, defaulted=False) == "MARGIN_SPIRAL"
    assert classify_crisis_regime(15.0, 0.25, 4.5, defaulted=False) == "CATASTROPHIC_RUNAWAY"
    assert classify_crisis_regime(4.0, 0.02, 1.4, defaulted=True) == "CATASTROPHIC_RUNAWAY"

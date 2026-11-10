"""Acceptance test suite for Atlas A20: macro trade-construction engine (atlas.strategy).

Tests duration-neutral curve hedge ratios, carry and roll-down decomposition,
option convexity and analytical Greeks, payoff asymmetry ratios,
fractional Kelly position sizing, non-linear scenario revaluation grids,
and end-to-end engine orchestration across 50 random seeds.
"""

from __future__ import annotations

import math
import os
from typing import Any, cast

import numpy as np
import pytest
from instance import make_instance  # type: ignore[import-not-found, unused-ignore]

try:
    from atlas.strategy import (  # type: ignore[import-not-found, unused-ignore]
        MacroTradeEngine,
        MacroView,
        compute_asymmetry_ratio,
        compute_dv01_hedge_ratio,
        compute_expression_convexity,
        construct_curve_spread,
        evaluate_carry_and_rolldown,
        scenario_pnl_grid,
        size_trade_fractional_kelly,
    )
except ImportError:
    try:
        from strategy import (  # type: ignore[import-not-found, unused-ignore]
            MacroTradeEngine,
            MacroView,
            compute_asymmetry_ratio,
            compute_dv01_hedge_ratio,
            compute_expression_convexity,
            construct_curve_spread,
            evaluate_carry_and_rolldown,
            scenario_pnl_grid,
            size_trade_fractional_kelly,
        )
    except ImportError:
        from reference import (  # type: ignore[import-not-found, unused-ignore]
            MacroTradeEngine,
            MacroView,
            compute_asymmetry_ratio,
            compute_dv01_hedge_ratio,
            compute_expression_convexity,
            construct_curve_spread,
            evaluate_carry_and_rolldown,
            scenario_pnl_grid,
            size_trade_fractional_kelly,
        )


@pytest.fixture
def inst() -> dict[str, Any]:
    """Load test instance generated deterministically for seed."""
    seed = int(os.environ.get("PYTEST_SEED", "0"))
    return make_instance(seed)


def test_dv01_hedge_ratio_invariants(inst: dict[str, Any]) -> None:
    """Verify hedge ratio equals dv01_1 / dv01_2 and enforces domain constraints."""
    dv01_1 = float(inst["dv01_1"])
    dv01_2 = float(inst["dv01_2"])

    ratio = compute_dv01_hedge_ratio(dv01_1, dv01_2)
    expected = dv01_1 / dv01_2
    assert abs(ratio - expected) < 1e-9, f"Hedge ratio {ratio} != expected {expected}"

    # Error handling
    with pytest.raises(ValueError):
        compute_dv01_hedge_ratio(-10.0, dv01_2)
    with pytest.raises(ValueError):
        compute_dv01_hedge_ratio(dv01_1, 0.0)
    with pytest.raises(TypeError):
        compute_dv01_hedge_ratio(cast(float, "invalid"), dv01_2)


def test_curve_spread_duration_neutrality(inst: dict[str, Any]) -> None:
    """Verify spread construction satisfies net zero DV01 invariance."""
    n1 = float(inst["notional_1"])
    dv01_1 = float(inst["dv01_1"])
    dv01_2 = float(inst["dv01_2"])

    pos1, pos2 = construct_curve_spread(n1, dv01_1, dv01_2, direction="steepener")
    assert pos1 > 0, "Steepener must be long front-end leg 1"
    assert pos2 < 0, "Steepener must be short back-end leg 2"

    net_dv01 = pos1 * dv01_1 + pos2 * dv01_2
    assert abs(net_dv01) < 1e-4, f"Duration neutrality violated: net DV01 = {net_dv01}"

    # Test flattener
    flat1, flat2 = construct_curve_spread(n1, dv01_1, dv01_2, direction="flattener")
    assert flat1 < 0, "Flattener must be short front-end leg 1"
    assert flat2 > 0, "Flattener must be long back-end leg 2"
    assert abs(flat1 * dv01_1 + flat2 * dv01_2) < 1e-4

    with pytest.raises(ValueError):
        construct_curve_spread(n1, dv01_1, dv01_2, direction="invalid_dir")


def test_carry_and_rolldown_attribution(inst: dict[str, Any]) -> None:
    """Verify mathematical identity of gross carry, roll-down, and repo drag."""
    spot_yield = float(inst["spot_yield"])
    duration = float(inst["duration"])
    roll_down_bps = float(inst["roll_down_bps"])
    repo_rate = float(inst["repo_rate"])
    horizon_years = float(inst["horizon_years"])

    res = evaluate_carry_and_rolldown(
        spot_yield,
        duration,
        roll_down_bps,
        repo_rate,
        horizon_years,
    )

    expected_gross = spot_yield * horizon_years
    expected_roll = (roll_down_bps * 1e-4) * duration * horizon_years
    expected_repo = repo_rate * horizon_years
    expected_net = expected_gross + expected_roll - expected_repo

    assert abs(res["gross_carry"] - expected_gross) < 1e-8
    assert abs(res["roll_down"] - expected_roll) < 1e-8
    assert abs(res["repo_drag"] - expected_repo) < 1e-8
    assert abs(res["net_carry"] - expected_net) < 1e-8
    assert abs(res["net_carry_bps"] - expected_net * 10_000.0) < 1e-6

    # Invariant: high repo rate induces negative net carry
    res_high_repo = evaluate_carry_and_rolldown(0.02, 5.0, 5.0, 0.08, 1.0)
    assert res_high_repo["net_carry"] < 0.0

    with pytest.raises(ValueError):
        evaluate_carry_and_rolldown(0.04, -2.0, 10.0, 0.03, 1.0)


def test_expression_convexity_and_greeks(inst: dict[str, Any]) -> None:
    """Verify analytical option Greek aggregation and convexity score."""
    spot = float(inst["opt_spot"])
    strikes = cast(np.ndarray, inst["opt_strikes"])
    vols = cast(np.ndarray, inst["opt_vols"])
    expiry = float(inst["opt_expiry"])
    rate = float(inst["opt_rate"])
    weights = cast(np.ndarray, inst["opt_weights"])
    is_call = cast(np.ndarray, inst["opt_is_call"])

    res = compute_expression_convexity(
        spot,
        strikes,
        vols,
        expiry,
        rate,
        weights,
        is_call,
    )

    for greek in ("delta", "gamma", "vega", "theta", "convexity_score"):
        assert greek in res
        assert not math.isnan(res[greek])

    expected_score = res["gamma"] * (spot**2) / 100.0
    assert abs(res["convexity_score"] - expected_score) < 1e-8

    # Single call option test: positive gamma and vega
    single_call = compute_expression_convexity(
        100.0,
        np.array([100.0]),
        np.array([0.20]),
        0.5,
        0.04,
        np.array([1.0]),
        np.array([1]),
    )
    assert 0.40 < single_call["delta"] < 0.65
    assert single_call["gamma"] > 0.0
    assert single_call["vega"] > 0.0
    assert single_call["theta"] < 0.0


def test_risk_reward_asymmetry_ratio(inst: dict[str, Any]) -> None:
    """Verify expected upside / expected downside ratio and boundary limits."""
    pnl = cast(np.ndarray, inst["pnl_dist"])
    ratio = compute_asymmetry_ratio(pnl)
    assert ratio > 0.0

    # Test boundary limits
    all_positive = np.array([0.05, 0.10, 0.02, 0.15])
    assert compute_asymmetry_ratio(all_positive) == float("inf")

    all_negative = np.array([-0.05, -0.10, -0.02, -0.15])
    assert compute_asymmetry_ratio(all_negative) == 0.0

    # Symmetric distribution ~ 1.0
    sym = np.array([-0.10, -0.05, 0.05, 0.10])
    assert abs(compute_asymmetry_ratio(sym) - 1.0) < 1e-6

    with pytest.raises(ValueError):
        compute_asymmetry_ratio(np.array([]))


def test_fractional_kelly_sizing_bounds(inst: dict[str, Any]) -> None:
    """Verify fractional Kelly scaling, directional sign, and leverage cap."""
    mu = float(inst["kelly_mu"])
    var = float(inst["kelly_var"])
    w = size_trade_fractional_kelly(mu, var, fraction=0.25, max_leverage=4.0)

    unconstrained_quarter = 0.25 * (mu / var)
    expected_w = min(4.0, max(-4.0, unconstrained_quarter))
    assert abs(w - expected_w) < 1e-8

    # Test leverage ceiling
    capped_w = size_trade_fractional_kelly(0.50, 0.01, fraction=0.50, max_leverage=3.0)
    assert capped_w == 3.0

    # Test short position
    short_w = size_trade_fractional_kelly(-0.50, 0.01, fraction=0.50, max_leverage=3.0)
    assert short_w == -3.0

    with pytest.raises(ValueError):
        size_trade_fractional_kelly(0.05, -0.01)


def test_scenario_pnl_grid_shape_and_monotonicity(inst: dict[str, Any]) -> None:
    """Verify non-linear scenario P&L grid dimensions and zero-shock anchor."""
    spot_shocks = cast(np.ndarray, inst["scen_spot_shocks"])
    vol_shocks = cast(np.ndarray, inst["scen_vol_shocks"])
    spot = float(inst["opt_spot"])
    vols = cast(np.ndarray, inst["opt_vols"])
    strikes = cast(np.ndarray, inst["opt_strikes"])
    expiry = float(inst["opt_expiry"])
    rate = float(inst["opt_rate"])
    weights = cast(np.ndarray, inst["opt_weights"])
    is_call = cast(np.ndarray, inst["opt_is_call"])

    grid = scenario_pnl_grid(
        spot_shocks,
        vol_shocks,
        spot,
        vols,
        strikes,
        expiry,
        rate,
        weights,
        is_call,
        holding_period=0.0,
    )

    n_vols = len(vol_shocks)
    n_spots = len(spot_shocks)
    assert grid.shape == (n_vols, n_spots)

    # Invariant: at zero shocks and zero holding period, P&L is 0.0
    zero_vol_idx = int(np.where(np.isclose(vol_shocks, 0.0))[0][0])
    zero_spot_idx = int(np.where(np.isclose(spot_shocks, 0.0))[0][0])
    assert abs(grid[zero_vol_idx, zero_spot_idx]) < 1e-6

    # Test non-linear convexity and vega sensitivity
    # Long call option must exhibit strictly positive convexity (gamma) and positive vega
    call_grid = scenario_pnl_grid(
        np.array([-0.05, 0.0, 0.05]),
        np.array([-0.02, 0.02]),
        100.0,
        np.array([0.20]),
        np.array([100.0]),
        0.5,
        0.04,
        np.array([1.0]),
        np.array([1]),
    )
    # Monotonicity in spot
    assert call_grid[0, 0] < call_grid[0, 1] < call_grid[0, 2]
    # Positive vega: higher vol increases call value
    assert call_grid[1, 1] > call_grid[0, 1] + 1e-4
    # Positive gamma: convexity exceeds linear delta approximation
    convexity_spread = call_grid[0, 2] + call_grid[0, 0] - 2.0 * call_grid[0, 1]
    assert convexity_spread > 0.01, f"Convexity spread {convexity_spread} must be strictly positive"


def test_macro_trade_engine_end_to_end(inst: dict[str, Any]) -> None:
    """Verify complete MacroTradeEngine pipeline execution."""
    view = MacroView(
        view_id=str(inst["view_id"]),
        asset_ids=["UST_2Y", "UST_10Y"],
        view_type=str(inst["view_type"]),
        expected_move_bps=float(inst["view_expected_move_bps"]),
        confidence=float(inst["view_confidence"]),
        horizon_days=int(inst["view_horizon_days"]),
    )

    leg1 = {
        "dv01": float(inst["dv01_1"]),
        "spot_yield": float(inst["spot_yield"]),
        "duration": 2.0,
        "roll_down_bps": 5.0,
    }
    leg2 = {
        "dv01": float(inst["dv01_2"]),
        "spot_yield": 0.045,
        "duration": float(inst["duration"]),
        "roll_down_bps": float(inst["roll_down_bps"]),
    }

    engine = MacroTradeEngine(risk_free_rate=0.045)
    trade = engine.construct_trade(view, leg1, leg2, sizing_budget=1_000_000.0)

    assert trade["view_id"] == view.view_id
    assert trade["trade_type"] == "curve_steepener"
    assert trade["leg1_notional"] > 0
    assert trade["leg2_notional"] < 0
    assert abs(trade["net_dv01"]) < 1e-4
    assert trade["allocated_capital"] > 0

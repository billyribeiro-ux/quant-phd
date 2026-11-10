"""Autograder test suite for AC3 project: PEAD replication engine.

Tests all required functions against deterministic per-seed instances, verifying
algebraic invariants, boundary behavior, error handling, and numerical accuracy.
"""

from __future__ import annotations

import copy
import json
import math
import os
from typing import Any, cast

import pead_replication as sol
import pytest
from instance import make_instance


@pytest.fixture(scope="module")
def inst() -> dict[str, Any]:
    """Retrieve instance for current seed."""
    seed = int(os.environ.get("QF_SEED", "0"))
    res: dict[str, Any] = make_instance(seed)
    return cast(dict[str, Any], json.loads(res["payload"]))


# ============================================================================
# 1. Standardized Unexpected Earnings (SUE) Tests
# ============================================================================


def test_sue_accuracy_on_instance(inst: dict[str, Any]) -> None:
    """Verify SUE matches exact formula on all instance firms."""
    for firm in inst["firms"]:
        history = list(firm["history"])
        current = float(firm["current"])

        # Analytical reference
        diffs = [history[t] - history[t - 4] for t in range(4, len(history))]
        drift = sum(diffs) / len(diffs)
        expected = history[-4] + drift
        raw_error = current - expected

        errors = [d - drift for d in diffs]
        var = sum(e**2 for e in errors) / (len(errors) - 1)
        std_dev = math.sqrt(var)
        expected_sue = raw_error / std_dev

        got_sue = sol.standardized_unexpected_earnings(history, current)
        assert math.isclose(got_sue, expected_sue, rel_tol=1e-5, abs_tol=1e-5), (
            f"SUE mismatch for firm {firm['firm_id']}: got {got_sue}, expected {expected_sue}"
        )


def test_sue_scale_invariance() -> None:
    """SUE must be scale-invariant under multiplicative currency/unit changes."""
    base_history = [10.0, 11.0, 12.0, 13.0, 10.8, 11.9, 12.6, 13.9]
    base_current = 11.5

    sue_base = sol.standardized_unexpected_earnings(base_history, base_current)

    # Scale by 1000 (e.g. thousands to dollars)
    scale = 1000.0
    scaled_hist = [x * scale for x in base_history]
    scaled_curr = base_current * scale

    sue_scaled = sol.standardized_unexpected_earnings(scaled_hist, scaled_curr)
    assert math.isclose(sue_base, sue_scaled, rel_tol=1e-9, abs_tol=1e-9), (
        "SUE should be invariant to positive scalar multiplication"
    )


def test_sue_validation_errors() -> None:
    """Verify that standardized_unexpected_earnings raises ValueError for invalid inputs."""
    valid_hist = [10.0, 11.0, 12.0, 13.0, 10.5, 11.6, 12.7, 13.8]

    # Too short (< 8 observations)
    with pytest.raises(ValueError):
        sol.standardized_unexpected_earnings(valid_hist[:7], 10.0)

    # Constant seasonal differences (zero variance)
    zero_var_hist = [10.0, 11.0, 12.0, 13.0, 11.0, 12.0, 13.0, 14.0]
    with pytest.raises(ValueError):
        sol.standardized_unexpected_earnings(zero_var_hist, 12.0)

    # Unsupported forecast model
    with pytest.raises(ValueError):
        sol.standardized_unexpected_earnings(valid_hist, 10.0, forecast_type="arima")

    # Non-finite inputs
    with pytest.raises(ValueError):
        sol.standardized_unexpected_earnings(valid_hist, float("nan"))
    with pytest.raises(ValueError):
        sol.standardized_unexpected_earnings([float("inf"), *valid_hist[1:]], 10.0)


# ============================================================================
# 2. Decile Assignment Tests
# ============================================================================


def test_assign_deciles_properties(inst: dict[str, Any]) -> None:
    """Verify decile assignment properties: 10 deciles, proper bounds, monotonicity."""
    scores = {f["firm_id"]: sol.standardized_unexpected_earnings(f["history"], f["current"]) for f in inst["firms"]}

    deciles = sol.assign_deciles(scores)
    assert len(deciles) == len(scores)
    assert set(deciles.values()) == set(range(1, 11)), "All 10 deciles (1..10) must be populated"

    # Monotonicity check
    for f1, d1 in deciles.items():
        for f2, d2 in deciles.items():
            if scores[f1] < scores[f2]:
                assert d1 <= d2, f"Monotonicity violated: score {f1} < {f2} but decile {d1} > {d2}"

    # Extreme deciles
    min_firm = min(scores.keys(), key=lambda fid: scores[fid])
    max_firm = max(scores.keys(), key=lambda fid: scores[fid])
    assert deciles[min_firm] == 1, "Firm with lowest SUE must be in Decile 1"
    assert deciles[max_firm] == 10, "Firm with highest SUE must be in Decile 10"


def test_assign_deciles_deterministic_ties() -> None:
    """Ties must be broken deterministically by firm identifier ascending."""
    scores = {f"FIRM_{i:02d}": 1.50 for i in range(10)}
    deciles = sol.assign_deciles(scores)
    assert deciles["FIRM_00"] == 1
    assert deciles["FIRM_09"] == 10


def test_assign_deciles_validation() -> None:
    """assign_deciles must raise ValueError for fewer than 10 firms or invalid types."""
    with pytest.raises(ValueError):
        sol.assign_deciles({"F1": 0.5, "F2": 1.2})
    with pytest.raises(ValueError):
        sol.assign_deciles({f"F{i}": float("nan") for i in range(10)})


# ============================================================================
# 3. Post-Announcement Drift Returns Tests
# ============================================================================


def test_drift_returns_calculation(inst: dict[str, Any]) -> None:
    """Verify drift return calculation excludes announcement window and calculates mean CAR."""
    ann = inst["pre_2000_announcements"]
    h_period = (2, 60)
    drift = sol.drift_returns(ann, holding_period=h_period)

    assert set(drift.keys()) == set(range(1, 11))

    # Recompute manually for Decile 1 and Decile 10
    for test_d in [1, 10]:
        recs = [r for r in ann if r["decile"] == test_d]
        manual_cars = []
        for r in recs:
            t0 = r["announcement_day"]
            car = sum(r["daily_returns"][t0 + k] for k in range(2, 61))
            manual_cars.append(car)
        expected_mean = sum(manual_cars) / len(manual_cars)
        assert math.isclose(drift[test_d], expected_mean, rel_tol=1e-6, abs_tol=1e-6)


def test_drift_window_excludes_announcement() -> None:
    """Drift window [2, 60] must strictly exclude day 0 and day 1."""
    # Create single announcement with known returns: 100% return on day 0, 0% elsewhere
    ann = [
        {
            "firm_id": "TEST_01",
            "decile": 10,
            "daily_returns": [0.0] * 10 + [1.00] + [0.0] * 70,  # 1.00 on day 10 (announcement)
            "announcement_day": 10,
        }
    ]
    # Fill remaining deciles with zeros
    for d in range(1, 10):
        ann.append(
            {
                "firm_id": f"TEST_{d:02d}",
                "decile": d,
                "daily_returns": [0.0] * 81,
                "announcement_day": 10,
            }
        )

    drift = sol.drift_returns(ann, holding_period=(2, 60))
    # Day 10 return should NOT enter drift window [12, 70]
    assert math.isclose(drift[10], 0.0, abs_tol=1e-9), (
        "Immediate announcement day reaction must be excluded from post-announcement drift"
    )


def test_drift_returns_validation() -> None:
    """drift_returns must raise ValueError for invalid inputs."""
    with pytest.raises(ValueError):
        sol.drift_returns([])
    with pytest.raises(ValueError):
        sol.drift_returns([{"decile": 1}], holding_period=(10, 5))


# ============================================================================
# 4. Hedge Portfolio Tests
# ============================================================================


def test_hedge_portfolio_spread_and_two_leg_cost() -> None:
    """Verify hedge spread formula and two-leg cost deduction: 2 * (cost_bps / 10000)."""
    decile_rets = {1: -0.035, 10: +0.045}
    for d in range(2, 10):
        decile_rets[d] = 0.0

    cost_bps = 25.0
    hedge = sol.hedge_portfolio(decile_rets, cost_bps=cost_bps)

    expected_gross = 0.045 - (-0.035)  # 0.080
    expected_cost = 2.0 * (25.0 / 10000.0)  # 0.0050
    expected_net = expected_gross - expected_cost  # 0.0750

    assert math.isclose(hedge["gross_spread"], expected_gross, rel_tol=1e-7)
    assert math.isclose(hedge["cost_deduction"], expected_cost, rel_tol=1e-7)
    assert math.isclose(hedge["net_spread"], expected_net, rel_tol=1e-7)


def test_hedge_portfolio_negative_spread_direction() -> None:
    """Ensure hedge spread is strictly D10 - D1, not D1 - D10."""
    decile_rets = {1: +0.02, 10: -0.02}
    hedge = sol.hedge_portfolio(decile_rets, cost_bps=0.0)
    assert math.isclose(hedge["gross_spread"], -0.04, abs_tol=1e-7)


def test_hedge_portfolio_validation() -> None:
    """hedge_portfolio must raise ValueError for negative costs or missing keys."""
    with pytest.raises(ValueError):
        sol.hedge_portfolio({1: 0.01, 10: 0.05}, cost_bps=-5.0)
    with pytest.raises(ValueError):
        sol.hedge_portfolio({2: 0.01, 10: 0.05})


# ============================================================================
# 5. Subsample Decay & Transaction Cost Analysis
# ============================================================================


def test_subsample_decay_test_keys_and_properties(inst: dict[str, Any]) -> None:
    """Verify subsample decay test outputs and empirical decay relationships."""
    pre = inst["pre_2000_announcements"]
    post = inst["post_2000_announcements"]
    cost = float(inst["cost_bps"])

    res = sol.subsample_decay_test(pre, post, cost_bps=cost)

    required_keys = {"pre_gross", "pre_net", "post_gross", "post_net", "gross_decay", "net_decay"}
    assert required_keys <= set(res.keys())

    # Invariants
    assert math.isclose(res["gross_decay"], res["post_gross"] - res["pre_gross"], abs_tol=1e-8)
    assert math.isclose(res["net_decay"], res["post_net"] - res["pre_net"], abs_tol=1e-8)

    # Pre-2000 gross spread should be substantially larger than post-2000 (gross decay is negative)
    assert res["pre_gross"] > res["post_gross"], "Pre-2000 gross PEAD spread must exceed post-2000 spread"
    assert res["gross_decay"] < 0, "Gross drift decay must be negative"


# ============================================================================
# 6. Purity and Immutability Tests
# ============================================================================


def test_functions_do_not_mutate_inputs(inst: dict[str, Any]) -> None:
    """Functions must be pure and never mutate input arguments."""
    firm = inst["firms"][0]
    hist_copy = copy.deepcopy(firm["history"])
    sol.standardized_unexpected_earnings(firm["history"], firm["current"])
    assert firm["history"] == hist_copy, "earnings_history was mutated"

    pre_copy = copy.deepcopy(inst["pre_2000_announcements"])
    sol.drift_returns(inst["pre_2000_announcements"])
    assert inst["pre_2000_announcements"] == pre_copy, "announcements list was mutated"

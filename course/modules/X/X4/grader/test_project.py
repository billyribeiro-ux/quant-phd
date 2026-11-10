"""Acceptance test suite for X4 project: Stablecoin reserve stress test (stablecoin_stress.py).

Dual-mode: runs identically in the browser (Pyodide) and locally:
    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error grader/test_project.py
"""

from __future__ import annotations

import importlib
import os
from collections.abc import Callable
from typing import Any

import pytest

sol: Any = importlib.import_module(os.environ.get("QF_SOL", "stablecoin_stress"))
instance_mod = importlib.import_module("instance")
make_instance: Callable[[int], dict[str, Any]] = instance_mod.make_instance
get_reserve_assets: Callable[[dict[str, Any]], dict[str, dict[str, float]]] = instance_mod.get_reserve_assets

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
ASSETS = get_reserve_assets(INST)


def expect(condition: bool, hint: str) -> None:
    """Fail with a descriptive hint if condition is false."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(hint, pytrace=False)


def must_raise(call: Callable[[], object], condition: str, *, substring: str = "") -> None:
    """Check that call() raises ValueError with optional required substring."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError as err:
        if substring and substring not in str(err):
            pytest.fail(
                f"{condition}: ValueError message must contain '{substring}' (got: {err})",
                pytrace=False,
            )
        return
    except Exception as exc:
        pytest.fail(f"{condition}: expected ValueError, got {type(exc).__name__}: {exc}", pytrace=False)
    pytest.fail(f"{condition}: expected ValueError, none was raised", pytrace=False)


def test_input_validation() -> None:
    """Verify input validation handles invalid balance sheets, shocks, and thresholds."""
    assets = ASSETS

    must_raise(
        lambda: sol.validate_inputs(-100.0, assets, 100.0, 0.995),
        "negative total liabilities",
        substring="total_liabilities",
    )
    must_raise(
        lambda: sol.validate_inputs(10000.0, assets, -10.0, 0.995),
        "negative rate shock",
        substring="rate_shock_bps",
    )
    must_raise(
        lambda: sol.validate_inputs(10000.0, assets, 100.0, 0.40),
        "peg threshold < 0.50",
        substring="peg_threshold",
    )
    must_raise(
        lambda: sol.validate_inputs(10000.0, assets, 100.0, 1.05),
        "peg threshold > 1.00",
        substring="peg_threshold",
    )

    # Bad asset tier parameters
    bad_assets = {
        "cash": {"par": 1000.0, "duration": 0.0, "haircut": 0.0},
        "bad_tier": {"par": 1000.0, "duration": -1.0, "haircut": 0.05},
    }
    must_raise(
        lambda: sol.validate_inputs(1000.0, bad_assets, 50.0, 0.99),
        "negative duration in asset tier",
        substring="duration",
    )

    bad_haircut = {
        "cash": {"par": 1000.0, "duration": 0.0, "haircut": 1.2},
    }
    must_raise(
        lambda: sol.validate_inputs(1000.0, bad_haircut, 50.0, 0.99),
        "haircut >= 1.0",
        substring="haircut",
    )


def test_rate_shock_duration_pricing() -> None:
    """Verify modified duration mark-to-market pricing under zero and positive rate shocks."""
    assets = ASSETS

    # 1. Zero shock preserves par market value
    shocked_zero = sol.apply_rate_shock(assets, 0.0)
    for tier, data in shocked_zero.items():
        expect(
            abs(data["market_value"] - assets[tier]["par"]) < 1e-6,
            f"Zero shock should leave market value equal to par for tier '{tier}'",
        )

    # 2. Positive shock reduces value proportionally to duration
    shock_bps = INST["rate_shock_bps"]
    dy = shock_bps / 10000.0
    shocked = sol.apply_rate_shock(assets, shock_bps)

    for tier, data in shocked.items():
        base = assets[tier]
        expected_price_factor = max(0.0, 1.0 - base["duration"] * dy)
        expected_mv = base["par"] * expected_price_factor
        expect(
            abs(data["market_value"] - expected_mv) < 1e-4,
            f"Tier '{tier}' market value {data['market_value']} does not match expected {expected_mv}",
        )
        if base["duration"] > 0.0 and shock_bps > 0.0:
            expect(
                data["market_value"] < base["par"],
                f"Asset tier '{tier}' with duration {base['duration']} must lose market value under positive shock",
            )


def test_redemption_waterfall_priority_and_conservation() -> None:
    """Verify liquidation priority order, haircut accounting, and balance sheet conservation."""
    liab = INST["total_liabilities"]
    shocked = sol.apply_rate_shock(ASSETS, INST["rate_shock_bps"])
    cash_par = shocked["cash"]["market_value"]

    # 1. Small redemption covered entirely by cash has ZERO haircut loss
    small_r = min(100.0, cash_par * 0.5)
    res_small = sol.simulate_redemption_waterfall(liab, shocked, small_r)
    expect(
        abs(res_small["total_haircut_loss"]) < 1e-6,
        f"Redemptions satisfied from cash buffer must incur 0 haircut loss, got {res_small['total_haircut_loss']}",
    )
    expect(
        abs(res_small["cash_raised"] - small_r) < 1e-6,
        f"Cash raised must equal redemption request: {res_small['cash_raised']} vs {small_r}",
    )

    # 2. Large redemption exhausting cash and hitting repo/bills
    large_r = INST["test_redemptions"][1]  # 25% of liabilities
    res_large = sol.simulate_redemption_waterfall(liab, shocked, large_r)

    if large_r > cash_par:
        expect(
            res_large["total_haircut_loss"] > 0.0,
            "Redemptions exceeding cash buffer must liquidate non-cash tiers and incur positive haircut loss",
        )

    # Conservation checks
    expect(
        abs(res_large["cash_raised"] + res_large["unfulfilled_redemptions"] - large_r) < 1e-5,
        "Conservation of cash: cash_raised + unfulfilled must equal requested redemptions",
    )
    expect(
        abs(res_large["remaining_tokens"] + large_r - liab) < 1e-5,
        "Remaining tokens + redemptions must equal total initial liabilities",
    )

    # Initial shocked asset sum
    init_total_mv = sum(v["market_value"] for v in shocked.values())
    reconstructed_init = (
        res_large["remaining_market_value"] + res_large["cash_raised"] + res_large["total_haircut_loss"]
    )
    expect(
        abs(init_total_mv - reconstructed_init) < 1e-4,
        f"Asset balance sheet conservation failed: initial MV {init_total_mv} != {reconstructed_init}",
    )

    # NAV definition: remaining_market_value / remaining_tokens
    if res_large["remaining_tokens"] > 1e-6:
        expected_nav = res_large["remaining_market_value"] / res_large["remaining_tokens"]
        expect(
            abs(res_large["nav"] - expected_nav) < 1e-5,
            f"NAV must equal remaining market value / remaining tokens: {res_large['nav']} vs {expected_nav}",
        )


def test_nav_monotonic_decay() -> None:
    """Verify that NAV is monotonically non-increasing in redemptions and in rate shocks.

    When assets <= liabilities (no surplus cushion), every dollar of redemption
    depletes reserves at least 1:1, causing NAV to be strictly non-increasing in R.
    Across rate shocks, higher yield shocks strictly reduce bond values and NAV.
    """
    liab = INST["total_liabilities"]
    base_assets = ASSETS

    # 1. Monotonicity with respect to redemptions when reserves are at par (no initial surplus)
    tot_par = sum(v["par"] for v in base_assets.values())
    par_assets = {
        k: {"par": v["par"] * liab / tot_par, "duration": v["duration"], "haircut": v["haircut"]}
        for k, v in base_assets.items()
    }
    shocked = sol.apply_rate_shock(par_assets, 100.0)
    redemption_steps = [0.0, liab * 0.1, liab * 0.25, liab * 0.5, liab * 0.75]
    navs = [sol.simulate_redemption_waterfall(liab, shocked, r)["nav"] for r in redemption_steps]

    for i in range(len(navs) - 1):
        expect(
            navs[i] >= navs[i + 1] - 1e-6,
            f"NAV must be non-increasing with redemptions: step {i} ({navs[i]}) < step {i + 1} ({navs[i + 1]})",
        )

    # 2. Monotonicity with respect to interest rate shocks
    fixed_r = liab * 0.20
    shocks = [0.0, 50.0, 150.0, 300.0]
    navs_by_shock = [
        sol.simulate_redemption_waterfall(liab, sol.apply_rate_shock(base_assets, s), fixed_r)["nav"] for s in shocks
    ]

    for i in range(len(navs_by_shock) - 1):
        expect(
            navs_by_shock[i] >= navs_by_shock[i + 1] - 1e-6,
            f"NAV must be non-increasing with rate shocks: {navs_by_shock[i]} < {navs_by_shock[i + 1]}",
        )


def test_peg_break_threshold_search() -> None:
    """Verify bisection search accurately locates the critical run size R*."""
    liab = INST["total_liabilities"]
    shocked = sol.apply_rate_shock(ASSETS, INST["rate_shock_bps"])
    threshold = INST["peg_threshold"]

    pb = sol.find_peg_break_run_size(liab, shocked, threshold)

    expect("peg_broken" in pb, "Output missing 'peg_broken' flag")
    expect("critical_run_amount" in pb, "Output missing 'critical_run_amount'")
    expect("critical_run_pct" in pb, "Output missing 'critical_run_pct'")

    r_star = pb["critical_run_amount"]
    expect(
        0.0 <= r_star <= liab,
        f"Critical run amount R* must lie in [0, liabilities]: got {r_star}",
    )
    expect(
        abs(pb["critical_run_pct"] - (r_star / liab)) < 1e-5,
        "Critical run percentage must equal critical_run_amount / total_liabilities",
    )

    # If peg breaks strictly within (10, liab - 10), verify boundary behavior
    if 10.0 < r_star < (liab - 10.0):
        nav_below = sol.simulate_redemption_waterfall(liab, shocked, r_star - 1.0)["nav"]
        nav_above = sol.simulate_redemption_waterfall(liab, shocked, r_star + 1.0)["nav"]
        expect(
            nav_below >= threshold - 1e-4,
            f"Right below R*, NAV must be >= threshold: NAV({r_star - 1:.1f})={nav_below} vs {threshold}",
        )
        expect(
            nav_above <= threshold + 1e-4,
            f"Right above R*, NAV must be <= threshold: NAV({r_star + 1:.1f})={nav_above} vs {threshold}",
        )


def test_liquidity_coverage_ratio() -> None:
    """Verify Liquidity Coverage Ratio (LCR) computation."""
    assets = ASSETS
    outflow = INST["stressed_outflow_30d"]

    lcr = sol.compute_liquidity_coverage_ratio(assets, outflow)
    expected_lcr = (assets["cash"]["par"] + assets["overnight_repo"]["par"]) / outflow

    expect(
        abs(lcr - expected_lcr) < 1e-5,
        f"LCR should be {expected_lcr:.4f}, got {lcr:.4f}",
    )

    must_raise(
        lambda: sol.compute_liquidity_coverage_ratio(assets, -500.0),
        "negative stressed outflow",
        substring="stressed_outflow_30d",
    )


def test_stress_grid_execution() -> None:
    """Verify 2D stress grid returns correct matrix dimensions and monotonic values."""
    liab = INST["total_liabilities"]
    base_assets = ASSETS
    shocks = [0.0, 100.0, 250.0]
    fracs = [0.10, 0.30, 0.60]

    grid = sol.run_stress_grid(liab, base_assets, shocks, fracs, peg_threshold=0.995)

    expect("nav_matrix" in grid, "Grid output missing 'nav_matrix'")
    matrix = grid["nav_matrix"]

    expect(len(matrix) == len(shocks), f"Matrix row count must be {len(shocks)}, got {len(matrix)}")
    for row in matrix:
        expect(len(row) == len(fracs), f"Matrix col count must be {len(fracs)}, got {len(row)}")

    # Check top-left vs bottom-right (least stressed vs most stressed)
    expect(
        matrix[0][0] >= matrix[-1][-1],
        f"Zero shock / 10% run ({matrix[0][0]}) must have higher NAV than 250bps / 60% run ({matrix[-1][-1]})",
    )

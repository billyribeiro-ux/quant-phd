"""Acceptance suite for the BK3 project: LDI collateral-spiral model (ldi_model.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your ldi_model.py next to this file. Warnings are treated as errors.

Each test verifies one property or boundary condition from the project specification:
- Integer arithmetic and exact Fraction rounding (half-up)
- Non-negative parameter validations (ValueError on negative inputs)
- Exact margin calls and monotone growth in cumulative yield moves
- Forced-selling threshold formula verified against exhaustive discrete search
- Collateral spiral steps, conservation of cash buffer, backstop absorption, and termination
"""

from __future__ import annotations

import math
import os
from fractions import Fraction
from typing import Any

import ldi_model as sol  # type: ignore[import-not-found]
import pytest
from instance import make_instance  # type: ignore[import-not-found]

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(SEED + 7_919)


def _oracle_round_half_up(val: Fraction) -> int:
    __tracebackhide__ = True
    return math.floor(val + Fraction(1, 2))


def _make_fund_from_dict(d: dict[str, Any]) -> Any:
    __tracebackhide__ = True
    return sol.Fund(
        assets_cents=d["assets_cents"],
        asset_duration_cy=d["asset_duration_cy"],
        overlay_notional_cents=d["overlay_notional_cents"],
        overlay_duration_cy=d["overlay_duration_cy"],
        buffer_cents=d["buffer_cents"],
        impact_bps_per_gcent=d["impact_bps_per_gcent"],
        backstop_trigger_bps=d["backstop_trigger_bps"],
        backstop_capacity_cents=d["backstop_capacity_cents"],
    )


# =====================================================================================================================
# 1. Fund Dataclass and Parameter Validation
# =====================================================================================================================


def test_fund_creation_valid() -> None:
    fund = _make_fund_from_dict(INST)
    assert fund.assets_cents == INST["assets_cents"], "Fund.assets_cents mismatch"
    assert fund.buffer_cents == INST["buffer_cents"], "Fund.buffer_cents mismatch"
    assert fund.overlay_notional_cents == INST["overlay_notional_cents"], "Fund.overlay_notional_cents mismatch"


@pytest.mark.parametrize(
    ("field", "val"),
    [
        ("assets_cents", 0),
        ("assets_cents", -100),
        ("asset_duration_cy", -1),
        ("overlay_notional_cents", -50),
        ("overlay_duration_cy", -10),
        ("buffer_cents", -1),
        ("impact_bps_per_gcent", -5),
        ("backstop_trigger_bps", -1),
        ("backstop_capacity_cents", -1),
    ],
)
def test_fund_invalid_parameters_raise(field: str, val: int) -> None:
    params = {
        "assets_cents": 1_000_000_000,
        "asset_duration_cy": 1000,
        "overlay_notional_cents": 500_000_000,
        "overlay_duration_cy": 1500,
        "buffer_cents": 10_000_000,
        "impact_bps_per_gcent": 1000,
        "backstop_trigger_bps": 50,
        "backstop_capacity_cents": 20_000_000,
    }
    params[field] = val
    with pytest.raises(ValueError):
        sol.Fund(**params)


# =====================================================================================================================
# 2. Cumulative Margin Call
# =====================================================================================================================


def test_margin_call_zero_at_zero() -> None:
    fund = _make_fund_from_dict(INST)
    assert sol.margin_call_cents(fund, 0) == 0, "margin call at 0 bps must be 0 cents"


def test_margin_call_negative_raises() -> None:
    fund = _make_fund_from_dict(INST)
    with pytest.raises(ValueError):
        sol.margin_call_cents(fund, -1)


def test_margin_call_monotone() -> None:
    fund = _make_fund_from_dict(INST)
    prev = 0
    for bps in range(0, 150, 10):
        call = sol.margin_call_cents(fund, bps)
        assert call >= prev, "margin_call_cents must be non-decreasing in cumulative_bps"
        prev = call


def test_margin_call_rounding_half_up() -> None:
    # Construct exact .5 fixture: N * D_h * Y / 10^6 ends in .5
    # Let N = 100_000, D_h = 10, then N * D_h = 1_000_000.
    # N * D_h * Y / 10^6 = Y.
    # To get .5: let N * D_h = 500_000, then Y = 1 gives 500_000 / 10^6 = 0.5 cents -> rounds to 1 cent.
    fund = sol.Fund(
        assets_cents=100_000_000,
        asset_duration_cy=500,
        overlay_notional_cents=50_000,
        overlay_duration_cy=10,  # 50_000 * 10 = 500_000
        buffer_cents=1_000_000,
        impact_bps_per_gcent=100,
        backstop_trigger_bps=50,
        backstop_capacity_cents=500_000,
    )
    call = sol.margin_call_cents(fund, 1)
    assert call == 1, "0.5 cents must round half up to 1 cent (not truncate to 0)"


def test_margin_call_matches_oracle_on_instance() -> None:
    fund = _make_fund_from_dict(INST)
    for bps in [5, 17, 33, 75, 120]:
        exact = Fraction(fund.overlay_notional_cents * fund.overlay_duration_cy * bps, 1_000_000)
        expected = _oracle_round_half_up(exact)
        actual = sol.margin_call_cents(fund, bps)
        assert actual == expected, "margin call must match round_half_up(N * D_h * Y / 10^6)"


# =====================================================================================================================
# 3. Forced Selling Threshold
# =====================================================================================================================


def test_threshold_bps_oracle_search() -> None:
    fund = _make_fund_from_dict(INST)
    thresh = sol.threshold_bps(fund)
    assert thresh is not None, "threshold_bps must not be None when overlay notional and duration are positive"

    # Oracle search: find smallest s in 0..10_000 where call > buffer
    oracle_s: int | None = None
    for s in range(10_001):
        if sol.margin_call_cents(fund, s) > fund.buffer_cents:
            oracle_s = s
            break

    assert thresh == oracle_s, "threshold_bps must match the discrete search oracle"


def test_threshold_bps_boundary_check() -> None:
    fund = _make_fund_from_dict(INST)
    s_star = sol.threshold_bps(fund)
    assert s_star is not None
    assert s_star > 0, "threshold_bps should be positive for positive buffer"

    # Below threshold: call <= buffer
    call_below = sol.margin_call_cents(fund, s_star - 1)
    assert call_below <= fund.buffer_cents, "margin call at (threshold - 1) must be <= buffer_cents"

    # At threshold: call > buffer
    call_at = sol.margin_call_cents(fund, s_star)
    assert call_at > fund.buffer_cents, "margin call at threshold must be > buffer_cents"


def test_threshold_bps_none_when_zero_overlay() -> None:
    fund_zero_notional = sol.Fund(
        assets_cents=100_000_000,
        asset_duration_cy=500,
        overlay_notional_cents=0,
        overlay_duration_cy=1000,
        buffer_cents=1_000_000,
        impact_bps_per_gcent=100,
        backstop_trigger_bps=50,
        backstop_capacity_cents=500_000,
    )
    assert sol.threshold_bps(fund_zero_notional) is None, "threshold_bps must return None when overlay notional is 0"

    fund_zero_dur = sol.Fund(
        assets_cents=100_000_000,
        asset_duration_cy=500,
        overlay_notional_cents=500_000_000,
        overlay_duration_cy=0,
        buffer_cents=1_000_000,
        impact_bps_per_gcent=100,
        backstop_trigger_bps=50,
        backstop_capacity_cents=500_000,
    )
    assert sol.threshold_bps(fund_zero_dur) is None, "threshold_bps must return None when overlay duration is 0"


# =====================================================================================================================
# 4. Hand-Computed Fixtures (Independent of Random Seeds)
# =====================================================================================================================


def test_hand_computed_fixture() -> None:
    # Fixture: N = 10^8 cents ($1,000,000), D_h = 500 (5.00y), B = 10^6 cents ($10,000)
    # N * D_h = 50_000_000_000
    # num = (2 * 10^6 + 1) * 10^6 = 2_000_001_000_000
    # den = 2 * 50_000_000_000 = 100_000_000_000
    # num / den = 20.00001 -> ceil gives 21 bps.
    fund = sol.Fund(
        assets_cents=500_000_000,
        asset_duration_cy=800,
        overlay_notional_cents=100_000_000,
        overlay_duration_cy=500,
        buffer_cents=1_000_000,
        impact_bps_per_gcent=2000,
        backstop_trigger_bps=80,
        backstop_capacity_cents=10_000_000,
    )
    assert sol.threshold_bps(fund) == 21, "threshold_bps for hand fixture must be 21"
    assert sol.margin_call_cents(fund, 20) == 1_000_000, "call at 20 bps must be 1,000,000 cents"
    assert sol.margin_call_cents(fund, 21) == 1_050_000, "call at 21 bps must be 1,050,000 cents"


# =====================================================================================================================
# 5. Collateral Spiral Simulation (run_steps)
# =====================================================================================================================


def test_run_steps_negative_shock_raises() -> None:
    fund = _make_fund_from_dict(INST)
    with pytest.raises(ValueError):
        sol.run_steps(fund, -5, backstop=False)


def test_run_steps_initial_conditions() -> None:
    fund = _make_fund_from_dict(INST)
    shock = INST["shock_bps"]
    steps = sol.run_steps(fund, shock, backstop=False)
    assert len(steps) >= 1, "run_steps must return at least one step"
    step0 = steps[0]
    assert step0.step == 0, "first step index must be 0"
    assert step0.cumulative_bps == shock, "step 0 cumulative_bps must match the initial shock"
    assert step0.margin_call_cents == sol.margin_call_cents(fund, shock), (
        "step 0 margin call must match margin_call_cents(fund, shock)"
    )


def test_run_steps_buffer_conservation() -> None:
    fund = _make_fund_from_dict(INST)
    steps = sol.run_steps(fund, INST["shock_bps"], backstop=False)
    total_buffer_paid = sum(s.buffer_paid_cents for s in steps)
    assert total_buffer_paid <= fund.buffer_cents, (
        "total buffer paid across all steps cannot exceed initial buffer_cents"
    )


def test_run_steps_forced_sale_identity() -> None:
    fund = _make_fund_from_dict(INST)
    steps = sol.run_steps(fund, INST["shock_bps"], backstop=False)
    for s in steps:
        assert s.forced_sale_cents == s.margin_call_cents - s.buffer_paid_cents, (
            "forced_sale_cents must equal margin_call_cents minus buffer_paid_cents"
        )


def test_run_steps_termination_condition() -> None:
    fund = _make_fund_from_dict(INST)
    steps = sol.run_steps(fund, INST["shock_bps"], backstop=False)
    assert len(steps) <= 50, "run_steps must not exceed the 50-step cap"
    last_step = steps[-1]
    # If terminated before 50 steps, forced_sale == 0 or price_impact == 0
    if len(steps) < 50:
        assert last_step.forced_sale_cents == 0 or last_step.price_impact_bps == 0, (
            "early termination requires forced_sale == 0 or price_impact == 0"
        )


def test_run_steps_large_buffer_no_forced_sales() -> None:
    # A fund with a very large buffer should pay step 0 in full and terminate immediately
    fund = sol.Fund(
        assets_cents=1_000_000_000,
        asset_duration_cy=1000,
        overlay_notional_cents=100_000_000,
        overlay_duration_cy=500,
        buffer_cents=100_000_000,  # $1,000,000 buffer
        impact_bps_per_gcent=1000,
        backstop_trigger_bps=50,
        backstop_capacity_cents=10_000_000,
    )
    steps = sol.run_steps(fund, 10, backstop=False)
    assert len(steps) == 1, "simulation with large buffer must terminate after step 0"
    assert steps[0].forced_sale_cents == 0, "step 0 forced sales must be 0 when buffer covers margin call"
    assert steps[0].price_impact_bps == 0, "step 0 price impact must be 0 when forced sales are 0"


def test_run_steps_backstop_absorption() -> None:
    fund = _make_fund_from_dict(INST)
    shock = fund.backstop_trigger_bps + 20  # ensure yield is above backstop trigger
    steps_no_backstop = sol.run_steps(fund, shock, backstop=False)
    steps_with_backstop = sol.run_steps(fund, shock, backstop=True)

    assert all(s.backstop_absorbed_cents == 0 for s in steps_no_backstop), (
        "no sales may be absorbed when backstop is False"
    )

    total_absorbed = sum(s.backstop_absorbed_cents for s in steps_with_backstop)
    assert total_absorbed <= fund.backstop_capacity_cents, "total absorbed sales cannot exceed backstop_capacity_cents"

    # Absorbed sales reduce unabsorbed sales, which dampens price impact
    total_yield_no = steps_no_backstop[-1].cumulative_bps + steps_no_backstop[-1].price_impact_bps
    total_yield_with = steps_with_backstop[-1].cumulative_bps + steps_with_backstop[-1].price_impact_bps
    assert total_yield_with <= total_yield_no, (
        "backstop must not result in higher cumulative yield moves than no backstop"
    )


def test_second_instance_distinction() -> None:
    fund1 = _make_fund_from_dict(INST)
    fund2 = _make_fund_from_dict(INST2)
    thresh1 = sol.threshold_bps(fund1)
    thresh2 = sol.threshold_bps(fund2)
    assert thresh1 is not None and thresh2 is not None
    # Instances vary across seeds
    assert (
        fund1.overlay_notional_cents != fund2.overlay_notional_cents
        or fund1.buffer_cents != fund2.buffer_cents
        or thresh1 != thresh2
    ), "different seeds must produce different fund parameters"

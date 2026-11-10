"""Acceptance test suite for the BK5 project: retirement planning engine (retirement_plan.py).

Runs in the browser (Pyodide) and locally:
    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any

import pytest
from instance import make_instance

try:
    import retirement_plan as sol
except ImportError:
    import reference as sol

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(SEED + 9_973)


# -----------------------------------------------------------------------------
# Oracles based on first principles and the project specification
# -----------------------------------------------------------------------------


def oracle_human_capital(earnings_cents: list[int], discount_rate_bps: int) -> int:
    r = discount_rate_bps / 10_000.0
    return round(sum(e / ((1.0 + r) ** t) for t, e in enumerate(earnings_cents, start=1)))


def oracle_asset_location(
    eq_target: int, bond_target: int, tax_cap: int, tda_cap: int, roth_cap: int
) -> dict[str, dict[str, int]]:
    tda_bond = min(bond_target, tda_cap)
    rem_bond = bond_target - tda_bond
    tax_bond = min(rem_bond, tax_cap)
    roth_bond = rem_bond - tax_bond
    return {
        "taxable": {"equity": tax_cap - tax_bond, "bond": tax_bond},
        "tda": {"equity": tda_cap - tda_bond, "bond": tda_bond},
        "roth": {"equity": roth_cap - roth_bond, "bond": roth_bond},
    }


# -----------------------------------------------------------------------------
# Part 1: Human Capital Valuation Tests
# -----------------------------------------------------------------------------


def test_human_capital_validations() -> None:
    with pytest.raises(ValueError):
        sol.human_capital_value([], 350)
    with pytest.raises(ValueError):
        sol.human_capital_value([100, -50, 100], 350)
    with pytest.raises(ValueError):
        sol.human_capital_value([100, 100], -10)


def test_human_capital_zero_discount_rate() -> None:
    earnings = [1_000_000, 2_000_000, 3_000_000]
    expected = sum(earnings)
    result = sol.human_capital_value(earnings, 0)
    assert result == expected, "Zero discount rate must equal exact sum of earnings"


def test_human_capital_monotonicity() -> None:
    earnings = INST["earnings_cents"]
    pv_low = sol.human_capital_value(earnings, 200)
    pv_mid = sol.human_capital_value(earnings, 400)
    pv_high = sol.human_capital_value(earnings, 600)
    assert pv_low > pv_mid > pv_high, "Human capital must strictly decrease as discount rate increases"


def test_human_capital_oracle_agreement() -> None:
    for case in (INST, INST2):
        actual = sol.human_capital_value(case["earnings_cents"], case["discount_rate_bps"])
        expected = oracle_human_capital(case["earnings_cents"], case["discount_rate_bps"])
        assert actual == expected, "Human capital value must match exact analytical oracle"


# -----------------------------------------------------------------------------
# Part 2: Asset Location Tests
# -----------------------------------------------------------------------------


def test_asset_location_validations() -> None:
    with pytest.raises(ValueError):
        sol.optimal_asset_location(-100, 200, 100, 100, 0)
    with pytest.raises(ValueError):
        sol.optimal_asset_location(100, 100, 50, 50, 50)  # total target 200 != capacity 150


def test_asset_location_conservation_and_invariants() -> None:
    for case in (INST, INST2):
        loc = sol.optimal_asset_location(
            case["equity_target_cents"],
            case["bond_target_cents"],
            case["taxable_capacity_cents"],
            case["tda_capacity_cents"],
            case["roth_capacity_cents"],
        )
        total_eq = loc["taxable"]["equity"] + loc["tda"]["equity"] + loc["roth"]["equity"]
        total_bond = loc["taxable"]["bond"] + loc["tda"]["bond"] + loc["roth"]["bond"]
        assert total_eq == case["equity_target_cents"], "Total allocated equity must equal equity target"
        assert total_bond == case["bond_target_cents"], "Total allocated bonds must equal bond target"

        assert loc["taxable"]["equity"] + loc["taxable"]["bond"] == case["taxable_capacity_cents"]
        assert loc["tda"]["equity"] + loc["tda"]["bond"] == case["tda_capacity_cents"]
        assert loc["roth"]["equity"] + loc["roth"]["bond"] == case["roth_capacity_cents"]


def test_asset_location_priority_tda_first() -> None:
    # When TDA has plenty of room, all bonds must be in TDA
    loc = sol.optimal_asset_location(
        equity_target_cents=60_000_000,
        bond_target_cents=40_000_000,
        taxable_capacity_cents=30_000_000,
        tda_capacity_cents=50_000_000,
        roth_capacity_cents=20_000_000,
    )
    assert loc["tda"]["bond"] == 40_000_000, "All bonds should be placed in TDA when TDA capacity allows"
    assert loc["taxable"]["bond"] == 0, "No bonds should be placed in Taxable when TDA has room"
    assert loc["roth"]["bond"] == 0, "No bonds should be placed in Roth when TDA has room"
    assert loc["roth"]["equity"] == 20_000_000, "Roth should hold pure equity"


def test_asset_location_oracle_agreement() -> None:
    for case in (INST, INST2):
        actual = sol.optimal_asset_location(
            case["equity_target_cents"],
            case["bond_target_cents"],
            case["taxable_capacity_cents"],
            case["tda_capacity_cents"],
            case["roth_capacity_cents"],
        )
        expected = oracle_asset_location(
            case["equity_target_cents"],
            case["bond_target_cents"],
            case["taxable_capacity_cents"],
            case["tda_capacity_cents"],
            case["roth_capacity_cents"],
        )
        assert actual == expected, "Asset location must match exact oracle"


# -----------------------------------------------------------------------------
# Part 3: Moving-Block Bootstrap Tests
# -----------------------------------------------------------------------------


def test_moving_block_bootstrap_validations() -> None:
    with pytest.raises(ValueError):
        sol.moving_block_bootstrap([], 3, 10, 5, 42)
    with pytest.raises(ValueError):
        sol.moving_block_bootstrap([0.05, 0.02], 5, 10, 5, 42)  # block_length > len(returns)
    with pytest.raises(ValueError):
        sol.moving_block_bootstrap([0.05, 0.02], 0, 10, 5, 42)  # block_length < 1


def test_moving_block_bootstrap_shape_and_range() -> None:
    returns = INST["historical_returns"]
    b = INST["block_length"]
    h = INST["horizon_years"]
    n_p = INST["n_simulations"]
    paths = sol.moving_block_bootstrap(returns, b, h, n_p, 42)
    assert len(paths) == n_p, f"Expected {n_p} paths"
    for p in paths:
        assert len(p) == h, f"Expected path length {h}"
        for ret in p:
            assert ret in returns, "Every resampled return must come from the original historical series"


def test_moving_block_bootstrap_preserves_intra_block_structure() -> None:
    # A distinct marker series: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    series = [float(x) for x in range(10)]
    block_len = 3
    paths = sol.moving_block_bootstrap(series, block_len, 30, 50, seed=123)
    # Consecutive elements within a block must satisfy path[t+1] == path[t] + 1 (unless at a block boundary)
    matched_transitions = 0
    total_transitions = 0
    for p in paths:
        for t in range(len(p) - 1):
            total_transitions += 1
            if p[t + 1] == p[t] + 1.0:
                matched_transitions += 1

    ratio = matched_transitions / total_transitions
    assert ratio >= 0.50, f"Moving block bootstrap must preserve intra-block dependence (found ratio {ratio:.3f})"


# -----------------------------------------------------------------------------
# Part 4: Withdrawal Simulation and Safe Withdrawal Rate Tests
# -----------------------------------------------------------------------------


def test_withdrawal_simulation_beginning_of_year_timing() -> None:
    single_path = [[0.50]]
    sim = sol.simulate_withdrawals(initial_wealth_cents=10_000, initial_withdrawal_bps=10_000, return_paths=single_path)
    assert sim["ruin_probability"] == 1.0, (
        "Beginning-of-year withdrawal must ruin immediately when withdrawal equals wealth"
    )


def test_withdrawal_simulation_properties() -> None:
    paths = sol.moving_block_bootstrap(INST["historical_returns"], INST["block_length"], 30, 100, seed=77)
    sim_low = sol.simulate_withdrawals(100_000_000, 300, paths)
    sim_high = sol.simulate_withdrawals(100_000_000, 700, paths)

    assert 0.0 <= sim_low["ruin_probability"] <= 1.0
    assert 0.0 <= sim_high["ruin_probability"] <= 1.0
    assert sim_low["ruin_probability"] <= sim_high["ruin_probability"], (
        "Ruin probability must be non-decreasing in withdrawal rate"
    )
    assert sim_low["median_terminal_wealth_cents"] >= sim_high["median_terminal_wealth_cents"]


def test_safe_withdrawal_rate_bounds() -> None:
    paths = sol.moving_block_bootstrap(INST["historical_returns"], INST["block_length"], 30, 100, seed=77)
    swr = sol.safe_withdrawal_rate(100_000_000, paths, max_ruin_prob=0.05, step_bps=10)
    assert 100 <= swr <= 1000, f"SWR {swr} bps should be within plausible range [100, 1000]"

    sim_swr = sol.simulate_withdrawals(100_000_000, swr, paths)
    assert sim_swr["ruin_probability"] <= 0.05 + 1e-6, "SWR must respect maximum ruin probability constraint"

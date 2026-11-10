"""Test suite for SR2 Leverage-cycle model (Dual-mode pytest suite).

Evaluates solver.py on deterministic per-seed instances against theoretical invariants,
marginal buyer indifference conditions, market-clearing identities, margin-shock directionality,
and exception contracts.
"""

from __future__ import annotations

import os
from typing import Any

import pytest
from instance import make_instance  # type: ignore[import-not-found]

try:
    from solver import (  # type: ignore[import-not-found]
        simulate_margin_shock,
        solve_geanakoplos_equilibrium,
        solve_three_period_cycle,
    )
except ImportError:
    from reference import (  # type: ignore[import-not-found]
        simulate_margin_shock,
        solve_geanakoplos_equilibrium,
        solve_three_period_cycle,
    )


@pytest.fixture
def instance() -> dict[str, Any]:
    """Retrieve deterministic instance parameters for the active test seed."""
    seed = int(os.environ.get("QF_SEED", "0"))
    inst: dict[str, Any] = make_instance(seed)
    return inst


def test_equilibrium_keys_and_types(instance: dict[str, Any]) -> None:
    """Verify solve_geanakoplos_equilibrium returns required keys with valid float values."""
    __tracebackhide__ = True
    res = solve_geanakoplos_equilibrium(
        v_u=instance["v_u"],
        v_d=instance["v_d"],
        risk_free_rate=instance["risk_free_rate"],
        max_loan_ratio=instance["initial_loan_ratio"],
    )
    assert isinstance(res, dict), "solve_geanakoplos_equilibrium must return a dictionary"
    required_keys = {"price", "marginal_buyer", "loan", "margin", "leverage", "haircut"}
    for k in required_keys:
        assert k in res, f"Missing required key '{k}' in equilibrium output"
        assert isinstance(res[k], (float, int)), f"Key '{k}' must be numeric"

    assert 0.0 <= res["marginal_buyer"] <= 1.0, "marginal_buyer must lie in [0, 1]"
    assert res["price"] > 0.0, "price must be strictly positive"
    assert res["loan"] >= 0.0, "loan must be non-negative"
    assert res["margin"] > 0.0, "margin must be strictly positive"
    assert res["leverage"] >= 1.0, "leverage must be >= 1.0"
    assert 0.0 <= res["haircut"] <= 1.0, "haircut must lie in [0, 1]"


def test_balance_sheet_and_margin_identities(instance: dict[str, Any]) -> None:
    """Check that price = loan + margin, leverage = price / margin, and haircut = margin / price."""
    __tracebackhide__ = True
    res = solve_geanakoplos_equilibrium(
        v_u=instance["v_u"],
        v_d=instance["v_d"],
        risk_free_rate=instance["risk_free_rate"],
        max_loan_ratio=instance["initial_loan_ratio"],
    )
    p = res["price"]
    loan_val = res["loan"]
    m = res["margin"]
    lev = res["leverage"]
    hc = res["haircut"]

    assert abs(p - (loan_val + m)) < 1e-9, (
        f"Balance sheet identity violated: price ({p}) != loan ({loan_val}) + margin ({m})"
    )
    assert abs(lev - (p / m)) < 1e-9, f"Leverage definition violated: {lev} != {p / m}"
    assert abs(hc - (m / p)) < 1e-9, f"Haircut definition violated: {hc} != {m / p}"


def test_marginal_buyer_indifference_condition(instance: dict[str, Any]) -> None:
    """Verify that the marginal buyer's expected return on equity equals the gross risk-free rate."""
    __tracebackhide__ = True
    vu = instance["v_u"]
    vd = instance["v_d"]
    rf = instance["risk_free_rate"]
    theta = instance["initial_loan_ratio"]

    res = solve_geanakoplos_equilibrium(vu, vd, rf, theta)
    h_star = res["marginal_buyer"]
    margin = res["margin"]

    # In equilibrium, equity payoff at t=1:
    # State U: vu - theta * vd
    # State D: (1 - theta) * vd
    # Expected equity payoff for marginal buyer h*:
    expected_payoff = (1.0 - theta) * vd + h_star * (vu - vd)
    # Return on equity: expected_payoff / margin
    return_on_equity = expected_payoff / margin

    assert abs(return_on_equity - rf) < 1e-7, (
        f"Marginal buyer indifference condition failed: return {return_on_equity:.6f} != rf {rf:.6f}"
    )


def test_market_clearing_condition(instance: dict[str, Any]) -> None:
    """Check that total asset demand from optimists [h*, 1] clears the supply Q = 1."""
    __tracebackhide__ = True
    vu = instance["v_u"]
    vd = instance["v_d"]
    rf = instance["risk_free_rate"]
    theta = instance["initial_loan_ratio"]

    res = solve_geanakoplos_equilibrium(vu, vd, rf, theta)
    h_star = res["marginal_buyer"]
    margin = res["margin"]

    # Optimists have wealth integral_{h*}^1 1 dh = 1 - h*
    optimist_wealth = 1.0 - h_star
    # Total asset demand: optimist_wealth / margin
    asset_demand = optimist_wealth / margin

    assert abs(asset_demand - 1.0) < 1e-7, (
        f"Asset market clearing violated: total demand {asset_demand:.6f} != supply 1.0"
    )


def test_margin_shock_properties(instance: dict[str, Any]) -> None:
    """Check that an exogenous margin tightening drives price down and increases haircuts."""
    __tracebackhide__ = True
    vu = instance["v_u"]
    vd = instance["v_d"]
    rf = instance["risk_free_rate"]
    theta_0 = instance["initial_loan_ratio"]
    theta_1 = instance["shocked_loan_ratio"]

    res = simulate_margin_shock(vu, vd, theta_0, theta_1, rf)
    required = {
        "initial_price",
        "shocked_price",
        "price_drop",
        "price_drop_pct",
        "initial_leverage",
        "shocked_leverage",
        "initial_haircut",
        "shocked_haircut",
        "marginal_buyer_shift",
    }
    for k in required:
        assert k in res, f"simulate_margin_shock output missing '{k}'"

    # Price must strictly drop
    assert res["price_drop"] > 0.0, (
        f"Margin shock did not reduce price: initial={res['initial_price']}, shocked={res['shocked_price']}"
    )
    assert res["price_drop_pct"] > 0.0, "price_drop_pct must be positive"
    # Haircut must increase
    assert res["shocked_haircut"] > res["initial_haircut"], (
        f"Haircut did not widen: initial={res['initial_haircut']}, shocked={res['shocked_haircut']}"
    )
    # Leverage must fall
    assert res["shocked_leverage"] < res["initial_leverage"], (
        f"Leverage did not decline: initial={res['initial_leverage']}, shocked={res['shocked_leverage']}"
    )


def test_three_period_cycle_consistency(instance: dict[str, Any]) -> None:
    """Verify that 3-period cycle generates a positive crash drop when down state is reached."""
    __tracebackhide__ = True
    vuu = instance["v_uu"]
    vud = instance["v_ud"]
    vdu = instance["v_du"]
    vdd = instance["v_dd"]
    rf = instance["risk_free_rate"]

    res = solve_three_period_cycle(vuu, vud, vdu, vdd, rf)
    required = {"p0", "l0", "m0", "leverage0", "p_u", "p_d", "crash_drop", "crash_drop_pct"}
    for k in required:
        assert k in res, f"solve_three_period_cycle missing '{k}'"

    # p_u must exceed p_d
    assert res["p_u"] > res["p_d"], f"Good state price p_u ({res['p_u']}) must exceed p_d ({res['p_d']})"
    # p0 must exceed p_d
    assert res["p0"] > res["p_d"], f"t=0 price p0 ({res['p0']}) must exceed down-state price p_d ({res['p_d']})"
    assert res["crash_drop"] > 0.0, "crash_drop must be positive"
    assert res["crash_drop_pct"] > 0.0, "crash_drop_pct must be positive"


def test_exception_contracts() -> None:
    """Check that functions raise ValueError on invalid or unphysical inputs."""
    __tracebackhide__ = True

    # v_u <= v_d
    with pytest.raises(ValueError):
        solve_geanakoplos_equilibrium(v_u=1.0, v_d=1.5)
    with pytest.raises(ValueError):
        solve_geanakoplos_equilibrium(v_u=1.0, v_d=1.0)

    # v_d <= 0
    with pytest.raises(ValueError):
        solve_geanakoplos_equilibrium(v_u=1.0, v_d=-0.2)

    # risk_free_rate < 1.0
    with pytest.raises(ValueError):
        solve_geanakoplos_equilibrium(v_u=1.5, v_d=0.5, risk_free_rate=0.95)

    # max_loan_ratio out of (0, 1]
    with pytest.raises(ValueError):
        solve_geanakoplos_equilibrium(v_u=1.5, v_d=0.5, max_loan_ratio=0.0)
    with pytest.raises(ValueError):
        solve_geanakoplos_equilibrium(v_u=1.5, v_d=0.5, max_loan_ratio=1.2)

    # shocked_loan_ratio > initial_loan_ratio in simulate_margin_shock
    with pytest.raises(ValueError):
        simulate_margin_shock(v_u=1.5, v_d=0.5, initial_loan_ratio=0.5, shocked_loan_ratio=0.8)

    # invalid payoffs in three period cycle
    with pytest.raises(ValueError):
        solve_three_period_cycle(v_uu=1.0, v_ud=1.2, v_du=0.8, v_dd=0.2)

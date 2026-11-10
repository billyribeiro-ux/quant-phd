"""Autograder test suite for PR6: Dynamic & Long-Horizon Allocation.

Tests mathematical invariants, Merton financial allocations, human capital discounting,
CRRA certainty equivalents, and comparative target-date fund glide path evaluations.
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest
from instance import make_instance
from integrity import validate_lifecycle_params

try:
    import lifecycle
except ImportError:
    import reference as lifecycle


@pytest.fixture
def current_instance() -> dict[str, Any]:
    """Load deterministic parameter instance for current QF_SEED."""
    seed = int(os.environ.get("QF_SEED", "0"))
    return make_instance(seed)


def test_instance_validity(current_instance: dict[str, Any]) -> None:
    """Verify that the instance generator produces structurally valid inputs."""
    validated = validate_lifecycle_params(dict(current_instance))
    assert int(validated["initial_age"]) < int(validated["retire_age"])
    assert float(validated["gamma"]) > 0.0
    assert -1.0 <= float(validated["rho"]) <= 1.0


def test_human_capital_discounting() -> None:
    """Verify backward present value discounting of wage streams."""
    wages = np.array([50000.0, 50000.0, 50000.0, 50000.0])
    r_disc = 0.05
    hc = lifecycle.compute_human_capital(wages, r_discount=r_disc)

    assert len(hc) == 4
    # Terminal year human capital must equal final year wage exactly
    assert abs(hc[-1] - 50000.0) < 1e-6
    # Strictly monotonically decreasing with age for constant wages
    for i in range(len(hc) - 1):
        assert hc[i] > hc[i + 1]

    # Explicit present value formula for 4 years of 50k at 5%
    expected_hc0 = 50000.0 * (1.0 + 1.0 / 1.05 + 1.0 / (1.05**2) + 1.0 / (1.05**3))
    assert abs(hc[0] - expected_hc0) < 1e-4

    # Higher discount rate must strictly reduce human capital
    hc_high_disc = lifecycle.compute_human_capital(wages, r_discount=0.10)
    assert hc_high_disc[0] < hc[0]


def test_certainty_equivalent_properties() -> None:
    """Verify that CRRA certainty equivalent wealth satisfies theoretical axioms."""
    # Axiom 1: Certainty equivalent of a degenerate (constant) distribution is the constant itself
    const_wealth = np.full(100, 150000.0)
    ce_const = lifecycle.compute_certainty_equivalent(const_wealth, gamma=3.0)
    assert abs(ce_const - 150000.0) < 1e-6

    # Axiom 2: Risk aversion implies CE < E[W] for non-degenerate risky wealth
    risky_wealth = np.array([50000.0, 150000.0, 250000.0])
    mean_w = float(np.mean(risky_wealth))
    ce_risky = lifecycle.compute_certainty_equivalent(risky_wealth, gamma=2.0)
    assert ce_risky < mean_w

    # Axiom 3: Higher risk aversion strictly decreases certainty equivalent
    ce_more_averse = lifecycle.compute_certainty_equivalent(risky_wealth, gamma=5.0)
    assert ce_more_averse < ce_risky

    # Axiom 4: Exponent correctness (guards against (1-gamma)*U^(1/gamma) mutant)
    u_gamma = float(np.mean((risky_wealth ** (1.0 - 2.0)) / (1.0 - 2.0)))
    exact_ce = ((1.0 - 2.0) * u_gamma) ** (1.0 / (1.0 - 2.0))
    assert abs(ce_risky - exact_ce) < 1e-8


def test_optimal_policy_human_capital_and_aging(current_instance: dict[str, Any]) -> None:
    """Verify that optimal equity allocation declines with age and accounts for human capital."""
    inst = dict(current_instance)
    total_years = int(inst["retire_age"]) - int(inst["initial_age"])

    # Young worker: high human capital ratio
    alpha_young = lifecycle.compute_optimal_policy(
        t=0,
        total_years=total_years,
        wealth=25000.0,
        x_state=0.0,
        hc_val=1500000.0,
        params=inst,
    )
    # Near retirement worker: low human capital ratio
    alpha_old = lifecycle.compute_optimal_policy(
        t=total_years - 1,
        total_years=total_years,
        wealth=1000000.0,
        x_state=0.0,
        hc_val=50000.0,
        params=inst,
    )

    # When wages are safe, young workers have higher equity demand than older workers
    assert alpha_young >= alpha_old
    assert 0.0 <= alpha_young <= 1.0
    assert 0.0 <= alpha_old <= 1.0

    # At exact retirement (t=total_years, hc_val=0, tau=0), policy must match pure myopic Merton fraction
    gamma = float(inst["gamma"])
    eq_vol = float(inst["equity_vol"])
    eq_prem = float(inst["equity_premium"])
    merton_unconstrained = eq_prem / (gamma * eq_vol**2)
    expected_retire_alloc = min(1.0, max(0.0, merton_unconstrained))

    alpha_retire = lifecycle.compute_optimal_policy(
        t=total_years,
        total_years=total_years,
        wealth=1000000.0,
        x_state=0.0,
        hc_val=0.0,
        params=inst,
    )
    assert abs(alpha_retire - expected_retire_alloc) < 1e-6


def test_wage_beta_hedging_sensitivity(current_instance: dict[str, Any]) -> None:
    """Verify that cyclical labour income (wage_beta > 0) strictly reduces financial equity demand."""
    inst_safe = dict(current_instance)
    inst_safe["wage_beta"] = 0.0

    inst_cyclical = dict(current_instance)
    inst_cyclical["wage_beta"] = 0.80

    total_years = int(inst_safe["retire_age"]) - int(inst_safe["initial_age"])
    wealth = 500000.0
    hc_val = 1000000.0

    alpha_safe = lifecycle.compute_optimal_policy(
        t=10,
        total_years=total_years,
        wealth=wealth,
        x_state=0.0,
        hc_val=hc_val,
        params=inst_safe,
    )
    alpha_cyclical = lifecycle.compute_optimal_policy(
        t=10,
        total_years=total_years,
        wealth=wealth,
        x_state=0.0,
        hc_val=hc_val,
        params=inst_cyclical,
    )

    # Cyclical income acts as an implicit equity position; financial equity must be lower
    assert alpha_safe >= alpha_cyclical


def test_predictability_hedging_direction(current_instance: dict[str, Any]) -> None:
    """Verify that negative correlation between return and expected return shocks creates positive hedging demand."""
    inst_hedged = dict(current_instance)
    inst_hedged["rho"] = -0.75
    inst_hedged["gamma"] = 4.0

    inst_unhedged = dict(current_instance)
    inst_unhedged["rho"] = 0.0
    inst_unhedged["gamma"] = 4.0

    total_years = int(inst_hedged["retire_age"]) - int(inst_hedged["initial_age"])
    wealth = 1000000.0
    hc_val = 0.0  # Isolate predictability effect without human capital leverage

    alpha_hedged = lifecycle.compute_optimal_policy(
        t=0,
        total_years=total_years,
        wealth=wealth,
        x_state=0.0,
        hc_val=hc_val,
        params=inst_hedged,
    )
    alpha_unhedged = lifecycle.compute_optimal_policy(
        t=0,
        total_years=total_years,
        wealth=wealth,
        x_state=0.0,
        hc_val=hc_val,
        params=inst_unhedged,
    )

    # Long-horizon negative correlation (rho < 0) provides positive hedging demand for gamma > 1
    assert alpha_hedged >= alpha_unhedged


def test_simulation_runs_and_satisfies_invariants(current_instance: dict[str, Any]) -> None:
    """Verify that full lifecycle Monte Carlo simulation produces coherent wealth and risk metrics."""
    res = lifecycle.simulate_lifecycle(dict(current_instance), policy="dynamic", n_paths=2000, seed=123)

    mean_w = res["mean_terminal_wealth"]
    med_w = res["median_terminal_wealth"]
    p5_w = res["p5_terminal_wealth"]
    ce_w = res["certainty_equivalent"]
    drawdown_p95 = res["max_late_drawdown_p95"]
    weights = res["equity_weights"]

    assert p5_w < med_w <= mean_w
    assert 0.0 < ce_w <= mean_w
    assert 0.0 <= drawdown_p95 <= 1.0

    # Equity weights must be in [0, 1] and generally downward sloping over career
    assert np.all(weights >= 0.0)
    assert np.all(weights <= 1.0)
    assert weights[0] >= weights[-1]


def test_tdf_glide_path_shapes(current_instance: dict[str, Any]) -> None:
    """Verify that target-date fund deterministic glide paths conform to stated specifications."""
    inst = dict(current_instance)
    years = int(inst["retire_age"]) - int(inst["initial_age"])

    res_to = lifecycle.simulate_lifecycle(inst, policy="to_retirement", n_paths=500, seed=42)
    res_through = lifecycle.simulate_lifecycle(inst, policy="through_retirement", n_paths=500, seed=42)
    res_static = lifecycle.simulate_lifecycle(inst, policy="static_60_40", n_paths=500, seed=42)

    w_to = res_to["equity_weights"]
    w_through = res_through["equity_weights"]
    w_static = res_static["equity_weights"]

    assert len(w_to) == years
    assert abs(w_static[0] - 0.60) < 1e-6
    assert abs(w_static[-1] - 0.60) < 1e-6

    # "To" glide path descends to 30% near retirement
    assert abs(w_to[-1] - 0.30) < 0.05
    # "Through" glide path descends to 50% at retirement
    assert abs(w_through[-1] - 0.50) < 0.05
    # "To" glide path has lower late sequence-of-returns drawdown risk than "Through"
    assert res_to["max_late_drawdown_p95"] <= res_through["max_late_drawdown_p95"] + 0.05


def test_invalid_parameters_raise_error(current_instance: dict[str, Any]) -> None:
    """Verify input validation catches boundary violations."""
    bad_inst = dict(current_instance)
    bad_inst["gamma"] = -1.0
    with pytest.raises(ValueError):
        lifecycle.simulate_lifecycle(bad_inst)

    bad_ages = dict(current_instance)
    bad_ages["initial_age"] = 65
    bad_ages["retire_age"] = 25
    with pytest.raises(ValueError):
        lifecycle.simulate_lifecycle(bad_ages)

    bad_rho = dict(current_instance)
    bad_rho["rho"] = 1.5
    with pytest.raises(ValueError):
        lifecycle.simulate_lifecycle(bad_rho)

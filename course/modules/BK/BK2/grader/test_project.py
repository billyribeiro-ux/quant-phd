"""Autograder test suite for BK2: Berk-Green Fund Economics Model.

Tests:
1. Precision additivity and Bayesian belief updating invariants.
2. Capacity AUM monotonicity, non-negativity bound, and boundary conditions.
3. Gross and net alpha articulation and zero-net-alpha equilibrium identity.
4. Scale-invariant signal extraction from noisy portfolio returns.
5. Multi-period lifecycle flow articulation: Flow_t = q^*_{t+1} - A_t^end.
6. Cumulative manager fee and investor profit rent extraction decomposition.
7. Numerical determinism and consistency across all 50 seeds.
"""

from __future__ import annotations

import math
import os
from typing import Any, cast

import pytest
from fund_model import (
    FundParameters,
    capacity_aum,
    extract_signal,
    gross_alpha,
    manager_rent_share,
    net_alpha,
    simulate_fund_lifecycle,
    update_belief,
)
from instance import make_instance


def get_seed() -> int:
    return int(os.environ.get("QF_SEED", "0"))


def get_current_instance() -> dict[str, Any]:
    seed = get_seed()
    return cast(dict[str, Any], make_instance(seed))


def test_instance_validity() -> None:
    inst = get_current_instance()
    assert isinstance(inst["prior_mean"], float)
    assert isinstance(inst["prior_variance"], float)
    assert isinstance(inst["noise_variance"], float)
    assert isinstance(inst["fee_rate"], float)
    assert isinstance(inst["cost_parameter"], float)
    assert isinstance(inst["initial_aum"], float)
    assert isinstance(inst["true_skill"], float)
    assert isinstance(inst["num_periods"], int)
    assert isinstance(inst["noise_shocks"], list)
    assert len(inst["noise_shocks"]) == inst["num_periods"]


def test_update_belief_precision_and_bounds() -> None:
    inst = get_current_instance()
    p_mean = float(inst["prior_mean"])
    p_var = float(inst["prior_variance"])
    n_var = float(inst["noise_variance"])

    # Test on instance test signals
    signals = inst["test_signals"]
    assert isinstance(signals, list)

    for sig in signals:
        sig_f = float(sig)
        post_mean, post_var = update_belief(p_mean, p_var, sig_f, n_var)

        # Invariant 1: precision additivity
        tau_prior = 1.0 / p_var
        tau_noise = 1.0 / n_var
        expected_tau_post = tau_prior + tau_noise
        actual_tau_post = 1.0 / post_var
        assert math.isclose(actual_tau_post, expected_tau_post, rel_tol=1e-6)

        # Invariant 2: posterior variance strictly smaller than prior and noise variance
        assert 0.0 < post_var < p_var
        assert post_var < n_var

        # Invariant 3: posterior mean lies strictly between prior mean and signal (or equal if sig == prior)
        if sig_f > p_mean:
            assert p_mean < post_mean < sig_f
        elif sig_f < p_mean:
            assert sig_f < post_mean < p_mean
        else:
            assert math.isclose(post_mean, p_mean, rel_tol=1e-9)

    # Test error handling
    with pytest.raises(ValueError):
        update_belief(0.02, 0.0, 0.05, 0.01)
    with pytest.raises(ValueError):
        update_belief(0.02, -0.001, 0.05, 0.01)
    with pytest.raises(ValueError):
        update_belief(0.02, 0.001, 0.05, 0.0)


def test_capacity_aum_mechanics() -> None:
    inst = get_current_instance()
    fee = float(inst["fee_rate"])
    cost = float(inst["cost_parameter"])

    # Case 1: expected skill <= fee => capacity is zero
    assert capacity_aum(fee, fee, cost) == 0.0
    assert capacity_aum(fee - 0.005, fee, cost) == 0.0
    assert capacity_aum(-0.01, fee, cost) == 0.0

    # Case 2: expected skill > fee => capacity is exactly (skill - fee) / cost
    skill = fee + 0.02
    expected_cap = 0.02 / cost
    actual_cap = capacity_aum(skill, fee, cost)
    assert math.isclose(actual_cap, expected_cap, rel_tol=1e-7)

    # Monotonicity checks
    # d(cap)/d(skill) > 0
    assert capacity_aum(skill + 0.01, fee, cost) > actual_cap
    # d(cap)/d(fee) < 0
    assert capacity_aum(skill, fee + 0.005, cost) < actual_cap
    # d(cap)/d(cost) < 0
    assert capacity_aum(skill, fee, cost * 1.5) < actual_cap

    # Error handling
    with pytest.raises(ValueError):
        capacity_aum(0.05, fee, 0.0)
    with pytest.raises(ValueError):
        capacity_aum(0.05, fee, -1e-5)
    with pytest.raises(ValueError):
        capacity_aum(0.05, -0.01, cost)


def test_gross_and_net_alpha() -> None:
    inst = get_current_instance()
    skill = float(inst["true_skill"])
    cost = float(inst["cost_parameter"])
    fee = float(inst["fee_rate"])

    aum = 50.0
    g_alpha = gross_alpha(skill, aum, cost)
    n_alpha = net_alpha(skill, aum, cost, fee)

    # Articulation: net_alpha = gross_alpha - fee
    assert math.isclose(n_alpha, g_alpha - fee, rel_tol=1e-9)

    # Monotonicity: larger AUM reduces alpha
    assert gross_alpha(skill, aum + 10.0, cost) < g_alpha
    assert net_alpha(skill, aum + 10.0, cost, fee) < n_alpha

    # Zero-net-alpha equilibrium condition:
    # At capacity AUM q* = (skill - fee) / cost, net alpha must be exactly 0.0!
    if skill > fee:
        cap = capacity_aum(skill, fee, cost)
        eq_net_alpha = net_alpha(skill, cap, cost, fee)
        assert math.isclose(eq_net_alpha, 0.0, abs_tol=1e-12)


def test_signal_extraction_scale_invariance() -> None:
    inst = get_current_instance()
    skill = float(inst["true_skill"])
    cost = float(inst["cost_parameter"])
    shock = 0.025

    # Check across various fund sizes: extracted signal must equal skill + shock
    for aum in [10.0, 50.0, 200.0]:
        r_gross = gross_alpha(skill, aum, cost) + shock
        extracted = extract_signal(r_gross, aum, cost)
        assert math.isclose(extracted, skill + shock, rel_tol=1e-8)


def test_lifecycle_simulation_identities() -> None:
    inst = get_current_instance()
    p_mean = float(inst["prior_mean"])
    p_var = float(inst["prior_variance"])
    n_var = float(inst["noise_variance"])
    fee = float(inst["fee_rate"])
    cost = float(inst["cost_parameter"])
    init_aum = float(inst["initial_aum"])
    true_skill = float(inst["true_skill"])
    raw_num_p = inst["num_periods"]
    assert isinstance(raw_num_p, int)
    num_p: int = raw_num_p
    raw_shocks = inst["noise_shocks"]
    assert isinstance(raw_shocks, list)
    shocks: list[float] = [float(x) for x in raw_shocks]

    params = FundParameters(
        prior_mean=p_mean,
        prior_variance=p_var,
        noise_variance=n_var,
        fee_rate=fee,
        cost_parameter=cost,
        initial_aum=init_aum,
    )

    res = simulate_fund_lifecycle(params, true_skill, shocks)

    # Check series lengths
    for key in [
        "aum",
        "gross_returns",
        "net_returns",
        "signals",
        "posterior_means",
        "posterior_variances",
        "target_capacities",
        "net_flows",
        "manager_fees",
        "investor_profits",
    ]:
        series = res[key]
        assert isinstance(series, list)
        assert len(series) == num_p, f"Length mismatch for key {key}"

    # Flow accounting and asset dynamics check
    for t in range(num_p):
        aum_t = float(res["aum"][t])
        net_ret_t = float(res["net_returns"][t])
        gross_ret_t = float(res["gross_returns"][t])
        flow_t = float(res["net_flows"][t])
        target_cap_t = float(res["target_capacities"][t])
        fees_t = float(res["manager_fees"][t])
        inv_prof_t = float(res["investor_profits"][t])

        if aum_t > 0.0:
            assert math.isclose(net_ret_t, gross_ret_t - fee, rel_tol=1e-8)
            assert math.isclose(fees_t, fee * aum_t, rel_tol=1e-8)
            assert math.isclose(inv_prof_t, aum_t * net_ret_t, rel_tol=1e-8)

            assets_end_t = max(0.0, aum_t * (1.0 + net_ret_t))
            assert math.isclose(flow_t, target_cap_t - assets_end_t, rel_tol=1e-8)

        if t < num_p - 1:
            assert math.isclose(float(res["aum"][t + 1]), target_cap_t, rel_tol=1e-8)

    # Cumulative totals check
    cum_fees = float(res["cumulative_fees"])
    cum_inv_profit = float(res["cumulative_investor_profit"])
    assert math.isclose(sum(res["manager_fees"]), cum_fees, rel_tol=1e-8)
    assert math.isclose(sum(res["investor_profits"]), cum_inv_profit, rel_tol=1e-8)

    # Rent share range check
    rent_share = float(res["rent_share"])
    assert 0.0 <= rent_share <= 1.0


def test_manager_rent_share_behavior() -> None:
    # 1. Zero fees
    assert manager_rent_share(0.0, 100.0) == 0.0
    # 2. Negative investor profit with positive fees => 100% rent capture
    assert manager_rent_share(50.0, -10.0) == 1.0
    assert manager_rent_share(50.0, 0.0) == 1.0
    # 3. Standard split
    assert math.isclose(manager_rent_share(50.0, 50.0), 0.5, rel_tol=1e-9)
    assert math.isclose(manager_rent_share(80.0, 20.0), 0.8, rel_tol=1e-9)


def test_berk_green_rational_equilibrium_convergence() -> None:
    """Under deterministic zero shocks and true skill known, AUM reaches capacity and net alpha is zero."""
    skill = 0.035
    fee = 0.015
    cost = 2.0e-5
    params = FundParameters(
        prior_mean=skill,
        prior_variance=1e-6,  # Very tight prior around skill
        noise_variance=0.01,
        fee_rate=fee,
        cost_parameter=cost,
        initial_aum=50.0,
    )
    shocks = [0.0] * 5
    res = simulate_fund_lifecycle(params, skill, shocks)

    # Capacity should be (0.035 - 0.015) / 2e-5 = 0.020 / 2e-5 = 1000.0 million
    target_cap = (skill - fee) / cost
    assert math.isclose(target_cap, 1000.0, rel_tol=1e-5)

    # In period 1 onward, AUM is target capacity and net return is zero
    for t in range(1, 5):
        assert math.isclose(float(res["aum"][t]), target_cap, rel_tol=1e-3)
        assert math.isclose(float(res["net_returns"][t]), 0.0, abs_tol=1e-5)
        # Manager fees per period: 1000.0 * 0.015 = 15.0 million
        assert math.isclose(float(res["manager_fees"][t]), target_cap * fee, rel_tol=1e-3)

"""Test suite for PR5 Pod Allocation Simulator.

Validates analytical formulas, cushion policies, and platform simulation properties.
"""

from __future__ import annotations

import math
import os
from typing import Any

import numpy as np
import pytest

# Load instance generator and student solution
from instance import make_instance
from simulator import (
    compute_allocation_weights,
    compute_pod_drawdowns,
    expected_mdd_brownian,
    grossman_zhou_cushion_allocation,
    simulate_platform,
)


@pytest.fixture
def seed() -> int:
    """Read test instance seed from environment, default to 0."""
    return int(os.environ.get("QF_SEED", "0"))


@pytest.fixture
def instance(seed: int) -> dict[str, Any]:
    """Generate instance for current seed."""
    return make_instance(seed)


def test_expected_mdd_zero_drift() -> None:
    """Verify zero-drift Magdon-Ismail expected MDD matches sigma * sqrt(pi * t / 2)."""
    sigma = 0.20
    t = 1.0
    val = expected_mdd_brownian(mu=0.0, sigma=sigma, t=t)
    expected = sigma * math.sqrt(math.pi * t / 2.0)
    assert math.isclose(val, expected, rel_tol=1e-5), (
        f"Zero-drift Brownian MDD must equal sigma*sqrt(pi*t/2) = {expected:.6f}, got {val:.6f}"
    )

    # Edge cases
    assert expected_mdd_brownian(mu=0.0, sigma=0.0, t=1.0) == 0.0
    assert expected_mdd_brownian(mu=0.0, sigma=0.2, t=0.0) == 0.0


def test_expected_mdd_drift_regimes() -> None:
    """Verify that positive drift dampens MDD while negative drift amplifies MDD."""
    sigma = 0.20
    t = 1.0
    mdd_zero = expected_mdd_brownian(mu=0.0, sigma=sigma, t=t)
    mdd_pos = expected_mdd_brownian(mu=0.10, sigma=sigma, t=t)
    mdd_neg = expected_mdd_brownian(mu=-0.10, sigma=sigma, t=t)

    assert mdd_pos < mdd_zero, f"Positive drift must reduce expected MDD ({mdd_pos:.4f} vs zero-drift {mdd_zero:.4f})"
    assert mdd_neg > mdd_zero, f"Negative drift must increase expected MDD ({mdd_neg:.4f} vs zero-drift {mdd_zero:.4f})"


def test_grossman_zhou_cushion_properties() -> None:
    """Verify Grossman-Zhou floor protection: allocation is zero at or below floor, linear above."""
    peak = 100.0
    alpha = 0.85
    m_star = 2.5
    floor = alpha * peak  # 85.0

    # At or below floor: allocation must be zero
    assert grossman_zhou_cushion_allocation(wealth=85.0, peak=peak, alpha=alpha, m_multiplier=m_star) == 0.0
    assert grossman_zhou_cushion_allocation(wealth=80.0, peak=peak, alpha=alpha, m_multiplier=m_star) == 0.0

    # Above floor: linear in cushion
    w1 = 90.0
    alloc1 = grossman_zhou_cushion_allocation(wealth=w1, peak=peak, alpha=alpha, m_multiplier=m_star)
    expected1 = m_star * (w1 - floor)  # 2.5 * 5.0 = 12.5
    assert math.isclose(alloc1, expected1, rel_tol=1e-6)

    w2 = 95.0
    alloc2 = grossman_zhou_cushion_allocation(wealth=w2, peak=peak, alpha=alpha, m_multiplier=m_star)
    expected2 = m_star * (w2 - floor)  # 2.5 * 10.0 = 25.0
    assert math.isclose(alloc2, expected2, rel_tol=1e-6)
    assert math.isclose(alloc2 - alloc1, m_star * (w2 - w1), rel_tol=1e-6)


def test_compute_pod_drawdowns_fixture() -> None:
    """Verify pod drawdown computation on known wealth trajectories."""
    # 2 pods, 4 time steps (5 points)
    # Pod 0: 100 -> 120 -> 90 -> 110 -> 80
    # (Peak: 100, 120, 120, 120, 120; DD: 0, 0, 30/120=0.25, 10/120=0.0833, 40/120=0.3333)
    # Pod 1: 100 -> 90 -> 80 -> 70 -> 60 (Peak: 100 everywhere; DD: 0, 0.10, 0.20, 0.30, 0.40)
    w_paths = np.array(
        [
            [100.0, 120.0, 90.0, 110.0, 80.0],
            [100.0, 90.0, 80.0, 70.0, 60.0],
        ]
    )
    peaks, dds, mdds = compute_pod_drawdowns(w_paths)

    assert peaks.shape == (2, 5)
    assert dds.shape == (2, 5)
    assert mdds.shape == (2,)

    # Pod 0 checks
    assert math.isclose(dds[0, 2], 30.0 / 120.0, rel_tol=1e-6)
    assert math.isclose(dds[0, 4], 40.0 / 120.0, rel_tol=1e-6)
    assert math.isclose(mdds[0], 40.0 / 120.0, rel_tol=1e-6)

    # Pod 1 checks
    assert math.isclose(mdds[1], 0.40, rel_tol=1e-6)


def test_allocation_weights_normalization(instance: dict[str, Any]) -> None:
    """Verify allocation weights sum to 1.0 across active pods and 0 for inactive pods."""
    n_pods = instance["n_pods"]
    active = np.ones(n_pods, dtype=bool)
    active[0] = False  # Pod 0 inactive
    active[3] = False  # Pod 3 inactive

    dds = np.full(n_pods, 0.03)
    hard_stops = np.full(n_pods, 0.08)
    sigmas = np.array(instance["sigmas"])

    for pol in ["equal", "risk_parity", "cushion"]:
        w = compute_allocation_weights(pol, active, dds, hard_stops, sigmas)
        assert len(w) == n_pods
        assert math.isclose(float(np.sum(w)), 1.0, abs_tol=1e-6), f"Weights under {pol} must sum to 1.0"
        assert w[0] == 0.0 and w[3] == 0.0, f"Inactive pods under {pol} must have weight 0"
        assert np.all(w >= 0.0), f"Weights under {pol} must be non-negative"


def test_risk_parity_inverse_volatility_scaling() -> None:
    """Verify risk parity scales weights inversely with volatility."""
    active = np.array([True, True])
    dds = np.array([0.0, 0.0])
    hard_stops = np.array([0.10, 0.10])
    sigmas = np.array([0.10, 0.20])  # Pod 0 has half the vol of Pod 1

    w = compute_allocation_weights("risk_parity", active, dds, hard_stops, sigmas)
    assert w[0] > w[1], "Lower volatility pod must receive higher risk parity weight"
    assert math.isclose(w[0] / w[1], 2.0, rel_tol=1e-5), (
        f"Risk parity weight ratio must be 2.0 (inverse vol), got {w[0] / w[1]:.4f}"
    )


def test_cushion_allocation_monotonicity() -> None:
    """Verify cushion policy allocates less capital to pods closer to their stop-loss."""
    active = np.array([True, True])
    hard_stops = np.array([0.10, 0.10])
    sigmas = np.array([0.15, 0.15])  # equal volatility

    # Pod 0 at 2% drawdown (cushion = 8%), Pod 1 at 8% drawdown (cushion = 2%)
    dds = np.array([0.02, 0.08])
    w = compute_allocation_weights("cushion", active, dds, hard_stops, sigmas)

    assert w[0] > w[1], f"Pod with larger cushion must receive higher weight (Pod 0: {w[0]:.4f} vs Pod 1: {w[1]:.4f})"
    # Ratio of weights should be (0.10 - 0.02) / (0.10 - 0.08) = 0.08 / 0.02 = 4.0
    assert math.isclose(w[0] / w[1], 4.0, rel_tol=1e-4)


def test_stop_loss_halts_terminated_pods(instance: dict[str, Any]) -> None:
    """Verify that pods hitting hard stop are halted and overall survival is tracked."""
    res = simulate_platform(instance, policy="cushion")

    assert "skilled_churn_rate" in res
    assert "unskilled_stopped_rate" in res
    assert "overall_survival_rate" in res
    assert 0.0 <= res["skilled_churn_rate"] <= 1.0
    assert 0.0 <= res["unskilled_stopped_rate"] <= 1.0
    assert 0.0 <= res["overall_survival_rate"] <= 1.0

    # Deterministic test: pod with guaranteed catastrophic loss must be halted
    test_inst = {
        "seed": 123,
        "n_pods": 2,
        "mus": [-0.50, 0.15],
        "sigmas": [0.02, 0.02],
        "skills": [0, 1],
        "soft_stops": [0.04, 0.10],
        "hard_stops": [0.08, 0.20],
        "corr_rho": 0.0,
        "n_days": 252,
        "t_years": 1.0,
    }
    test_res = simulate_platform(test_inst, policy="equal")
    assert test_res["unskilled_stopped_rate"] == 1.0, (
        f"Doomed pod must be halted by hard stop-loss: got unskilled_stopped_rate={test_res['unskilled_stopped_rate']}"
    )
    assert test_res["overall_survival_rate"] < 1.0, (
        "Simulator failed to halt terminated pod: overall_survival_rate must be < 1.0"
    )


def test_platform_simulation_metrics(instance: dict[str, Any]) -> None:
    """Verify platform simulation metrics articulation and invariants."""
    res = simulate_platform(instance, policy="cushion")

    # Wealth path check
    w_path = res["platform_wealth_path"]
    dd_path = res["platform_drawdown_path"]
    assert len(w_path) == instance["n_days"] + 1
    assert len(dd_path) == instance["n_days"] + 1
    assert w_path[0] == 1.0
    assert dd_path[0] == 0.0
    assert np.all(dd_path >= 0.0)

    # Return and Vol
    ret = res["platform_annualized_return"]
    vol = res["platform_annualized_volatility"]
    sr = res["platform_sharpe"]
    mdd = res["platform_mdd"]
    calmar = res["calmar_ratio"]

    assert vol >= 0.0
    assert 0.0 <= mdd <= 1.0
    if vol > 1e-4:
        assert math.isclose(sr, ret / vol, rel_tol=1e-5)
    if mdd > 1e-4:
        assert math.isclose(calmar, ret / mdd, rel_tol=1e-5)


def test_skilled_vs_unskilled_survival(instance: dict[str, Any]) -> None:
    """Verify that stop-loss rules track churn rates and satisfy boundary conditions."""
    res = simulate_platform(instance, policy="cushion")

    # Invariant: overall survival rate + stopped rate must articulate
    instance["n_pods"]
    surviving = res["overall_survival_rate"]
    assert 0.0 <= surviving <= 1.0, f"Survival rate must be in [0, 1], got {surviving}"

    # Verify on a high-drift vs strongly negative drift synthetic scenario
    test_inst = {
        "seed": 42,
        "n_pods": 2,
        "mus": [0.25, -0.25],
        "sigmas": [0.12, 0.12],
        "skills": [1, 0],
        "soft_stops": [0.05, 0.05],
        "hard_stops": [0.10, 0.10],
        "corr_rho": 0.0,
        "n_days": 252,
        "t_years": 1.0,
    }
    test_res = simulate_platform(test_inst, policy="equal")
    assert test_res["unskilled_stopped_rate"] >= test_res["skilled_churn_rate"], (
        f"Toxic pod must be stopped at >= rate of skilled pod: "
        f"got toxic={test_res['unskilled_stopped_rate']} vs skilled={test_res['skilled_churn_rate']}"
    )

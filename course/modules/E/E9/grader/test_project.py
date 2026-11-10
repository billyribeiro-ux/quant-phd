"""Acceptance test suite for E9 Sovereign DSA and Fan Chart Engine project.

Tests exact debt dynamics, primary gap formulas, deterministic trajectory simulation,
fan chart percentile monotonicity, anytime debt-ceiling breach probability,
and end-to-end dsa_summary execution on per-seed instances.
"""

from __future__ import annotations

import math
import os
from typing import Any

import pytest
from instance import make_instance
from reference import (
    breach_probability,
    compute_fan_chart,
    debt_dynamics_step,
    dsa_summary,
    primary_gap,
    simulate_trajectory,
)

pytestmark = pytest.mark.filterwarnings("error")

_SEED = int(os.environ.get("QF_SEED", "0"))
_INST: dict[str, Any] = make_instance(_SEED)


def close(a: float, b: float, tol: float = 1e-7) -> bool:
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= tol * (1.0 + abs(b))


def test_exact_debt_dynamics_step() -> None:
    """T01: debt_dynamics_step satisfies exact discrete-time identity b_t = [(1+r)/(1+g)]*b_{t-1} - s."""
    __tracebackhide__ = True

    # Invariant: when r == g and s == 0, debt ratio is strictly invariant
    b0 = 0.85
    r_eq = 0.03
    g_eq = 0.03
    s_zero = 0.0
    b_inv = debt_dynamics_step(b0, r_eq, g_eq, s_zero)
    assert close(b_inv, b0, tol=1e-9), f"When r==g and s==0, debt ratio must be constant: got {b_inv}, expected {b0}"

    # Numerical check with positive surplus
    r = 0.04
    g = 0.02
    s = 0.015
    # (1.04 / 1.02) * 0.85 - 0.015 = 1.0196078 * 0.85 - 0.015 = 0.8666667 - 0.015 = 0.8516667
    expected = ((1.0 + r) / (1.0 + g)) * b0 - s
    b_step = debt_dynamics_step(b0, r, g, s)
    assert close(b_step, expected, tol=1e-9), f"Exact step mismatch: got {b_step}, expected {expected}"

    # Sensitivity: higher primary surplus strictly reduces debt
    b_higher_s = debt_dynamics_step(b0, r, g, s + 0.01)
    assert b_higher_s < b_step, "A higher primary surplus must strictly lower next period debt"

    # Exact non-linear formula differs from linear approximation (r - g)*b
    approx_val = (1.0 + r - g) * b0 - s
    assert not close(b_step, approx_val, tol=1e-5), "Exact step must not match linear approximation"


def test_debt_dynamics_validation_exceptions() -> None:
    """T02: Functions raise ValueError on non-physical rates (g <= -1, r <= -1) or negative debt."""
    __tracebackhide__ = True

    with pytest.raises(ValueError):
        debt_dynamics_step(0.80, 0.03, -1.0, 0.0)
    with pytest.raises(ValueError):
        debt_dynamics_step(0.80, 0.03, -1.2, 0.0)

    with pytest.raises(ValueError):
        debt_dynamics_step(0.80, -1.0, 0.02, 0.0)
    with pytest.raises(ValueError):
        debt_dynamics_step(0.80, -1.5, 0.02, 0.0)

    with pytest.raises(ValueError):
        debt_dynamics_step(-0.10, 0.03, 0.02, 0.0)

    with pytest.raises(ValueError):
        primary_gap(0.80, 0.03, -1.0, 0.0)
    with pytest.raises(ValueError):
        primary_gap(-0.50, 0.03, 0.02, 0.0)


def test_primary_gap_math_and_sign() -> None:
    """T03: primary_gap computes s* - s = [(r - g)/(1 + g)] * b_target - s."""
    __tracebackhide__ = True

    b_target = 0.90
    r = 0.04
    g = 0.01  # r - g = +0.03 > 0
    s_actual = -0.01  # Running 1% deficit

    # s* = (0.03 / 1.01) * 0.90 = 0.0267327
    # gap = s* - s_actual = 0.0267327 - (-0.01) = 0.0367327
    s_star = ((r - g) / (1.0 + g)) * b_target
    expected_gap = s_star - s_actual

    actual_gap = primary_gap(b_target, r, g, s_actual)
    assert close(actual_gap, expected_gap, tol=1e-9), f"Primary gap mismatch: got {actual_gap}, expected {expected_gap}"

    # Sign convention check: when actual surplus equals s*, gap is zero
    zero_gap = primary_gap(b_target, r, g, s_star)
    assert abs(zero_gap) < 1e-9, f"Gap must be zero when actual balance equals stabilizing balance, got {zero_gap}"

    # When r < g and actual balance is 0, stabilizing balance is negative => gap is negative
    gap_neg = primary_gap(b_target, 0.01, 0.03, 0.0)
    assert gap_neg < 0.0, "When r < g, stabilizing balance is negative; zero balance yields negative gap"


def test_simulate_trajectory() -> None:
    """T04: simulate_trajectory propagates initial debt across horizon with strict validation."""
    __tracebackhide__ = True

    b0 = float(_INST["b0"])
    r_path = list(_INST["r_path"])
    g_path = list(_INST["g_path"])
    s_path = list(_INST["s_path"])

    traj = simulate_trajectory(b0, r_path, g_path, s_path)

    # Length must be len(r_path) + 1
    assert len(traj) == len(r_path) + 1, f"Trajectory length must be {len(r_path) + 1}, got {len(traj)}"
    assert traj[0] == b0, f"Trajectory must start at b0={b0}"

    # Check step-by-step equivalence
    b_curr = b0
    for t in range(len(r_path)):
        b_curr = debt_dynamics_step(b_curr, r_path[t], g_path[t], s_path[t])
        assert close(traj[t + 1], b_curr, tol=1e-9), f"Step {t + 1} discrepancy in simulate_trajectory"

    # Input validation: unequal lengths
    with pytest.raises(ValueError):
        simulate_trajectory(b0, r_path[:-1], g_path, s_path)
    with pytest.raises(ValueError):
        simulate_trajectory(b0, [], [], [])


def test_fan_chart_properties() -> None:
    """T05: compute_fan_chart produces monotonic percentile curves starting from identical b0."""
    __tracebackhide__ = True

    mc_paths = list(_INST["mc_paths"])
    percentiles = [0.10, 0.25, 0.50, 0.75, 0.90]

    fan = compute_fan_chart(mc_paths, percentiles)

    # All requested percentiles must be present
    for p in percentiles:
        assert p in fan, f"Percentile {p} missing from fan chart"
        assert len(fan[p]) == len(mc_paths[0]), "Percentile trajectory length must match path length"

    # Monotonicity invariant: at every time period t, P10 <= P25 <= P50 <= P75 <= P90
    for t in range(len(mc_paths[0])):
        for i in range(len(percentiles) - 1):
            p_low = percentiles[i]
            p_high = percentiles[i + 1]
            assert fan[p_low][t] <= fan[p_high][t] + 1e-9, (
                f"Percentile ordering violated at t={t}: P{int(p_low * 100)}={fan[p_low][t]} > "
                f"P{int(p_high * 100)}={fan[p_high][t]}"
            )

    # Validation: empty trajectories or invalid percentile
    with pytest.raises(ValueError):
        compute_fan_chart([], percentiles)
    with pytest.raises(ValueError):
        compute_fan_chart(mc_paths, [-0.1])
    with pytest.raises(ValueError):
        compute_fan_chart(mc_paths, [1.2])


def test_breach_probability_anytime() -> None:
    """T06: breach_probability evaluates anytime breach max_t(b_t) > ceiling, not merely terminal value."""
    __tracebackhide__ = True

    ceiling = 1.00

    # Path 1: reaches 1.05 at t=2, falls to 0.80 at t=5 (Anytime breach = True, Terminal breach = False)
    path_mid_breach = [0.85, 0.95, 1.05, 0.90, 0.85, 0.80]

    # Path 2: never exceeds 0.98 (Anytime breach = False)
    path_safe = [0.85, 0.88, 0.91, 0.94, 0.96, 0.98]

    # Path 3: ends at 1.02 (Anytime breach = True, Terminal breach = True)
    path_term_breach = [0.85, 0.87, 0.90, 0.95, 0.99, 1.02]

    # Combined paths: 2 out of 3 breach anytime!
    test_paths = [path_mid_breach, path_safe, path_term_breach]

    prob = breach_probability(test_paths, ceiling)
    assert close(prob, 2.0 / 3.0, tol=1e-7), (
        f"Breach probability must be 2/3 (0.6667) for anytime breaches, got {prob}. "
        "A mutant checking only terminal periods would incorrectly return 1/3."
    )

    # Infinite ceiling -> 0.0
    assert breach_probability(test_paths, 1e9) == 0.0
    # Zero ceiling -> 1.0
    assert breach_probability(test_paths, 0.0) == 1.0


def test_dsa_summary_instance() -> None:
    """T07: dsa_summary executes complete pipeline and returns structured risk metrics."""
    __tracebackhide__ = True

    summary = dsa_summary(_INST)

    required_keys = (
        "baseline_trajectory",
        "terminal_debt",
        "max_primary_gap",
        "fan_chart",
        "breach_probability",
        "is_sustainable",
    )
    for k in required_keys:
        assert k in summary, f"Missing key in dsa_summary output: {k}"

    assert isinstance(summary["is_sustainable"], bool)
    assert math.isfinite(float(summary["terminal_debt"]))
    assert math.isfinite(float(summary["max_primary_gap"]))
    assert 0.0 <= float(summary["breach_probability"]) <= 1.0

    # Missing key handling
    bad_inst = dict(_INST)
    del bad_inst["b0"]
    with pytest.raises(ValueError):
        dsa_summary(bad_inst)


def test_future_independence() -> None:
    """T08: Simulating up to horizon t is completely independent of data past t."""
    __tracebackhide__ = True

    b0 = float(_INST["b0"])
    r_path = list(_INST["r_path"])
    g_path = list(_INST["g_path"])
    s_path = list(_INST["s_path"])

    full_traj = simulate_trajectory(b0, r_path, g_path, s_path)

    # Mutate later entries (t >= 5)
    r_mut = list(r_path)
    g_mut = list(g_path)
    s_mut = list(s_path)
    for t in range(5, len(r_path)):
        r_mut[t] += 0.05
        g_mut[t] -= 0.03
        s_mut[t] -= 0.02

    mut_traj = simulate_trajectory(b0, r_mut, g_mut, s_mut)

    # Trajectories must match up to t=5
    for t in range(6):
        assert close(full_traj[t], mut_traj[t], tol=1e-9), f"Period {t} changed when mutating future inputs"

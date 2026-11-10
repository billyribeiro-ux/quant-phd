"""Test suite for SR1 Run Dynamics Model (Dual-mode pytest suite).

Evaluates solver.py on deterministic per-seed instances against theoretical invariants,
solvency threshold identities, calibration precision, and exception contracts.
"""

from __future__ import annotations

import os

import pytest
from instance import make_instance  # type: ignore[import-not-found]

try:
    from solver import calibrate_buffer, solve_model  # type: ignore[import-not-found]
except ImportError:
    from reference import calibrate_buffer, solve_model  # type: ignore[import-not-found]


@pytest.fixture
def instance() -> dict[str, float]:
    """Retrieve deterministic instance parameters for the active test seed."""
    seed = int(os.environ.get("QF_SEED", "0"))
    inst: dict[str, float] = make_instance(seed)
    return inst


def test_solution_keys_and_types(instance: dict[str, float]) -> None:
    """Verify solve_model returns exact required keys with finite float values."""
    __tracebackhide__ = True
    u = instance["uninsured_share"]
    k = instance["liquidation_value"]
    b = instance["liquid_buffer"]

    res = solve_model(u, k, b)
    assert isinstance(res, dict), "solve_model must return a dictionary"
    assert "run_threshold" in res, "Missing 'run_threshold' key in solve_model output"
    assert "run_fraction" in res, "Missing 'run_fraction' key in solve_model output"

    th = res["run_threshold"]
    frac = res["run_fraction"]
    assert isinstance(th, (float, int)), "run_threshold must be a numeric float"
    assert isinstance(frac, (float, int)), "run_fraction must be a numeric float"
    assert 0.0 <= float(th) <= 1.0, "run_threshold must lie within [0.0, 1.0]"
    assert 0.0 <= float(frac) <= 1.0, "run_fraction must lie within [0.0, 1.0]"


def test_equilibrium_run_threshold_identity(instance: dict[str, float]) -> None:
    """Check that solve_model matches the theoretical run threshold to tolerance 1e-9."""
    __tracebackhide__ = True
    u = instance["uninsured_share"]
    k = instance["liquidation_value"]
    b = instance["liquid_buffer"]

    res = solve_model(u, k, b)
    th = res["run_threshold"]

    # Independent oracle calculation
    oracle_raw = (u - b) / (k * (1.0 - b))
    expected_th = min(1.0, max(0.0, oracle_raw))

    assert abs(th - expected_th) < 1e-9, (
        "Reported run_threshold does not satisfy the theoretical solvency threshold condition"
    )


def test_no_run_convention() -> None:
    """Verify no-run convention: zero uninsured share or liquid buffer exceeding claims."""
    __tracebackhide__ = True
    res_zero = solve_model(0.0, 0.70, 0.20)
    assert res_zero["run_threshold"] == 0.0, "run_threshold must be 0.0 when uninsured_share is 0.0"
    assert res_zero["run_fraction"] == 0.0, "run_fraction must be 0.0 when uninsured_share is 0.0"

    res_covered = solve_model(0.20, 0.70, 0.30)
    assert res_covered["run_threshold"] == 0.0, "run_threshold must be 0.0 when liquid buffer covers uninsured deposits"
    assert res_covered["run_fraction"] == 0.0, "run_fraction must be 0.0 when liquid buffer covers uninsured deposits"


def test_calibration_accuracy(instance: dict[str, float]) -> None:
    """Verify calibrate_buffer produces a buffer matching target_threshold within 1e-8."""
    __tracebackhide__ = True
    target = instance["target_threshold"]
    u = instance["uninsured_share"]
    k = instance["liquidation_value"]

    calibrated_ell = calibrate_buffer(target, u, k)
    assert isinstance(calibrated_ell, (float, int)), "calibrate_buffer must return a float"
    assert 0.0 < float(calibrated_ell) < 1.0, "calibrated buffer must lie strictly within (0, 1)"

    check_res = solve_model(u, k, float(calibrated_ell))
    residual = abs(check_res["run_threshold"] - target)
    assert residual < 1e-8, (
        "Calibrated buffer failed residual check: solve_model(ell) differs from target by more than 1e-8"
    )


def test_monotone_dependence_on_uninsured_share() -> None:
    """Verify run_threshold is monotonically non-decreasing in uninsured deposit share."""
    __tracebackhide__ = True
    k = 0.70
    b = 0.25
    grid = [0.10, 0.25, 0.40, 0.60, 0.80, 0.95]
    thresholds = [solve_model(u_val, k, b)["run_threshold"] for u_val in grid]

    for i in range(len(thresholds) - 1):
        assert thresholds[i] <= thresholds[i + 1] + 1e-12, (
            "Run threshold must be monotonically non-decreasing in uninsured_share"
        )


def test_monotone_dependence_on_liquidation_value() -> None:
    """Verify run_threshold is monotonically non-increasing in liquidation recovery value."""
    __tracebackhide__ = True
    u = 0.80
    b = 0.25
    grid = [0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
    thresholds = [solve_model(u, k_val, b)["run_threshold"] for k_val in grid]

    for i in range(len(thresholds) - 1):
        assert thresholds[i] >= thresholds[i + 1] - 1e-12, (
            "Run threshold must be monotonically non-increasing in liquidation_value"
        )


def test_monotone_dependence_on_liquid_buffer() -> None:
    """Verify run_threshold is monotonically non-increasing in liquid reserve buffer."""
    __tracebackhide__ = True
    u = 0.80
    k = 0.70
    grid = [0.10, 0.20, 0.30, 0.40, 0.50]
    thresholds = [solve_model(u, k, b_val)["run_threshold"] for b_val in grid]

    for i in range(len(thresholds) - 1):
        assert thresholds[i] >= thresholds[i + 1] - 1e-12, (
            "Run threshold must be monotonically non-increasing in liquid_buffer"
        )


def test_uninsured_share_out_of_bounds() -> None:
    """Demand ValueError with exact message for uninsured share out of [0, 1]."""
    __tracebackhide__ = True
    expected_msg = "uninsured share must lie in [0, 1]"

    with pytest.raises(ValueError) as exc_low:
        solve_model(-0.01, 0.70, 0.20)
    assert expected_msg in str(exc_low.value)

    with pytest.raises(ValueError) as exc_high:
        solve_model(1.01, 0.70, 0.20)
    assert expected_msg in str(exc_high.value)

    with pytest.raises(ValueError) as exc_cal_low:
        calibrate_buffer(0.50, -0.01, 0.70)
    assert expected_msg in str(exc_cal_low.value)

    with pytest.raises(ValueError) as exc_cal_high:
        calibrate_buffer(0.50, 1.01, 0.70)
    assert expected_msg in str(exc_cal_high.value)


def test_liquidation_value_out_of_bounds() -> None:
    """Demand ValueError with exact message for liquidation value not in (0, 1]."""
    __tracebackhide__ = True
    expected_msg = "liquidation value must lie in (0, 1]"

    with pytest.raises(ValueError) as exc_zero:
        solve_model(0.80, 0.0, 0.20)
    assert expected_msg in str(exc_zero.value)

    with pytest.raises(ValueError) as exc_neg:
        solve_model(0.80, -0.10, 0.20)
    assert expected_msg in str(exc_neg.value)

    with pytest.raises(ValueError) as exc_high:
        solve_model(0.80, 1.01, 0.20)
    assert expected_msg in str(exc_high.value)

    with pytest.raises(ValueError) as exc_cal_zero:
        calibrate_buffer(0.50, 0.80, 0.0)
    assert expected_msg in str(exc_cal_zero.value)

    with pytest.raises(ValueError) as exc_cal_high:
        calibrate_buffer(0.50, 0.80, 1.01)
    assert expected_msg in str(exc_cal_high.value)


def test_target_threshold_unattainable() -> None:
    """Demand ValueError with exact message for target threshold outside attainable range."""
    __tracebackhide__ = True
    expected_msg = "target threshold is not attainable"

    with pytest.raises(ValueError) as exc_zero:
        calibrate_buffer(0.0, 0.80, 0.70)
    assert expected_msg in str(exc_zero.value)

    with pytest.raises(ValueError) as exc_one:
        calibrate_buffer(1.0, 0.80, 0.70)
    assert expected_msg in str(exc_one.value)

    with pytest.raises(ValueError) as exc_exceed:
        # mu = 0.50, k = 0.80 ==> max threshold = 0.50 / 0.80 = 0.625. Target 0.70 is unattainable.
        calibrate_buffer(0.70, 0.50, 0.80)
    assert expected_msg in str(exc_exceed.value)

    with pytest.raises(ValueError) as exc_no_uninsured:
        calibrate_buffer(0.20, 0.0, 0.70)
    assert expected_msg in str(exc_no_uninsured.value)

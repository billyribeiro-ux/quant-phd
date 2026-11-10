"""Acceptance test suite for the E6 New Keynesian model solver (nk_solver.py).

Runs identically in Pyodide and locally:
    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Validates mathematical properties, boundary conditions, input validation, equation residuals,
and impulse response signs and decay without leaking expected numeric values.
"""

from __future__ import annotations

import copy
import json
import os
from typing import Any

import nk_solver as sol
import numpy as np
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INSTANCE_DATA: dict[str, Any] = json.loads(make_instance(SEED)["payload"])
TOL = 1e-8


def _get_base_determinate_params() -> dict[str, Any]:
    """Return a guaranteed determinate parameter set based on the seed's instance."""
    params = copy.deepcopy(INSTANCE_DATA)
    # Ensure determinacy: phi_pi well above critical threshold
    crit = 1.0 - (1.0 - float(params["beta"])) * float(params["phi_y"]) / float(params["kappa"])
    params["phi_pi"] = max(float(params["phi_pi"]), crit + 0.5)
    return params


def _get_base_indeterminate_params() -> dict[str, Any]:
    """Return a guaranteed indeterminate parameter set based on the seed's instance."""
    params = copy.deepcopy(INSTANCE_DATA)
    crit = 1.0 - (1.0 - float(params["beta"])) * float(params["phi_y"]) / float(params["kappa"])
    params["phi_pi"] = max(0.0, crit - 0.5)
    return params


# ---------------------------------------------------------------------------
# Input Validation Tests (each parameter domain tested independently)
# ---------------------------------------------------------------------------


def test_invalid_beta_nonpositive() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    params["beta"] = 0.0
    try:
        sol.is_determinate(params)
    except ValueError:
        return
    pytest.fail("is_determinate must raise ValueError when beta <= 0.")


def test_invalid_beta_one_or_greater() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    params["beta"] = 1.0
    try:
        sol.is_determinate(params)
    except ValueError:
        return
    pytest.fail("is_determinate must raise ValueError when beta >= 1.")


def test_invalid_sigma_nonpositive() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    params["sigma"] = 0.0
    try:
        sol.is_determinate(params)
    except ValueError:
        return
    pytest.fail("is_determinate must raise ValueError when sigma <= 0.")


def test_invalid_kappa_nonpositive() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    params["kappa"] = 0.0
    try:
        sol.is_determinate(params)
    except ValueError:
        return
    pytest.fail("is_determinate must raise ValueError when kappa <= 0.")


def test_invalid_rho_upper_bound() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    params["rho"] = 1.0
    try:
        sol.is_determinate(params)
    except ValueError:
        return
    pytest.fail("is_determinate must raise ValueError when rho >= 1.")


def test_invalid_rho_lower_bound() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    params["rho"] = -1.0
    try:
        sol.is_determinate(params)
    except ValueError:
        return
    pytest.fail("is_determinate must raise ValueError when rho <= -1.")


def test_invalid_horizon_negative() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    try:
        sol.impulse_responses(params, -1)
    except ValueError:
        return
    pytest.fail("impulse_responses must raise ValueError when horizon is negative.")


def test_invalid_horizon_non_integer() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    bad_horizon: Any = 3.5
    try:
        sol.impulse_responses(params, bad_horizon)
    except ValueError:
        return
    pytest.fail("impulse_responses must raise ValueError when horizon is not an integer.")


# ---------------------------------------------------------------------------
# Permissible Boundary / Edge Case Tests
# ---------------------------------------------------------------------------


def test_valid_edge_beta() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    params["beta"] = 0.999
    res = sol.is_determinate(params)
    if not isinstance(res, bool):
        pytest.fail("is_determinate must return a boolean.")


def test_valid_edge_rho_zero() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    params["rho"] = 0.0
    b, a = sol.solve_undetermined(params, "demand")
    if not (isinstance(b, float) and isinstance(a, float)):
        pytest.fail("solve_undetermined must return a tuple of floats.")


def test_valid_edge_horizon_zero() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    irfs = sol.impulse_responses(params, 0)
    if len(irfs.get("date", [])) != 1 or len(irfs.get("x_demand", [])) != 1:
        pytest.fail("impulse_responses with horizon=0 must return exactly one date (date 0).")


# ---------------------------------------------------------------------------
# Determinacy and Taylor Principle Tests
# ---------------------------------------------------------------------------


def test_determinacy_boundary_above() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    beta = float(params["beta"])
    kappa = float(params["kappa"])
    phi_y = float(params["phi_y"])
    crit = 1.0 - (1.0 - beta) * phi_y / kappa
    params["phi_pi"] = crit + 0.05
    if not sol.is_determinate(params):
        pytest.fail("is_determinate must return True when phi_pi sits strictly above the determinacy threshold.")


def test_determinacy_boundary_below() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    beta = float(params["beta"])
    kappa = float(params["kappa"])
    phi_y = float(params["phi_y"])
    crit = 1.0 - (1.0 - beta) * phi_y / kappa
    params["phi_pi"] = max(0.0, crit - 0.05)
    if sol.is_determinate(params):
        pytest.fail("is_determinate must return False when phi_pi sits strictly below the determinacy threshold.")


def test_determinacy_boundary_strictness() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    beta = float(params["beta"])
    kappa = float(params["kappa"])
    phi_y = float(params["phi_y"])
    crit = 1.0 - (1.0 - beta) * phi_y / kappa
    params["phi_pi"] = crit
    if sol.is_determinate(params):
        pytest.fail("is_determinate must return False exactly at the boundary (strict inequality required).")


def test_indeterminate_raises_value_error() -> None:
    __tracebackhide__ = True
    params = _get_base_indeterminate_params()
    try:
        sol.solve_undetermined(params)
    except ValueError:
        return
    pytest.fail("solve_undetermined must raise ValueError when called on an indeterminate model.")


def test_instance_determinacy_classification() -> None:
    __tracebackhide__ = True
    expected_det = INSTANCE_DATA["is_determinate"]
    actual_det = sol.is_determinate(INSTANCE_DATA)
    if actual_det != expected_det:
        pytest.fail("is_determinate classification failed on the seed instance.")


# ---------------------------------------------------------------------------
# Mathematical Residuals and Equation Consistency
# ---------------------------------------------------------------------------


def test_demand_shock_equation_residuals() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    beta = float(params["beta"])
    sigma = float(params["sigma"])
    kappa = float(params["kappa"])
    phi_pi = float(params["phi_pi"])
    phi_y = float(params["phi_y"])
    rho = float(params["rho"])

    b, a = sol.solve_undetermined(params, "demand")

    # NKPC residual: pi_t - beta * E_t[pi_{t+1}] - kappa * x_t = 0
    nkpc_res = abs(a - beta * rho * a - kappa * b)
    if nkpc_res > TOL:
        pytest.fail("The NK Phillips curve residual exceeds tolerance under the demand shock.")

    # IS residual: x_t - E_t[x_{t+1}] + (1/sigma)*(i_t - E_t[pi_{t+1}] - r^n_t) = 0
    # where i_t = phi_pi * pi_t + phi_y * x_t and r^n_t = 1
    i_val = phi_pi * a + phi_y * b
    is_res = abs((b - rho * b) + (1.0 / sigma) * (i_val - rho * a - 1.0))
    if is_res > TOL:
        pytest.fail("The dynamic IS curve residual exceeds tolerance under the demand shock.")


def test_policy_shock_equation_residuals() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    beta = float(params["beta"])
    sigma = float(params["sigma"])
    kappa = float(params["kappa"])
    phi_pi = float(params["phi_pi"])
    phi_y = float(params["phi_y"])
    rho = float(params["rho"])

    b, a = sol.solve_undetermined(params, "policy")

    # NKPC residual
    nkpc_res = abs(a - beta * rho * a - kappa * b)
    if nkpc_res > TOL:
        pytest.fail("The NK Phillips curve residual exceeds tolerance under the policy shock.")

    # IS residual: with policy shock, r^n_t = 0, i_t = phi_pi * a + phi_y * b + 1.0
    i_val = phi_pi * a + phi_y * b + 1.0
    is_res = abs((b - rho * b) + (1.0 / sigma) * (i_val - rho * a))
    if is_res > TOL:
        pytest.fail("The dynamic IS curve residual exceeds tolerance under the policy shock.")


def test_matrix_solve_agreement() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    beta = float(params["beta"])
    sigma = float(params["sigma"])
    kappa = float(params["kappa"])
    phi_pi = float(params["phi_pi"])
    phi_y = float(params["phi_y"])
    rho = float(params["rho"])

    b, a = sol.solve_undetermined(params, "demand")

    # Independent matrix solve: M * [a, b]^T = [0, 1]^T
    mat = np.array(
        [
            [1.0 - beta * rho, -kappa],
            [phi_pi - rho, sigma * (1.0 - rho) + phi_y],
        ],
        dtype=np.float64,
    )
    rhs = np.array([0.0, 1.0], dtype=np.float64)
    expected_a, expected_b = np.linalg.solve(mat, rhs)

    if abs(a - expected_a) > TOL or abs(b - expected_b) > TOL:
        pytest.fail("solve_undetermined disagrees with direct linear matrix solve.")


# ---------------------------------------------------------------------------
# Impulse Response Properties
# ---------------------------------------------------------------------------


def test_irf_keys_and_length() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    h = 10
    irfs = sol.impulse_responses(params, h)

    required_keys = {"date", "x_demand", "pi_demand", "i_demand", "x_policy", "pi_policy", "i_policy"}
    if not required_keys.issubset(irfs.keys()):
        pytest.fail("impulse_responses output is missing required keys.")

    for k in required_keys:
        if len(irfs[k]) != h + 1:
            pytest.fail(f"impulse_responses[{k!r}] length must equal horizon + 1.")


def test_irf_impact_signs() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    params["rho"] = 0.3
    params["sigma"] = max(float(params["sigma"]), 1.0)
    irfs = sol.impulse_responses(params, 5)

    # Demand shock: positive natural rate shock increases output gap and inflation
    if irfs["x_demand"][0] <= 0.0:
        pytest.fail("Positive demand shock must increase output gap on impact.")
    if irfs["pi_demand"][0] <= 0.0:
        pytest.fail("Positive demand shock must increase inflation on impact.")
    if irfs["i_demand"][0] <= 0.0:
        pytest.fail("Positive demand shock must raise nominal interest rate on impact.")

    # Policy shock: monetary contraction lowers output gap, lowers inflation, raises rate
    if irfs["x_policy"][0] >= 0.0:
        pytest.fail("Positive monetary policy shock must contract output gap on impact.")
    if irfs["pi_policy"][0] >= 0.0:
        pytest.fail("Positive monetary policy shock must lower inflation on impact.")
    if irfs["i_policy"][0] <= 0.0:
        pytest.fail("Positive monetary policy shock must increase nominal interest rate on impact.")


def test_irf_decay() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    params["rho"] = 0.5
    irfs = sol.impulse_responses(params, 20)

    # At horizon 20 with rho=0.5, impact decays by 0.5^20 < 1e-6
    if abs(irfs["x_demand"][-1]) > 1e-4:
        pytest.fail("Impulse response function fails to decay towards zero as persistence predicts.")


def test_irf_policy_rule_consistency() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    phi_pi = float(params["phi_pi"])
    phi_y = float(params["phi_y"])
    rho = float(params["rho"])
    irfs = sol.impulse_responses(params, 5)

    for t in range(6):
        expected_i_demand = phi_pi * irfs["pi_demand"][t] + phi_y * irfs["x_demand"][t]
        if abs(irfs["i_demand"][t] - expected_i_demand) > TOL:
            pytest.fail("Impulse response nominal rate fails the policy rule relation on the demand shock path.")

        u_t = float(rho**t)
        expected_i_policy = phi_pi * irfs["pi_policy"][t] + phi_y * irfs["x_policy"][t] + u_t
        if abs(irfs["i_policy"][t] - expected_i_policy) > TOL:
            pytest.fail("Impulse response nominal rate fails the policy rule relation on the policy shock path.")


def test_argument_purity() -> None:
    __tracebackhide__ = True
    params = _get_base_determinate_params()
    snapshot = copy.deepcopy(params)
    sol.is_determinate(params)
    sol.solve_undetermined(params)
    sol.impulse_responses(params, 5)
    if params != snapshot:
        pytest.fail("Functions must not mutate input parameter dictionaries in place.")

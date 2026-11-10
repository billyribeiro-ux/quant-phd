"""Acceptance suite for the SC6 project: HJB solver (hjb_solver.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your hjb_solver.py next to this file. Warnings are failures, as in the browser.

Each test checks mathematical properties, exact invariants, numerical convergence,
or agreement with closed-form continuous-time Merton solutions. Failing tests name
the property violated and provide a concept hint. They never reveal expected numbers.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Iterator
from typing import Any

import hjb_solver as sol  # type: ignore[import-not-found]
import pytest
from instance import make_instance  # type: ignore[import-not-found]

pytestmark = pytest.mark.filterwarnings("error")


@pytest.fixture(autouse=True)
def _no_stray_output(capsys: pytest.CaptureFixture[str]) -> Iterator[None]:
    """After every test, no output may have been printed by the engine."""
    yield
    expect(capsys.readouterr().out == "", "no function may print to stdout")


SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(SEED + 9_876)


def expect(condition: bool, message: str) -> None:
    """Fail with message when condition is false. The message never displays expected values."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(message)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError, but none was raised.")


def within(value: float, target: float, tolerance: float, message: str) -> None:
    """Fail unless |value - target| is at most the tolerance."""
    __tracebackhide__ = True
    expect(abs(value - target) <= tolerance, message)


# ---------------------------------------------------------------------------
# Instance and Parameter Checks
# ---------------------------------------------------------------------------


def test_make_instance_properties() -> None:
    """The instance generator must be deterministic, valid, and exhibit distinct values across seeds."""
    inst_a = make_instance(SEED)
    inst_b = make_instance(SEED)
    expect(inst_a == inst_b, "make_instance must be deterministic for identical seeds")
    expect(inst_a != INST2, "make_instance must generate materially different instances across seeds")
    expect(inst_a.get("label") == "SIMULATED", "instance must carry the label 'SIMULATED'")

    for key in ("r", "mu", "sigma", "gamma", "rho", "pi_max", "w_min", "w_max", "n_points", "wealth_grid"):
        expect(key in inst_a, f"instance dictionary must contain key '{key}'")

    expect(inst_a["r"] > 0.0, "risk-free rate r must be strictly positive")
    expect(inst_a["mu"] > inst_a["r"], "risky asset drift mu must exceed risk-free rate r")
    expect(inst_a["sigma"] > 0.0, "volatility sigma must be strictly positive")
    expect(inst_a["gamma"] > 1.0, "risk aversion gamma must exceed 1.0")
    expect(inst_a["rho"] > 0.0, "discount rate rho must be strictly positive")
    expect(inst_a["pi_max"] > 0.0, "borrowing constraint pi_max must be positive")
    expect(inst_a["w_min"] > 0.0, "wealth lower bound w_min must be positive")
    expect(inst_a["w_max"] > inst_a["w_min"], "wealth upper bound w_max must exceed w_min")
    expect(len(inst_a["wealth_grid"]) == inst_a["n_points"], "wealth grid length must match n_points")


# ---------------------------------------------------------------------------
# Merton Fraction and Closed-Form Solvers
# ---------------------------------------------------------------------------


def test_merton_fraction_formula() -> None:
    """merton_fraction computes the analytical optimal unconstrained allocation pi* = (mu - r) / (gamma * sigma^2)."""
    r = float(INST["r"])
    mu = float(INST["mu"])
    sigma = float(INST["sigma"])
    gamma = float(INST["gamma"])

    pi_star = sol.merton_fraction(r, mu, sigma, gamma)
    expected_pi = (mu - r) / (gamma * (sigma**2))
    within(pi_star, expected_pi, 1e-9, "merton_fraction formula mismatch")


def test_exact_merton_solution() -> None:
    """exact_merton_solution returns the exact scale-invariant CRRA value function and policy."""
    r = float(INST["r"])
    mu = float(INST["mu"])
    sigma = float(INST["sigma"])
    gamma = float(INST["gamma"])
    rho = float(INST["rho"])
    w = [float(x) for x in INST["wealth_grid"]]

    res = sol.exact_merton_solution(w, r, mu, sigma, gamma, rho)
    expect("pi" in res and "nu" in res and "v" in res and "c" in res, "exact solution missing required keys")
    expect(len(res["v"]) == len(w), "value function vector length mismatch")
    expect(len(res["c"]) == len(w), "consumption vector length mismatch")

    nu = float(res["nu"])
    expect(nu > 0.0, "transversality failed: consumption-wealth ratio nu must be positive")

    # Verify scaling law: V(w) = nu^(-gamma) / (1 - gamma) * w^(1 - gamma)
    for i, x in enumerate(w):
        expected_v = (nu ** (-gamma)) / (1.0 - gamma) * (x ** (1.0 - gamma))
        within(res["v"][i], expected_v, 1e-9, "exact value function scaling law mismatch")
        within(res["c"][i], nu * x, 1e-9, "exact consumption linearity mismatch")


def test_tridiagonal_solver() -> None:
    """solve_tridiagonal correctly solves diagonally dominant tridiagonal linear systems."""
    sub = [0.0, -1.0, -2.0, -1.0]
    diag = [4.0, 5.0, 6.0, 4.0]
    sup = [-1.0, -2.0, -1.0, 0.0]
    rhs = [3.0, 2.0, 3.0, 3.0]

    # Solution is x = [1.0, 1.0, 1.0, 1.0]
    x = sol.solve_tridiagonal(sub, diag, sup, rhs)
    expect(len(x) == 4, "tridiagonal solution length mismatch")
    for val in x:
        within(val, 1.0, 1e-9, "tridiagonal solver failed on diagonally dominant test system")


# ---------------------------------------------------------------------------
# HJB Policy Iteration Solver Convergence & Properties
# ---------------------------------------------------------------------------


def test_hjb_solver_convergence() -> None:
    """solve_merton_hjb must converge monotonically within 30 iterations on valid instances."""
    res = sol.solve_merton_hjb(INST, max_iter=50, tol=1e-6)
    expect(res.get("converged") is True, "HJB policy iteration failed to converge within allowed iterations")
    expect(res.get("iterations", 999) <= 30, "policy iteration required excessive iterations (>30)")
    expect(res.get("max_residual", 999.0) <= 1e-5, "policy iteration residual exceeds tolerance threshold")


def test_value_function_properties() -> None:
    """The computed value function must be strictly increasing and strictly concave across wealth."""
    res = sol.solve_merton_hjb(INST)
    v: list[float] = res["v"]
    n = len(v)

    # Monotonicity: V'(w) > 0 (for gamma > 1, V is negative and increasing toward 0)
    for i in range(1, n):
        expect(v[i] > v[i - 1], "value function must be strictly monotonically increasing in wealth")

    # Concavity: V''(w) < 0
    # Second difference on uniform grid: (v[i+1] - 2*v[i] + v[i-1]) / dw^2 < 0
    for i in range(1, n - 1):
        d2 = v[i + 1] - 2.0 * v[i] + v[i - 1]
        expect(d2 < 0.0, "value function must be strictly concave (negative second difference)")


def test_policy_properties() -> None:
    """The computed policy must maintain positive consumption and observe the borrowing constraint."""
    res = sol.solve_merton_hjb(INST)
    c: list[float] = res["c"]
    pi: list[float] = res["pi"]
    pi_max = float(INST["pi_max"])

    for val in c:
        expect(val > 0.0, "consumption must be strictly positive across all wealth nodes")

    for val in pi:
        expect(val >= -1e-6, "portfolio fraction must not permit short selling below zero")
        expect(val <= pi_max + 1e-6, "portfolio fraction must not violate the borrowing constraint upper bound pi_max")


# ---------------------------------------------------------------------------
# Verification Against Closed-Form Merton Benchmarks
# ---------------------------------------------------------------------------


def test_unconstrained_limit_agreement() -> None:
    """When the borrowing constraint does not bind, numerical policy and value function match unconstrained Merton."""
    unconstrained_inst = dict(INST)
    pi_star = (INST["mu"] - INST["r"]) / (INST["gamma"] * (INST["sigma"] ** 2))
    # Set pi_max well above pi_star to guarantee constraint is inactive
    unconstrained_inst["pi_max"] = round(max(2.0, 2.5 * pi_star), 3)

    res = sol.solve_merton_hjb(unconstrained_inst, tol=1e-7)
    exact = sol.exact_merton_solution(
        unconstrained_inst["wealth_grid"],
        unconstrained_inst["r"],
        unconstrained_inst["mu"],
        unconstrained_inst["sigma"],
        unconstrained_inst["gamma"],
        unconstrained_inst["rho"],
    )

    # Interior policy agreement (central 50% of grid, away from boundary discretizations)
    pi_num: list[float] = res["pi"]
    n = len(pi_num)
    interior_pi = pi_num[n // 4 : 3 * n // 4]
    mean_interior_pi = sum(interior_pi) / len(interior_pi)
    within(
        mean_interior_pi,
        pi_star,
        0.025 * pi_star + 0.01,
        "interior numerical allocation deviates from unconstrained Merton fraction",
    )

    # Relative error of value function against exact closed form
    v_num: list[float] = res["v"]
    v_exact: list[float] = exact["v"]
    rel_errors = [abs(v_num[i] - v_exact[i]) / abs(v_exact[i]) for i in range(n)]
    max_rel_error = max(rel_errors)
    expect(
        max_rel_error < 0.04,
        "maximum relative error of value function vs unconstrained closed form exceeds 4.0% discretization bound",
    )


def test_constrained_borrowing_limit() -> None:
    """When the borrowing constraint binds strictly, numerical policy clamps to pi_max across the interior."""
    constrained_inst = dict(INST)
    pi_star = (INST["mu"] - INST["r"]) / (INST["gamma"] * (INST["sigma"] ** 2))
    # Set pi_max strictly below pi_star
    pi_bound = round(0.6 * pi_star, 4)
    constrained_inst["pi_max"] = pi_bound

    res = sol.solve_merton_hjb(constrained_inst, tol=1e-7)
    exact = sol.exact_merton_solution(
        constrained_inst["wealth_grid"],
        constrained_inst["r"],
        constrained_inst["mu"],
        constrained_inst["sigma"],
        constrained_inst["gamma"],
        constrained_inst["rho"],
        pi_bound=pi_bound,
    )

    pi_num: list[float] = res["pi"]
    n = len(pi_num)
    interior_pi = pi_num[n // 4 : 3 * n // 4]
    mean_interior_pi = sum(interior_pi) / len(interior_pi)
    within(mean_interior_pi, pi_bound, 0.01, "interior allocation failed to clamp to binding borrowing limit pi_max")

    v_num: list[float] = res["v"]
    v_exact: list[float] = exact["v"]
    rel_errors = [abs(v_num[i] - v_exact[i]) / abs(v_exact[i]) for i in range(n)]
    max_rel_error = max(rel_errors)
    expect(
        max_rel_error < 0.04,
        "maximum relative error of value function vs constrained closed form exceeds 4.0% discretization bound",
    )


# ---------------------------------------------------------------------------
# Error Handling & Edge Cases
# ---------------------------------------------------------------------------


def test_invalid_inputs_raise() -> None:
    """Non-positive parameters, invalid grids, or non-positive wealth must raise ValueError."""
    must_raise(lambda: sol.merton_fraction(0.02, 0.08, -0.2, 2.0), "negative sigma in merton_fraction")
    must_raise(lambda: sol.merton_fraction(0.02, 0.08, 0.2, 0.0), "zero gamma in merton_fraction")
    must_raise(lambda: sol.merton_fraction(0.02, 0.08, 0.2, 1.0), "log utility (gamma=1) in merton_fraction")

    bad_inst = dict(INST)
    bad_inst["sigma"] = -0.1
    must_raise(lambda: sol.solve_merton_hjb(bad_inst), "negative sigma in solve_merton_hjb")

    bad_grid_inst = dict(INST)
    bad_grid_inst["wealth_grid"] = [1.0]
    must_raise(lambda: sol.solve_merton_hjb(bad_grid_inst), "singleton wealth grid in solve_merton_hjb")

    negative_wealth_inst = dict(INST)
    negative_wealth_inst["wealth_grid"] = [-1.0, 0.0, 1.0]
    must_raise(lambda: sol.solve_merton_hjb(negative_wealth_inst), "negative wealth in solve_merton_hjb")

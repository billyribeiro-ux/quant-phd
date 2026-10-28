"""Acceptance suite for the M5 project: the discounted Bellman operator and its solver (contraction_solver.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your contraction_solver.py next to this file. Warnings are failures, as in the browser.

Each test checks a property or a number against the definitions of the M5 lessons and the project specification.
Two instances are used, seed SEED and seed SEED + 7919, so a fixed answer for one seed must also match the other.
The expected values are computed here, from the instance's parameters, by this file's own loop: never from the
student's module. A failing test names the property it checks and the idea to revisit; it never prints the value
the property should have.

A test expects an exception only for the conditions the specification names as invalid (ValueError). Every other
failure is a plain check that names the property.
"""

from __future__ import annotations

import math
import os
import random
from collections.abc import Callable, Mapping, Sequence
from functools import cache
from typing import Any

import contraction_solver as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INSTANCES: tuple[dict[str, Any], dict[str, Any]] = (make_instance(SEED), make_instance(SEED + 7_919))
MAX_SWEEPS = 100_000
SMALL_GRID: list[float] = [0.5, 0.9, 1.4]


def expect(condition: bool, message: str) -> None:
    """Fail with the property's message. The message never contains a computed value."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(message)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError. Used only for the conditions the specification names as invalid."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError, and none was raised.")


def is_real(x: object) -> bool:
    """A finite real number that is not a boolean."""
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))


def close(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(b))


def params_of(inst: Mapping[str, Any]) -> dict[str, float]:
    return {"beta": inst["beta"], "alpha": inst["alpha"]}


def ref_sweep(beta: float, alpha: float, grid: Sequence[float], values: Sequence[float]) -> list[float]:
    """The test's own synchronous operator: max over feasible k' of sqrt(k**alpha - k') + beta V(k')."""
    out: list[float] = []
    for k in grid:
        resources = k**alpha
        out.append(
            max(math.sqrt(resources - kp) + beta * v for kp, v in zip(grid, values, strict=False) if kp <= resources)
        )
    return out


def ref_fixed_point(beta: float, alpha: float, grid: Sequence[float], tol: float = 1e-12) -> list[float]:
    """The grid's fixed point, from the test's own iteration from zero until the certified change is at most tol."""
    values = [0.0] * len(grid)
    factor = beta / (1 - beta)
    for _ in range(200_000):
        new = ref_sweep(beta, alpha, grid, values)
        change = max(abs(a - b) for a, b in zip(new, values, strict=False))
        values = new
        if factor * change <= tol:
            return values
    raise AssertionError("the test's own reference iteration did not converge: the instance is malformed")


@cache
def reference_value(which: int) -> tuple[float, ...]:
    inst = INSTANCES[which]
    return tuple(ref_fixed_point(inst["beta"], inst["alpha"], inst["grid"]))


def a_priori_sweeps(beta: float, alpha: float, grid: Sequence[float], tol: float) -> int:
    """The least n with beta**n * U / (1 - beta) <= tol, where U = sqrt(max grid**alpha) bounds the first sweep."""
    bound_u = math.sqrt(max(grid) ** alpha)
    n = 0
    while beta**n * bound_u / (1 - beta) > tol:
        n += 1
    return n


def as_value_list(out: Mapping[str, Any], size: int) -> list[float]:
    value: Any = out.get("value")
    expect(isinstance(value, (list, tuple)), "solve must return value as a list with one entry per grid point")
    expect(len(value) == size, "solve must return value with one entry per grid point")
    for entry in value:
        expect(is_real(entry), "every entry of value must be a finite real number, not a boolean")
    return [float(x) for x in value]


# --- the operator


@pytest.mark.parametrize("which", [0, 1])
def test_operator_matches_its_definition(which: int) -> None:
    """(B V)(k) is the maximum over feasible k' <= k**alpha of sqrt(k**alpha - k') + beta V(k'), on seeded vectors."""
    inst = INSTANCES[which]
    p = params_of(inst)
    grid = inst["grid"]
    rng = random.Random(SEED + 101 + which)
    for _ in range(3):
        values = [rng.uniform(0.0, 3.0) for _ in grid]
        got = sol.bellman_operator(p, grid, values)
        expect(
            isinstance(got, (list, tuple)) and len(got) == len(grid),
            "bellman_operator must return one value per grid point",
        )
        want = ref_sweep(p["beta"], p["alpha"], grid, values)
        expect(
            all(close(a, b, 1e-9) for a, b in zip(got, want, strict=False)),
            "bellman_operator disagrees with the definition: check the feasible successors, the consumption "
            "k**alpha - k' and the continuation term beta * V(k')",
        )


@pytest.mark.parametrize("which", [0, 1])
def test_operator_is_a_contraction_in_the_sup_norm(which: int) -> None:
    """sup|BV - BW| <= beta * sup|V - W| on seeded pairs: the contraction property of the discounted operator."""
    inst = INSTANCES[which]
    p = params_of(inst)
    grid = inst["grid"]
    rng = random.Random(SEED + 211 + which)
    for _ in range(40):
        v = [rng.uniform(0.0, 4.0) for _ in grid]
        w = [rng.uniform(0.0, 4.0) for _ in grid]
        bv = sol.bellman_operator(p, grid, v)
        bw = sol.bellman_operator(p, grid, w)
        lhs = max(abs(a - b) for a, b in zip(bv, bw, strict=False))
        rhs = p["beta"] * max(abs(a - b) for a, b in zip(v, w, strict=False))
        expect(
            lhs <= rhs + 1e-12,
            "the operator is not a contraction in the sup norm with modulus beta: the distance of the images exceeds "
            "beta times the distance of the inputs",
        )


@pytest.mark.parametrize("which", [0, 1])
def test_operator_is_monotone(which: int) -> None:
    """V <= W componentwise implies BV <= BW componentwise, on seeded pairs."""
    inst = INSTANCES[which]
    p = params_of(inst)
    grid = inst["grid"]
    rng = random.Random(SEED + 307 + which)
    for _ in range(40):
        v = [rng.uniform(0.0, 4.0) for _ in grid]
        w = [x + rng.uniform(0.0, 1.0) for x in v]
        bv = sol.bellman_operator(p, grid, v)
        bw = sol.bellman_operator(p, grid, w)
        expect(
            all(b_v <= b_w + 1e-12 for b_v, b_w in zip(bv, bw, strict=False)),
            "the operator is not monotone: a larger input vector must not give a smaller image",
        )


@pytest.mark.parametrize("which", [0, 1])
def test_successors_above_the_resources_are_infeasible(which: int) -> None:
    """A successor k' above k**alpha cannot be chosen, however large its value is."""
    inst = INSTANCES[which]
    p = params_of(inst)
    grid = inst["grid"]
    alpha = inst["alpha"]
    values = [0.0] * (len(grid) - 1) + [1.0e6]
    out = sol.bellman_operator(p, grid, values)
    constrained = [got for k, got in zip(grid, out, strict=False) if grid[-1] > k**alpha]
    expect(
        bool(constrained), "the instance has no state that cannot afford the top grid point: the instance is malformed"
    )
    expect(
        all(got < 1.0e5 for got in constrained),
        "a successor above the state's resources is infeasible: the operator must not choose it",
    )


def test_operator_does_not_change_its_inputs() -> None:
    """Neither the grid nor the values are changed by the call."""
    inst = INSTANCES[0]
    grid = list(inst["grid"])
    values = [0.5 * i for i in range(len(grid))]
    grid_before, values_before = list(grid), list(values)
    sol.bellman_operator(params_of(inst), grid, values)
    expect(grid == grid_before, "bellman_operator must not change the grid it is given")
    expect(values == values_before, "bellman_operator must not change the values it is given")


# --- the solver: validity of the certified error


@pytest.mark.parametrize("which", [0, 1])
def test_solver_returns_the_four_fields(which: int) -> None:
    """solve returns value, iterations, certified_error and converged, with iterations a whole number of sweeps."""
    inst = INSTANCES[which]
    out = sol.solve(params_of(inst), inst["grid"], inst["tol"], MAX_SWEEPS)
    expect(
        isinstance(out, Mapping), "solve must return a mapping with value, iterations, certified_error and converged"
    )
    for key in ("value", "iterations", "certified_error", "converged"):
        expect(key in out, f"solve must return the field {key}")
    it = out["iterations"]
    expect(
        isinstance(it, int) and not isinstance(it, bool) and it >= 1,
        "iterations must be a whole number of sweeps, at least 1",
    )
    expect(isinstance(out["converged"], bool), "converged must be a boolean")
    expect(
        is_real(out["certified_error"]) and out["certified_error"] >= 0,
        "certified_error must be a non-negative real number",
    )


@pytest.mark.parametrize("which", [0, 1])
def test_certified_error_bounds_the_distance_to_the_fixed_point(which: int) -> None:
    """|value - V*| <= certified_error in the sup norm, with V* the fixed point of the grid operator."""
    inst = INSTANCES[which]
    out = sol.solve(params_of(inst), inst["grid"], inst["tol"], MAX_SWEEPS)
    value = as_value_list(out, len(inst["grid"]))
    star = reference_value(which)
    gap = max(abs(a - b) for a, b in zip(value, star, strict=False))
    expect(
        gap <= float(out["certified_error"]) + 1e-9,
        "the certified error does not bound the distance to the fixed point of the grid operator: a certified "
        "bound must be at least the actual error (check the factor beta / (1 - beta) and the change it multiplies)",
    )


@pytest.mark.parametrize("which", [0, 1])
def test_residual_is_within_the_certified_bound(which: int) -> None:
    """|BV - V| <= (1 + beta) * |V - V*| <= (1 + beta) * certified_error: the residual is bounded by the certificate."""
    inst = INSTANCES[which]
    p = params_of(inst)
    grid = inst["grid"]
    out = sol.solve(p, grid, inst["tol"], MAX_SWEEPS)
    value = as_value_list(out, len(grid))
    image = sol.bellman_operator(p, grid, value)
    residual = max(abs(a - b) for a, b in zip(image, value, strict=False))
    expect(
        residual <= (1 + p["beta"]) * float(out["certified_error"]) + 1e-9,
        "the fixed-point residual exceeds (1 + beta) times the certified error, which the contraction forbids",
    )


@pytest.mark.parametrize("which", [0, 1])
def test_converged_means_certified_within_tolerance(which: int) -> None:
    """converged is True exactly when certified_error is at most tol; the instance tolerance is reachable."""
    inst = INSTANCES[which]
    out = sol.solve(params_of(inst), inst["grid"], inst["tol"], MAX_SWEEPS)
    expect(
        (out["converged"] is True) == (float(out["certified_error"]) <= inst["tol"]),
        "converged must be True exactly when certified_error is at most tol",
    )
    expect(
        out["converged"] is True,
        "the iteration did not report convergence within the budget for the instance tolerance",
    )
    star = reference_value(which)
    gap = max(abs(a - b) for a, b in zip(as_value_list(out, len(star)), star, strict=False))
    expect(
        gap <= inst["tol"] + 1e-9, "at convergence the value must be within tol of the fixed point of the grid operator"
    )


@pytest.mark.parametrize("which", [0, 1])
def test_iterations_within_the_a_priori_count(which: int) -> None:
    """iterations is at most the a priori count from beta, the grid and tol, plus one."""
    inst = INSTANCES[which]
    n_apriori = a_priori_sweeps(inst["beta"], inst["alpha"], inst["grid"], inst["tol"])
    out = sol.solve(params_of(inst), inst["grid"], inst["tol"], MAX_SWEEPS)
    expect(
        out["iterations"] <= n_apriori + 1,
        "iterations exceed the a priori count from beta and tol by more than one: "
        "check the stopping rule and the sweep count",
    )


@pytest.mark.parametrize("which", [0, 1])
def test_values_are_finite_and_nonnegative(which: int) -> None:
    """Iteration from zero keeps every value finite and nonnegative, since utilities are nonnegative."""
    inst = INSTANCES[which]
    out = sol.solve(params_of(inst), inst["grid"], inst["tol"], MAX_SWEEPS)
    value = as_value_list(out, len(inst["grid"]))
    expect(
        all(x >= -1e-12 for x in value),
        "values must be nonnegative: the iteration starts at zero and utilities are nonnegative",
    )


def test_budget_of_one_sweep_is_reported_as_not_converged() -> None:
    """With max_iter=1 and tol=1e-12, one sweep is made and the result is reported as not converged."""
    inst = INSTANCES[0]
    out = sol.solve(params_of(inst), inst["grid"], 1e-12, 1)
    expect(out["iterations"] == 1, "with a budget of one sweep, iterations must report exactly one sweep")
    expect(out["converged"] is False, "one sweep cannot meet a tolerance of 1e-12 here, so converged must be False")


def test_converged_is_false_when_the_budget_ends_with_the_certificate_above_tol() -> None:
    """converged tests the certified error, not the last change: when the budget ends first, a last change at most
    tol does not make converged True while the certified error is above tol.

    The tolerance is a fifth of the solver's own certified error after three sweeps, so the certified error is above
    tol at the budget. With beta = 0.9 the last change is one ninth of the certified error, so it is below tol."""
    p = {"beta": 0.9, "alpha": 0.5}
    first = sol.solve(p, SMALL_GRID, 1e-12, 3)
    expect(
        is_real(first["certified_error"]) and float(first["certified_error"]) > 0,
        "after three sweeps the certified error must be a positive real number",
    )
    tol = float(first["certified_error"]) / 5
    out = sol.solve(p, SMALL_GRID, tol, 3)
    expect(
        out["converged"] is False,
        "the budget ended with the certified error above tol, so converged must be False, whatever the last change is",
    )


def test_successor_exactly_at_the_resources_is_feasible() -> None:
    """A saving k' equal to k**alpha leaves zero consumption, which is allowed: k' <= k**alpha includes equality."""
    p = {"beta": 0.5, "alpha": 0.5}
    grid = [1.0, 2.0]
    got = sol.bellman_operator(p, grid, [2.0, 0.0])
    expect(
        isinstance(got, (list, tuple)) and len(got) == 2 and all(is_real(x) for x in got),
        "bellman_operator must return finite values for a grid whose first point equals the resources",
    )
    # From k = 1 the resources are 1, so only k' = 1 is feasible: sqrt(1 - 1) + beta * V(1) = 0.5 * 2.
    expect(
        close(float(got[0]), 1.0, 1e-12),
        "a successor equal to k**alpha is feasible (k' <= k**alpha): the state 1 can save all of its output",
    )
    out = sol.solve(p, grid, 1e-6, 3)
    value = as_value_list(out, len(grid))
    expect(
        all(math.isfinite(x) for x in value),
        "solve must return finite values when the first grid point equals 1",
    )


@pytest.mark.parametrize("which", [0, 1])
def test_the_first_sweep_starts_from_zero_and_is_synchronous(which: int) -> None:
    """solve starts from V0 = 0; one sweep of max_iter = 1 returns B(0), computed from the whole zero vector."""
    inst = INSTANCES[which]
    grid = inst["grid"]
    out = sol.solve(params_of(inst), grid, 1e-12, 1)
    expect(out["iterations"] == 1, "with a budget of one sweep, iterations must report exactly one sweep")
    value = as_value_list(out, len(grid))
    want = ref_sweep(inst["beta"], inst["alpha"], grid, [0.0] * len(grid))
    expect(
        all(close(a, b, 1e-9) for a, b in zip(value, want, strict=False)),
        "after one sweep from zero the value must be the operator applied to the zero vector: the iteration starts "
        "from V0 = 0 and each sweep uses the previous vector as a whole",
    )


def test_certified_error_exactly_at_tol_stops_the_first_sweep() -> None:
    """The stop is at the first sweep whose certified error is at most tol, so a tie stops it.

    The tolerance is the solver's own certified error after one sweep, read from a run with a budget of one sweep.
    Any valid certified error is accepted this way, because the tie is then exact for the solver's own bound: a
    correct solver must stop at sweep 1 with converged True."""
    p = {"beta": 0.5, "alpha": 0.5}
    grid = [0.75, 1.0]
    first = sol.solve(p, grid, 1e-12, 1)
    expect(
        is_real(first["certified_error"]) and float(first["certified_error"]) > 0,
        "after one sweep on this grid the certified error must be a positive real number",
    )
    tie = float(first["certified_error"])
    out = sol.solve(p, grid, tie, 1000)
    expect(
        out["iterations"] == 1,
        "a certified error equal to tol must stop the iteration at that sweep, not at a later one",
    )
    expect(out["converged"] is True, "a certified error equal to tol means converged is True")


def test_tolerance_just_below_the_first_certified_error_does_not_stop() -> None:
    """The stop is not looser than the definition: a tolerance just below the solver's own first certified error does
    not stop. The tolerance is read from the solver's certificate after one sweep, so any valid certified error is
    accepted; the test does not assume which bound the solver uses."""
    p = {"beta": 0.5, "alpha": 0.5}
    grid = [0.75, 1.0]
    first = sol.solve(p, grid, 1e-12, 1)
    expect(
        is_real(first["certified_error"]) and float(first["certified_error"]) > 0,
        "after one sweep on this grid the certified error must be a positive real number",
    )
    out = sol.solve(p, grid, math.nextafter(float(first["certified_error"]), 0.0), 1000)
    expect(
        out["iterations"] >= 2,
        "a tolerance just below the first certified error must not stop the iteration after one sweep",
    )


def test_one_point_grid_is_accepted() -> None:
    """A grid with one point is non-empty and strictly increasing, so the page does not name it as invalid."""
    out = sol.solve({"beta": 0.9, "alpha": 0.5}, [0.5], 1e-6, 5)
    expect(isinstance(out, Mapping), "solve must return a mapping for a grid of one point")


def test_tiny_positive_grid_point_is_accepted() -> None:
    """A grid point just above zero is a positive real number, so it is valid."""
    out = sol.solve({"beta": 0.9, "alpha": 0.5}, [1e-9, 0.5], 1e-6, 5)
    expect(
        isinstance(out, Mapping), "solve must return a mapping for a grid whose first point is a tiny positive number"
    )


def test_solver_does_not_change_its_inputs_or_print(capsys: pytest.CaptureFixture[str]) -> None:
    """The solver neither changes its grid nor prints anything."""
    inst = INSTANCES[1]
    grid = list(inst["grid"])
    before = list(grid)
    sol.solve(params_of(inst), grid, inst["tol"], 50)
    sol.bellman_operator(params_of(inst), grid, [0.0] * len(grid))
    expect(grid == before, "solve must not change the grid it is given")
    expect(capsys.readouterr().out == "", "no function may print")


# --- named invalid inputs (the only conditions that expect ValueError)


@pytest.mark.parametrize("beta", [0.0, 1.0, -0.1, 1.2, math.nan, math.inf, -math.inf, True, "0.9"])
def test_beta_outside_the_open_interval_is_refused(beta: Any) -> None:
    """beta must lie in the open interval (0, 1); a boolean or a non-finite number is refused."""
    params = {"beta": beta, "alpha": 0.5}
    must_raise(lambda: sol.bellman_operator(params, SMALL_GRID, [0.0, 0.0, 0.0]), "beta must lie in (0, 1)")
    must_raise(lambda: sol.solve(params, SMALL_GRID, 1e-6, 5), "beta must lie in (0, 1)")


@pytest.mark.parametrize("alpha", [0.0, 1.0, -0.5, 1.5, math.nan, math.inf, -math.inf, True, "0.5"])
def test_alpha_outside_the_open_interval_is_refused(alpha: Any) -> None:
    """alpha must lie in the open interval (0, 1); a boolean or a non-finite number is refused."""
    params = {"beta": 0.9, "alpha": alpha}
    must_raise(lambda: sol.bellman_operator(params, SMALL_GRID, [0.0, 0.0, 0.0]), "alpha must lie in (0, 1)")
    must_raise(lambda: sol.solve(params, SMALL_GRID, 1e-6, 5), "alpha must lie in (0, 1)")


def test_beta_and_alpha_just_inside_the_interval_are_accepted() -> None:
    """Values just inside (0, 1) are valid inputs and return a result."""
    for params in ({"beta": 1e-9, "alpha": 0.001}, {"beta": 0.999999, "alpha": 0.999}):
        out = sol.solve(params, SMALL_GRID, 1e-6, 3)
        expect(isinstance(out, Mapping), "solve must return a mapping for beta and alpha inside (0, 1)")


@pytest.mark.parametrize("tol", [0.0, -1e-9, math.nan, math.inf, -math.inf, True, "1e-6"])
def test_tolerance_must_be_positive_and_finite(tol: Any) -> None:
    """tol must be a finite real number above zero; zero, negative, non-finite and boolean values are refused."""
    must_raise(
        lambda: sol.solve({"beta": 0.9, "alpha": 0.5}, SMALL_GRID, tol, 5), "tol must be finite and greater than zero"
    )


def test_tolerance_just_above_zero_is_accepted() -> None:
    """A tiny positive tolerance is a valid input."""
    out = sol.solve({"beta": 0.9, "alpha": 0.5}, SMALL_GRID, 1e-300, 2)
    expect(isinstance(out, Mapping), "solve must return a mapping for a tolerance above zero")


@pytest.mark.parametrize("max_iter", [0, -3, 2.0, 1.0, True, "5"])
def test_budget_must_be_a_whole_number_of_sweeps_one_or_more(max_iter: Any) -> None:
    """max_iter must be a whole number of sweeps, one or more; zero, a negative, a float or a boolean is refused."""
    must_raise(
        lambda: sol.solve({"beta": 0.9, "alpha": 0.5}, SMALL_GRID, 1e-6, max_iter),
        "max_iter must be a whole number of sweeps, one or more",
    )


def test_budget_of_one_sweep_is_accepted() -> None:
    """A budget of exactly one sweep is valid."""
    out = sol.solve({"beta": 0.9, "alpha": 0.5}, SMALL_GRID, 1e-6, 1)
    expect(isinstance(out, Mapping), "solve must return a mapping for a budget of one sweep")


@pytest.mark.parametrize(
    "grid",
    [
        [],
        [0.5, 0.5],
        [0.7, 0.6],
        [0.5, 0.9, 0.7],
        [0.5, 0.9, 0.9],
        [0.0, 0.5],
        [-0.2, 0.5],
        [1.01, 2.0],
        [0.5, math.nan],
        [0.5, True],
        [0.5, math.inf],
        ["0.5", 0.9],
    ],
    ids=[
        "empty",
        "equal-points",
        "decreasing",
        "decrease-in-the-middle",
        "equal-last-pair",
        "zero-point",
        "negative-point",
        "first-above-one",
        "nan-point",
        "boolean-point",
        "infinite-point",
        "string-point",
    ],
)
def test_grid_must_be_nonempty_positive_strictly_increasing_and_start_at_most_one(grid: list[Any]) -> None:
    """A grid is non-empty, strictly increasing, of positive real points, and its first point is at most 1."""
    p = {"beta": 0.9, "alpha": 0.5}
    must_raise(lambda: sol.bellman_operator(p, grid, [0.0] * len(grid)), "invalid grid")
    must_raise(lambda: sol.solve(p, grid, 1e-6, 5), "invalid grid")


def test_grid_starting_at_exactly_one_is_accepted() -> None:
    """A first grid point equal to 1 is valid: its resources are 1, so it can save everything."""
    out = sol.solve({"beta": 0.9, "alpha": 0.5}, [1.0, 2.0], 1e-6, 3)
    expect(isinstance(out, Mapping), "solve must return a mapping for a grid whose first point is exactly 1")


def test_values_must_match_the_grid_length() -> None:
    """bellman_operator needs one value per grid point; a shorter or a longer vector is refused."""
    p = {"beta": 0.9, "alpha": 0.5}
    must_raise(lambda: sol.bellman_operator(p, SMALL_GRID, [0.0, 0.0]), "values must match the grid length")
    must_raise(lambda: sol.bellman_operator(p, SMALL_GRID, [0.0, 0.0, 0.0, 0.0]), "values must match the grid length")

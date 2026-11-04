"""Acceptance suite for the SC1 project: the reflection-principle engine (bm_checks.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your bm_checks.py next to this file. Warnings are failures, as in the browser.

Each test checks a property or an exact number. The expected numbers come from closed forms, from exact enumeration
over the 2**n walks, from a quadrature written in this file, or from identities. Several tests check one of the engine's
functions against another: the srw reflection identity, the one-step estimate against reflection_tail, the nested counts
against discrete_max_exceedance, and the coarse count against the fine count. One test calls discrete_max_exceedance
twice on the same instance and requires the same answer. A seeded-simulation check uses a band of five standard errors
plus one path (1/N), so that a target near zero is not a false failure. A failing test names the property it checks and
the idea to revisit. It never prints the expected value.
"""

from __future__ import annotations

import itertools
import math
import os
from collections.abc import Callable
from typing import Any

import bm_checks as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(SEED + 7_919)  # a second instance, so one fixed answer cannot pass both
GRID_PAIRS = [(8, 8), (8, 4), (8, 2), (8, 1), (12, 3), (12, 6), (16, 4), (4, 2)]


def with_(inst: dict[str, Any], **changes: Any) -> dict[str, Any]:
    """A copy of an instance with some fields changed."""
    return {**inst, **changes}


def expect(condition: bool, message: str) -> None:
    """Fail with the property's message when the condition is false. The message never holds a value."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(message)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError. Used only for the conditions the specification names."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError, and none was raised.")


def must_accept(call: Callable[[], Any], condition: str) -> Any:
    """Return call()'s value. Fail if a valid input under the named condition raises ValueError."""
    __tracebackhide__ = True
    try:
        return call()
    except ValueError:
        pytest.fail(f"{condition}: this input is valid under the specification and must not raise ValueError.")
    return None


def within(value: float, target: float, tolerance: float, message: str) -> None:
    """Fail unless |value - target| is at most the tolerance. The message never holds a value."""
    __tracebackhide__ = True
    expect(abs(value - target) <= tolerance, message)


def simulation_band(se: float, n_paths: int) -> float:
    """Five standard errors, plus one path, as the tolerance for a seeded-simulation comparison."""
    return 5.0 * se + 1.0 / n_paths


def gaussian_tail_by_quadrature(level: float, horizon: float, intervals: int = 4000) -> float:
    """2 * P(B_t >= a) by Simpson's rule on the N(0, t) density over [a, a + 12 sqrt(t)], written independently here."""
    top = level + 12.0 * math.sqrt(horizon)
    step = (top - level) / intervals

    def density(x: float) -> float:
        return math.exp(-x * x / (2.0 * horizon)) / math.sqrt(2.0 * math.pi * horizon)

    total = density(level) + density(top)
    for k in range(1, intervals):
        total += (4.0 if k % 2 else 2.0) * density(level + k * step)
    return 2.0 * total * step / 3.0


def brute_counts(n: int, a: int) -> tuple[int, int]:
    """The exact counts over all 2**n equally likely walks: (#{max >= a}, #{S_n >= a}), by enumeration."""
    max_hits = 0
    end_hits = 0
    for steps in itertools.product((1, -1), repeat=n):
        sums = list(itertools.accumulate(steps))
        if max(sums) >= a:
            max_hits += 1
        if sums[-1] >= a:
            end_hits += 1
    return max_hits, end_hits


# ---------------------------------------------------------------------------------------------------------------------
# Instances.


@pytest.mark.parametrize("inst", [INST, INST2], ids=["student seed", "second seed"])
def test_instance_is_labelled_and_valid(inst: dict[str, Any]) -> None:
    expect(inst["label"] == "SIMULATED", "every instance must carry the label SIMULATED")
    expect(inst["H"] > 0, "the horizon H must be positive")
    expect(inst["a"] > 0, "the level a must be positive")
    expect(4 <= inst["n_steps"] <= 256, "the grid size must lie between 4 and 256 steps")
    expect(400 <= inst["n_paths"] <= 800, "the path count must lie between 400 and 800")
    expect(inst["n_steps"] * inst["n_paths"] <= 200_000, "the instance draws too many increments for the time limit")


def test_make_instance_is_deterministic() -> None:
    expect(make_instance(SEED) == make_instance(SEED), "the same seed must give the same instance")


def test_fifty_seeds_give_valid_instances_with_distinct_levels() -> None:
    instances = [make_instance(seed) for seed in range(50)]
    for inst in instances:
        expect(inst["H"] > 0 and inst["a"] > 0, "every seed in 0 to 49 must give a positive horizon and level")
        expect(4 <= inst["n_steps"] <= 256 and 400 <= inst["n_paths"] <= 800, "every seed must respect the ranges")
    expect(len({inst["a"] for inst in instances}) >= 45, "the levels must differ across seeds 0 to 49")


# ---------------------------------------------------------------------------------------------------------------------
# reflection_tail: P(M_t >= a) = erfc(a / sqrt(2 t)) = 2 P(B_t >= a).


@pytest.mark.parametrize("inst", [INST, INST2], ids=["student seed", "second seed"])
def test_reflection_tail_is_the_erfc_closed_form(inst: dict[str, Any]) -> None:
    target = math.erfc(inst["a"] / math.sqrt(2.0 * inst["H"]))
    within(sol.reflection_tail(inst["a"], inst["H"]), target, 1e-10, "the tail must equal erfc(a / sqrt(2 t)) to 1e-10")


@pytest.mark.parametrize("inst", [INST, INST2], ids=["student seed", "second seed"])
def test_reflection_tail_equals_twice_the_gaussian_tail_by_quadrature(inst: dict[str, Any]) -> None:
    target = gaussian_tail_by_quadrature(inst["a"], inst["H"])
    within(sol.reflection_tail(inst["a"], inst["H"]), target, 1e-8, "the tail must equal 2 P(B_t >= a) (reflection)")


@pytest.mark.parametrize("inst", [INST, INST2], ids=["student seed", "second seed"])
def test_reflection_tail_is_strictly_decreasing_in_the_level(inst: dict[str, Any]) -> None:
    a, t = inst["a"], inst["H"]
    delta = a / 10.0
    lower = sol.reflection_tail(a - delta, t)
    middle = sol.reflection_tail(a, t)
    upper = sol.reflection_tail(a + delta, t)
    expect(lower > middle > upper, "the tail P(M_t >= a) must fall strictly as the level a rises")


@pytest.mark.parametrize("inst", [INST, INST2], ids=["student seed", "second seed"])
def test_reflection_tail_is_strictly_increasing_in_time(inst: dict[str, Any]) -> None:
    a, t = inst["a"], inst["H"]
    shorter = sol.reflection_tail(a, t / 2.0)
    middle = sol.reflection_tail(a, t)
    longer = sol.reflection_tail(a, 2.0 * t)
    expect(shorter < middle < longer, "the tail P(M_t >= a) must rise strictly with the time t")


@pytest.mark.parametrize("inst", [INST, INST2], ids=["student seed", "second seed"])
def test_reflection_tail_is_a_probability_strictly_between_zero_and_one(inst: dict[str, Any]) -> None:
    value = sol.reflection_tail(inst["a"], inst["H"])
    expect(0.0 < value < 1.0, "a tail probability for a positive level must lie strictly between 0 and 1")


def test_reflection_tail_rejects_zero_level() -> None:
    must_raise(lambda: sol.reflection_tail(0.0, INST["H"]), "a = 0")


def test_reflection_tail_rejects_negative_level() -> None:
    must_raise(lambda: sol.reflection_tail(-0.5, INST["H"]), "a < 0")


def test_reflection_tail_level_just_above_zero_is_accepted() -> None:
    value = must_accept(lambda: sol.reflection_tail(1e-9, INST["H"]), "a = 1e-9")
    expect(value > 0.999999, "a level of 1e-9 must give a tail that is near one")


def test_reflection_tail_rejects_zero_time() -> None:
    must_raise(lambda: sol.reflection_tail(INST["a"], 0.0), "t = 0")


def test_reflection_tail_rejects_negative_time() -> None:
    must_raise(lambda: sol.reflection_tail(INST["a"], -1.0), "t < 0")


def test_reflection_tail_time_just_above_zero_is_accepted() -> None:
    value = must_accept(lambda: sol.reflection_tail(INST["a"], 1e-9), "t = 1e-9")
    expect(value < 1e-6, "a tiny time must give a tail that is near zero")


def test_reflection_tail_tiny_level_gives_a_tail_near_one() -> None:
    within(sol.reflection_tail(1e-9, INST["H"]), 1.0, 1e-8, "a tail at a level near zero must be near one")


# ---------------------------------------------------------------------------------------------------------------------
# srw_max_count and srw_terminal_count: exact integers over the 2**n simple random walks.


@pytest.mark.parametrize("n", list(range(1, 13)))
def test_srw_counts_match_enumeration_for_n_up_to_12(n: int) -> None:
    for a in range(1, n + 1):
        max_hits, end_hits = brute_counts(n, a)
        expect(sol.srw_max_count(n, a) == max_hits, "srw_max_count must equal the enumerated count of paths")
        expect(sol.srw_terminal_count(n, a) == end_hits, "srw_terminal_count must equal the enumerated count")


@pytest.mark.parametrize("n", list(range(1, 13)))
def test_srw_reflection_identity_holds_exactly(n: int) -> None:
    for a in range(1, n + 1):
        identity = sol.srw_terminal_count(n, a) + sol.srw_terminal_count(n, a + 1)
        expect(sol.srw_max_count(n, a) == identity, "#{max >= a} must equal #{S_n >= a} + #{S_n >= a + 1}")


@pytest.mark.parametrize("n", list(range(1, 13)))
def test_srw_max_count_bounds(n: int) -> None:
    for a in range(1, n + 1):
        maximum = sol.srw_max_count(n, a)
        expect(
            sol.srw_terminal_count(n, a) <= maximum <= 2**n,
            "the maximum count must lie between the endpoint count and 2**n",
        )


@pytest.mark.parametrize("n", list(range(1, 13)))
def test_srw_level_one_terminal_count_by_symmetry(n: int) -> None:
    ties = 0 if n % 2 else math.comb(n, n // 2)
    expect(sol.srw_terminal_count(n, 1) == (2**n - ties) // 2, "#{S_n >= 1} must equal (2**n - #{S_n = 0}) / 2")


def test_srw_level_beyond_the_length_counts_nothing() -> None:
    expect(sol.srw_max_count(5, 6) == 0, "no walk of length 5 can reach level 6")
    expect(sol.srw_terminal_count(5, 6) == 0, "no walk of length 5 can end at level 6 or above")


def test_srw_integers_are_exact_for_a_long_odd_walk() -> None:
    expect(sol.srw_terminal_count(41, 1) == 2**40, "for odd n the endpoint count at level 1 is 2**(n-1)")


@pytest.mark.parametrize("name", ["srw_max_count", "srw_terminal_count"])
def test_srw_rejects_zero_length(name: str) -> None:
    function = getattr(sol, name)
    must_raise(lambda: function(0, 1), f"{name} with n = 0")


@pytest.mark.parametrize("name", ["srw_max_count", "srw_terminal_count"])
def test_srw_accepts_one_step(name: str) -> None:
    function = getattr(sol, name)
    must_accept(lambda: function(1, 1), f"{name} with n = 1")


@pytest.mark.parametrize("name", ["srw_max_count", "srw_terminal_count"])
def test_srw_rejects_negative_length(name: str) -> None:
    function = getattr(sol, name)
    must_raise(lambda: function(-1, 1), f"{name} with n = -1")


@pytest.mark.parametrize("name", ["srw_max_count", "srw_terminal_count"])
def test_srw_rejects_zero_level(name: str) -> None:
    function = getattr(sol, name)
    must_raise(lambda: function(4, 0), f"{name} with a = 0")


@pytest.mark.parametrize("name", ["srw_max_count", "srw_terminal_count"])
def test_srw_rejects_negative_level(name: str) -> None:
    function = getattr(sol, name)
    must_raise(lambda: function(4, -1), f"{name} with a = -1")


@pytest.mark.parametrize("name", ["srw_max_count", "srw_terminal_count"])
def test_srw_accepts_level_one(name: str) -> None:
    function = getattr(sol, name)
    must_accept(lambda: function(4, 1), f"{name} with a = 1")


# ---------------------------------------------------------------------------------------------------------------------
# discrete_max_exceedance: estimate and standard error on the instance's seeded grid.


@pytest.mark.parametrize("inst", [INST, INST2], ids=["student seed", "second seed"])
def test_estimate_is_a_fraction_of_the_paths(inst: dict[str, Any]) -> None:
    estimate, _ = sol.discrete_max_exceedance(inst, inst["n_steps"])
    expect(0.0 <= estimate <= 1.0, "the estimate is a fraction of paths and must lie in [0, 1]")
    expect(abs(estimate * inst["n_paths"] - round(estimate * inst["n_paths"])) < 1e-9, "a fraction of N paths")


@pytest.mark.parametrize("inst", [INST, INST2], ids=["student seed", "second seed"])
def test_standard_error_uses_divisor_n_minus_one(inst: dict[str, Any]) -> None:
    estimate, se = sol.discrete_max_exceedance(inst, inst["n_steps"])
    n = inst["n_paths"]
    target = math.sqrt(estimate * (1.0 - estimate) / (n - 1))
    within(se, target, 1e-12, "the standard error must be the sample sd of the indicators divided by sqrt(N)")


def test_standard_error_is_zero_when_no_path_reaches_the_level() -> None:
    estimate, se = sol.discrete_max_exceedance(with_(INST, a=1000.0), 4)
    expect(estimate == 0.0, "no path reaches a level of 1000 on a grid of horizon at most 4")
    expect(se == 0.0, "a standard error of a constant indicator is zero")


def test_one_step_estimate_matches_the_one_step_gaussian_law() -> None:
    estimate, se = sol.discrete_max_exceedance(INST, 1)
    target = sol.reflection_tail(INST["a"], INST["H"]) / 2.0
    expect(
        abs(estimate - target) <= simulation_band(se, INST["n_paths"]),
        "with one grid step the maximum is B_H, so P(B_H >= a) is half the tail",
    )


def test_one_step_estimate_matches_the_one_step_law_for_second_seed() -> None:
    estimate, se = sol.discrete_max_exceedance(INST2, 1)
    target = sol.reflection_tail(INST2["a"], INST2["H"]) / 2.0
    expect(
        abs(estimate - target) <= simulation_band(se, INST2["n_paths"]),
        "with one grid step the maximum is B_H, so P(B_H >= a) is half the tail",
    )


@pytest.mark.parametrize("inst", [INST, INST2], ids=["student seed", "second seed"])
def test_grid_estimate_does_not_exceed_the_continuous_tail(inst: dict[str, Any]) -> None:
    tail = sol.reflection_tail(inst["a"], inst["H"])
    for n_steps in (4, inst["n_steps"]):
        estimate, se = sol.discrete_max_exceedance(inst, n_steps)
        expect(
            estimate <= tail + simulation_band(se, inst["n_paths"]),
            "a grid maximum is at most the continuous maximum, so the grid estimate cannot exceed the tail",
        )


def test_estimate_is_reproducible_for_the_same_instance() -> None:
    first = sol.discrete_max_exceedance(INST, INST["n_steps"])
    second = sol.discrete_max_exceedance(INST, INST["n_steps"])
    expect(first == second, "the same instance and grid must give the same estimate and standard error")


def test_draws_depend_on_the_instance_seed() -> None:
    other = with_(INST, seed=INST["seed"] + 7_919)
    changed = [
        sol.discrete_max_exceedance(INST, g) != sol.discrete_max_exceedance(other, g) for g in (4, 8, 16, 32, 64)
    ]
    expect(
        any(changed), "changing only the instance seed must change the sampled paths, so a grid estimate must change"
    )


def test_two_paths_give_an_estimate_and_a_standard_error() -> None:
    estimate, se = sol.discrete_max_exceedance(with_(INST, n_paths=2), 4)
    expect(estimate in (0.0, 0.5, 1.0), "with two paths the estimate is 0, one half or 1")
    within(se, math.sqrt(estimate * (1.0 - estimate)), 1e-12, "with N = 2 the divisor is 1")


def test_n_steps_zero_raises_value_error() -> None:
    must_raise(lambda: sol.discrete_max_exceedance(INST, 0), "n_steps = 0")


def test_one_grid_step_is_accepted() -> None:
    must_accept(lambda: sol.discrete_max_exceedance(INST, 1), "n_steps = 1")


def test_one_path_raises_value_error() -> None:
    must_raise(lambda: sol.discrete_max_exceedance(with_(INST, n_paths=1), 4), "n_paths = 1")


def test_zero_paths_raises_value_error() -> None:
    must_raise(lambda: sol.discrete_max_exceedance(with_(INST, n_paths=0), 4), "n_paths = 0")


def test_negative_grid_size_raises_value_error() -> None:
    must_raise(lambda: sol.discrete_max_exceedance(INST, -3), "n_steps = -3")


def test_two_paths_are_accepted() -> None:
    must_accept(lambda: sol.discrete_max_exceedance(with_(INST, n_paths=2), 4), "n_paths = 2")


# ---------------------------------------------------------------------------------------------------------------------
# nested_grid_counts: the coarse grid is a subset of the fine grid, on the same paths.


@pytest.mark.parametrize(("n_fine", "n_coarse"), GRID_PAIRS)
def test_coarse_count_never_exceeds_the_fine_count(n_fine: int, n_coarse: int) -> None:
    fine, coarse = sol.nested_grid_counts(INST, n_fine, n_coarse)
    expect(coarse <= fine, "a coarse grid is a subset of the fine grid, so its maximum is never larger")
    expect(fine >= 0 and coarse >= 0, "counts are never negative")


def test_fine_count_is_the_discrete_estimate_times_n() -> None:
    fine, _ = sol.nested_grid_counts(INST, 8, 4)
    estimate, _ = sol.discrete_max_exceedance(INST, 8)
    within(estimate, fine / INST["n_paths"], 1e-12, "the fine count must equal the discrete estimate times N")


def test_equal_grids_give_equal_counts() -> None:
    fine, coarse = sol.nested_grid_counts(INST2, 6, 6)
    expect(fine == coarse, "when the coarse grid is the fine grid the two counts must agree")


def test_one_step_coarse_grid_tracks_the_terminal_law() -> None:
    fine, coarse = sol.nested_grid_counts(INST, 8, 1)
    estimate = coarse / INST["n_paths"]
    se = math.sqrt(estimate * (1.0 - estimate) / (INST["n_paths"] - 1))
    target = sol.reflection_tail(INST["a"], INST["H"]) / 2.0
    expect(
        abs(estimate - target) <= simulation_band(se, INST["n_paths"]),
        "a one-step coarse grid observes B_H, whose exceedance probability is half the tail",
    )
    expect(fine >= coarse, "the fine count still dominates the coarse count")


@pytest.mark.parametrize(("n_fine", "n_coarse"), [(4, 3), (6, 4), (4, 8), (10, 4)])
def test_coarse_grid_that_does_not_divide_fine_raises_value_error(n_fine: int, n_coarse: int) -> None:
    must_raise(lambda: sol.nested_grid_counts(INST, n_fine, n_coarse), f"n_coarse = {n_coarse} does not divide n_fine")


@pytest.mark.parametrize(("n_fine", "n_coarse"), [(4, 2), (4, 4), (4, 1), (12, 6)])
def test_coarse_grid_that_divides_fine_is_accepted(n_fine: int, n_coarse: int) -> None:
    must_accept(lambda: sol.nested_grid_counts(INST, n_fine, n_coarse), f"n_coarse = {n_coarse} divides n_fine")


def test_fine_grid_of_zero_steps_raises_value_error() -> None:
    must_raise(lambda: sol.nested_grid_counts(INST, 0, 1), "n_fine = 0")


def test_coarse_grid_of_zero_steps_raises_value_error() -> None:
    must_raise(lambda: sol.nested_grid_counts(INST, 4, 0), "n_coarse = 0")


@pytest.mark.parametrize(("n_fine", "n_coarse"), [(-4, 2), (4, -2), (-1, -1)])
def test_negative_grid_sizes_raise_value_error(n_fine: int, n_coarse: int) -> None:
    must_raise(lambda: sol.nested_grid_counts(INST, n_fine, n_coarse), f"n_fine = {n_fine}, n_coarse = {n_coarse}")


def test_one_fine_step_and_one_coarse_step_are_accepted() -> None:
    must_accept(lambda: sol.nested_grid_counts(INST, 1, 1), "n_fine = 1 and n_coarse = 1")


# ---------------------------------------------------------------------------------------------------------------------
# Output and types.


def test_no_function_prints_or_warns(capsys: pytest.CaptureFixture[str]) -> None:
    sol.reflection_tail(INST["a"], INST["H"])
    sol.discrete_max_exceedance(INST, 4)
    sol.nested_grid_counts(INST, 4, 2)
    sol.srw_max_count(6, 2)
    sol.srw_terminal_count(6, 2)
    expect(capsys.readouterr().out == "", "no function may print")


def test_count_functions_return_integers() -> None:
    expect(isinstance(sol.srw_max_count(6, 2), int), "srw_max_count must return an exact integer")
    expect(isinstance(sol.srw_terminal_count(6, 2), int), "srw_terminal_count must return an exact integer")
    fine, coarse = sol.nested_grid_counts(INST, 4, 2)
    expect(isinstance(fine, int) and isinstance(coarse, int), "nested counts must be integers")

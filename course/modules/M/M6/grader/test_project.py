"""Acceptance suite for the M6 project: the martingale checks engine (martingale_checks.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your martingale_checks.py next to this file. Warnings are failures, as in the browser.

Each test checks a property or an exact number. The expected numbers come from exact enumeration, from closed forms,
or from values worked out by hand in this file, never from the engine. Money is compared as integer cents, after the
specification's rule (rounded once, half up, from the exact value). A failing test names the property it checks and
the idea to revisit. It never prints the expected value.
"""

from __future__ import annotations

import itertools
import math
import os
import warnings
from collections.abc import Callable
from fractions import Fraction
from typing import Any

import martingale_checks as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(SEED + 7_919)  # a second instance, so one fixed answer cannot pass both
HALF = Fraction(1, 2)
CONTROL_WIN = Fraction(1, 3)  # the non-martingale control: the same walk with an unfair coin


def with_(inst: dict[str, Any], **changes: Any) -> dict[str, Any]:
    """A copy of an instance with some fields changed."""
    return {**inst, **changes}


def control(inst: dict[str, Any]) -> dict[str, Any]:
    """The control instance: the same stopping rule and capital, with win probability 1/3."""
    return with_(inst, win_probability=CONTROL_WIN)


def nearest_cent(x: Fraction) -> int:
    """The test's own rule: an exact amount in cents, rounded once, half up."""
    return math.floor(x + HALF)


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


# ---------------------------------------------------------------------------------------------------------------------
# Exact enumerations, independent of the engine.


def enum_stopped(inst: dict[str, Any]) -> Fraction:
    """E[S_tau] by enumerating all 2**N paths: tau is the first time S reaches stop_level, or stop_cap if earlier."""
    n = int(inst["horizon"])
    level = int(inst["stop_level"])
    cap = int(inst["stop_cap"])
    p = Fraction(inst["win_probability"])
    total = Fraction(0)
    for steps in itertools.product((1, -1), repeat=n):
        weight = Fraction(1)
        for step in steps:
            weight *= p if step == 1 else 1 - p
        position = 0
        value: int | None = None
        for step in steps[:cap]:
            position += step
            if position == level:
                value = position
                break
        if value is None:
            value = sum(steps[:cap])
        total += weight * value
    return total


def enum_doob(inst: dict[str, Any], lam: int) -> tuple[Fraction, Fraction]:
    """The fair walk's P(max_{k<=N} |S_k| >= lam) and E|S_N| / lam, by enumerating all 2**N equally likely paths."""
    n = int(inst["horizon"])
    hits = Fraction(0)
    expected_abs = Fraction(0)
    weight = Fraction(1, 2**n)
    for steps in itertools.product((1, -1), repeat=n):
        position = 0
        peak = 0
        for step in steps:
            position += step
            peak = max(peak, abs(position))
        if peak >= lam:
            hits += weight
        expected_abs += weight * abs(position)
    return hits, expected_abs / lam


def enum_doubling(capital: int, base: int, p: Fraction) -> dict[str, Any]:
    """The doubling strategy by recursion over the bets: win and ruin probabilities, wealths and E[final wealth]."""
    branches: list[tuple[Fraction, int, str, int]] = []

    def play(wealth: int, bet: int, weight: Fraction, placed: int) -> None:
        stake = base * 2 ** (bet - 1)
        if stake > wealth:
            branches.append((weight, wealth, "ruin", placed))
            return
        branches.append((weight * p, wealth + stake, "win", placed + 1))
        play(wealth - stake, bet + 1, weight * (1 - p), placed + 1)

    play(capital, 1, Fraction(1), 0)
    win = sum((w for w, _, kind, _ in branches if kind == "win"), Fraction(0))
    ruin = sum((w for w, _, kind, _ in branches if kind == "ruin"), Fraction(0))
    expected = sum((w * wealth for w, wealth, _, _ in branches), Fraction(0))
    wealth_on_win = {wealth for _, wealth, kind, _ in branches if kind == "win"}
    wealth_on_ruin = {wealth for _, wealth, kind, _ in branches if kind == "ruin"}
    bets = next(placed for _, _, kind, placed in branches if kind == "ruin")
    return {
        "win": win,
        "ruin": ruin,
        "expected": expected,
        "wealth_on_win": wealth_on_win,
        "wealth_on_ruin": wealth_on_ruin,
        "bets": bets,
    }


SEEDED_INSTANCES = (INST, INST2)


# ---------------------------------------------------------------------------------------------------------------------
# Instances: the generator is part of the project's check and must give valid, SIMULATED cases.


@pytest.mark.parametrize("inst", SEEDED_INSTANCES)
def test_instance_is_labelled_and_valid(inst: dict[str, Any]) -> None:
    expect(inst["label"] == "SIMULATED", "every generated instance must be labelled SIMULATED")
    expect(4 <= inst["horizon"] <= 10, "the generated horizon must lie between 4 and 10 steps")
    expect(1 <= inst["stop_cap"] <= inst["horizon"], "the generated stopping cap must lie between 1 and the horizon")
    expect(1 <= inst["base_stake_cents"] <= inst["capital_cents"], "a generated base stake must be at most the capital")
    expect(Fraction(inst["win_probability"]) == HALF, "the generated coin must be fair, so each walk is a martingale")


def test_seeds_give_different_instances() -> None:
    expect(INST != INST2, "two seeds must give different instances, or the seed would not test anything")


# ---------------------------------------------------------------------------------------------------------------------
# Optional stopping, bounded case: E[S_tau] = S_0 for every bounded stopping time of the fair walk.


@pytest.mark.parametrize("inst", SEEDED_INSTANCES)
def test_fair_walk_bounded_stopping_keeps_expectation(inst: dict[str, Any]) -> None:
    value = must_accept(lambda: sol.stopped_value_expectation(inst), "optional stopping, bounded case")
    expect(
        value == 0,
        "optional stopping (bounded case): for the fair walk and a stopping time bounded by N, E[S_tau] must equal "
        "the starting value S_0 of the walk. Revisit the stopped-martingale identity in Lesson 10.",
    )


@pytest.mark.parametrize("inst", SEEDED_INSTANCES)
def test_stopped_value_matches_enumeration(inst: dict[str, Any]) -> None:
    value = must_accept(lambda: sol.stopped_value_expectation(inst), "optional stopping, bounded case")
    expect(
        value == enum_stopped(inst),
        "the expectation of the walk at the stopping time differs from the exact enumeration of every path. Check "
        "the rule: the walk stops at the first time it reaches the level, or at the cap, whichever is earlier.",
    )


@pytest.mark.parametrize("inst", SEEDED_INSTANCES)
def test_control_walk_breaks_the_identity(inst: dict[str, Any]) -> None:
    ctl = control(inst)
    value = must_accept(lambda: sol.stopped_value_expectation(ctl), "optional stopping, control")
    expect(
        value == enum_stopped(ctl),
        "the control walk (win probability 1/3) differs from the exact enumeration. The win probability must come "
        "from the instance, not from a fixed value.",
    )
    expect(
        value != 0,
        "the control walk is not a martingale, so its stopped expectation must differ from the starting value of the "
        "walk. A fixed fair coin would make the control pass the identity.",
    )


def test_cap_equal_to_horizon_is_accepted() -> None:
    inst = with_(INST, stop_cap=INST["horizon"])
    value = must_accept(lambda: sol.stopped_value_expectation(inst), "a stopping rule bounded by N")
    expect(value == enum_stopped(inst), "a stopping time equal to the horizon N must be handled exactly")


def test_cap_above_horizon_raises_value_error() -> None:
    inst = with_(INST, stop_cap=INST["horizon"] + 1)
    must_raise(
        lambda: sol.stopped_value_expectation(inst),
        "a stopping rule that is not bounded by the horizon N",
    )


def test_stopping_rule_that_never_fires_stops_at_its_cap() -> None:
    inst = with_(INST, stop_level=1000)
    value = must_accept(lambda: sol.stopped_value_expectation(inst), "a stopping rule that never fires")
    expect(
        value == enum_stopped(inst),
        "a stopping rule whose level is never reached must stop at its cap: check the walk's value at the cap.",
    )


def test_horizon_zero_raises_value_error() -> None:
    inst = with_(INST, horizon=0, stop_cap=0)
    must_raise(lambda: sol.stopped_value_expectation(inst), "a horizon N below 1")


def test_horizon_minus_one_raises_value_error() -> None:
    inst = with_(INST, horizon=-1, stop_cap=-1)
    must_raise(lambda: sol.stopped_value_expectation(inst), "a horizon N below 1 (negative)")


@pytest.mark.parametrize("level", [-2, -1, 0, 1, 2])
@pytest.mark.parametrize("win", [HALF, CONTROL_WIN, Fraction(2, 3)])
def test_stopping_level_both_directions_matches_enumeration(level: int, win: Fraction) -> None:
    inst = with_(INST, stop_level=level, win_probability=win)
    value = must_accept(lambda: sol.stopped_value_expectation(inst), "a stopping level on either side of the start")
    expect(
        value == enum_stopped(inst),
        "the stopped expectation for a stopping level on either side of the start must match the exact enumeration. "
        "Check the sign of the level and which step of the path it is compared with.",
    )


def test_horizon_one_is_accepted() -> None:
    inst = with_(INST, horizon=1, stop_cap=1, stop_level=1)
    value = must_accept(lambda: sol.stopped_value_expectation(inst), "a horizon of 1 step")
    expect(
        value == enum_stopped(inst),
        "with horizon 1 the walk stops after one step: check the expectation against the one-step paths.",
    )


# ---------------------------------------------------------------------------------------------------------------------
# Doob's maximal inequality: P(max_{k<=N} X_k >= lam) <= E[X_N] / lam for the nonnegative submartingale X_k = |S_k|.


@pytest.mark.parametrize("inst", SEEDED_INSTANCES)
def test_doob_probability_and_bound_match_enumeration(inst: dict[str, Any]) -> None:
    for lam in range(1, int(inst["horizon"]) + 2):
        prob, bound = sol.doob_max_probability(inst, lam)
        exact_prob, exact_bound = enum_doob(inst, lam)
        expect(
            prob == exact_prob,
            "Doob's inequality: the probability that the largest |S_k| reaches the level, up to the horizon, differs "
            "from the exact enumeration. Check that the maximum includes the last time N.",
        )
        expect(
            bound == exact_bound,
            "Doob's inequality: the bound must be E|S_N| divided by the level, with the first power of |S_N|. Revisit "
            "Corollary 11.4 in Lesson 11.",
        )


@pytest.mark.parametrize("inst", SEEDED_INSTANCES)
def test_doob_probability_is_at_most_the_bound(inst: dict[str, Any]) -> None:
    for lam in range(1, int(inst["horizon"]) + 2):
        prob, bound = sol.doob_max_probability(inst, lam)
        expect(
            prob <= bound,
            "Doob's inequality: the probability must not exceed the bound for a nonnegative submartingale",
        )


def test_doob_last_time_is_counted() -> None:
    n = int(INST["horizon"])
    prob, _ = sol.doob_max_probability(INST, n)
    expect(
        prob == Fraction(2, 2**n),
        "Doob's inequality: at level equal to the horizon, count the paths that reach the level by time N. "
        "The maximum must include time N.",
    )


def test_doob_level_zero_raises_value_error() -> None:
    must_raise(lambda: sol.doob_max_probability(INST, 0), "a level lambda that is not positive (zero)")


def test_doob_level_negative_raises_value_error() -> None:
    must_raise(lambda: sol.doob_max_probability(INST, -1), "a level lambda that is not positive (negative)")


def test_doob_level_one_is_accepted() -> None:
    must_accept(lambda: sol.doob_max_probability(INST, 1), "a level lambda of one step")


def test_doob_horizon_one_edge_case() -> None:
    inst = with_(INST, horizon=1)
    prob, bound = must_accept(lambda: sol.doob_max_probability(inst, 1), "Doob's inequality with horizon 1")
    expect(
        prob == enum_doob(inst, 1)[0] and bound == enum_doob(inst, 1)[1],
        "with horizon 1 and level 1, check the probability and the bound against the two one-step paths.",
    )


def test_doob_horizon_zero_raises_value_error() -> None:
    inst = with_(INST, horizon=0)
    must_raise(lambda: sol.doob_max_probability(inst, 1), "a horizon N below 1 in Doob's inequality")


def test_doob_horizon_minus_one_raises_value_error() -> None:
    inst = with_(INST, horizon=-1)
    must_raise(lambda: sol.doob_max_probability(inst, 1), "a horizon N below 1 in Doob's inequality (negative)")


# ---------------------------------------------------------------------------------------------------------------------
# Doubling with finite capital: bet k stakes base * 2**(k-1) cents; a bet is placed only if the stake fits the wealth.


@pytest.mark.parametrize("inst", SEEDED_INSTANCES)
def test_doubling_bets_and_wealths_match_enumeration(inst: dict[str, Any]) -> None:
    capital = int(inst["capital_cents"])
    base = int(inst["base_stake_cents"])
    exact = enum_doubling(capital, base, HALF)
    out = must_accept(lambda: sol.doubling_outcome(inst), "doubling with finite capital")
    expect(
        out["bets_allowed"] == exact["bets"],
        "doubling: the number of bets the capital allows differs from the exact enumeration. A bet is placed only if "
        "its stake does not exceed the wealth on hand.",
    )
    expect(
        exact["wealth_on_win"] == {out["wealth_on_win_cents"]},
        "doubling: after a win, check what the winning bet returns to the wealth, in cents",
    )
    expect(
        exact["wealth_on_ruin"] == {out["wealth_on_ruin_cents"]},
        "doubling: after ruin, check the wealth against the total of the stakes lost on the placed bets, in cents",
    )


@pytest.mark.parametrize("inst", SEEDED_INSTANCES)
def test_doubling_probabilities_match_and_sum_to_one(inst: dict[str, Any]) -> None:
    capital = int(inst["capital_cents"])
    base = int(inst["base_stake_cents"])
    exact = enum_doubling(capital, base, HALF)
    out = sol.doubling_outcome(inst)
    expect(out["win_probability"] == exact["win"], "doubling: the win probability differs from the exact enumeration")
    expect(
        out["ruin_probability"] == exact["ruin"], "doubling: the ruin probability differs from the exact enumeration"
    )
    expect(
        out["win_probability"] + out["ruin_probability"] == 1,
        "doubling: the ruin and win probabilities must sum to 1, since the strategy either wins or is ruined",
    )


@pytest.mark.parametrize("inst", SEEDED_INSTANCES)
def test_fair_doubling_expected_wealth_is_the_capital(inst: dict[str, Any]) -> None:
    out = sol.doubling_outcome(inst)
    expect(
        out["expected_final_wealth_cents"] == int(inst["capital_cents"]),
        "doubling with a fair coin: the expected final wealth follows from the martingale property of the wealth "
        "and the boundedness of the strategy. Revisit Proposition 10.7 in Lesson 10.",
    )


@pytest.mark.parametrize("inst", SEEDED_INSTANCES)
def test_control_expected_wealth_rounded_half_up(inst: dict[str, Any]) -> None:
    ctl = control(inst)
    capital = int(inst["capital_cents"])
    base = int(inst["base_stake_cents"])
    exact = enum_doubling(capital, base, CONTROL_WIN)
    out = must_accept(lambda: sol.doubling_outcome(ctl), "doubling, control coin")
    expect(
        out["expected_final_wealth_cents"] == nearest_cent(exact["expected"]),
        "doubling: the expected final wealth must be the exact value rounded once, half up, to the nearest "
        "cent. Do not "
        "round the probabilities, and do not round before the expectation is complete.",
    )
    expect(
        out["win_probability"] == exact["win"] and out["ruin_probability"] == exact["ruin"],
        "doubling, control coin: the probabilities must come from the instance's win probability",
    )


@pytest.mark.parametrize("inst", SEEDED_INSTANCES)
def test_no_bet_exceeds_the_capital_and_wealth_stays_nonnegative(inst: dict[str, Any]) -> None:
    for candidate in (inst, control(inst)):
        out = sol.doubling_outcome(candidate)
        expect(
            out["max_stake_cents"] <= int(candidate["capital_cents"]),
            "doubling: no bet may exceed the wealth on hand, so no stake may exceed the capital",
        )
        expect(
            out["wealth_on_ruin_cents"] >= 0,
            "doubling: the wealth after ruin must not be negative. A bet larger than the wealth on hand is not placed.",
        )


def test_capital_zero_raises_value_error() -> None:
    must_raise(lambda: sol.doubling_outcome(with_(INST, capital_cents=0, base_stake_cents=1)), "a capital of zero")


def test_capital_negative_raises_value_error() -> None:
    must_raise(lambda: sol.doubling_outcome(with_(INST, capital_cents=-5, base_stake_cents=1)), "a negative capital")


def test_capital_one_cent_is_accepted() -> None:
    inst = with_(INST, capital_cents=1, base_stake_cents=1)
    out = must_accept(lambda: sol.doubling_outcome(inst), "a capital of 1 cent")
    expect(
        out["bets_allowed"] == enum_doubling(1, 1, HALF)["bets"],
        "doubling with capital 1 cent: the number of bets allowed must match the exact enumeration",
    )


def test_stake_larger_than_capital_raises_value_error() -> None:
    must_raise(
        lambda: sol.doubling_outcome(with_(INST, capital_cents=10, base_stake_cents=11)),
        "a stake larger than the capital",
    )


def test_capital_equal_to_first_stake_is_accepted() -> None:
    out = must_accept(
        lambda: sol.doubling_outcome(with_(INST, capital_cents=7, base_stake_cents=7)),
        "a capital equal to the first stake",
    )
    expect(
        out["bets_allowed"] == 1 and out["ruin_probability"] == HALF,
        "with capital equal to the first stake, check how many bets fit the wealth on hand and the ruin probability "
        "after them",
    )


def test_expectation_below_half_cent_rounds_down() -> None:
    # Capital 1 cent, base 1 cent, win probability 1/5: the expectation is exactly 2/5 cent, which half up gives 0.
    out = sol.doubling_outcome({**INST, "capital_cents": 1, "base_stake_cents": 1, "win_probability": Fraction(1, 5)})
    expect(
        out["expected_final_wealth_cents"] == 0,
        "doubling: an expectation below half a cent must round down under the half-up rule, not up",
    )


def test_half_cent_expectation_rounds_up() -> None:
    # Capital 1 cent, base 1 cent, win probability 1/4: one bet, win 2 cents with probability 1/4, ruin 0 cents with
    # probability 3/4, so the expectation is exactly 1/2 cent, and half up gives 1 cent.
    out = sol.doubling_outcome({**INST, "capital_cents": 1, "base_stake_cents": 1, "win_probability": Fraction(1, 4)})
    expect(
        out["expected_final_wealth_cents"] == 1,
        "doubling: an expectation of exactly one half cent must follow the half-up rule, not the floor",
    )


# ---------------------------------------------------------------------------------------------------------------------
# Dyadic martingale: M_n = E[Y | F_n] for Y(x) = x on [0, 1], with M_n the midpoint of each level-n dyadic cell.


@pytest.mark.parametrize("n", list(range(0, 11)))
def test_dyadic_mean_square_error_closed_form(n: int) -> None:
    value = sol.dyadic_martingale_error(INST, n)
    expect(
        value == Fraction(1, 12 * 4**n),
        "dyadic martingale: E[(M_n - Y)^2] must follow the closed form of Proposition 12.8 of Lesson 12, exactly. "
        "Revisit the cell integral.",
    )


def test_dyadic_error_at_the_instance_level() -> None:
    n = int(INST["dyadic_level"])
    expect(
        sol.dyadic_martingale_error(INST, n) == Fraction(1, 12 * 4**n),
        "dyadic martingale: the error at the instance's level must follow the closed form exactly",
    )


def test_dyadic_value_at_zero_uses_the_first_cell() -> None:
    expect(
        sol.dyadic_martingale_value(INST, 1, Fraction(0)) == Fraction(1, 4),
        "x = 0 lies in the first cell, so the level-1 value is that cell's midpoint",
    )


def test_dyadic_value_just_below_a_cell_edge_stays_in_the_cell() -> None:
    expect(
        sol.dyadic_martingale_value(INST, 1, Fraction(1, 2) - Fraction(1, 1000)) == Fraction(1, 4),
        "a point just below a cell edge lies in the cell on its left, so the value is that cell's midpoint",
    )


def test_dyadic_value_is_the_cell_midpoint() -> None:
    expect(
        sol.dyadic_martingale_value(INST, 1, Fraction(1, 10)) == Fraction(1, 4),
        "the level-1 value at a point of the first cell must be that cell's midpoint",
    )
    expect(
        sol.dyadic_martingale_value(INST, 1, Fraction(1, 2)) == Fraction(3, 4),
        "a cell contains its left edge, so the value at an edge is the midpoint of the cell that starts there",
    )
    expect(sol.dyadic_martingale_value(INST, 1, Fraction(1)) == Fraction(3, 4), "x = 1 lies in the last cell")
    expect(
        sol.dyadic_martingale_value(INST, 2, Fraction(3, 10)) == Fraction(3, 8),
        "the level-2 value must be the midpoint of the level-2 cell that contains x",
    )


@pytest.mark.parametrize("n", list(range(0, 11)))
def test_dyadic_values_converge_pointwise(n: int) -> None:
    for j in range(0, 65):
        x = Fraction(j, 64)
        value = sol.dyadic_martingale_value(INST, n, x)
        expect(
            abs(value - x) <= Fraction(1, 2 ** (n + 1)),
            "dyadic martingale: on each grid point the value must lie within half a cell of x, so the path values "
            "approach Y as the level grows. Check the cell that contains x.",
        )


def test_dyadic_path_value_at_a_third() -> None:
    x = Fraction(1, 3)
    for n in range(0, 11):
        value = sol.dyadic_martingale_value(INST, n, x)
        expect(
            abs(value - x) <= Fraction(1, 2 ** (n + 1)),
            "dyadic martingale: the value at a fixed point must approach Y(x) = x at the rate of the cell width",
        )


def test_dyadic_level_zero_is_the_mean() -> None:
    expect(
        sol.dyadic_martingale_value(INST, 0, Fraction(9, 10)) == HALF,
        "dyadic martingale: at level 0 the value must be the mean of Y over [0, 1], at every point",
    )


# ---------------------------------------------------------------------------------------------------------------------
# Edge cases that combine the parts.


def test_horizon_one_stopping_and_doob_agree_with_enumeration() -> None:
    inst = with_(INST, horizon=1, stop_cap=1, stop_level=2)
    expect(
        sol.stopped_value_expectation(inst) == enum_stopped(inst),
        "horizon 1: the stopped value must match the enumeration",
    )
    prob, bound = sol.doob_max_probability(inst, 1)
    expect(prob == enum_doob(inst, 1)[0] and bound == enum_doob(inst, 1)[1], "horizon 1: Doob's values must match")


def test_horizon_drives_the_enumeration_length() -> None:
    inst = with_(INST, horizon=10)
    prob, _ = sol.doob_max_probability(inst, 10)
    expect(
        prob == Fraction(2, 2**10),
        "horizon 10 at level 10: count the paths that reach the level and check the probability",
    )


# ---------------------------------------------------------------------------------------------------------------------
# Boundary classes. Each test names one condition from the specification and fails only for that condition.


@pytest.mark.parametrize("win", [HALF, CONTROL_WIN, Fraction(2, 3)])
def test_stopping_cap_of_one_step_matches_enumeration(win: Fraction) -> None:
    inst = with_(INST, stop_cap=1, win_probability=win)
    value = must_accept(lambda: sol.stopped_value_expectation(inst), "a stopping cap of one step")
    expect(
        value == enum_stopped(inst),
        "a stopping rule with cap 1 stops after its first step, at the first time the level is reached or at time 1.",
    )


@pytest.mark.parametrize("win", [CONTROL_WIN, Fraction(2, 3)])
def test_cap_equal_to_horizon_matches_enumeration_for_biased_walk(win: Fraction) -> None:
    inst = with_(INST, stop_cap=INST["horizon"], win_probability=win)
    value = must_accept(lambda: sol.stopped_value_expectation(inst), "a stopping rule bounded by N, biased walk")
    expect(value == enum_stopped(inst), "a stopping time equal to the horizon N must be handled exactly")


@pytest.mark.parametrize("win", [CONTROL_WIN, Fraction(2, 3)])
def test_level_equal_to_start_is_first_checked_after_a_step(win: Fraction) -> None:
    inst = with_(INST, stop_level=0, win_probability=win)
    value = must_accept(lambda: sol.stopped_value_expectation(inst), "a stopping level equal to the start")
    expect(
        value == enum_stopped(inst),
        "a stopping level equal to the starting value is first checked at time 1, after the first step, not at time 0.",
    )


def test_doob_uses_the_fair_walk_whatever_the_instance_win_probability() -> None:
    biased = control(INST)
    for lam in range(1, int(INST["horizon"]) + 1):
        prob, bound = sol.doob_max_probability(biased, lam)
        exact_prob, exact_bound = enum_doob(INST, lam)
        expect(
            prob == exact_prob and bound == exact_bound,
            "Doob's inequality is stated for the fair walk X_k = |S_k|: its values must not use the instance's win "
            "probability.",
        )


def test_doob_probability_and_bound_are_exact_fractions() -> None:
    prob, bound = sol.doob_max_probability(INST, 1)
    expect(
        type(prob) is Fraction and type(bound) is Fraction,
        "Doob's inequality: the probability and the bound are both exact fractions.Fraction values",
    )


def test_stopped_expectation_is_an_exact_fraction() -> None:
    value = sol.stopped_value_expectation(INST)
    expect(type(value) is Fraction, "optional stopping: E[S_tau] is returned as an exact fractions.Fraction")


@pytest.mark.parametrize("capital", [62, 63, 64, 1, 2])
def test_max_stake_is_the_largest_stake_placed(capital: int) -> None:
    out = sol.doubling_outcome(with_(INST, capital_cents=capital, base_stake_cents=1))
    bets = enum_doubling(capital, 1, HALF)["bets"]
    expect(
        out["max_stake_cents"] == 2 ** (bets - 1),
        "doubling: max_stake_cents is the largest stake placed, which is the stake of the last bet that is placed",
    )


def test_bet_count_changes_exactly_where_the_stake_stops_fitting() -> None:
    for capital in range(1, 41):
        out = sol.doubling_outcome(with_(INST, capital_cents=capital, base_stake_cents=1))
        expect(
            out["bets_allowed"] == enum_doubling(capital, 1, HALF)["bets"],
            "doubling: the number of bets placed changes only when the next stake stops fitting the wealth on hand. "
            "Check the condition that a stake must not exceed the wealth on hand.",
        )


@pytest.mark.parametrize("win", [CONTROL_WIN, HALF, Fraction(2, 3)])
def test_doubling_every_small_capital_and_base_matches_enumeration(win: Fraction) -> None:
    for base in (1, 2, 3):
        for capital in range(base, 41):
            inst = with_(INST, capital_cents=capital, base_stake_cents=base, win_probability=win)
            out = sol.doubling_outcome(inst)
            exact = enum_doubling(capital, base, win)
            expect(
                out["bets_allowed"] == exact["bets"]
                and out["win_probability"] == exact["win"]
                and out["ruin_probability"] == exact["ruin"]
                and exact["wealth_on_win"] == {out["wealth_on_win_cents"]}
                and exact["wealth_on_ruin"] == {out["wealth_on_ruin_cents"]}
                and out["max_stake_cents"] == base * 2 ** (exact["bets"] - 1)
                and out["expected_final_wealth_cents"] == nearest_cent(exact["expected"]),
                "doubling: for a small capital and base, the bets, probabilities, wealths, largest stake and rounded "
                "expectation must all match the exact enumeration",
            )


def test_base_one_cent_below_the_capital_is_accepted() -> None:
    inst = with_(INST, capital_cents=10, base_stake_cents=9)
    out = must_accept(lambda: sol.doubling_outcome(inst), "a base stake one cent below the capital")
    expect(
        out["bets_allowed"] == enum_doubling(10, 9, HALF)["bets"],
        "doubling with base 9 and capital 10: the number of bets allowed must match the exact enumeration",
    )


def test_base_one_cent_above_the_capital_raises_value_error() -> None:
    must_raise(
        lambda: sol.doubling_outcome(with_(INST, capital_cents=1, base_stake_cents=2)),
        "a base stake one cent above a positive capital",
    )


@pytest.mark.parametrize("capital", [0, -1])
def test_capital_of_zero_or_less_raises_whatever_the_base(capital: int) -> None:
    must_raise(
        lambda: sol.doubling_outcome(with_(INST, capital_cents=capital, base_stake_cents=capital)),
        "a capital of zero or less, with a base stake equal to it",
    )


def test_expectation_exactly_half_a_cent_above_a_cent_rounds_up_not_to_even() -> None:
    # Capital 2 cents, base 1 cent, win probability 3/4: one placed bet. A win leaves 3 cents with probability 3/4 and
    # a loss leaves 1 cent with probability 1/4, so E = 5/2 cents. Half up gives 3 cents; rounding half to even gives 2.
    out = sol.doubling_outcome({**INST, "capital_cents": 2, "base_stake_cents": 1, "win_probability": Fraction(3, 4)})
    expect(
        out["expected_final_wealth_cents"] == 3,
        "doubling: an expectation of exactly 5/2 cents must round half up, not to the even neighbour",
    )


def test_expectation_is_rounded_once_not_after_the_probability() -> None:
    # Capital 1 cent, base 1 cent: E = 2p cents. For p = 1/4 - 1/10**7 the exact value is 0.4999998 cents, which half
    # up gives as 0 cents. Rounding p to six decimals first gives 0.25 and then 0.5 cents, which gives 1 cent.
    p = Fraction(1, 4) - Fraction(1, 10**7)
    out = sol.doubling_outcome({**INST, "capital_cents": 1, "base_stake_cents": 1, "win_probability": p})
    expect(
        out["expected_final_wealth_cents"] == 0,
        "doubling: the expectation is rounded once, half up, from the exact value, "
        "not after the probability is rounded",
    )


def test_expectation_is_rounded_from_the_exact_value_not_a_float() -> None:
    # Capital 1 cent, base 1 cent: E = 2p cents. For p = 1/4 - 1/2**60 the exact value is 1/2 - 2**-59 cents, which
    # half up gives as 0 cents. Converting to a float first rounds the value to exactly 1/2, which gives 1 cent.
    p = Fraction(1, 4) - Fraction(1, 2**60)
    out = sol.doubling_outcome({**INST, "capital_cents": 1, "base_stake_cents": 1, "win_probability": p})
    expect(
        out["expected_final_wealth_cents"] == 0,
        "doubling: the expectation is computed from the exact value and rounded once, half up, so a float must not be "
        "used on the way",
    )


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6])
def test_dyadic_value_at_each_cell_left_edge_takes_the_cell_to_the_right(n: int) -> None:
    cells = 2**n
    for j in range(cells):
        expect(
            sol.dyadic_martingale_value(INST, n, Fraction(j, cells)) == Fraction(2 * j + 1, 2 * cells),
            "dyadic martingale: cells are half-open, so a point on the left edge of a cell belongs to that cell, and "
            "its value is that cell's midpoint",
        )


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6])
def test_dyadic_value_just_below_each_cell_edge_stays_in_the_cell_on_the_left(n: int) -> None:
    cells = 2**n
    for j in range(1, cells):
        x = Fraction(j, cells) - Fraction(1, 10**6)
        expect(
            sol.dyadic_martingale_value(INST, n, x) == Fraction(2 * (j - 1) + 1, 2 * cells),
            "dyadic martingale: a point just below a cell edge lies in the cell on its left, so the value is that "
            "cell's midpoint",
        )


@pytest.mark.parametrize("n", [1, 10])
def test_dyadic_value_at_one_is_in_the_closed_last_cell(n: int) -> None:
    cells = 2**n
    expect(
        sol.dyadic_martingale_value(INST, n, Fraction(1)) == Fraction(2 * cells - 1, 2 * cells),
        "dyadic martingale: the last cell is closed at 1, so x = 1 takes that cell's midpoint",
    )


def test_no_function_prints_or_warns(capsys: pytest.CaptureFixture[str]) -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        sol.stopped_value_expectation(INST)
        sol.doob_max_probability(INST, 1)
        sol.doubling_outcome(INST)
        sol.dyadic_martingale_error(INST, 2)
        sol.dyadic_martingale_value(INST, 2, Fraction(1, 3))
    captured = capsys.readouterr()
    expect(captured.out == "" and captured.err == "", "no function may print: the engine returns values only")
    expect(not caught, "no function may warn: the engine must run without a warning")


def test_money_fields_are_integers_of_cents() -> None:
    for candidate in (INST, control(INST)):
        out = sol.doubling_outcome(candidate)
        for key in ("wealth_on_win_cents", "wealth_on_ruin_cents", "max_stake_cents", "expected_final_wealth_cents"):
            expect(
                type(out[key]) is int,
                "every money amount is an integer number of cents: the doubling outcome must return int values for its "
                "cent fields",
            )

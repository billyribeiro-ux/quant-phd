"""Acceptance suite for the E1 project: the trade-fee market engine (market_structure.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your market_structure.py next to this file. Warnings are failures, as in the browser.

Every expected value is computed here from the inputs a, b and c by a separate route: the volume and fee come from the
closed forms of the specification, and the surpluses come from the integral of the inverse demand, evaluated exactly by
the trapezoid rule, which is exact for a linear function. The oracle does not call the reference. A failure names the
property it checks and the idea to revisit; it never prints the expected value.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import math
import os
import sys
import warnings
from collections.abc import Callable
from fractions import Fraction
from typing import Any

import market_structure as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
CASE: dict[str, int] = make_instance(SEED)
A: int = CASE["a"]
B: int = CASE["b"]
C: int = CASE["c"]
STRUCTURES: tuple[str, ...] = ("monopoly", "cournot", "bertrand")
KEYS: tuple[str, ...] = (
    "volume_trades",
    "fee_cents",
    "profit_cents",
    "consumer_surplus_cents",
    "welfare_cents",
    "deadweight_loss_cents",
)


def check(condition: bool, message: str) -> None:
    """Fail with message unless condition holds. The message names the property; it never shows a value."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(message)


def half_up(x: Fraction) -> int:
    """The nearest whole number to a non-negative exact value, a tie going up: the rounding rule of the page."""
    return math.floor(x + Fraction(1, 2))


def gross_value(x: Fraction, a: int, b: int) -> Fraction:
    """The integral of the inverse demand (a - t) / b from 0 to x, by the trapezoid rule: exact for a line."""
    return x * (Fraction(a, b) + (a - x) / b) / 2


def exact(structure: str, a: int, b: int, c: int) -> dict[str, Fraction]:
    """Every output of the specification as an exact value, before rounding."""
    gap = Fraction(a - b * c)
    volume = {"monopoly": gap / 2, "cournot": 2 * gap / 3, "bertrand": gap}[structure]
    fee = (a - volume) / b  # the inverse demand at the volume; it equals c for Bertrand
    gross = gross_value(volume, a, b)
    consumer = gross - fee * volume
    profit = (fee - c) * volume
    welfare = gross - c * volume
    deadweight = (gross_value(gap, a, b) - c * gap) - welfare
    return {
        "volume_trades": volume,
        "fee_cents": fee,
        "profit_cents": profit,
        "consumer_surplus_cents": consumer,
        "welfare_cents": welfare,
        "deadweight_loss_cents": deadweight,
    }


def expected(structure: str, a: int, b: int, c: int) -> dict[str, int]:
    """Every output of the specification, rounded once by the rule of the page."""
    return {key: half_up(value) for key, value in exact(structure, a, b, c).items()}


def must_raise(call: Callable[[], object], condition: str, phrases: tuple[str, ...]) -> None:
    """Fail unless call() raises ValueError whose message contains every phrase: the specification names the type."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError as error:
        text = str(error)
        missing = [p for p in phrases if p not in text]
        check(not missing, f"the ValueError for {condition} must state the condition it checks, as the page names it")
        return
    pytest.fail(f"{condition} must raise ValueError, as the specification requires")


def test_instance_is_a_valid_case() -> None:
    check(set(CASE) == {"a", "b", "c"}, "make_instance must return the three inputs a, b and c")
    check(all(type(v) is int for v in CASE.values()), "make_instance must return whole numbers")
    check(A > B * C > 0, "the instance must satisfy a > b*c > 0")


def test_outcome_has_exactly_the_six_keys() -> None:
    for structure in STRUCTURES:
        result = sol.outcome(structure, A, B, C)
        check(set(result) == set(KEYS), f"outcome for {structure} must return exactly the six keys of the page")


@pytest.mark.parametrize("structure", STRUCTURES)
def test_every_output_is_an_int(structure: str) -> None:
    result: dict[str, Any] = sol.outcome(structure, A, B, C)
    check(all(type(v) is int for v in result.values()), f"every output for {structure} must be an int, not a float")


@pytest.mark.parametrize("structure", STRUCTURES)
@pytest.mark.parametrize("key", KEYS)
def test_closed_form_matches(structure: str, key: str) -> None:
    result = sol.outcome(structure, A, B, C)
    check(
        result[key] == expected(structure, A, B, C)[key],
        f"{key} for {structure} differs from the closed form after the stated rounding; revisit the first-order "
        "condition of the exchange and the rounding rule",
    )


def test_volume_ordering() -> None:
    mono = sol.outcome("monopoly", A, B, C)["volume_trades"]
    cournot = sol.outcome("cournot", A, B, C)["volume_trades"]
    bertrand = sol.outcome("bertrand", A, B, C)["volume_trades"]
    check(mono < cournot < bertrand, "trade volume must rise from monopoly to Cournot to Bertrand")


def test_fee_ordering() -> None:
    mono = sol.outcome("monopoly", A, B, C)["fee_cents"]
    cournot = sol.outcome("cournot", A, B, C)["fee_cents"]
    check(mono > cournot, "the monopoly fee must exceed the Cournot fee")


def test_bertrand_fee_is_marginal_cost() -> None:
    check(sol.outcome("bertrand", A, B, C)["fee_cents"] == C, "the Bertrand fee must equal the cost of one trade")


def test_bertrand_has_no_deadweight_loss() -> None:
    check(
        sol.outcome("bertrand", A, B, C)["deadweight_loss_cents"] == 0,
        "Bertrand trade volume is the competitive volume, so its deadweight loss must be zero",
    )


def test_bertrand_profit_is_zero() -> None:
    check(sol.outcome("bertrand", A, B, C)["profit_cents"] == 0, "two Bertrand exchanges must earn zero profit")


def test_cournot_fee_above_bertrand_fee() -> None:
    cournot = sol.outcome("cournot", A, B, C)["fee_cents"]
    check(cournot > C, "the Cournot fee must exceed the cost of one trade, because the Bertrand fee is that cost")


def test_welfare_ordering() -> None:
    mono = sol.outcome("monopoly", A, B, C)["welfare_cents"]
    cournot = sol.outcome("cournot", A, B, C)["welfare_cents"]
    bertrand = sol.outcome("bertrand", A, B, C)["welfare_cents"]
    check(mono < cournot < bertrand, "welfare must rise from monopoly to Cournot to Bertrand")


def test_deadweight_loss_ordering() -> None:
    mono = sol.outcome("monopoly", A, B, C)["deadweight_loss_cents"]
    cournot = sol.outcome("cournot", A, B, C)["deadweight_loss_cents"]
    bertrand = sol.outcome("bertrand", A, B, C)["deadweight_loss_cents"]
    check(mono > cournot > bertrand, "deadweight loss must fall from monopoly to Cournot to the zero of Bertrand")


def test_monopoly_profit_exceeds_cournot_total() -> None:
    mono = sol.outcome("monopoly", A, B, C)["profit_cents"]
    cournot = sol.outcome("cournot", A, B, C)["profit_cents"]
    check(mono > cournot, "the monopoly profit must exceed the total profit of the two Cournot exchanges")


@pytest.mark.parametrize("structure", STRUCTURES)
def test_welfare_is_consumer_surplus_plus_profit(structure: str) -> None:
    values = exact(structure, A, B, C)
    result = sol.outcome(structure, A, B, C)
    total = values["consumer_surplus_cents"] + values["profit_cents"]
    check(
        result["welfare_cents"] == half_up(total),
        f"welfare for {structure} must be consumer surplus plus exchange profit, rounded once from the exact sum",
    )


TIE_CASES: tuple[tuple[str, str, int, int, int], ...] = (
    ("monopoly", "volume_trades", 8, 1, 1),
    ("monopoly", "fee_cents", 8, 1, 1),
    ("monopoly", "profit_cents", 16, 2, 1),
    ("monopoly", "consumer_surplus_cents", 11, 1, 1),
    ("monopoly", "welfare_cents", 11, 1, 1),
    ("monopoly", "deadweight_loss_cents", 11, 1, 1),
    ("cournot", "fee_cents", 17, 2, 1),
    ("cournot", "profit_cents", 31, 4, 1),
    ("cournot", "consumer_surplus_cents", 31, 4, 1),
    ("cournot", "deadweight_loss_cents", 10, 1, 1),
    ("bertrand", "consumer_surplus_cents", 8, 1, 1),
    ("bertrand", "welfare_cents", 8, 1, 1),
)


@pytest.mark.parametrize("structure, key, a, b, c", TIE_CASES)
def test_tie_rounds_up_for_each_output(structure: str, key: str, a: int, b: int, c: int) -> None:
    exact_value = exact(structure, a, b, c)[key]
    assert exact_value.denominator == 2, "the case must make this output an exact half cent or trade"
    result = sol.outcome(structure, a, b, c)
    check(
        result[key] == expected(structure, a, b, c)[key],
        f"{key} for {structure} is an exact half, which must round up; the rounding rule is the one of the page",
    )


@pytest.mark.parametrize("structure", STRUCTURES)
@pytest.mark.parametrize("key", KEYS)
def test_reference_case_matches_closed_forms(structure: str, key: str) -> None:
    result = sol.outcome(structure, 120, 1, 20)
    check(
        result[key] == expected(structure, 120, 1, 20)[key],
        f"{key} for {structure} in the reference case differs from the closed form after the stated rounding",
    )


def test_outcome_warns_nothing() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for structure in STRUCTURES:
            sol.outcome(structure, A, B, C)
    check(not caught, "outcome must not warn")


def test_tie_rounds_up_for_fee_and_volume() -> None:
    # a = 121, b = 1, c = 20: the monopoly fee is 141/2 and the volume is 101/2 (exact halves).
    result = sol.outcome("monopoly", 121, 1, 20)
    want = expected("monopoly", 121, 1, 20)
    check(result["fee_cents"] == want["fee_cents"], "a fee that is an exact half cent must round up")
    check(result["volume_trades"] == want["volume_trades"], "a volume that is an exact half trade must round up")


UNKNOWN_STRUCTURES: tuple[Any, ...] = (
    "duopoly",
    "",
    "Monopoly",
    "Cournot",
    "Bertrand",
    "perfect",
    " monopoly",
    "cournot ",
    "bertrand ",
    b"monopoly",
    None,
    1,
)


@pytest.mark.parametrize("name", UNKNOWN_STRUCTURES)
def test_unknown_structure_raises_value_error(name: Any) -> None:
    must_raise(
        lambda: sol.outcome(name, A, B, C),
        "a structure that is not one of the three names",
        STRUCTURES,
    )


@pytest.mark.parametrize("structure", STRUCTURES)
@pytest.mark.parametrize("a, b, c", [(20, 2, 10), (19, 2, 10), (-3, 1, 1)])
def test_a_not_above_b_times_c_raises_value_error(structure: str, a: int, b: int, c: int) -> None:
    must_raise(lambda: sol.outcome(structure, a, b, c), "a <= b*c", ("a must exceed b*c",))


@pytest.mark.parametrize("structure", STRUCTURES)
@pytest.mark.parametrize("a, b, c", [(10, 0, 5), (10, -1, 5)])
def test_b_not_positive_raises_value_error(structure: str, a: int, b: int, c: int) -> None:
    must_raise(lambda: sol.outcome(structure, a, b, c), "b <= 0", ("b must be positive",))


@pytest.mark.parametrize("structure", STRUCTURES)
@pytest.mark.parametrize("a, b, c", [(10, 2, 0), (10, 2, -1)])
def test_c_not_positive_raises_value_error(structure: str, a: int, b: int, c: int) -> None:
    must_raise(lambda: sol.outcome(structure, a, b, c), "c <= 0", ("c must be positive",))


@pytest.mark.parametrize("structure", STRUCTURES)
@pytest.mark.parametrize("a, b, c", [(B * C + 1, B, C), (2, 1, 1)])
def test_smallest_valid_case_is_accepted(structure: str, a: int, b: int, c: int) -> None:
    result = sol.outcome(structure, a, b, c)
    check(
        result == expected(structure, a, b, c),
        f"the valid case a = b*c + 1 for {structure} must match the closed forms",
    )


@pytest.mark.parametrize("structure", STRUCTURES)
def test_unit_cost_is_accepted(structure: str) -> None:
    # c = 1 is the smallest positive cost. a = 10 > b*c = 5 and b = 5 > 0, so only the c check is at its edge.
    check(
        sol.outcome(structure, 10, 5, 1) == expected(structure, 10, 5, 1),
        f"c = 1 is positive and must be accepted for {structure}; the closed forms apply",
    )


@pytest.mark.parametrize("structure", STRUCTURES)
def test_smallest_positive_b_is_accepted(structure: str) -> None:
    # b = 1 is the smallest positive b. a = 100 > b*c = 50 and c = 50 > 0, so only the b check is at its edge.
    check(
        sol.outcome(structure, 100, 1, 50) == expected(structure, 100, 1, 50),
        f"b = 1 is positive and must be accepted for {structure}; the closed forms apply",
    )


@pytest.mark.parametrize("structure", STRUCTURES)
def test_large_exact_inputs_round_from_exact_values(structure: str) -> None:
    # a = 15000000000000002 makes the Cournot volume 10^16 + 2/3, which rounds to 10^16 + 1. A float computation loses
    # the fraction at this size, so every output must come from the exact value.
    a, b, c = 15000000000000002, 1, 1
    check(
        sol.outcome(structure, a, b, c) == expected(structure, a, b, c),
        f"large exact inputs for {structure} must round from the exact fractions, not from floating-point values",
    )


def test_value_below_a_half_rounds_down() -> None:
    # Reference case: the Cournot welfare is 40000/9 cents, 4444 and 4/9, so its fraction is below one half.
    exact_value = exact("cournot", 120, 1, 20)["welfare_cents"]
    check(exact_value - math.floor(exact_value) < Fraction(1, 2), "the case must have a fraction below one half")
    check(
        sol.outcome("cournot", 120, 1, 20)["welfare_cents"] == math.floor(exact_value),
        "a money value whose exact fraction is below one half must round down, not up",
    )


def test_value_above_a_half_rounds_up() -> None:
    # Reference case: the Cournot deadweight loss is 5000/9 cents, 555 and 5/9, so its fraction is above one half.
    exact_value = exact("cournot", 120, 1, 20)["deadweight_loss_cents"]
    check(exact_value - math.floor(exact_value) > Fraction(1, 2), "the case must have a fraction above one half")
    check(
        sol.outcome("cournot", 120, 1, 20)["deadweight_loss_cents"] == math.floor(exact_value) + 1,
        "a money value whose exact fraction is above one half must round up",
    )


def test_module_imports_only_the_standard_library() -> None:
    tree = ast.parse(inspect.getsource(sol))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module is not None:
            roots.add(node.module.split(".")[0])
    check(
        roots <= set(sys.stdlib_module_names),
        "market_structure must import the standard library only, as the Constraints of the page state",
    )


def test_outcome_prints_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    for structure in STRUCTURES:
        sol.outcome(structure, A, B, C)
    captured = capsys.readouterr()
    check(captured.out == "" and captured.err == "", "outcome must not print anything")


def test_import_prints_nothing_and_warns_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    # The module is run again under capture, so a print or a warning left at module level is caught.
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        importlib.reload(sol)
    captured = capsys.readouterr()
    check(captured.out == "" and captured.err == "", "market_structure must print nothing when it is imported")
    check(not caught, "market_structure must warn nothing when it is imported")


def test_repeated_calls_agree() -> None:
    first = sol.outcome("cournot", A, B, C)
    sol.outcome("monopoly", A + 1, B, C)
    check(sol.outcome("cournot", A, B, C) == first, "outcome must give the same answer on every call")


@pytest.mark.parametrize("structure", STRUCTURES)
def test_second_instance_matches_closed_forms(structure: str) -> None:
    other = make_instance(SEED + 1)
    check(other["a"] > other["b"] * other["c"] > 0, "the second instance must be valid")
    result = sol.outcome(structure, other["a"], other["b"], other["c"])
    check(
        result == expected(structure, other["a"], other["b"], other["c"]),
        f"outcome for {structure} must match the closed forms on a second instance as well",
    )

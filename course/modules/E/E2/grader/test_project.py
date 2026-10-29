"""Acceptance suite for the E2 project: the sealed-bid unit auction engine (auction_sim.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your auction_sim.py next to this file. Warnings are failures, as in the browser.

Each test checks a property or a number against the rules in the project specification. Money is compared exactly:
the specification fixes integer cents and a tie going up for the symmetric bid, so a correct implementation returns the
same integers. The oracles in this file are written from the specification, not copied from any solution. A failing
test names the property it checks and the idea to revisit. It never prints the expected value.
"""

from __future__ import annotations

import os
import re
from collections.abc import Callable
from functools import partial
from typing import Any

import auction_sim as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
OTHER: dict[str, Any] = make_instance(SEED + 7_919)  # a second instance, so a fixed answer for one seed must fail here
N: int = INST["n"]
UNITS: int = INST["units"]
VALUES: list[int] = INST["values"]
BIDS: list[int] = INST["bids"]
CASES: list[tuple[list[int], list[int], int]] = [
    (INST["values"], INST["bids"], INST["units"]),
    (OTHER["values"], OTHER["bids"], OTHER["units"]),
]
SWEEP: list[int] = sorted({0, 1, 2, 3, 99, 100, 101, 5_000, 9_999, 10_000, *VALUES, *OTHER["values"]})
BAD_FORMATS: tuple[str, ...] = ("Uniform", "uniform ", "first-price", "second-price", "", "discriminatory-price")


# ---- oracles, written from the specification -------------------------------------------------------------------------


def beats(bids: list[int], j: int, i: int) -> bool:
    """True when bidder j ranks above bidder i: a higher bid, or an equal bid from a lower index."""
    return bids[j] > bids[i] or (bids[j] == bids[i] and j < i)


def oracle_winners(bids: list[int], units: int) -> set[int]:
    """The bidders beaten by fewer than `units` others: exactly the `units` highest, ties to the lower index."""
    return {i for i in range(len(bids)) if sum(beats(bids, j, i) for j in range(len(bids)) if j != i) < units}


def oracle_clearing(bids: list[int], units: int) -> int:
    """The (units+1)-th highest bid, read off the sorted bids."""
    return sorted(bids, reverse=True)[units]


def oracle_payments(fmt: str, bids: list[int], units: int) -> list[int]:
    winners = oracle_winners(bids, units)
    price = oracle_clearing(bids, units)
    return [(price if fmt == "uniform" else bids[i]) if i in winners else 0 for i in range(len(bids))]


def oracle_bid(n: int, value: int) -> int:
    """(n-1)/n times value, rounded half up to the cent: floor((n-1)*value/n + 1/2), in integers."""
    return (2 * (n - 1) * value + n) // (2 * n)


def oracle_efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]:
    won = sum(values[i] for i in oracle_winners(bids, units))
    best = sum(sorted(values, reverse=True)[:units])
    return won, best


# ---- helpers ---------------------------------------------------------------------------------------------------------


def valid(fn: Callable[..., Any], *args: Any) -> Any:
    """Call fn on a valid input. Any exception is a failure: the input obeys the specification."""
    __tracebackhide__ = True
    try:
        return fn(*args)
    except Exception as exc:
        pytest.fail(
            f"{getattr(fn, '__name__', 'the function')} raised {type(exc).__name__} on a valid input: "
            "re-read the constraints on valid inputs in the specification"
        )


def must_refuse(call: Callable[[], object], condition: str, names: str = "") -> None:
    """Fail unless call() raises ValueError, the exception the specification names for this condition.

    When `names` is given it is a regular expression that the ValueError message (lower case) must match, because
    the specification says the message must name the condition.
    """
    __tracebackhide__ = True
    try:
        call()
    except ValueError as exc:
        if names and re.search(names, str(exc).lower()) is None:
            pytest.fail(f"{condition}: the ValueError must name the condition it reports")
        return
    except Exception as exc:
        pytest.fail(f"{condition}: the specification requires a ValueError, but {type(exc).__name__} was raised")
    pytest.fail(f"{condition}: the specification requires a ValueError, and none was raised")


def is_cents(x: object) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def is_flag(x: object) -> bool:
    return isinstance(x, bool)


# ---- the instance ----------------------------------------------------------------------------------------------------


def test_instance_is_valid_and_simulated() -> None:
    for inst in (INST, OTHER):
        if inst["label"] != "SIMULATED":
            pytest.fail("the instance must be labelled SIMULATED")
        if not (2 <= inst["n"] <= 5 and 1 <= inst["units"] < inst["n"]):
            pytest.fail("the instance must have 2 to 5 bidders and 1 <= units < n")
        if len(inst["values"]) != inst["n"] or len(inst["bids"]) != inst["n"]:
            pytest.fail("the instance must give one value and one bid per bidder")


# ---- symmetric single-unit bid ---------------------------------------------------------------------------------------


def test_first_price_symmetric_bid_is_n_minus_1_over_n_times_value() -> None:
    for n in range(2, 6):
        for value in SWEEP:
            got = valid(sol.symmetric_bid_single_unit, "discriminatory", n, value)
            if not is_cents(got) or got != oracle_bid(n, value):
                pytest.fail(
                    "first-price symmetric bid: (n-1)/n times the value, rounded half up to the cent, for every "
                    "n from 2 to 5; revisit the first-order condition of the single-unit bidder"
                )


def test_symmetric_bid_rounds_an_exact_half_cent_up() -> None:
    # Hand derivations, each exact: (2-1)/2 * 1 = 0.5, (2-1)/2 * 3 = 1.5, (2-1)/2 * 5 = 2.5, (4-1)/4 * 2 = 1.5.
    # A tie goes up, so the bids are 1, 2, 3 and 2.
    table = [(2, 1, 1), (2, 3, 2), (2, 5, 3), (4, 2, 2)]
    for n, value, expected in table:
        if valid(sol.symmetric_bid_single_unit, "discriminatory", n, value) != expected:
            pytest.fail(
                "a bid that is exactly half a cent is rounded up; revisit the rounding rule in the specification"
            )


def test_first_price_bid_is_below_value_for_every_bidder_count() -> None:
    for n in range(2, 6):
        for value in SWEEP:
            bid = valid(sol.symmetric_bid_single_unit, "discriminatory", n, value)
            if bid > value:
                pytest.fail("a first-price bid must not exceed the bidder's value; revisit bid shading")
            if value >= 100 and bid >= value:
                pytest.fail(
                    "with n >= 2 and a value of at least 100 cents, the first-price bid is strictly below value"
                )


def test_uniform_symmetric_bid_is_the_value() -> None:
    for n in range(2, 6):
        for value in SWEEP:
            got = valid(sol.symmetric_bid_single_unit, "uniform", n, value)
            if not is_cents(got) or got != value:
                pytest.fail(
                    "under the uniform rule with one unit the price is the second bid, so the symmetric bid is the "
                    "value itself; revisit why truthful bidding is weakly dominant"
                )


def test_symmetric_bid_zero_value_is_zero() -> None:
    for fmt in ("uniform", "discriminatory"):
        if valid(sol.symmetric_bid_single_unit, fmt, 2, 0) != 0:
            pytest.fail("a bidder whose value is zero bids nothing above zero under either rule")


def test_symmetric_bid_refuses_n_below_two() -> None:
    for n in (1, 0, -3):
        must_refuse(
            partial(sol.symmetric_bid_single_unit, "discriminatory", n, 100),
            "n below two in the symmetric bid",
            names=r"\bn\b",
        )


def test_symmetric_bid_refuses_n_below_two_under_uniform_too() -> None:
    for n in (1, 0):
        must_refuse(
            partial(sol.symmetric_bid_single_unit, "uniform", n, 100),
            "n below two in the symmetric bid under the uniform format",
            names=r"\bn\b",
        )


def test_symmetric_bid_accepts_n_equal_to_two() -> None:
    for fmt in ("uniform", "discriminatory"):
        if not is_cents(valid(sol.symmetric_bid_single_unit, fmt, 2, 100)):
            pytest.fail("with n = 2 (the smallest allowed bidder count) the bid must be an integer number of cents")


def test_symmetric_bid_refuses_negative_value() -> None:
    for fmt in ("uniform", "discriminatory"):
        must_refuse(
            partial(sol.symmetric_bid_single_unit, fmt, 3, -1),
            "a negative value in the symmetric bid",
            names=r"bid|value",
        )


def test_symmetric_bid_accepts_zero_value() -> None:
    for fmt in ("uniform", "discriminatory"):
        if not is_cents(valid(sol.symmetric_bid_single_unit, fmt, 3, 0)):
            pytest.fail("a value of zero cents is a valid input, and its bid must be an integer cent amount")


# ---- format ----------------------------------------------------------------------------------------------------------


def test_unknown_format_name_is_refused_by_every_format_function() -> None:
    for bad in BAD_FORMATS:
        must_refuse(
            partial(sol.payments, bad, BIDS, UNITS), f"format {bad!r} in payments", names=r"uniform.*discriminatory"
        )
        must_refuse(
            partial(sol.revenue, bad, BIDS, UNITS), f"format {bad!r} in revenue", names=r"uniform.*discriminatory"
        )
        must_refuse(
            partial(sol.symmetric_bid_single_unit, bad, N, 100),
            f"format {bad!r} in the symmetric bid",
            names=r"uniform.*discriminatory",
        )


def test_both_format_names_are_accepted() -> None:
    for fmt in ("uniform", "discriminatory"):
        got = valid(sol.payments, fmt, BIDS, UNITS)
        if not isinstance(got, list) or len(got) != N:
            pytest.fail("payments must return one amount per bidder under each allowed format name")


# ---- units -----------------------------------------------------------------------------------------------------------


def unit_callers(units: int) -> list[Callable[[], object]]:
    """Each function that takes a unit count, with that count (instance bids, values and bidder count)."""
    return [
        partial(sol.allocate, BIDS, units),
        partial(sol.payments, "uniform", BIDS, units),
        partial(sol.revenue, "discriminatory", BIDS, units),
        partial(sol.efficiency, VALUES, BIDS, units),
    ]


def test_zero_units_is_refused() -> None:
    for call in unit_callers(0):
        must_refuse(call, "units below one", names=r"units")


def test_negative_units_is_refused() -> None:
    for call in unit_callers(-1):
        must_refuse(call, "a negative unit count", names=r"units")


def test_units_equal_to_bidder_count_is_refused() -> None:
    for call in unit_callers(N):
        must_refuse(call, "units equal to the bidder count", names=r"units")


def test_units_above_bidder_count_is_refused() -> None:
    for call in unit_callers(N + 1):
        must_refuse(call, "units above the bidder count", names=r"units")


def test_one_unit_is_accepted() -> None:
    for call in unit_callers(1):
        valid(call)


def test_units_one_below_bidder_count_is_accepted() -> None:
    for call in unit_callers(N - 1):
        valid(call)


# ---- negative and zero money -----------------------------------------------------------------------------------------


def test_negative_bid_is_refused() -> None:
    bad = [-1, *BIDS[1:]]
    must_refuse(partial(sol.allocate, bad, UNITS), "a negative bid in allocate", names=r"bid")
    must_refuse(partial(sol.payments, "uniform", bad, UNITS), "a negative bid in payments", names=r"bid")
    must_refuse(partial(sol.revenue, "discriminatory", bad, UNITS), "a negative bid in revenue", names=r"bid")
    must_refuse(partial(sol.efficiency, VALUES, bad, UNITS), "a negative bid in efficiency", names=r"bid")


def test_negative_bid_in_last_position_is_refused() -> None:
    bad = [*BIDS[:-1], -1]
    must_refuse(partial(sol.allocate, bad, UNITS), "a negative last bid in allocate", names=r"bid")
    must_refuse(partial(sol.payments, "discriminatory", bad, UNITS), "a negative last bid in payments", names=r"bid")
    must_refuse(partial(sol.revenue, "uniform", bad, UNITS), "a negative last bid in revenue", names=r"bid")
    must_refuse(partial(sol.efficiency, VALUES, bad, UNITS), "a negative last bid in efficiency", names=r"bid")


def test_zero_bid_is_accepted() -> None:
    zeros = [0] * N
    if valid(sol.allocate, zeros, UNITS) != [True] * UNITS + [False] * (N - UNITS):
        pytest.fail("a zero bid is valid and ranks like any other bid; a tie at zero goes to the lower index")
    if valid(sol.payments, "uniform", zeros, UNITS) != [0] * N:
        pytest.fail("with every bid at zero, the uniform payments are all set by the clearing bid")
    if valid(sol.revenue, "discriminatory", zeros, UNITS) != 0:
        pytest.fail("with every bid at zero, the winners pay their own bids, so revenue is the sum of the winning bids")
    valid(sol.efficiency, VALUES, zeros, UNITS)


def test_negative_value_is_refused_in_efficiency() -> None:
    bad = [-1, *VALUES[1:]]
    must_refuse(partial(sol.efficiency, bad, BIDS, UNITS), "a negative value in efficiency", names=r"value")


def test_negative_value_in_last_position_is_refused_in_efficiency() -> None:
    bad = [*VALUES[:-1], -1]
    must_refuse(partial(sol.efficiency, bad, BIDS, UNITS), "a negative last value in efficiency", names=r"value")


def test_zero_value_is_accepted_in_efficiency() -> None:
    zeros = [0] * N
    if valid(sol.efficiency, zeros, BIDS, UNITS) != (0, 0):
        pytest.fail("with every value at zero cents, both entries of the efficiency pair must match")


# ---- allocation ------------------------------------------------------------------------------------------------------


def test_allocation_winners_are_the_units_highest_bids() -> None:
    for _values, bids, units in CASES:
        got = valid(sol.allocate, bids, units)
        if not isinstance(got, list) or len(got) != len(bids) or not all(is_flag(x) for x in got):
            pytest.fail("allocate must return one True or False per bidder")
        if {i for i, won in enumerate(got) if won} != oracle_winners(bids, units):
            pytest.fail("the winners are the units highest bids; revisit the ranking of bids")


def test_exactly_units_bidders_win() -> None:
    for _values, bids, units in CASES:
        if sum(valid(sol.allocate, bids, units)) != units:
            pytest.fail("exactly `units` bidders win a unit; a rule that awards more or fewer breaks the auction")


def test_ties_go_to_the_lower_index() -> None:
    cases = [
        ([5, 5, 5], 1, [True, False, False]),
        ([3, 7, 7, 1], 1, [False, True, False, False]),
        ([7, 7, 7, 2], 2, [True, True, False, False]),
        ([4, 9, 4, 4], 2, [True, True, False, False]),
    ]
    for bids, units, expected in cases:
        if valid(sol.allocate, bids, units) != expected:
            pytest.fail("a tie in bids goes to the bidder with the lower index; revisit the tie rule")


def test_two_bidder_case_by_hand() -> None:
    if valid(sol.allocate, [5, 3], 1) != [True, False]:
        pytest.fail("with two bidders and one unit, the higher bidder wins")
    if valid(sol.payments, "uniform", [5, 3], 1) != [3, 0]:
        pytest.fail("the uniform winner pays the second bid, not its own bid")
    if valid(sol.payments, "discriminatory", [5, 3], 1) != [5, 0]:
        pytest.fail("the discriminatory winner pays its own bid, not the second bid")
    if valid(sol.efficiency, [10, 4], [5, 3], 1) != (10, 10):
        pytest.fail("the higher bidder holds the higher value here, so the two efficiency entries are equal")


# ---- payments --------------------------------------------------------------------------------------------------------


def test_uniform_winners_pay_the_units_plus_one_highest_bid() -> None:
    for _values, bids, units in CASES:
        if valid(sol.payments, "uniform", bids, units) != oracle_payments("uniform", bids, units):
            pytest.fail(
                "under uniform pricing each winner pays the (units+1)-th highest bid; revisit the clearing rank"
            )
    if valid(sol.payments, "uniform", [9, 6, 4], 1) != [6, 0, 0]:
        pytest.fail("with one unit, the winner pays the second-highest bid")
    if valid(sol.payments, "uniform", [9, 6, 4], 2) != [4, 4, 0]:
        pytest.fail("with two units, both winners pay the third-highest bid")


def test_discriminatory_winners_pay_their_own_bid() -> None:
    for _values, bids, units in CASES:
        if valid(sol.payments, "discriminatory", bids, units) != oracle_payments("discriminatory", bids, units):
            pytest.fail("under discriminatory pricing each winner pays its own bid; revisit the payment rule")
    if valid(sol.payments, "discriminatory", [9, 6, 4], 2) != [9, 6, 0]:
        pytest.fail("with two units, each winner pays its own bid, not the losing bid")


def test_losers_pay_zero_under_both_formats() -> None:
    for _values, bids, units in CASES:
        winners = oracle_winners(bids, units)
        for fmt in ("uniform", "discriminatory"):
            got = valid(sol.payments, fmt, bids, units)
            if any(got[i] != 0 for i in range(len(bids)) if i not in winners):
                pytest.fail("a bidder who does not win a unit pays nothing; revisit which bidders are charged")


def test_tie_at_the_clearing_rank_is_priced_as_the_rank_says() -> None:
    if valid(sol.payments, "uniform", [7, 7, 3], 1) != [7, 0, 0]:
        pytest.fail("with a tie for first, the lower index wins and pays the highest losing bid, which is the tied bid")
    if valid(sol.payments, "discriminatory", [7, 7, 3], 1) != [7, 0, 0]:
        pytest.fail("with a tie for first, the lower index wins and pays its own bid under the discriminatory rule")


def test_payments_are_integer_cents() -> None:
    for _values, bids, units in CASES:
        for fmt in ("uniform", "discriminatory"):
            got = valid(sol.payments, fmt, bids, units)
            if not all(is_cents(x) for x in got):
                pytest.fail("every payment is an integer number of cents, not a float or a bool")


# ---- revenue ---------------------------------------------------------------------------------------------------------


def test_revenue_is_the_sum_of_payments() -> None:
    for _values, bids, units in CASES:
        for fmt in ("uniform", "discriminatory"):
            got = valid(sol.revenue, fmt, bids, units)
            if not is_cents(got) or got != sum(oracle_payments(fmt, bids, units)):
                pytest.fail("revenue is the total of what the winners pay, not the total of all bids")


def test_uniform_revenue_never_exceeds_the_winning_bids() -> None:
    for _values, bids, units in CASES:
        winning_total = sum(bids[i] for i in oracle_winners(bids, units))
        if valid(sol.revenue, "uniform", bids, units) > winning_total:
            pytest.fail("a uniform winner pays no more than its own bid; revenue cannot exceed the winning bids")
        if valid(sol.revenue, "discriminatory", bids, units) != winning_total:
            pytest.fail("discriminatory revenue equals the winning bids; revisit the payment rule")


# ---- efficiency ------------------------------------------------------------------------------------------------------


def test_efficiency_uses_values_of_the_winners() -> None:
    for values, bids, units in CASES:
        if valid(sol.efficiency, values, bids, units) != oracle_efficiency(values, bids, units):
            pytest.fail("efficiency is the value of the winners, read from values rather than bids; revisit the pair")
    if valid(sol.efficiency, [1, 2, 3], [3, 2, 1], 1) != (1, 3):
        pytest.fail("the winner's value is read from values, not bids; the best is the sum of the top values")


def test_truthful_bids_attain_the_best_value() -> None:
    for values, _bids, units in CASES:
        best = sum(sorted(values, reverse=True)[:units])
        if valid(sol.efficiency, values, values, units) != (best, best):
            pytest.fail("with bids equal to values, the winners hold the highest values, so both entries match")


def test_efficiency_first_entry_is_not_above_second() -> None:
    for values, bids, units in CASES:
        won, best = valid(sol.efficiency, values, bids, units)
        if won > best:
            pytest.fail("no allocation beats the k highest values; the first entry cannot exceed the second")


def test_efficiency_returns_two_integers() -> None:
    for values, bids, units in CASES:
        got = valid(sol.efficiency, values, bids, units)
        if not isinstance(got, tuple) or len(got) != 2 or not all(is_cents(x) for x in got):
            pytest.fail("efficiency returns a pair of integer cent totals")

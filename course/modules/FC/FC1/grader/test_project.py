"""Acceptance suite for the FC1 project: the cash-instrument engine (instruments.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your instruments.py next to this file. Warnings are failures, as in the browser.

Each test checks one property or one number against the conventions of the project page. Money is compared exactly:
the page fixes the rule (exact arithmetic, one rounding per output, halves away from zero), so a correct implementation
returns the same integers. Only the conditions the page names with ValueError are required to raise it; any other
invalid input may raise any exception or return. A failing test names the property it checks and the idea to revisit,
and it never prints an expected value.
"""

from __future__ import annotations

import functools
import math
import os
import warnings
from collections.abc import Callable
from fractions import Fraction
from typing import Any

import instruments as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(
    SEED + 7_919
)  # a second case, so a fixed answer for one seed must also match this one
ROUNDING_CASE: dict[str, Any] = make_instance(6)  # a fixed case where rounding each term differs from rounding the sum


def half_away(x: Fraction) -> int:
    """The test's own rule: the nearest whole cent of an exact amount, an exact half going away from zero."""
    magnitude = abs(x)
    whole = math.floor(magnitude + Fraction(1, 2))
    return whole if x >= 0 else -whole


def oracle_events(face: int, coupon_bps: int, periods: int) -> list[tuple[int, int]]:
    """Coupon in each period 1..periods (face times coupon_bps over 10000, half away), face added in the last one."""
    coupon = half_away(Fraction(face * coupon_bps, 10_000))
    rows = [(t, coupon) for t in range(1, periods + 1)]
    rows[-1] = (periods, coupon + face)
    return rows


def oracle_price(events: list[tuple[int, int]], yield_bps: int) -> int:
    """Each event discounted by (1 + y) ** -t with y = yield_bps / 10000, summed exactly, rounded once."""
    y = Fraction(yield_bps, 10_000)
    total = sum((Fraction(amount) / (1 + y) ** period for period, amount in events), Fraction(0))
    return half_away(total)


def bond_of(case: dict[str, Any]) -> Any:
    return sol.Bond(face_cents=case["face_cents"], coupon_bps=case["coupon_bps"], periods=case["periods"])


def trade_of(case: dict[str, Any]) -> Any:
    return sol.CashTrade(
        quantity=case["quantity"],
        price_cents=case["price_cents"],
        side=case["side"],
        settlement_day=case["settlement_day"],
    )


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError. Used only for the conditions the project page names with ValueError."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the page requires a ValueError for this input, and none was raised.")


def must_accept(call: Callable[[], object], condition: str) -> object:
    """Fail if call() raises. Used for the boundary values the page allows."""
    __tracebackhide__ = True
    try:
        return call()
    except NotImplementedError:
        raise
    except Exception:
        pytest.fail(f"{condition}: the page allows this input, and the call raised an exception.")


def checked_events(value: object, prop: str) -> list[tuple[int, int]]:
    """events() must be a list of (period, amount) pairs of plain ints, not floats and not bools."""
    __tracebackhide__ = True
    if not isinstance(value, list):
        pytest.fail(f"{prop}: events() must return a list of (period, amount_cents) pairs.")
    for item in value:
        if not isinstance(item, (tuple, list)) or len(item) != 2:
            pytest.fail(f"{prop}: each event must be a (period, amount_cents) pair.")
        for part in item:
            if isinstance(part, bool) or not isinstance(part, int):
                pytest.fail(f"{prop}: every period and every amount must be an int in cents, not a float or a bool.")
    return [(int(period), int(amount)) for period, amount in value]


def checked_int(value: object, prop: str) -> int:
    __tracebackhide__ = True
    if isinstance(value, bool) or not isinstance(value, int):
        pytest.fail(f"{prop}: a money output must be an int in cents, not a float or a bool.")
    return int(value)


# ---------------------------------------------------------------------------------------------------------------
# Bond: the event schedule
# ---------------------------------------------------------------------------------------------------------------


def test_bond_events_are_period_amount_pairs() -> None:
    """Bond.events() returns a list of (period, amount_cents) pairs of plain ints."""
    checked_events(bond_of(INST).events(), "Bond.events")


def test_bond_has_one_event_per_period_numbered_one_to_n() -> None:
    """Periods are whole numbers 1..periods, one event each, in order (period 0 is the trade date, not a coupon)."""
    __tracebackhide__ = True
    rows = checked_events(bond_of(INST).events(), "Bond.events")
    assert [p for p, _ in rows] == list(range(1, INST["periods"] + 1)), "periods must run 1..periods, one event each"


def test_bond_coupon_is_face_times_coupon_rate_rounded_half_away() -> None:
    """Every coupon except the last equals face * coupon_bps / 10000, rounded to the nearest cent, halves away."""
    rows = checked_events(bond_of(INST).events(), "Bond.events")
    expected = oracle_events(INST["face_cents"], INST["coupon_bps"], INST["periods"])
    for (period, amount), (_, want) in zip(rows[:-1], expected[:-1], strict=True):
        assert amount == want, f"coupon in period {period}: the coupon is face times the coupon rate, rounded once"


def test_bond_last_period_carries_the_principal() -> None:
    """The last event is the last coupon plus the face: the principal is paid in the final period, with that coupon."""
    __tracebackhide__ = True
    rows = checked_events(bond_of(INST).events(), "Bond.events")
    expected = oracle_events(INST["face_cents"], INST["coupon_bps"], INST["periods"])
    assert rows[-1] == expected[-1], "the final period must carry its coupon and the face together"


def test_bond_total_is_coupons_plus_face() -> None:
    """The amounts sum to periods times the coupon, plus the face, exactly."""
    rows = checked_events(bond_of(INST).events(), "Bond.events")
    coupon = half_away(Fraction(INST["face_cents"] * INST["coupon_bps"], 10_000))
    total = sum(a for _, a in rows)
    assert total == INST["periods"] * coupon + INST["face_cents"], "the total must be coupons plus face, in cents"


def test_bond_events_match_the_oracle_on_both_cases() -> None:
    """The whole event list equals the oracle on the learner's case and on a second case."""
    for case in (INST, INST2):
        rows = checked_events(bond_of(case).events(), "Bond.events")
        assert rows == oracle_events(case["face_cents"], case["coupon_bps"], case["periods"]), "events differ"


def test_bond_events_are_sorted_and_within_the_periods() -> None:
    """Events are sorted by period, and every period lies in 1..periods."""
    __tracebackhide__ = True
    rows = checked_events(bond_of(INST2).events(), "Bond.events")
    periods = [p for p, _ in rows]
    assert periods == sorted(periods), "events must be sorted by period"
    assert all(1 <= p <= INST2["periods"] for p in periods), "every period must lie in 1..periods"


def test_bond_one_period_fixture_is_par_coupon_plus_face() -> None:
    """Hand fixture: face 10000 cents, coupon 500 bps, one period: the one event carries the coupon and the face."""
    __tracebackhide__ = True
    assert checked_events(sol.Bond(10_000, 500, 1).events(), "Bond.events") == [(1, 10_500)], (
        "the one-period bond must pay its coupon and its face in one event"
    )


def test_bond_zero_coupon_pays_only_the_face_in_the_last_period() -> None:
    """Hand fixture: a zero coupon is kept as an event of zero; the face arrives only in period 3."""
    __tracebackhide__ = True
    rows = checked_events(sol.Bond(1_000_000, 0, 3).events(), "Bond.events")
    assert rows == [(1, 0), (2, 0), (3, 1_000_000)], "zero amounts are kept; the face is paid in the last period"


def test_bond_half_cent_coupon_rounds_away_from_zero() -> None:
    """Hand fixture: a face of 10001 cents at 50 % has an exact half-cent coupon, and a tie goes up, not down."""
    __tracebackhide__ = True
    assert checked_events(sol.Bond(10_001, 5_000, 2).events(), "Bond.events") == [(1, 5_001), (2, 15_002)], (
        "a half-cent coupon must round away from zero, with the face in the last period"
    )


def test_bond_half_cent_on_a_one_cent_face_rounds_up_not_to_zero() -> None:
    """Hand fixture: a one-cent face at 50 % has an exact half-cent coupon, which rounds up, not down to zero."""
    __tracebackhide__ = True
    assert checked_events(sol.Bond(1, 5_000, 1).events(), "Bond.events") == [(1, 2)], (
        "a half-cent coupon on a one-cent face must round up, not to zero"
    )


def test_bond_coupon_is_exact_for_a_face_too_large_for_floats() -> None:
    """Hand check: a face of 10**17 + 4999 cents at 1 bps has a coupon, (10**17 + 4999) / 10000 cents, that rounds down
    to a whole cent. A binary float cannot hold this face, so the coupon must come from exact fractions; the one event
    adds the face to that coupon."""
    __tracebackhide__ = True
    face = 10**17 + 4999
    rows = checked_events(must_accept(lambda: sol.Bond(face, 1, 1).events(), "face above 2**53"), "Bond.events")
    assert rows == [(1, face + 10**13)], "the coupon of a face above 2**53 must be computed from exact fractions"


def test_bond_periods_zero_is_refused() -> None:
    """The page names periods < 1 as a ValueError: a bond with no coupon period is not a bond."""
    must_raise(lambda: bond_of({**INST, "periods": 0}).events(), "periods < 1")


def test_bond_periods_minus_one_is_refused() -> None:
    """The page names periods < 1 as a ValueError; a negative count is below 1 too."""
    must_raise(lambda: bond_of({**INST, "periods": -1}).events(), "periods = -1")


def test_bond_periods_one_is_accepted() -> None:
    """The boundary periods = 1 is valid and gives one event."""
    __tracebackhide__ = True
    rows = checked_events(must_accept(lambda: sol.Bond(10_000, 500, 1).events(), "periods = 1"), "Bond.events")
    assert len(rows) == 1, "periods = 1 must give exactly one event"


def test_bond_face_zero_is_refused() -> None:
    """The page names face_cents <= 0 as a ValueError."""
    must_raise(lambda: sol.Bond(0, 500, 3).events(), "face_cents <= 0")


def test_bond_face_minus_one_is_refused() -> None:
    """The page names face_cents <= 0 as a ValueError; a negative face is refused too."""
    must_raise(lambda: sol.Bond(-1, 500, 3).events(), "face_cents = -1")


def test_bond_face_one_cent_is_accepted() -> None:
    """The boundary face_cents = 1 is valid: the single event is the one cent of face plus its coupon."""
    __tracebackhide__ = True
    assert checked_events(sol.Bond(1, 0, 1).events(), "Bond.events") == [(1, 1)], (
        "a one-cent face with no coupon must pay its face in its one period"
    )


def test_bond_face_of_ten_million_units_is_accepted() -> None:
    """The page names face_cents not positive as refused, so a face of 10**9 cents is valid. Hand check: its coupon
    is 500 bps of the face, 5 * 10**7 cents, and the one event adds the face to that coupon."""
    __tracebackhide__ = True
    rows = checked_events(must_accept(lambda: sol.Bond(10**9, 500, 1).events(), "face_cents = 10**9"), "Bond.events")
    assert rows == [(1, 10**9 + 5 * 10**7)], "a one-period bond pays its coupon and its face in that one event"


def test_bond_negative_coupon_is_refused() -> None:
    """The page names coupon_bps < 0 as a ValueError."""
    must_raise(lambda: sol.Bond(10_000, -1, 2).events(), "coupon_bps < 0")


def test_bond_zero_coupon_boundary_is_accepted() -> None:
    """The boundary coupon_bps = 0 is valid (a zero-coupon bond)."""
    must_accept(lambda: sol.Bond(10_000, 0, 2).events(), "coupon_bps = 0")


def test_bond_with_twelve_periods_is_valid_and_silent() -> None:
    """The page refuses periods below 1 and names no upper limit, so a 12-period bond is valid: it gives one event per
    period, and neither events() nor bond_price_cents() warns on it."""
    __tracebackhide__ = True
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        bond = sol.Bond(10_000, 500, 12)
        rows = checked_events(bond.events(), "Bond.events")
        checked_int(sol.bond_price_cents(bond, 400), "bond_price_cents")
    assert [p for p, _ in rows] == list(range(1, 13)), "a 12-period bond must have one event per period 1..12"
    assert caught == [], "a valid input must not warn"


def test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period() -> None:
    """The page gives every period 1..periods a coupon and discounts an event in period t by (1 + y) ** -t, with no
    upper limit on t. For 13 to 15 periods the event list must equal the oracle's, and bond_price_cents at 400 bps must
    equal the exact Fraction sum of every event discounted by (1 + y) ** -t, rounded once. The yield is not the coupon
    rate here: at 500 bps a bond whose face is paid with its last coupon is at par for every number of periods, so a
    schedule that stopped early and paid its face in the last period it kept would still price at 10000 cents, and only
    the 400 bps price and the event list catch that."""
    __tracebackhide__ = True
    for periods in (13, 14, 15):
        bond = sol.Bond(10_000, 500, periods)
        rows = checked_events(bond.events(), "Bond.events")
        assert rows == oracle_events(10_000, 500, periods), (
            "every period 1..periods must carry its coupon, and the face"
        )
        got = checked_int(sol.bond_price_cents(bond, 400), "bond_price_cents")
        want = oracle_price(oracle_events(10_000, 500, periods), 400)
        assert got == want, (
            "each event must be discounted by (1 + y) ** -t for its own period t, and the sum rounded once"
        )
        par = checked_int(sol.bond_price_cents(sol.Bond(10_000, 500, periods), 500), "bond_price_cents")
        assert par == 10_000, "a bond whose coupon rate equals the yield must price at par, for any number of periods"


def test_bond_schedule_longer_than_twenty_periods_is_complete() -> None:
    """The page gives every period 1..periods a coupon and names no upper limit on periods. A 24-period bond must have
    one event per period 1..24, with the face in period 24, and its price at 400 bps must be the exact sum of all 24
    events, each discounted by (1 + y) ** -t, rounded once."""
    __tracebackhide__ = True
    bond = sol.Bond(10_000, 500, 24)
    rows = checked_events(bond.events(), "Bond.events")
    assert rows == oracle_events(10_000, 500, 24), "every period 1..24 must carry its coupon, and the face the last one"
    got = checked_int(sol.bond_price_cents(bond, 400), "bond_price_cents")
    assert got == oracle_price(oracle_events(10_000, 500, 24), 400), (
        "all 24 events must be discounted by (1 + y) ** -t for their own periods, and the sum rounded once"
    )


def test_bond_schedule_of_forty_periods_is_complete_and_discounted_by_its_own_period() -> None:
    """The page gives every period 1..periods a coupon, discounts an event in period t by (1 + y) ** -t, and names no
    upper limit on periods. A 40-period bond must have one event per period 1..40, with the face in period 40, and its
    price at 400 bps must be the exact sum of all 40 events, each discounted by its own period, rounded once."""
    __tracebackhide__ = True
    bond = sol.Bond(10_000, 500, 40)
    rows = checked_events(bond.events(), "Bond.events")
    assert rows == oracle_events(10_000, 500, 40), "every period 1..40 must carry its coupon, and the face the last one"
    got = checked_int(sol.bond_price_cents(bond, 400), "bond_price_cents")
    assert got == oracle_price(oracle_events(10_000, 500, 40), 400), (
        "all 40 events must be discounted by (1 + y) ** -t for their own periods, and the sum rounded once"
    )


def test_bond_coupon_above_one_hundred_percent_is_accepted() -> None:
    """The page refuses only a negative coupon_bps and names no upper limit, so a coupon of 15000 bps (150 %) is
    valid: Bond(10000, 15000, 1) has one event, (1, 15000 + 10000)."""
    __tracebackhide__ = True
    rows = checked_events(
        must_accept(lambda: sol.Bond(10_000, 15_000, 1).events(), "coupon_bps = 15000"), "Bond.events"
    )
    assert rows == [(1, 25_000)], "a coupon of 150 % of face is paid in the one period, with the face"


# ---------------------------------------------------------------------------------------------------------------
# bond_price_cents: present value at a per-period yield
# ---------------------------------------------------------------------------------------------------------------


def test_bond_price_is_an_int_in_cents() -> None:
    """bond_price_cents returns a plain int, not a float and not a bool."""
    checked_int(sol.bond_price_cents(bond_of(INST), INST["yield_bps"]), "bond_price_cents")


def test_bond_price_matches_the_discounted_sum_on_both_cases() -> None:
    """Each event discounted by (1 + y) ** -t, y = yield_bps / 10000, summed exactly and rounded once, on two cases."""
    for case in (INST, INST2):
        got = checked_int(sol.bond_price_cents(bond_of(case), case["yield_bps"]), "bond_price_cents")
        want = oracle_price(oracle_events(case["face_cents"], case["coupon_bps"], case["periods"]), case["yield_bps"])
        assert got == want, "the price is the sum of each event discounted by (1 + y) ** -t, rounded once"


def test_bond_price_at_zero_yield_is_the_undiscounted_total() -> None:
    """At a zero yield no discounting happens, so the price is the sum of the events."""
    __tracebackhide__ = True
    total = sum(a for _, a in oracle_events(INST["face_cents"], INST["coupon_bps"], INST["periods"]))
    assert sol.bond_price_cents(bond_of(INST), 0) == total, "at zero yield the price is the undiscounted total"


def test_bond_price_one_period_at_its_coupon_rate_is_par() -> None:
    """Hand fixture: 10000 cents face, 500 bps coupon, one period, yield 500 bps: the coupon rate equals
    the yield, so the bond is at par."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(10_000, 500, 1), 500) == 10_000, (
        "a one-period bond priced at its own coupon rate must be at par"
    )


def test_bond_price_negative_yield_is_above_the_undiscounted_value() -> None:
    """Hand fixture: a one-period bond of 10000 cents face and 500 bps coupon, at a yield of -500 bps, is priced above
    the undiscounted sum of its events. The exact price is the discounted event, rounded once."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(10_000, 500, 1), -500) == 11_053, (
        "a negative yield must give the discounted sum of the events, rounded once"
    )


def test_bond_price_is_rounded_once_not_term_by_term() -> None:
    """The exact sum is rounded once. Rounding each discounted term and then adding gives a different answer here."""
    case = ROUNDING_CASE
    events = oracle_events(case["face_cents"], case["coupon_bps"], case["periods"])
    y = Fraction(case["yield_bps"], 10_000)
    per_term = sum(half_away(Fraction(a) / (1 + y) ** t) for t, a in events)
    got = checked_int(sol.bond_price_cents(bond_of(case), case["yield_bps"]), "bond_price_cents")
    assert got == oracle_price(events, case["yield_bps"]), "round the exact sum once, after all terms are added"
    assert per_term != got, "round the exact sum once, after all terms are added: term-by-term rounding differs here"


def test_bond_price_hand_fixture_rounds_the_sum_once() -> None:
    """Hand fixture: face 10000, 500 bps, three periods, 400 bps yield. The events are (1, 500), (2, 500), (3, 10500).
    Their exact present value is 10277.5091, which rounds once to 10278. The terms are 480.77, 462.28 and 9334.46
    before rounding; rounded one by one they give 481 + 462 + 9334 = 10277, so the two rules differ here."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(10_000, 500, 3), 400) == 10_278, (
        "the rounding fixture must round the exact sum once, after all terms are added"
    )


def test_bond_price_exact_half_cent_rounds_away_from_zero() -> None:
    """Hand fixture F: one cent of face, no coupon, one period, yield 10000 bps: the exact price is a half-cent tie, and
    a tie goes away from zero. Round-half-to-even (Python round()) or truncation gives 0."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(1, 0, 1), 10_000) == 1, (
        "an exact half cent must round away from zero, not to even"
    )


def test_bond_price_exact_half_at_five_thousand_point_five_rounds_up() -> None:
    """Hand fixture G: Bond(10001, 0, 1) at 10000 bps: the exact price is a half-cent tie, and it rounds up."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(10_001, 0, 1), 10_000) == 5_001, (
        "an exact half cent above a whole number of cents must round up"
    )


def test_bond_price_exact_half_cent_at_496_bps_is_exact_not_float() -> None:
    """Bond(1704285, 179, 1) at 496 bps: the exact present value is a half-cent tie, and it must be computed exactly.
    The coupon is 30506.7015 cents, rounded once, so the one event is (1, 1734792). Its exact present value is
    1734792 / 1.0496 = 3305625 / 2 cents, an exact half that rounds away from zero to 1652813. Discounting in binary
    floats gives 1652812.4999999998, which rounds to 1652812."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(1_704_285, 179, 1), 496) == 1_652_813, (
        "an exact half cent at a large face must be exact, not a float result"
    )


def test_bond_price_exact_half_above_ten_significant_digits_is_exact() -> None:
    """Exact halves of prices with more than ten significant digits. Bond(10**10 + 1, 0, 1) at 10000 bps has the one
    event (1, 10**10 + 1) and exact present value 5000000000.5 cents (eleven significant digits), which rounds away
    from zero to 5000000001. Bond(10**12 + 1, 0, 1) gives 500000000000.5 cents (thirteen significant digits), which
    rounds to 500000000001. A decimal context of ten significant digits drops the half before the final rounding."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(10**10 + 1, 0, 1), 10_000) == 5_000_000_001, (
        "an exact half cent of an eleven-significant-digit price must round away from zero, with no digits lost"
    )
    assert sol.bond_price_cents(sol.Bond(10**12 + 1, 0, 1), 10_000) == 500_000_000_001, (
        "an exact half cent of a thirteen-significant-digit price must round away from zero, with no digits lost"
    )


def test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield() -> None:
    """Hand check: Bond(13, 0, 1) at 400 bps has one event, whose exact present value is a half-cent tie that
    a float discount factor gets wrong. The event is (1, 13) and its exact present value is 13 / 1.04 cents,
    an exact half that rounds away from zero. A float discount factor, (1 + 0.04) ** -1 times 13, gives
    12.499999999999998 and rounds to 12, so this case catches that form; the exact Fraction form does not fail it."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(13, 0, 1), 400) == 13, (
        "an exact half cent must use the exact yield, not a float yield"
    )


def test_bond_price_just_under_a_half_cent_rounds_down() -> None:
    """Zero-coupon bond, three periods, yield 1 bps: its exact price is a whole number of cents plus a fraction a hair
    under a half, so it rounds down with no tolerance. Face 300075005 cents: the exact price is 299985000 plus 1/2 minus
    1/(2 * 1000300030001) cents, which rounds down to 299985000 (the nearest cent)."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(300_075_005, 0, 3), 1) == 299_985_000, (
        "a price a hair under a half cent must round down to the nearest cent, with no tolerance"
    )


def test_bond_price_falls_as_the_yield_rises() -> None:
    """Discounting harder gives a lower price: for a bond with positive cash flows, a higher yield lowers the price."""
    low = sol.bond_price_cents(bond_of(INST), 100)
    high = sol.bond_price_cents(bond_of(INST), 1_000)
    assert high < low, "a higher per-period yield must give a lower present value"


def test_bond_price_is_the_same_on_repeated_calls() -> None:
    """A pure function: the same bond and yield give the same price on every call."""
    first = sol.bond_price_cents(bond_of(INST), INST["yield_bps"])
    second = sol.bond_price_cents(bond_of(INST), INST["yield_bps"])
    assert first == second, "bond_price_cents must not keep state between calls"


def test_one_bond_priced_at_two_yields_gives_each_yield_its_own_price() -> None:
    """The same bond object priced at two yields: each price is the present value at the yield it was asked for, so
    the first price is not kept on the object. The second yield, 1000 bps, is outside the seeded yields (50 to 900)."""
    __tracebackhide__ = True
    bond = bond_of(INST)
    events = oracle_events(INST["face_cents"], INST["coupon_bps"], INST["periods"])
    first = checked_int(sol.bond_price_cents(bond, INST["yield_bps"]), "bond_price_cents")
    second = checked_int(sol.bond_price_cents(bond, 1_000), "bond_price_cents")
    assert first == oracle_price(events, INST["yield_bps"]), (
        "the price at the first yield must be the present value there"
    )
    assert second == oracle_price(events, 1_000), (
        "the price at the second yield must be the present value there, not the first price"
    )


def test_yield_at_minus_one_is_refused() -> None:
    """The page names yield_bps <= -10000 as a ValueError: 1 + y must be positive."""
    must_raise(lambda: sol.bond_price_cents(bond_of(INST), -10_000), "yield_bps = -10000")


def test_yield_below_minus_one_is_refused() -> None:
    """The same condition, one step further: yield_bps = -20000 is also refused."""
    must_raise(lambda: sol.bond_price_cents(bond_of(INST), -20_000), "yield_bps < -10000")


def test_yield_just_above_minus_one_is_accepted() -> None:
    """The boundary yield_bps = -9999 is valid and gives an int price."""
    value = must_accept(lambda: sol.bond_price_cents(bond_of(INST), -9_999), "yield_bps = -9999")
    checked_int(value, "bond_price_cents")


def test_yield_above_one_hundred_percent_is_accepted() -> None:
    """The page names one yield limit, yield_bps at or below -10000. A yield of 15000 bps (150 % per period) is valid:
    Bond(10000, 500, 1) at 15000 bps has the one event (1, 10500), and its price is 10500 / 2.5 = 4200 cents exactly."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(10_000, 500, 1), 15_000) == 4_200, (
        "a yield above 100 % per period is not named as refused; the price is the discounted event"
    )


# ---------------------------------------------------------------------------------------------------------------
# CashTrade: the settlement of one trade
# ---------------------------------------------------------------------------------------------------------------


def test_trade_has_one_settlement_event_on_its_settlement_day() -> None:
    """One event, in the settlement period, with the holder's cash flow -side * quantity * price."""
    rows = checked_events(trade_of(INST).events(), "CashTrade.events")
    want = (INST["settlement_day"], -INST["side"] * INST["quantity"] * INST["price_cents"])
    assert rows == [want], "a trade has one settlement event, from the holder's side"


def test_buyer_pays_cash_at_settlement() -> None:
    """Hand fixture: buying 10 units at 9850 cents, settling in period 2, is a payment, so the amount is negative."""
    __tracebackhide__ = True
    assert checked_events(sol.CashTrade(10, 9_850, 1, 2).events(), "CashTrade.events") == [(2, -98_500)], (
        "the settlement event of the buyer must pay cash, a negative amount"
    )


def test_seller_receives_cash_at_settlement() -> None:
    """Hand fixture: selling the same 10 units at 9850 cents is a receipt, so the settlement amount is positive."""
    __tracebackhide__ = True
    assert checked_events(sol.CashTrade(10, 9_850, -1, 2).events(), "CashTrade.events") == [(2, 98_500)], (
        "the settlement event of the seller must receive cash, a positive amount"
    )


def test_trade_settles_in_its_settlement_period_not_before() -> None:
    """The event is in the settlement period itself: an event one period early is the off-by-one error."""
    __tracebackhide__ = True
    rows = checked_events(trade_of(INST).events(), "CashTrade.events")
    assert rows[0][0] == INST["settlement_day"], "the event must be in the settlement period"


def test_trade_quantity_zero_is_refused() -> None:
    """The page names quantity < 1 as a ValueError."""
    must_raise(lambda: sol.CashTrade(0, 9_850, 1, 2).events(), "quantity < 1")


def test_trade_quantity_minus_one_is_refused() -> None:
    """The page names quantity < 1 as a ValueError; a negative quantity is refused too."""
    must_raise(lambda: sol.CashTrade(-1, 9_850, 1, 2).events(), "quantity = -1")


def test_trade_quantity_one_is_accepted() -> None:
    """The boundary quantity = 1 is valid."""
    __tracebackhide__ = True
    assert checked_events(sol.CashTrade(1, 9_850, 1, 2).events(), "CashTrade.events") == [(2, -9_850)], (
        "a trade of one unit must settle as quantity times price"
    )


def test_trade_quantity_of_501_is_accepted() -> None:
    """The page refuses quantity below 1 and names no upper limit, so 501 units is a valid trade with one settlement
    event: 501 units at 9850 cents each, bought in period 2."""
    __tracebackhide__ = True
    rows = checked_events(
        must_accept(lambda: sol.CashTrade(501, 9_850, 1, 2).events(), "quantity = 501"), "CashTrade.events"
    )
    assert rows == [(2, -501 * 9_850)], "501 units bought at the price settle in period 2 for quantity times price"


def test_trade_quantity_of_1001_is_accepted() -> None:
    """The page refuses quantity below 1 and names no upper limit, so 1001 units is a valid trade: one settlement
    event in period 2, the buyer paying 1001 times 9850 cents."""
    __tracebackhide__ = True
    rows = checked_events(
        must_accept(lambda: sol.CashTrade(1_001, 9_850, 1, 2).events(), "quantity = 1001"), "CashTrade.events"
    )
    assert rows == [(2, -1_001 * 9_850)], "1001 units bought at the price settle in period 2 for quantity times price"


def test_trade_cash_flow_is_exact_above_two_to_the_fifty_three() -> None:
    """Hand check: a trade of 2**40 + 1 units at 9851 cents has a cash flow above 2**53, which a float cannot hold.
    The settlement event is that exact product, negative for a buyer."""
    __tracebackhide__ = True
    quantity = 2**40 + 1
    rows = checked_events(
        must_accept(lambda: sol.CashTrade(quantity, 9_851, 1, 2).events(), "quantity = 2**40 + 1"), "CashTrade.events"
    )
    assert rows == [(2, -(quantity * 9_851))], "the cash flow of a product above 2**53 must be an exact integer"


def test_trade_price_negative_is_refused() -> None:
    """The page names price_cents < 0 as a ValueError."""
    must_raise(lambda: sol.CashTrade(10, -1, 1, 2).events(), "price_cents < 0")


def test_trade_price_zero_is_accepted_and_kept() -> None:
    """The boundary price_cents = 0 is valid, and its settlement event is kept as an event of zero."""
    __tracebackhide__ = True
    assert checked_events(sol.CashTrade(10, 0, 1, 2).events(), "CashTrade.events") == [(2, 0)], (
        "a zero price must be accepted, and its settlement event kept at zero"
    )


def test_trade_side_zero_is_refused() -> None:
    """The page names side not in {+1, -1} as a ValueError: zero is neither."""
    must_raise(lambda: sol.CashTrade(10, 9_850, 0, 2).events(), "side = 0")


def test_trade_side_two_is_refused() -> None:
    """The same condition, on the other side: side = 2 is not +1 or -1."""
    must_raise(lambda: sol.CashTrade(10, 9_850, 2, 2).events(), "side = 2")


def test_trade_side_minus_two_is_refused() -> None:
    """The page names side not in {+1, -1} as a ValueError: -2 is neither, on the negative side."""
    must_raise(lambda: sol.CashTrade(10, 9_850, -2, 2).events(), "side = -2")


def test_trade_side_three_is_refused() -> None:
    """The page names side not in {+1, -1} as a ValueError: 3 is neither, on the far positive side."""
    must_raise(lambda: sol.CashTrade(10, 9_850, 3, 2).events(), "side = 3")


def test_trade_side_minus_three_is_refused() -> None:
    """The page names side not in {+1, -1} as a ValueError: -3 is neither, on the far negative side."""
    must_raise(lambda: sol.CashTrade(10, 9_850, -3, 2).events(), "side = -3")


def test_trade_side_plus_and_minus_one_are_accepted() -> None:
    """Both allowed sides are accepted, and they give opposite signs."""
    __tracebackhide__ = True
    buy = checked_events(must_accept(lambda: sol.CashTrade(10, 9_850, 1, 2).events(), "side = +1"), "events")
    sell = checked_events(must_accept(lambda: sol.CashTrade(10, 9_850, -1, 2).events(), "side = -1"), "events")
    assert buy[0][1] == -sell[0][1], "the buyer's and seller's cash flows are equal and opposite"


def test_trade_settlement_day_zero_is_refused() -> None:
    """The page names settlement_day < 1 as a ValueError: periods are numbered from 1."""
    must_raise(lambda: sol.CashTrade(10, 9_850, 1, 0).events(), "settlement_day < 1")


def test_trade_settlement_day_minus_one_is_refused() -> None:
    """The page names settlement_day < 1 as a ValueError; a negative period is refused too."""
    must_raise(lambda: sol.CashTrade(10, 9_850, 1, -1).events(), "settlement_day = -1")


def test_trade_settlement_day_one_is_accepted() -> None:
    """The boundary settlement_day = 1 is valid and settles in period 1."""
    __tracebackhide__ = True
    assert checked_events(sol.CashTrade(10, 9_850, 1, 1).events(), "CashTrade.events") == [(1, -98_500)], (
        "a settlement period of one must be accepted and carry the one event"
    )


def test_trade_settlement_day_of_100_is_accepted() -> None:
    """The page names settlement_day less than 1 as refused, so a trade settling in period 100 is valid: its one event
    is in period 100."""
    __tracebackhide__ = True
    rows = checked_events(
        must_accept(lambda: sol.CashTrade(10, 9_850, 1, 100).events(), "settlement_day = 100"), "CashTrade.events"
    )
    assert rows == [(100, -98_500)], "a trade has its one event in its settlement period"


def test_trade_amount_is_an_int_in_cents() -> None:
    """The trade's cash flow is an int in cents, computed exactly."""
    rows = checked_events(trade_of(INST2).events(), "CashTrade.events")
    checked_int(rows[0][1], "CashTrade settlement amount")


# ---------------------------------------------------------------------------------------------------------------
# Integrity: silence, purity and wrong types the page does not name
# ---------------------------------------------------------------------------------------------------------------


def test_the_module_prints_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    """No function prints on a valid input: the captured standard output and error are empty after each run, on the
    learner's case and on the valid boundary inputs (negative yield, zero yield, zero coupon, zero price, sell side,
    quantity 1, settlement period 1, one cent of face, one period, twelve periods)."""
    runs: list[tuple[str, Callable[[], object]]] = [
        ("the seeded case", lambda: sol.bond_price_cents(bond_of(INST), INST["yield_bps"])),
        ("the seeded case's events", lambda: bond_of(INST).events()),
        ("the seeded case's trade", lambda: trade_of(INST).events()),
        ("yield_bps = -9999", lambda: sol.bond_price_cents(sol.Bond(10_000, 500, 3), -9_999)),
        ("yield_bps = -5000", lambda: sol.bond_price_cents(sol.Bond(10_000, 500, 3), -5_000)),
        ("yield_bps = 0", lambda: sol.bond_price_cents(sol.Bond(10_000, 500, 3), 0)),
        ("coupon_bps = 0", lambda: sol.Bond(10_000, 0, 2).events()),
        ("price_cents = 0", lambda: sol.CashTrade(10, 0, 1, 2).events()),
        ("side = -1", lambda: sol.CashTrade(10, 9_850, -1, 2).events()),
        ("quantity = 1", lambda: sol.CashTrade(1, 9_850, 1, 2).events()),
        ("settlement_day = 1", lambda: sol.CashTrade(10, 9_850, 1, 1).events()),
        ("face_cents = 1", lambda: sol.Bond(1, 500, 3).events()),
        ("periods = 1", lambda: sol.Bond(10_000, 500, 1).events()),
        ("periods = 12", lambda: sol.Bond(10_000, 500, 12).events()),
    ]
    for label, call in runs:
        call()
        captured = capsys.readouterr()
        assert captured.out == "" and captured.err == "", f"{label}: a valid input must print nothing"


def test_refused_inputs_print_nothing_before_they_raise(capsys: pytest.CaptureFixture[str]) -> None:
    """Each named refused input raises ValueError, and the module prints nothing on the way to the refusal."""
    refusals: list[tuple[str, Callable[[], object]]] = [
        ("periods < 1", lambda: bond_of({**INST, "periods": 0}).events()),
        ("face_cents <= 0", lambda: sol.Bond(0, 500, 3).events()),
        ("coupon_bps < 0", lambda: sol.Bond(10_000, -1, 2).events()),
        ("yield_bps <= -10000", lambda: sol.bond_price_cents(bond_of(INST), -10_000)),
        ("quantity < 1", lambda: sol.CashTrade(0, 9_850, 1, 2).events()),
        ("price_cents < 0", lambda: sol.CashTrade(10, -1, 1, 2).events()),
        ("side not in {+1, -1}", lambda: sol.CashTrade(10, 9_850, 0, 2).events()),
        ("settlement_day < 1", lambda: sol.CashTrade(10, 9_850, 1, 0).events()),
    ]
    for condition, call in refusals:
        must_raise(call, condition)
        captured = capsys.readouterr()
        assert captured.out == "" and captured.err == "", f"{condition}: a refused input must print nothing"


def test_repeated_events_calls_agree() -> None:
    """events() is pure: two calls on one object give the same list, for the bond and for the trade."""
    __tracebackhide__ = True
    bond = bond_of(INST)
    assert checked_events(bond.events(), "Bond.events") == checked_events(bond.events(), "Bond.events"), (
        "events() must return the same list on every call, for the bond"
    )
    trade = trade_of(INST)
    assert checked_events(trade.events(), "CashTrade.events") == checked_events(trade.events(), "CashTrade.events"), (
        "events() must return the same list on every call, for the trade"
    )


def test_non_whole_face_is_refused_or_gives_ints() -> None:
    """A float face is not a whole number of cents. The page does not name this input, so any exception passes; a
    returned answer must still be made of ints, never of floats."""
    try:
        rows = sol.Bond(1_000.5, 500, 1).events()  # type: ignore[arg-type]
    except Exception:
        return
    checked_events(rows, "Bond.events with a float face")


def test_bool_periods_is_not_quietly_accepted_as_a_number() -> None:
    """A bool is not a whole number of periods. The page does not name this input, so any exception passes; a
    returned answer must still be made of ints."""
    try:
        rows = sol.Bond(10_000, 500, True).events()
    except Exception:
        return
    checked_events(rows, "Bond.events with a bool periods")


def _named_when_unimplemented(test: Callable[..., None]) -> Callable[..., None]:
    """Turn the student module's NotImplementedError into a failure that names the property, with no traceback."""

    @functools.wraps(test)
    def run(*args: object, **kwargs: object) -> None:
        try:
            test(*args, **kwargs)
        except NotImplementedError as missing:
            name = str(missing)
        else:
            return
        # Failing outside the except block keeps the NotImplementedError out of the report, so no traceback shows.
        summary = (test.__doc__ or test.__name__).strip().splitlines()[0]
        pytest.fail(
            f"{summary} The student module has no implementation for {name} yet; write it in instruments.py.",
            pytrace=False,
        )

    return run


def test_bond_schedule_of_one_hundred_periods_is_complete_and_discounted_by_its_own_period() -> None:
    """Accepted-input check: a 100-period bond has one event per period 1..100, the face in period 100, and its price at
    400 bps is the exact sum of all 100 events, each discounted by its own period, rounded once."""
    __tracebackhide__ = True
    bond = sol.Bond(10_000, 500, 100)
    rows = checked_events(bond.events(), "Bond.events")
    assert rows == oracle_events(10_000, 500, 100), (
        "every period 1..100 must carry its coupon, and the face the last one"
    )
    got = checked_int(sol.bond_price_cents(bond, 400), "bond_price_cents")
    assert got == oracle_price(oracle_events(10_000, 500, 100), 400), (
        "all 100 events must be discounted by (1 + y) ** -t for their own periods, and the sum rounded once"
    )


def test_bond_schedule_of_one_thousand_and_one_periods_is_accepted() -> None:
    """Accepted-input check: the page refuses only periods below 1 and gives every period 1..periods a coupon, so a
    1001-period bond has one event per period 1..1001, and its price at 400 bps is the exact sum of those events,
    rounded once."""
    __tracebackhide__ = True
    bond = sol.Bond(10_000, 500, 1_001)
    rows = checked_events(bond.events(), "Bond.events")
    assert rows == oracle_events(10_000, 500, 1_001), (
        "every period 1..1001 must carry its coupon, and the face the last one"
    )
    got = checked_int(sol.bond_price_cents(bond, 400), "bond_price_cents")
    assert got == oracle_price(oracle_events(10_000, 500, 1_001), 400), (
        "all 1001 events must be discounted by (1 + y) ** -t for their own periods, and the sum rounded once"
    )


def test_yield_of_three_hundred_percent_per_period_is_accepted() -> None:
    """Accepted-input check: a yield of 30000 bps (300 % per period) is not named as refused; the price is the
    discounted event."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(10_000, 500, 1), 30_000) == 2_625, (
        "a yield above 100 % per period is not named as refused; the price is the discounted event"
    )


def test_trade_settling_after_period_one_hundred_is_accepted() -> None:
    """Accepted-input check: the page names only settlement_day < 1; a trade settling in period 1000 is valid."""
    __tracebackhide__ = True
    assert checked_events(sol.CashTrade(10, 9_850, 1, 1_000).events(), "CashTrade.events") == [(1_000, -98_500)], (
        "a trade's one event is in its settlement period, however late"
    )


def test_bond_price_exact_half_above_forty_significant_digits_is_exact() -> None:
    """Accepted-input check: Bond(10**40 + 1, 0, 1) at 10000 bps has a half-cent present value with forty-one
    significant digits, which must round away from zero with no digits lost.
    The exact present value is 5 * 10**39 + 1/2 cents."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(10**40 + 1, 0, 1), 10_000) == 5 * 10**39 + 1, (
        "an exact half cent of a price above forty significant digits must round away from zero, with no digits lost"
    )


# Every test is wrapped after the last one is defined, so that the tests added above are wrapped too.
for _name, _value in list(globals().items()):
    if _name.startswith("test_") and callable(_value):
        globals()[_name] = _named_when_unimplemented(_value)

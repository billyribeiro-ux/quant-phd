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

import math
import os
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
    rows = checked_events(bond_of(INST).events(), "Bond.events")
    assert [p for p, _ in rows] == list(range(1, INST["periods"] + 1)), "periods must run 1..periods, one event each"


def test_bond_coupon_is_face_times_coupon_rate_rounded_half_up() -> None:
    """Every coupon except the last equals face * coupon_bps / 10000, rounded to the nearest cent, halves away."""
    rows = checked_events(bond_of(INST).events(), "Bond.events")
    expected = oracle_events(INST["face_cents"], INST["coupon_bps"], INST["periods"])
    for (period, amount), (_, want) in zip(rows[:-1], expected[:-1], strict=True):
        assert amount == want, f"coupon in period {period}: the coupon is face times the coupon rate, rounded once"


def test_bond_last_period_carries_the_principal() -> None:
    """The last event is the last coupon plus the face: the principal is paid in the final period, with that coupon."""
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
    rows = checked_events(bond_of(INST2).events(), "Bond.events")
    periods = [p for p, _ in rows]
    assert periods == sorted(periods), "events must be sorted by period"
    assert all(1 <= p <= INST2["periods"] for p in periods), "every period must lie in 1..periods"


def test_bond_one_period_fixture_is_par_coupon_plus_face() -> None:
    """Hand fixture: face 10000 cents, coupon 500 bps, one period: the single event is (1, 500 + 10000)."""
    assert checked_events(sol.Bond(10_000, 500, 1).events(), "Bond.events") == [(1, 10_500)]


def test_bond_zero_coupon_pays_only_the_face_in_the_last_period() -> None:
    """Hand fixture: a zero coupon is kept as an event of zero; the face arrives only in period 3."""
    rows = checked_events(sol.Bond(1_000_000, 0, 3).events(), "Bond.events")
    assert rows == [(1, 0), (2, 0), (3, 1_000_000)], "zero amounts are kept; the face is paid in the last period"


def test_bond_half_cent_coupon_rounds_away_from_zero() -> None:
    """Hand fixture: 10001 cents at 50 % is 5000.5 cents, which rounds to 5001 (a tie goes up, not down)."""
    assert checked_events(sol.Bond(10_001, 5_000, 2).events(), "Bond.events") == [(1, 5_001), (2, 15_002)]


def test_bond_half_cent_on_a_one_cent_face_rounds_up_not_to_zero() -> None:
    """Hand fixture: 1 cent at 50 % is 0.5 cents, which rounds to 1 cent; truncation would give 0."""
    assert checked_events(sol.Bond(1, 5_000, 1).events(), "Bond.events") == [(1, 2)]


def test_bond_periods_zero_is_refused() -> None:
    """The page names periods < 1 as a ValueError: a bond with no coupon period is not a bond."""
    must_raise(lambda: bond_of({**INST, "periods": 0}).events(), "periods < 1")


def test_bond_periods_one_is_accepted() -> None:
    """The boundary periods = 1 is valid and gives one event."""
    rows = checked_events(must_accept(lambda: sol.Bond(10_000, 500, 1).events(), "periods = 1"), "Bond.events")  # type: ignore[arg-type]
    assert len(rows) == 1, "periods = 1 must give exactly one event"


def test_bond_face_zero_is_refused() -> None:
    """The page names face_cents <= 0 as a ValueError."""
    must_raise(lambda: sol.Bond(0, 500, 3).events(), "face_cents <= 0")


def test_bond_face_one_cent_is_accepted() -> None:
    """The boundary face_cents = 1 is valid: the single event is the one cent of face plus its coupon."""
    assert checked_events(sol.Bond(1, 0, 1).events(), "Bond.events") == [(1, 1)]


def test_bond_negative_coupon_is_refused() -> None:
    """The page names coupon_bps < 0 as a ValueError."""
    must_raise(lambda: sol.Bond(10_000, -1, 2).events(), "coupon_bps < 0")


def test_bond_zero_coupon_boundary_is_accepted() -> None:
    """The boundary coupon_bps = 0 is valid (a zero-coupon bond)."""
    must_accept(lambda: sol.Bond(10_000, 0, 2).events(), "coupon_bps = 0")


# ---------------------------------------------------------------------------------------------------------------
# bond_price_cents: present value at a per-period yield
# ---------------------------------------------------------------------------------------------------------------


def test_bond_price_is_an_int_in_cents() -> None:
    """bond_price_cents returns a plain int, not a float and not a bool."""
    checked_int(sol.bond_price_cents(bond_of(INST), INST["yield_bps"]), "bond_price_cents")


def test_bond_price_matches_the_closed_form_on_both_cases() -> None:
    """Sum of c * v**t plus F * v**n, with v = 1 + y, computed exactly and rounded once, on two cases."""
    for case in (INST, INST2):
        got = checked_int(sol.bond_price_cents(bond_of(case), case["yield_bps"]), "bond_price_cents")
        want = oracle_price(oracle_events(case["face_cents"], case["coupon_bps"], case["periods"]), case["yield_bps"])
        assert got == want, "the price is the sum of each event discounted by (1 + y) ** -t, rounded once"


def test_bond_price_at_zero_yield_is_the_undiscounted_total() -> None:
    """At a zero yield no discounting happens, so the price is the sum of the events."""
    total = sum(a for _, a in oracle_events(INST["face_cents"], INST["coupon_bps"], INST["periods"]))
    assert sol.bond_price_cents(bond_of(INST), 0) == total, "at zero yield the price is the undiscounted total"


def test_bond_price_one_period_at_its_coupon_rate_is_par() -> None:
    """Hand fixture: 10000 cents face, 500 bps coupon, one period, yield 500 bps: 10500 / 1.05 = 10000 exactly."""
    assert sol.bond_price_cents(sol.Bond(10_000, 500, 1), 500) == 10_000


def test_bond_price_negative_yield_is_above_the_undiscounted_value() -> None:
    """Hand fixture: 10500 at yield -500 bps is 10500 / 0.95 = 210000 / 19 = 11052.63..., which rounds to 11053."""
    assert sol.bond_price_cents(sol.Bond(10_000, 500, 1), -500) == 11_053


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
    assert sol.bond_price_cents(sol.Bond(10_000, 500, 3), 400) == 10_278


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


# ---------------------------------------------------------------------------------------------------------------
# CashTrade: the settlement of one trade
# ---------------------------------------------------------------------------------------------------------------


def test_trade_has_one_settlement_event_on_its_settlement_day() -> None:
    """One event, in the settlement period, with the holder's cash flow -side * quantity * price."""
    rows = checked_events(trade_of(INST).events(), "CashTrade.events")
    want = (INST["settlement_day"], -INST["side"] * INST["quantity"] * INST["price_cents"])
    assert rows == [want], "a trade has one settlement event, from the holder's side"


def test_buyer_pays_cash_at_settlement() -> None:
    """Hand fixture: buying 10 units at 9850 cents settling in period 2 is a payment of 98500 cents (negative)."""
    assert checked_events(sol.CashTrade(10, 9_850, 1, 2).events(), "CashTrade.events") == [(2, -98_500)]


def test_seller_receives_cash_at_settlement() -> None:
    """Hand fixture: selling the same 10 units at 9850 cents is a receipt of 98500 cents (positive)."""
    assert checked_events(sol.CashTrade(10, 9_850, -1, 2).events(), "CashTrade.events") == [(2, 98_500)]


def test_trade_settles_in_its_settlement_period_not_before() -> None:
    """The event is in the settlement period itself: an event one period early is the off-by-one error."""
    rows = checked_events(trade_of(INST).events(), "CashTrade.events")
    assert rows[0][0] == INST["settlement_day"], "the event must be in the settlement period"


def test_trade_quantity_zero_is_refused() -> None:
    """The page names quantity < 1 as a ValueError."""
    must_raise(lambda: sol.CashTrade(0, 9_850, 1, 2).events(), "quantity < 1")


def test_trade_quantity_one_is_accepted() -> None:
    """The boundary quantity = 1 is valid."""
    assert checked_events(sol.CashTrade(1, 9_850, 1, 2).events(), "CashTrade.events") == [(2, -9_850)]


def test_trade_price_negative_is_refused() -> None:
    """The page names price_cents < 0 as a ValueError."""
    must_raise(lambda: sol.CashTrade(10, -1, 1, 2).events(), "price_cents < 0")


def test_trade_price_zero_is_accepted_and_kept() -> None:
    """The boundary price_cents = 0 is valid, and its settlement event is kept as an event of zero."""
    assert checked_events(sol.CashTrade(10, 0, 1, 2).events(), "CashTrade.events") == [(2, 0)]


def test_trade_side_zero_is_refused() -> None:
    """The page names side not in {+1, -1} as a ValueError: zero is neither."""
    must_raise(lambda: sol.CashTrade(10, 9_850, 0, 2).events(), "side = 0")


def test_trade_side_two_is_refused() -> None:
    """The same condition, on the other side: side = 2 is not +1 or -1."""
    must_raise(lambda: sol.CashTrade(10, 9_850, 2, 2).events(), "side = 2")


def test_trade_side_plus_and_minus_one_are_accepted() -> None:
    """Both allowed sides are accepted, and they give opposite signs."""
    buy = checked_events(must_accept(lambda: sol.CashTrade(10, 9_850, 1, 2).events(), "side = +1"), "events")  # type: ignore[arg-type]
    sell = checked_events(must_accept(lambda: sol.CashTrade(10, 9_850, -1, 2).events(), "side = -1"), "events")  # type: ignore[arg-type]
    assert buy[0][1] == -sell[0][1], "the buyer's and seller's cash flows are equal and opposite"


def test_trade_settlement_day_zero_is_refused() -> None:
    """The page names settlement_day < 1 as a ValueError: periods are numbered from 1."""
    must_raise(lambda: sol.CashTrade(10, 9_850, 1, 0).events(), "settlement_day < 1")


def test_trade_settlement_day_one_is_accepted() -> None:
    """The boundary settlement_day = 1 is valid and settles in period 1."""
    assert checked_events(sol.CashTrade(10, 9_850, 1, 1).events(), "CashTrade.events") == [(1, -98_500)]


def test_trade_amount_is_an_int_in_cents() -> None:
    """The trade's cash flow is an int in cents, computed exactly."""
    rows = checked_events(trade_of(INST2).events(), "CashTrade.events")
    checked_int(rows[0][1], "CashTrade settlement amount")


# ---------------------------------------------------------------------------------------------------------------
# Integrity: silence, purity and wrong types the page does not name
# ---------------------------------------------------------------------------------------------------------------


def test_the_module_prints_nothing(capsys: pytest.CaptureFixture[str]) -> None:
    """No function prints: the captured standard output and error are empty after a full run."""
    bond = bond_of(INST)
    sol.bond_price_cents(bond, INST["yield_bps"])
    bond.events()
    trade_of(INST).events()
    captured = capsys.readouterr()
    assert captured.out == "" and captured.err == "", "the module must not print to standard output or error"


def test_repeated_events_calls_agree() -> None:
    """events() is pure: two calls on one object give the same list."""
    bond = bond_of(INST)
    assert checked_events(bond.events(), "Bond.events") == checked_events(bond.events(), "Bond.events")


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
        rows = sol.Bond(10_000, 500, True).events()  # type: ignore[arg-type]
    except Exception:
        return
    checked_events(rows, "Bond.events with a bool periods")

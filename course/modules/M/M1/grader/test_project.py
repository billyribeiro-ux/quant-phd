"""Acceptance suite for the M1 project: the annuity and mortgage engine (annuity_engine.py).

Runs identically in the browser (Pyodide) and locally:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

with your annuity_engine.py next to this file. Warnings are failures, as in the browser.

Each test checks a property or a number against the definitions of the M1 lessons and the project specification.
Integer money is compared exactly: the specification fixes the nearest-cent rule (a tie going up), so
an implementation that follows it returns the same integers. A failing test names the property it checks and the
idea to revisit. It never prints the expected value.
"""

from __future__ import annotations

import ast
import contextlib
import dataclasses
import io
import itertools
import math
import os
import sys
import warnings
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

import annuity_engine as sol
import pytest
from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
INST2 = make_instance(SEED + 7_919)  # a second instance, so a fixed answer for one seed cannot pass
PRINCIPAL: int = INST["principal_cents"]
BPS: int = INST["annual_bps"]
MONTHS: int = INST["months"]
RATE: float = INST["annual_rate"]
ANN_RATE: float = INST["annuity_rate"]
ANN_N: int = INST["annuity_periods"]
PERP_RATE: float = INST["perpetuity_rate"]
GROWTH: float = INST["growth_rate"]
PERP_BPS: int = INST["perpetuity_bps"]
GROWTH_BPS: int = INST["growth_bps"]
ANN_BPS: int = INST["annuity_bps"]

FIELDS = ("period", "opening_cents", "interest_cents", "principal_cents", "payment_cents", "closing_cents")
ROW_TUPLE = tuple[int, int, int, int, int, int]


def nearest(x: Fraction) -> int:
    """The test's own nearest-cent rule for a non-negative exact amount: floor(x + 1/2)."""
    return math.floor(x + Fraction(1, 2))


def exact_level(principal: int, bps: int, months: int) -> int:
    """The level payment in cents, computed exactly from the annual rate in basis points."""
    i = Fraction(bps, 120_000)
    return nearest(Fraction(principal) * i / (1 - (1 + i) ** (-months)))


def exact_rows(principal: int, bps: int, months: int) -> list[ROW_TUPLE]:
    """The exact schedule, one tuple per month: period, opening, interest, principal, payment, closing."""
    i = Fraction(bps, 120_000)
    payment = exact_level(principal, bps, months)
    rows: list[ROW_TUPLE] = []
    opening = principal
    for period in range(1, months + 1):
        interest = nearest(opening * i)
        paid = payment if period < months else opening + interest
        principal_paid = paid - interest
        closing = opening - principal_paid
        rows.append((period, opening, interest, principal_paid, paid, closing))
        opening = closing
    return rows


EXACT = exact_rows(PRINCIPAL, BPS, MONTHS)
EXACT_LEVEL = exact_level(PRINCIPAL, BPS, MONTHS)
EXACT2 = exact_rows(INST2["principal_cents"], INST2["annual_bps"], INST2["months"])


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Fail unless call() raises ValueError. The specification names ValueError for every invalid input."""
    try:
        call()
    except ValueError:
        return
    pytest.fail(f"{condition}: the specification requires a ValueError, and none was raised.")


def close(a: float, b: float, rel: float) -> bool:
    return math.isfinite(a) and abs(a - b) <= rel * max(1.0, abs(b))


def fields(row: object) -> ROW_TUPLE:
    """The six integer fields of one schedule row, in order. Anything else fails with the rule it breaks."""
    out: list[int] = []
    for name in FIELDS:
        if not hasattr(row, name):
            pytest.fail(
                "each schedule row must carry period, opening_cents, interest_cents, principal_cents, "
                "payment_cents and closing_cents"
            )
        value = getattr(row, name)
        if isinstance(value, bool) or not isinstance(value, int):
            pytest.fail(f"{name} must be an integer number of cents (or a whole period number), not a float")
        out.append(value)
    return (out[0], out[1], out[2], out[3], out[4], out[5])


def schedule(principal: int, rate: float, months: int) -> list[ROW_TUPLE]:
    rows = sol.amortization_schedule(principal, rate, months)
    if not isinstance(rows, tuple):
        pytest.fail("amortization_schedule must return a tuple of rows")
    return [fields(row) for row in rows]


# --- closed forms of the annuity, the perpetuity and the growing perpetuity


def test_annuity_factor_matches_direct_summation() -> None:
    """a(n) = sum of v^k for k = 1..n with v = 1/(1+r); relative tolerance 1e-9 (Lesson 6, closed form)."""
    v = 1 / (1 + ANN_RATE)
    direct = sum(v**k for k in range(1, ANN_N + 1))
    assert close(sol.annuity_factor(ANN_RATE, ANN_N), direct, 1e-9), (
        "annuity_factor disagrees with the sum of discount factors over the periods: check the closed form"
    )


def test_annuity_factor_matches_exact_closed_form() -> None:
    """(1 - (1+r)^-n) / r computed in exact rational arithmetic; relative tolerance 1e-9."""
    r = Fraction(ANN_BPS, 10_000)
    exact = float((1 - (1 + r) ** (-ANN_N)) / r)
    assert close(sol.annuity_factor(ANN_RATE, ANN_N), exact, 1e-9), (
        "annuity_factor is not the closed form (1 - (1+r)^-n) / r: check the sign of the exponent"
    )


def test_annuity_factor_one_period_at_a_time() -> None:
    """The factor grows by exactly v^n when one period is added: a(n) - a(n-1) = v^n (the induction step)."""
    v = 1 / (1 + ANN_RATE)
    for n in range(1, ANN_N + 1):
        step = sol.annuity_factor(ANN_RATE, n) - sol.annuity_factor(ANN_RATE, n - 1)
        assert close(step, v**n, 1e-9), "a(n) - a(n-1) must equal v^n: the factor must add one discounted payment"


def test_annuity_factor_zero_periods_is_zero() -> None:
    """With no payments the factor is 0, and it is a float like every closed form (the convention is binding)."""
    zero = sol.annuity_factor(ANN_RATE, 0)
    assert isinstance(zero, float), "annuity_factor must return a float at zero periods, not an int"
    assert zero == 0


def test_closed_forms_return_floats() -> None:
    """The closed forms return floats, including at a zero rate, where the factor is the number of periods."""
    assert isinstance(sol.annuity_factor(0, 5), float), "annuity_factor must return a float, also at a zero rate"
    assert isinstance(sol.annuity_due_factor(0, 5), float), "annuity_due_factor must return a float at a zero rate"
    assert isinstance(sol.perpetuity_factor(0.05), float), "perpetuity_factor must return a float"
    assert isinstance(sol.growing_perpetuity_factor(0.05, 0.02), float), "growing_perpetuity_factor must return a float"


@pytest.mark.parametrize(("rate", "periods"), [(-0.01, 12), (-0.5, 3)])
def test_annuity_factor_accepts_a_negative_rate_above_minus_one(rate: float, periods: int) -> None:
    """A rate in (-1, 0) is valid, since the specification requires only r > -1. The factor is computed at that
    rate, not refused and not replaced by the factor of |r|: the sum of v^k, v = 1/(1+r), and the exact closed form."""
    v = 1 / (1 + rate)
    direct = sum(v**k for k in range(1, periods + 1))
    exact_rate = Fraction(repr(rate))
    exact = float((1 - (1 + exact_rate) ** (-periods)) / exact_rate)
    assert close(sol.annuity_factor(rate, periods), direct, 1e-9), (
        "annuity_factor at a negative rate above -1 must equal the sum of discount factors at that rate"
    )
    assert close(sol.annuity_factor(rate, periods), exact, 1e-9), (
        "annuity_factor at a negative rate above -1 must be the closed form (1 - (1+r)^-n) / r at that rate"
    )


def test_annuity_factor_zero_rate_is_the_number_of_periods() -> None:
    """At a zero rate every payment is worth 1, so the factor is the number of payments (handled explicitly)."""
    assert sol.annuity_factor(0, ANN_N) == ANN_N
    assert sol.annuity_factor(0.0, 12) == 12


def test_annuity_factor_moves_the_right_way() -> None:
    """More periods raise the value of an annuity; a higher rate lowers it."""
    assert sol.annuity_factor(ANN_RATE, ANN_N + 1) > sol.annuity_factor(ANN_RATE, ANN_N)
    assert sol.annuity_factor(ANN_RATE + 0.01, ANN_N) < sol.annuity_factor(ANN_RATE, ANN_N)


def test_annuity_due_is_the_ordinary_annuity_one_period_earlier() -> None:
    """Payments at the start of each period: the due factor is the sum of v^k for k = 0..n-1 (Lesson 7)."""
    v = 1 / (1 + ANN_RATE)
    direct = sum(v**k for k in range(0, ANN_N))
    assert close(sol.annuity_due_factor(ANN_RATE, ANN_N), direct, 1e-9), (
        "annuity_due_factor must count the first payment at time zero: the ordinary factor times (1 + r)"
    )
    assert close(sol.annuity_due_factor(ANN_RATE, ANN_N), sol.annuity_factor(ANN_RATE, ANN_N) * (1 + ANN_RATE), 1e-12)


def test_annuity_due_zero_rate_is_the_number_of_periods() -> None:
    assert sol.annuity_due_factor(0, ANN_N) == ANN_N


def test_annuity_due_zero_periods_is_zero() -> None:
    """With no payments the due factor is 0 at any valid rate: the due factor is the ordinary factor times (1 + r)."""
    due = sol.annuity_due_factor(ANN_RATE, 0)
    assert isinstance(due, float), "annuity_due_factor must return a float at zero periods, not an int"
    assert due == 0
    assert isinstance(sol.annuity_due_factor(0.05, 0), float), "annuity_due_factor must return a float at zero periods"
    assert sol.annuity_due_factor(0.05, 0) == 0


def test_annuity_accepts_a_rate_just_above_minus_one() -> None:
    """The lower boundary is open: -1 is refused (tested above) and -0.999 is valid. v = 1000, so the three-period sum
    is 1000 + 10^6 + 10^9 = 1001001000, and the closed form (1 - (1+r)^-3) / r = (1 - 10^9) / (-0.999) gives the same
    value."""
    assert close(sol.annuity_factor(-0.999, 3), 1_001_001_000.0, 1e-9), (
        "a rate above -1 is valid: the factor must be the sum of discount factors at that rate"
    )
    assert close(sol.annuity_due_factor(-0.999, 3), 1_001_001_000.0 * (1 - 0.999), 1e-9), (
        "the due factor at a rate above -1 is the ordinary factor times (1 + r)"
    )


@pytest.mark.parametrize(
    ("rate", "periods"),
    [
        ("0.05", 5),
        (None, 5),
        (0.05, "5"),
        (0.05, None),
        (0.05, [5]),
        ("", 5),
        (" 0.05", 5),
        (0.05, " 5"),
        (0.05, []),
        (0.05, False),
    ],
)
def test_annuity_factor_rejects_the_wrong_types(rate: Any, periods: Any) -> None:
    must_raise(lambda: sol.annuity_factor(rate, periods), "a rate or a period count of the wrong type")


@pytest.mark.parametrize(
    ("rate", "periods", "condition"),
    [
        (ANN_RATE, -1, "negative periods for the due annuity"),
        (ANN_RATE, 12.0, "periods given as a float for the due annuity"),
        (ANN_RATE, True, "periods given as a bool for the due annuity"),
        (ANN_RATE, "5", "periods given as a string for the due annuity"),
        (-1.0, 5, "a rate of -1 for the due annuity, with periods"),
        ("0.05", 5, "a rate given as a string for the due annuity"),
        (None, 5, "a rate of None for the due annuity"),
        (ANN_RATE, None, "periods given as None for the due annuity"),
        (ANN_RATE, False, "periods given as a bool (False) for the due annuity"),
        (-1.0, 0, "a rate of -1 for the due annuity with zero periods"),
        (math.inf, 5, "an infinite rate for the due annuity"),
        (-math.inf, 5, "a rate of minus infinity for the due annuity"),
    ],
)
def test_annuity_due_rejects_invalid_inputs(rate: Any, periods: Any, condition: str) -> None:
    """The due factor is the ordinary factor times (1 + r), so it must refuse exactly what the ordinary one refuses."""
    must_raise(lambda: sol.annuity_due_factor(rate, periods), condition)


def test_perpetuity_factor_is_one_over_the_rate() -> None:
    exact = float(1 / Fraction(PERP_BPS, 10_000))
    assert close(sol.perpetuity_factor(PERP_RATE), exact, 1e-12), (
        "perpetuity_factor must be 1 / rate for a payment of 1 at the end of each period"
    )


def test_perpetuity_factor_accepts_a_rate_of_one_or_more() -> None:
    """The specification requires only r > 0 for the perpetuity, so a rate of 150 % is valid: 1 / 1.5."""
    assert close(sol.perpetuity_factor(1.5), 1 / 1.5, 1e-12), (
        "perpetuity_factor must be 1 / rate for every rate above zero, including rates of one or more"
    )


def test_perpetuity_factor_is_the_value_of_a_long_truncated_sum() -> None:
    """The sum of v^k up to N has the exact error v^N / r; N is chosen so that this error is below 1e-12."""
    r = PERP_RATE
    v = 1 / (1 + r)
    n_terms = math.ceil(math.log(1e-12 * r) / math.log(v)) + 1
    partial = sum(v**k for k in range(1, n_terms + 1))
    assert close(sol.perpetuity_factor(r), partial, 1e-9), (
        "the perpetuity's value is the limit of the partial sums of discount factors: check the 1/r closed form"
    )


def test_perpetuity_partial_sum_identity() -> None:
    """Sum of v^k for k = 1..N equals (1 - v^N) / r exactly, for several N (the finite identity behind 1/r)."""
    r = PERP_RATE
    v = 1 / (1 + r)
    for n in (1, 2, 12, 60, 360):
        partial = sum(v**k for k in range(1, n + 1))
        assert close(partial, (1 - v**n) / r, 1e-12), "the finite partial sum must equal (1 - v^N) / r"


def test_growing_perpetuity_factor_matches_one_over_rate_minus_growth() -> None:
    exact = float(1 / (Fraction(PERP_BPS, 10_000) - Fraction(GROWTH_BPS, 10_000)))
    assert close(sol.growing_perpetuity_factor(PERP_RATE, GROWTH), exact, 1e-12), (
        "growing_perpetuity_factor must be 1 / (rate - growth)"
    )


def test_growing_perpetuity_matches_a_long_truncated_sum() -> None:
    """Payments (1+g)^(k-1) at the end of period k. The tail after N periods is q^N / (r - g), q = (1+g)/(1+r)."""
    r, g = PERP_RATE, GROWTH
    q = (1 + g) / (1 + r)
    n_terms = math.ceil(math.log(1e-10 * (r - g)) / math.log(q)) + 1
    partial = sum(((1 + g) ** (k - 1)) / ((1 + r) ** k) for k in range(1, n_terms + 1))
    assert close(sol.growing_perpetuity_factor(r, g), partial, 1e-8), (
        "the growing perpetuity must equal the sum of (1+g)^(k-1) / (1+r)^k over all periods: check the ratio test"
    )


def test_growing_partial_sum_identity() -> None:
    """Sum of (1+g)^(k-1) v^k for k = 1..N equals (1 - q^N) / (r - g) (the finite identity behind 1/(r-g))."""
    r, g = PERP_RATE, GROWTH
    q = (1 + g) / (1 + r)
    for n in (1, 2, 10, 60):
        partial = sum(((1 + g) ** (k - 1)) / ((1 + r) ** k) for k in range(1, n + 1))
        assert close(partial, (1 - q**n) / (r - g), 1e-12), "the finite partial sum must equal (1 - q^N) / (r - g)"


def test_growing_perpetuity_with_zero_growth_is_the_perpetuity() -> None:
    assert close(sol.growing_perpetuity_factor(PERP_RATE, 0.0), sol.perpetuity_factor(PERP_RATE), 1e-12), (
        "with zero growth the growing perpetuity is the level perpetuity: check the growth term"
    )


# --- level payment and the amortization schedule


def test_level_payment_matches_exact_nearest_cent() -> None:
    assert sol.level_payment_cents(PRINCIPAL, RATE, MONTHS) == EXACT_LEVEL, (
        "level_payment_cents must be the loan times i / (1 - (1+i)^-n), with i = annual rate / 12, to the nearest cent"
    )


def test_level_payment_is_an_integer() -> None:
    value = sol.level_payment_cents(PRINCIPAL, RATE, MONTHS)
    assert isinstance(value, int) and not isinstance(value, bool), "money must be an integer number of cents"


def test_level_payment_zero_rate_is_the_loan_over_the_months() -> None:
    """At a zero rate the payment is the loan over the months, to the nearest cent: 100,000,000 / 12 = 8,333,333.33."""
    assert sol.level_payment_cents(100_000_000, 0, 12) == 8_333_333
    assert sol.level_payment_cents(100, 0.0, 7) == 14
    assert sol.level_payment_cents(PRINCIPAL, 0, MONTHS) == nearest(Fraction(PRINCIPAL, MONTHS))


def test_level_payment_at_a_tiny_rate_is_exact() -> None:
    """At an annual rate of 1e-7 the exact payment is 8,333,333.78 cents: the loan over the months, 8,333,333.33,
    plus a correction of 0.45 cents from the interest. It rounds up to 8,333,334. A rate treated as zero below a
    cutoff returns 8,333,333 and fails the nearest-cent rule."""
    assert sol.level_payment_cents(100_000_000, 1e-7, 12) == 8_333_334, (
        "a small non-zero rate still has interest: the payment must be the exact value, rounded to the nearest cent"
    )


def test_level_payment_below_the_old_cutoffs_is_exact() -> None:
    """At an annual rate of 5e-9 the loan over the months is 36,934.497 cents, and the interest lifts the exact
    payment above the half-cent line, so the nearest cent is 36,935. A rate taken as zero below a cutoff of 1e-8
    returns 36,934 instead. The expected value is recomputed here from the rate as written, in exact arithmetic."""
    i = Fraction("5e-9") / 12
    exact = nearest(Fraction(13_296_419) * i / (1 - (1 + i) ** (-360)))
    assert exact == 36_935
    assert sol.level_payment_cents(13_296_419, 5e-9, 360) == 36_935, (
        "a rate of 5e-9 a year still has interest: the payment must be the exact value, rounded to the nearest cent"
    )


def test_level_payment_accepts_a_term_above_360_months() -> None:
    """The specification gives a lower limit on the term (one month or more) and no upper limit. A 480-month loan of
    100,000 cents at 5 % has the exact payment 482 cents, and its schedule clears to zero in month 480."""
    assert sol.level_payment_cents(100_000, 0.05, 480) == 482, (
        "the term has no upper limit: a 480-month loan is valid and its payment is the exact value"
    )
    rows = schedule(100_000, 0.05, 480)
    assert len(rows) == 480 and rows[-1][0] == 480 and rows[-1][5] == 0, (
        "a 480-month schedule must have 480 rows and close to exactly zero in the last one"
    )


def test_level_payment_and_schedule_accept_a_term_of_1200_months() -> None:
    """The term has no upper limit, so a 1200-month loan of 100,000 cents at 3.84 % is valid. Its monthly rate is
    0.0032 = 2/625, whose denominator is odd, so no interest amount is a half cent; the level payment is 327 cents.
    The schedule must equal the exact schedule row for row, with 1200 rows and an exactly zero last balance."""
    assert sol.level_payment_cents(100_000, 0.0384, 1200) == 327, (
        "the term has no upper limit: a 1200-month loan is valid and its payment is the exact value"
    )
    rows = schedule(100_000, 0.0384, 1200)
    assert len(rows) == 1200 and rows[-1][0] == 1200 and rows[-1][5] == 0, (
        "a 1200-month schedule must have 1200 rows and close to exactly zero in the last one"
    )
    assert rows == exact_rows(100_000, 384, 1200), "the 1200-month schedule disagrees with the exact schedule"


def test_level_payment_tie_goes_up() -> None:
    """A payment of exactly half a cent goes up: 1 cent over 2 months at a zero rate is 0.5 cents, which is 1 cent."""
    assert sol.level_payment_cents(1, 0, 2) == 1, "a tie of half a cent must go up to the next whole cent"
    assert sol.level_payment_cents(1, 0.0, 2) == 1, "a tie of half a cent must go up at a zero rate given as a float"


def test_level_payment_tie_at_a_non_zero_rate_goes_up() -> None:
    """A payment of exactly 4.5 cents goes up to 5. With an annual rate of 6.0 (600 %) the monthly rate is 0.5, so
    a loan of 3 cents over one month is repaid by 3 x 1.5 = 4.5 cents, computed in exact arithmetic."""
    assert sol.level_payment_cents(3, 6.0, 1) == 5, "a payment of exactly half a cent above a whole cent must go up"


@pytest.mark.parametrize(
    ("principal", "annual_rate", "expected"),
    [
        # 0.06 a year is 0.005 a month; one month on 100 cents is exactly 100.5 cents, a tie that goes up to 101.
        # The binary float of 0.06 lies just below the tie, so the rate must be read as the decimal it is written as.
        (100, 0.06, 101),
        # 1.2e-11 a year is 1e-12 a month: the payment is 499999999999 * (1 + 1e-12) cents, which is
        # 499999999999.499999999999 cents, so it rounds down. Exact arithmetic is needed to see the last digits.
        (499_999_999_999, 1.2e-11, 499_999_999_999),
    ],
    ids=["tie-at-six-percent", "half-cent-at-tiny-rate"],
)
def test_level_payment_is_exact_in_the_rate_as_written(principal: int, annual_rate: float, expected: int) -> None:
    assert sol.level_payment_cents(principal, annual_rate, 1) == expected, (
        "level_payment_cents must be exact: the annual rate is read as its decimal, and the cent amount is rounded "
        "once, from the exact value"
    )


def test_schedule_interest_tie_goes_up() -> None:
    """Interest of exactly half a cent goes up. An annual rate of 6.0 (600 %) is a monthly rate of 0.5, so 1 cent
    accrues exactly 0.5 cents in month 1."""
    rows = schedule(1, 6.0, 2)
    assert rows[0][2] == 1, "interest of exactly half a cent must go up to one whole cent"


def test_schedule_interest_just_below_a_half_cent_goes_down() -> None:
    """The other side of the tie: 499 cents at 0.012 a year accrue exactly 0.499 cents in month 1, which rounds down
    to 0. A rule that rounds every fraction of a cent up returns 1 here."""
    assert schedule(499, 0.012, 3)[0][2] == 0, "interest below half a cent must round down to zero cents"


def test_schedule_accepts_one_cent_for_one_month() -> None:
    """The lower boundaries are both valid: a principal of one cent and a term of one month. At a zero rate the one
    row pays the cent and closes at zero, and at 5 % on 1000 cents it pays 1004 cents, its interest of 4 included."""
    assert schedule(1, 0.0, 1) == [(1, 1, 0, 1, 1, 0)], "a one-cent loan over one month is a single row that clears"
    assert schedule(1000, 0.05, 1) == [(1, 1000, 4, 1000, 1004, 0)], (
        "a one-month loan pays its opening balance plus that month's interest, and closes at zero"
    )


def test_schedule_closing_balance_is_never_negative() -> None:
    for period, _opening, _interest, _principal, _payment, closing in schedule(PRINCIPAL, RATE, MONTHS):
        assert closing >= 0, f"period {period}: the closing balance must never be negative"


def test_schedule_interest_is_exact_in_the_rate_as_written() -> None:
    """1000 cents at 0.018 a year accrues exactly 1.5 cents in month 1 (1000 x 0.018 / 12), a tie that goes up to 2.
    The binary float of 0.018 divided by 12 lies just below the tie and would round to 1."""
    assert schedule(1000, 0.018, 2)[0][2] == 2, "monthly interest must be read from the rate as written, exactly"


def test_level_payment_scales_with_the_loan() -> None:
    once = sol.level_payment_cents(PRINCIPAL, RATE, MONTHS)
    twice = sol.level_payment_cents(2 * PRINCIPAL, RATE, MONTHS)
    assert abs(twice - 2 * once) <= 1, "doubling the loan doubles the level payment, to within one cent"


def test_level_payment_rises_with_the_rate() -> None:
    assert sol.level_payment_cents(PRINCIPAL, RATE + 0.01, MONTHS) > sol.level_payment_cents(PRINCIPAL, RATE, MONTHS)


def test_schedule_matches_the_exact_schedule_row_for_row() -> None:
    """Every field of every month equals the exact schedule under the nearest-cent rule (zero tolerance)."""
    rows = schedule(PRINCIPAL, RATE, MONTHS)
    assert len(rows) == len(EXACT), "the schedule must have one row per month of the term"
    for got, want in zip(rows, EXACT, strict=True):
        if got != want:
            names = [n for n, a, b in zip(FIELDS, got, want, strict=True) if a != b]
            pytest.fail(
                f"period {got[0]} disagrees in {', '.join(names)}: check the monthly interest (nearest cent of the "
                "opening balance times the monthly rate) and the last-payment rule"
            )


def test_schedule_matches_the_exact_schedule_for_a_second_instance() -> None:
    rows = schedule(INST2["principal_cents"], INST2["annual_rate"], INST2["months"])
    assert rows == EXACT2, "the schedule for a second loan disagrees with the exact schedule: check the general rule"


def test_schedule_has_the_term_in_months_numbered_from_one() -> None:
    rows = schedule(PRINCIPAL, RATE, MONTHS)
    assert [r[0] for r in rows] == list(range(1, MONTHS + 1)), "periods must run 1 to the number of months"


def test_schedule_opens_at_the_loan() -> None:
    assert schedule(PRINCIPAL, RATE, MONTHS)[0][1] == PRINCIPAL, "month 1 must open at the full loan"


def test_schedule_payment_is_interest_plus_principal() -> None:
    for period, _opening, interest, principal, payment, _closing in schedule(PRINCIPAL, RATE, MONTHS):
        assert payment == interest + principal, f"period {period}: payment must equal interest plus principal"


def test_schedule_closing_balance_is_opening_less_principal() -> None:
    for period, opening, _interest, principal, _payment, closing in schedule(PRINCIPAL, RATE, MONTHS):
        assert closing == opening - principal, f"period {period}: closing balance must be opening less principal"


def test_schedule_balances_chain_from_month_to_month() -> None:
    rows = schedule(PRINCIPAL, RATE, MONTHS)
    for prev, nxt in itertools.pairwise(rows):
        assert nxt[1] == prev[5], f"period {nxt[0]}: the opening balance must be the previous closing balance"


def test_schedule_final_balance_is_exactly_zero() -> None:
    assert schedule(PRINCIPAL, RATE, MONTHS)[-1][5] == 0, "the last closing balance must be exactly zero"


def test_schedule_principal_sums_to_the_loan() -> None:
    total = sum(r[3] for r in schedule(PRINCIPAL, RATE, MONTHS))
    assert total == PRINCIPAL, "the principal column must sum to the loan, exactly"


def test_schedule_total_paid_is_the_loan_plus_the_interest() -> None:
    rows = schedule(PRINCIPAL, RATE, MONTHS)
    paid = sum(r[4] for r in rows)
    interest = sum(r[2] for r in rows)
    assert paid == PRINCIPAL + interest, "total payments must equal the loan plus total interest, exactly"


def test_schedule_pays_the_level_payment_until_the_last_month() -> None:
    level = sol.level_payment_cents(PRINCIPAL, RATE, MONTHS)
    rows = schedule(PRINCIPAL, RATE, MONTHS)
    assert all(r[4] == level for r in rows[:-1]), "every month before the last must pay the level payment"


def test_final_payment_is_within_the_stated_bound() -> None:
    """Each month's interest is taken to the nearest cent, an error of at most half a cent. The final payment
    therefore differs from the level payment by at most n * (1 + i)^n + 1 cents. The bound is loose; the test
    checks the stated rule, not a tighter one."""
    i = RATE / 12
    level = sol.level_payment_cents(PRINCIPAL, RATE, MONTHS)
    last = schedule(PRINCIPAL, RATE, MONTHS)[-1][4]
    bound = MONTHS * (1 + i) ** MONTHS + 1
    assert abs(last - level) <= bound, "the final payment strays from the level payment by more than the stated bound"


def test_interest_is_the_nearest_cent_of_the_opening_balance() -> None:
    i = RATE / 12
    for period, opening, interest, _principal, _payment, _closing in schedule(PRINCIPAL, RATE, MONTHS):
        assert abs(interest - opening * i) <= 0.5 + 1e-9, (
            f"period {period}: interest must be the opening balance times the monthly rate, to the nearest cent"
        )


def test_schedule_at_a_zero_rate_has_no_interest() -> None:
    rows = schedule(PRINCIPAL, 0, 120)
    assert all(r[2] == 0 for r in rows), "a zero rate must give zero interest in every month"
    assert rows[-1][5] == 0 and sum(r[3] for r in rows) == PRINCIPAL, "the zero-rate loan must still clear exactly"
    level = sol.level_payment_cents(PRINCIPAL, 0, 120)
    assert all(r[4] == level for r in rows[:-1]), "a zero-rate loan must pay the level payment until the last month"


def test_schedule_money_fields_are_integers() -> None:
    rows = sol.amortization_schedule(PRINCIPAL, RATE, MONTHS)
    for row in rows[:3]:
        fields(row)  # fails with a message if any field is not an integer
    assert all(isinstance(v, int) for row in rows for v in fields(row)), "every field must be an integer"


def test_schedule_rows_are_a_frozen_dataclass_with_the_named_fields() -> None:
    assert dataclasses.is_dataclass(sol.ScheduleRow), "ScheduleRow must be a dataclass"
    names = tuple(f.name for f in dataclasses.fields(sol.ScheduleRow))
    assert names == FIELDS, "ScheduleRow must have the six fields of the specification, in order"
    row = sol.amortization_schedule(PRINCIPAL, RATE, MONTHS)[0]
    with pytest.raises(dataclasses.FrozenInstanceError):
        untyped_row: Any = row
        untyped_row.payment_cents = 0


# --- invalid inputs fail loudly


def test_annuity_rejects_a_rate_at_or_below_minus_one() -> None:
    must_raise(lambda: sol.annuity_factor(-1.0, 5), "a rate of -1 per period")
    must_raise(lambda: sol.annuity_factor(-1.5, 5), "a rate below -1 per period")
    must_raise(lambda: sol.annuity_factor(-1.5, 0), "a rate below -1 per period with zero periods")
    must_raise(lambda: sol.annuity_due_factor(-1.5, 0), "a rate below -1 per period for the due annuity, zero periods")


def test_annuity_rejects_negative_or_fractional_periods() -> None:
    must_raise(lambda: sol.annuity_factor(0.01, -1), "negative periods")
    float_periods: Any = 12.0
    must_raise(lambda: sol.annuity_factor(0.01, float_periods), "periods given as a float")
    must_raise(lambda: sol.annuity_factor(0.01, True), "periods given as a bool")


def test_annuity_rejects_non_finite_rates() -> None:
    must_raise(lambda: sol.annuity_factor(math.nan, 5), "a NaN rate")
    must_raise(lambda: sol.annuity_factor(math.inf, 5), "an infinite rate")
    must_raise(lambda: sol.annuity_due_factor(math.nan, 5), "a NaN rate for the due annuity")


def test_perpetuity_rejects_a_zero_or_negative_rate() -> None:
    must_raise(lambda: sol.perpetuity_factor(0.0), "a zero rate: the value is not finite")
    must_raise(lambda: sol.perpetuity_factor(-0.02), "a negative rate")


def test_perpetuity_rejects_a_non_finite_rate() -> None:
    must_raise(lambda: sol.perpetuity_factor(math.nan), "a NaN rate")


@pytest.mark.parametrize(
    ("rate", "condition"),
    [
        (math.inf, "an infinite rate"),
        (-math.inf, "a rate of minus infinity"),
        ("0.05", "a rate given as a string"),
        (" 0.05", "a padded rate given as a string"),
        ("", "an empty rate string"),
        (None, "a rate of None"),
    ],
)
def test_perpetuity_rejects_non_finite_and_wrong_type_rates(rate: Any, condition: str) -> None:
    must_raise(lambda: sol.perpetuity_factor(rate), condition)


def test_perpetuity_accepts_a_tiny_positive_rate() -> None:
    """The lower boundary is open at zero: 10^-12 is valid and its value is 10^12."""
    assert close(sol.perpetuity_factor(1e-12), 1e12, 1e-9), (
        "a positive rate of 1e-12 is valid: the perpetuity's value is 1 / rate"
    )


@pytest.mark.parametrize(
    ("call", "condition"),
    [
        (lambda: sol.annuity_factor(True, 5), "a boolean rate for the annuity"),
        (lambda: sol.annuity_factor(False, 5), "a boolean (False) rate for the annuity"),
        (lambda: sol.annuity_due_factor(True, 5), "a boolean rate for the annuity due"),
        (lambda: sol.perpetuity_factor(True), "a boolean rate for the perpetuity"),
        (lambda: sol.perpetuity_factor(False), "a boolean (False) rate for the perpetuity"),
        (lambda: sol.growing_perpetuity_factor(True, 0.01), "a boolean rate for the growing perpetuity"),
        (lambda: sol.growing_perpetuity_factor(0.05, True), "a boolean growth rate"),
        (lambda: sol.growing_perpetuity_factor(0.05, False), "a boolean (False) growth rate"),
        (lambda: sol.level_payment_cents(1000, True, 12), "a boolean annual rate for the level payment"),
        (lambda: sol.level_payment_cents(True, 0.05, 12), "a boolean principal for the level payment"),
        (lambda: sol.level_payment_cents(1000, 0.05, False), "a boolean term for the level payment"),
        (lambda: sol.amortization_schedule(1000, True, 12), "a boolean annual rate for the schedule"),
        (lambda: sol.amortization_schedule(True, 0.05, 12), "a boolean principal for the schedule"),
        (lambda: sol.amortization_schedule(1000, 0.05, False), "a boolean term for the schedule"),
    ],
)
def test_booleans_are_rejected_where_a_number_is_meant(call: Callable[[], object], condition: str) -> None:
    """A boolean is not a number: True would be read as 1 and False as 0, so every rate and principal raises."""
    must_raise(call, condition)


def test_growing_perpetuity_rejects_growth_equal_to_the_rate() -> None:
    must_raise(lambda: sol.growing_perpetuity_factor(PERP_RATE, PERP_RATE), "growth equal to the rate")


def test_growing_perpetuity_rejects_growth_above_the_rate() -> None:
    must_raise(lambda: sol.growing_perpetuity_factor(0.03, 0.05), "growth above the rate")


def test_growing_perpetuity_rejects_a_non_positive_rate() -> None:
    must_raise(lambda: sol.growing_perpetuity_factor(0.0, -0.01), "a zero rate")
    must_raise(lambda: sol.growing_perpetuity_factor(-0.02, -0.05), "a negative rate")


def test_growing_perpetuity_rejects_growth_at_or_below_minus_one() -> None:
    must_raise(lambda: sol.growing_perpetuity_factor(0.05, -1.0), "growth of -100 %")


def test_growing_perpetuity_rejects_non_finite_inputs() -> None:
    must_raise(lambda: sol.growing_perpetuity_factor(math.inf, 0.01), "an infinite rate")
    must_raise(lambda: sol.growing_perpetuity_factor(0.05, math.nan), "a NaN growth rate")
    must_raise(lambda: sol.growing_perpetuity_factor(0.05, math.inf), "an infinite growth rate")


def test_growing_perpetuity_rejects_growth_below_minus_one() -> None:
    """The lower bound on growth is open at -1: a growth of -150 % per period is refused, not evaluated."""
    must_raise(lambda: sol.growing_perpetuity_factor(0.05, -1.5), "growth of -150 %")


@pytest.mark.parametrize(
    ("rate", "growth", "condition"),
    [
        ("0.05", 0.02, "a rate given as a string"),
        (0.05, "0.02", "a growth rate given as a string"),
        (" 0.05", 0.02, "a padded rate given as a string"),
        (0.05, " 0.02", "a padded growth rate given as a string"),
        (None, 0.02, "a rate of None"),
        (0.05, None, "a growth rate of None"),
    ],
)
def test_growing_perpetuity_rejects_wrong_types(rate: Any, growth: Any, condition: str) -> None:
    must_raise(lambda: sol.growing_perpetuity_factor(rate, growth), condition)


def test_growing_perpetuity_accepts_growth_just_inside_both_bounds() -> None:
    """Both bounds are open, and each is valid up to its edge. Growth -0.999 is above -1; growth 0.0499 is below 0.05.
    The values are 1 / (0.05 + 0.999) and 1 / (0.05 - 0.0499) = 10000."""
    assert close(sol.growing_perpetuity_factor(0.05, -0.999), 1 / (0.05 + 0.999), 1e-12), (
        "growth above -1 is valid: the value is 1 / (rate - growth)"
    )
    assert close(sol.growing_perpetuity_factor(0.05, 0.0499), 10_000.0, 1e-9), (
        "growth just below the rate is valid: the value is 1 / (rate - growth), which is large but finite"
    )


def test_growing_perpetuity_with_negative_growth_is_one_over_rate_minus_growth() -> None:
    """A negative growth lowers the value: 1 / (0.05 - (-0.02)) = 1 / 0.07, not 1 / (0.05 - 0.02)."""
    assert close(sol.growing_perpetuity_factor(0.05, -0.02), 1 / 0.07, 1e-12), (
        "with negative growth the value is 1 / (rate - growth), so the denominator grows"
    )


def test_growing_perpetuity_moves_the_right_way() -> None:
    """A higher growth raises the value of a growing perpetuity, and the value is finite below the rate."""
    low = sol.growing_perpetuity_factor(0.05, -0.02)
    mid = sol.growing_perpetuity_factor(0.05, 0.02)
    high = sol.growing_perpetuity_factor(0.05, 0.03)
    assert low < mid < high, "the growing perpetuity must rise with the growth rate"


@pytest.mark.parametrize(
    ("principal", "rate", "months"),
    [
        (0, 0.05, 12),
        (-100, 0.05, 12),
        (1000.0, 0.05, 12),
        (True, 0.05, 12),
        (1000, -0.01, 12),
        (1000, math.nan, 12),
        (1000, math.inf, 12),
        (1000, 0.05, 0),
        (1000, 0.05, -3),
        (1000, 0.05, 12.0),
        (1000, 0.05, True),
        (1000, 0.05, False),
        (1000, 0.05, 12.5),
        (1000, 0.05, -1),
        (-1, 0.05, 12),
        (1000, -1e-12, 12),
        (1000, -math.inf, 12),
        (False, 0.05, 12),
        ("1000", 0.05, 12),
        (" 1000", 0.05, 12),
        (None, 0.05, 12),
        (1000, "0.05", 12),
        (1000, None, 12),
        (1000, 0.05, "12"),
        (1000, 0.05, None),
    ],
)
def test_level_payment_rejects_invalid_loans(principal: Any, rate: Any, months: Any) -> None:
    must_raise(lambda: sol.level_payment_cents(principal, rate, months), "an invalid loan")


@pytest.mark.parametrize(
    ("principal", "rate", "months"),
    [
        (0, 0.05, 12),
        (-100, 0.05, 12),
        (1000.0, 0.05, 12),
        (True, 0.05, 12),
        (1000, -0.01, 12),
        (1000, math.inf, 12),
        (1000, 0.05, 0),
        (1000, 0.05, -3),
        (1000, 0.05, 2.0),
        (1000, 0.05, True),
        (1000, 0.05, False),
        (1000, 0.05, 12.5),
        ("1000", 0.05, 12),
        (" 1000", 0.05, 12),
        (None, 0.05, 12),
        (1000, "0.05", 12),
        (1000, None, 12),
        (1000, 0.05, "12"),
        (1000, 0.05, None),
        (1000, math.nan, 12),
        (1000, -math.inf, 12),
        (1000, -1e-12, 12),
        (1000, 0.05, -1),
        (-1, 0.05, 12),
        (False, 0.05, 12),
    ],
)
def test_schedule_rejects_invalid_loans(principal: Any, rate: Any, months: Any) -> None:
    must_raise(lambda: sol.amortization_schedule(principal, rate, months), "an invalid loan")


def test_invalid_input_message_names_the_condition() -> None:
    with pytest.raises(ValueError, match=r"\S"):
        sol.perpetuity_factor(0.0)


# --- isolated boundary checks: one condition per test, in both directions where an inequality is involved


def test_annuity_factor_refuses_rate_of_minus_one_even_with_zero_periods() -> None:
    """The rate check applies whatever the number of periods: at -1 the factor is refused even when there are none."""
    must_raise(lambda: sol.annuity_factor(-1.0, 0), "a rate of -1 with zero periods: the rate check still applies")
    must_raise(lambda: sol.annuity_due_factor(-1.0, 0), "a rate of -1 with zero periods for the due annuity")


def test_annuity_factor_accepts_rate_just_above_minus_one_with_zero_periods() -> None:
    """The other side of the boundary: at -0.999 with zero periods the factor is the float 0."""
    zero = sol.annuity_factor(-0.999, 0)
    assert isinstance(zero, float) and zero == 0.0, "a rate above -1 with zero periods gives the float 0"


def test_annuity_factor_refuses_a_non_finite_rate_even_with_zero_periods() -> None:
    must_raise(lambda: sol.annuity_factor(math.nan, 0), "a NaN rate with zero periods")
    must_raise(lambda: sol.annuity_factor(math.inf, 0), "an infinite rate with zero periods")
    must_raise(lambda: sol.annuity_factor(-math.inf, 5), "a rate of minus infinity")


def test_annuity_factor_zero_rate_with_zero_periods_is_float_zero() -> None:
    zero = sol.annuity_factor(0, 0)
    assert isinstance(zero, float) and zero == 0.0, "annuity_factor(0, 0) must be the float 0.0"
    due = sol.annuity_due_factor(0, 0)
    assert isinstance(due, float) and due == 0.0, "annuity_due_factor(0, 0) must be the float 0.0"


def test_annuity_factor_one_period_is_one_discounted_payment() -> None:
    """With one period the factor is the single discount factor v = 1/(1+r), and at a zero rate it is 1."""
    assert close(sol.annuity_factor(ANN_RATE, 1), 1 / (1 + ANN_RATE), 1e-12), "one period is one discounted payment"
    assert sol.annuity_factor(0, 1) == 1.0, "one period at a zero rate is a factor of 1"


def test_perpetuity_refuses_a_rate_just_below_zero() -> None:
    must_raise(lambda: sol.perpetuity_factor(-1e-12), "a rate of -1e-12: the rate must be above zero")


def test_perpetuity_value_moves_the_right_way() -> None:
    """A higher rate lowers the value of a perpetuity: 1/0.05 = 20 and 1/0.06 is about 16.7."""
    assert sol.perpetuity_factor(0.05) > sol.perpetuity_factor(0.06), "a higher rate must lower the perpetuity"


def test_growing_perpetuity_refuses_growth_just_above_the_rate() -> None:
    must_raise(lambda: sol.growing_perpetuity_factor(0.05, 0.0501), "growth 0.0501 just above a rate of 0.05")


def test_growing_perpetuity_refuses_a_nan_rate() -> None:
    must_raise(lambda: sol.growing_perpetuity_factor(math.nan, 0.01), "a NaN rate")


def test_growing_perpetuity_refuses_minus_infinite_growth() -> None:
    must_raise(lambda: sol.growing_perpetuity_factor(0.05, -math.inf), "growth of minus infinity")


def test_growing_perpetuity_refuses_a_rate_just_below_zero() -> None:
    must_raise(lambda: sol.growing_perpetuity_factor(-1e-12, -0.5), "a rate of -1e-12 with any growth")


def test_growing_perpetuity_accepts_a_tiny_positive_rate() -> None:
    """The other side: a rate of 1e-12 is valid with growth -0.5, and the value is 1 / (rate - growth)."""
    assert close(sol.growing_perpetuity_factor(1e-12, -0.5), 1 / (1e-12 + 0.5), 1e-12), (
        "a positive rate of 1e-12 is valid: the value is 1 / (rate - growth)"
    )


def test_level_payment_accepts_a_one_cent_loan_over_one_month() -> None:
    """One cent over one month: at a zero rate the payment is 1 cent, and at 5 % it is 1 cent plus a fraction that
    rounds down, so it is 1 cent in both cases."""
    assert sol.level_payment_cents(1, 0, 1) == 1, "a one-cent loan over one month at a zero rate is one cent"
    assert sol.level_payment_cents(1, 0.05, 1) == 1, "a one-cent loan over one month at 5 % is one cent"


def test_level_payment_rounds_a_below_half_cent_down() -> None:
    """499 cents over 1000 months at a zero rate is 0.499 cents a month: it rounds down to 0 (a ceiling gives 1)."""
    assert sol.level_payment_cents(499, 0, 1000) == 0, "a payment below half a cent must round down to zero cents"


def test_level_payment_rejects_a_principal_of_minus_one() -> None:
    must_raise(lambda: sol.level_payment_cents(-1, 0.05, 12), "a principal of -1 cent")
    must_raise(lambda: sol.amortization_schedule(-1, 0.05, 12), "a principal of -1 cent for the schedule")


def test_term_of_one_month_is_accepted_at_a_nonzero_rate() -> None:
    """The lower boundary of the term is one month, valid at a non-zero rate too: one row that clears."""
    rows = schedule(10_000, 0.12, 1)
    assert rows == [(1, 10_000, 100, 10_000, 10_100, 0)], "a one-month loan pays its balance plus one month of interest"


# --- purity and imports


def test_functions_do_not_print_or_warn() -> None:
    """No function prints or warns, on a valid input or on an invalid one (each invalid call must raise ValueError)."""
    float_periods: Any = 12.0
    invalid_calls: tuple[Callable[[], object], ...] = (
        lambda: sol.annuity_factor(-1.5, 5),
        lambda: sol.annuity_factor(0.01, float_periods),
        lambda: sol.annuity_due_factor(-1.5, 0),
        lambda: sol.perpetuity_factor(0.0),
        lambda: sol.growing_perpetuity_factor(0.03, 0.05),
        lambda: sol.level_payment_cents(0, RATE, MONTHS),
        lambda: sol.level_payment_cents(PRINCIPAL, RATE, 0),
        lambda: sol.amortization_schedule(PRINCIPAL, True, MONTHS),
    )
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        sol.annuity_factor(ANN_RATE, ANN_N)
        sol.annuity_due_factor(ANN_RATE, ANN_N)
        sol.perpetuity_factor(PERP_RATE)
        sol.growing_perpetuity_factor(PERP_RATE, GROWTH)
        sol.level_payment_cents(PRINCIPAL, RATE, MONTHS)
        sol.amortization_schedule(PRINCIPAL, RATE, 12)
        for invalid in invalid_calls:
            must_raise(invalid, "an invalid input in the purity check")
    assert buffer.getvalue() == "", "no function may print, on a valid or an invalid input"
    assert not caught, "no function may warn, on a valid or an invalid input"


def test_module_uses_only_the_standard_library() -> None:
    source = Path(sol.__file__).read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(source)):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            names = [node.module.split(".")[0]]
        for name in names:
            assert name in sys.stdlib_module_names, f"import of {name!r}: the project uses the standard library only"


def test_the_engine_is_not_a_lookup_table() -> None:
    """A second loan with a different term, rate and principal gets its own exact schedule."""
    assert sol.level_payment_cents(INST2["principal_cents"], INST2["annual_rate"], INST2["months"]) == exact_level(
        INST2["principal_cents"], INST2["annual_bps"], INST2["months"]
    ), "the level payment for a second loan disagrees with the exact rule"

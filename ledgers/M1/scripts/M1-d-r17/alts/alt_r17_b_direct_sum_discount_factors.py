"""Reference solution for the M1 project: annuity_engine.py, the annuity and mortgage engine.

It implements the contract in project.html, section "Rung 3 · Specification". Standard library only.

Conventions (binding, from the project specification):

* rates are per period as decimals (0.005 is half a percent); the monthly rate of a loan is the nominal annual rate
  divided by 12, never an effective conversion;
* money is integer cents; a cent amount that is not exact is taken to the nearest cent, a tie going up;
* a zero rate is handled explicitly: the annuity factor is the number of periods, the level payment is the loan
  divided by the number of months;
* invalid inputs raise ValueError; no function prints or warns.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class ScheduleRow:
    """One month of an amortization schedule. Every money field is an integer number of cents."""

    period: int
    opening_cents: int
    interest_cents: int
    principal_cents: int
    payment_cents: int
    closing_cents: int


def _real(name: str, value: object) -> float:
    """A finite real number, not a bool; anything else raises ValueError."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _periods(name: str, value: object) -> int:
    """A whole number of periods, zero or more; a float such as 12.0 is rejected."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a whole number of periods, zero or more")
    return value


def _months(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("months must be a whole number of months, one or more")
    return value


def _principal(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("principal_cents must be a whole number of cents, one or more")
    return value


def _annual_rate(value: object) -> float:
    rate = _real("annual_rate", value)
    if rate < 0:
        raise ValueError("annual_rate must be zero or positive: the engine takes no negative loan rates")
    return rate


def _exact_rate(annual_rate: float) -> Fraction:
    """The annual rate as the decimal it was written as (its shortest repr), in exact rational arithmetic."""
    return Fraction(repr(annual_rate))


def _nearest_cent(amount: Fraction) -> int:
    """The nearest whole cent of a non-negative exact amount, a tie going up: floor(amount + 1/2)."""
    return math.floor(amount + Fraction(1, 2))


def annuity_factor(rate: float, periods: int) -> float:
    """Present value of 1 paid at the end of each of `periods` periods, at the per-period rate `rate`.

    The factor is (1 - (1 + rate)^-periods) / rate. A zero rate gives `periods`; zero periods give 0.
    """
    r = _real("rate", rate)
    n = _periods("periods", periods)
    if r <= -1:
        raise ValueError("rate must be greater than -1 per period")
    if n == 0:
        return 0.0
    if r == 0:
        return float(n)
    return -math.expm1(-n * math.log1p(r)) / r


def annuity_due_factor(rate: float, periods: int) -> float:
    """Present value of 1 paid at the start of each of `periods` periods: the ordinary factor times (1 + rate)."""
    return annuity_factor(rate, periods) * (1 + _real("rate", rate))


def perpetuity_factor(rate: float) -> float:
    """Present value of 1 paid at the end of every period, forever, at a positive per-period rate: 1 / rate."""
    r = _real("rate", rate)
    if r <= 0:
        raise ValueError("a perpetuity needs a rate above zero: at a rate of zero or less its value is not finite")
    return 1 / r


def growing_perpetuity_factor(rate: float, growth: float) -> float:
    """Present value of a payment of 1 at the end of period 1, growing by (1 + growth) each period, forever.

    The value is 1 / (rate - growth). It requires a positive rate and -1 < growth < rate.
    """
    r = _real("rate", rate)
    g = _real("growth", growth)
    if r <= 0:
        raise ValueError("the rate must be above zero")
    if g <= -1:
        raise ValueError("growth must be above -1")
    if g >= r:
        raise ValueError("growth must be below the rate: at growth at or above the rate the value is not finite")
    return 1 / (r - g)


def level_payment_cents(principal_cents: int, annual_rate: float, months: int) -> int:
    """The level monthly payment, in cents, that repays the loan in `months` months.

    The payment is the loan times i / (1 - (1 + i)^-months) with i = annual_rate / 12, to the nearest cent.
    At a zero rate it is the loan divided by the months, to the nearest cent. The arithmetic is exact, so a
    payment of exactly half a cent is detected and goes up.
    """
    principal = _principal(principal_cents)
    i = _exact_rate(_annual_rate(annual_rate)) / 12
    n = _months(months)
    if i == 0:
        return _nearest_cent(Fraction(principal, n))
    denom = sum(((1 + i) ** -k for k in range(1, n + 1)), Fraction(0))
    return _nearest_cent(principal / denom)


def amortization_schedule(principal_cents: int, annual_rate: float, months: int) -> tuple[ScheduleRow, ...]:
    """The full monthly schedule of a level-payment loan, one row per month, in integer cents.

    Each month's interest is the opening balance times i, to the nearest cent. Months 1 to n-1 pay the level
    payment. Month n pays the opening balance plus its interest, so the closing balance is exactly zero.
    """
    principal = _principal(principal_cents)
    rate = _annual_rate(annual_rate)
    n = _months(months)
    i = _exact_rate(rate) / 12
    payment = level_payment_cents(principal, rate, n)
    rows: list[ScheduleRow] = []
    opening = principal
    for period in range(1, n + 1):
        interest = _nearest_cent(opening * i)
        paid = payment if period < n else opening + interest
        principal_paid = paid - interest
        closing = opening - principal_paid
        rows.append(ScheduleRow(period, opening, interest, principal_paid, paid, closing))
        opening = closing
    return tuple(rows)

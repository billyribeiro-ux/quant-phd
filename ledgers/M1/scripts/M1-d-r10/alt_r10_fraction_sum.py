"""Correct alternative (round 10): exact rational arithmetic on the rate as written; the level payment is L over the exact sum of discount factors."""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class ScheduleRow:
    period: int
    opening_cents: int
    interest_cents: int
    principal_cents: int
    payment_cents: int
    closing_cents: int


def _real(name: str, value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a real number")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number


def _whole(value: object, low: int, what: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < low:
        raise ValueError(f"{what} must be a whole number, {low} or more")
    return value


def _rate_exact(value: object) -> Fraction:
    rate = _real("annual_rate", value)
    if rate < 0:
        raise ValueError("annual_rate must be zero or positive")
    return Fraction(repr(rate))


def _round(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def annuity_factor(rate: float, periods: int) -> float:
    r = _real("rate", rate)
    n = _whole(periods, 0, "periods")
    if r <= -1:
        raise ValueError("rate must be greater than -1 per period")
    if n == 0:
        return 0.0
    if r == 0:
        return float(n)
    v = 1 / (1 + r)
    return sum(v**k for k in range(1, n + 1))


def annuity_due_factor(rate: float, periods: int) -> float:
    return annuity_factor(rate, periods) * (1 + _real("rate", rate))


def perpetuity_factor(rate: float) -> float:
    r = _real("rate", rate)
    if r <= 0:
        raise ValueError("a perpetuity needs a rate above zero")
    return 1 / r


def growing_perpetuity_factor(rate: float, growth: float) -> float:
    r = _real("rate", rate)
    g = _real("growth", growth)
    if r <= 0:
        raise ValueError("the rate must be above zero")
    if g <= -1:
        raise ValueError("growth must be above -1")
    if g >= r:
        raise ValueError("growth must be below the rate")
    return 1 / (r - g)


def _exact_payment(principal: int, i: Fraction, n: int) -> Fraction:
    if i == 0:
        return Fraction(principal, n)
    v = 1 / (1 + i)
    annuity = sum((v**k for k in range(1, n + 1)), Fraction(0))
    return principal / annuity


def level_payment_cents(principal_cents: int, annual_rate: float, months: int) -> int:
    principal = _whole(principal_cents, 1, "principal_cents")
    i = _rate_exact(annual_rate) / 12
    n = _whole(months, 1, "months")
    return _round(_exact_payment(principal, i, n))


def amortization_schedule(principal_cents: int, annual_rate: float, months: int) -> tuple[ScheduleRow, ...]:
    principal = _whole(principal_cents, 1, "principal_cents")
    i = _rate_exact(annual_rate) / 12
    n = _whole(months, 1, "months")
    payment = _round(_exact_payment(principal, i, n))
    rows: list[ScheduleRow] = []
    opening = principal
    for period in range(1, n + 1):
        interest = _round(opening * i)
        paid = payment if period < n else opening + interest
        principal_paid = paid - interest
        closing = opening - principal_paid
        rows.append(ScheduleRow(period, opening, interest, principal_paid, paid, closing))
        opening = closing
    return tuple(rows)

"""ddm_value discounts the terminal value by (1+r) to the power N-1"""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction


def gordon_value(d1: Fraction, r: Fraction, g: Fraction) -> Fraction:
    if d1 < 0:
        raise ValueError("d1 must be non-negative")
    if r <= g:
        raise ValueError("r must be strictly greater than g")
    return d1 / (r - g)


def ddm_value(dividends: Sequence[Fraction], r: Fraction, g: Fraction) -> Fraction:
    if not dividends:
        raise ValueError("dividends sequence must not be empty")
    if any(d < 0 for d in dividends):
        raise ValueError("dividends must be non-negative")
    if r <= g:
        raise ValueError("r must be strictly greater than g")
    if r <= -1:
        raise ValueError("r must be strictly greater than -1")

    factor = Fraction(1) + r
    disc = Fraction(1)
    pv = Fraction(0)
    for d in dividends:
        disc *= factor
        pv += d / disc

    n = len(dividends)
    terminal_d = dividends[-1] * (Fraction(1) + g)
    tv = terminal_d / (r - g)
    # Error: discounts terminal value by factor**(n-1) instead of factor**n
    pv_tv = tv / (factor ** (n - 1))
    return pv + pv_tv


def fcfe_value_per_share(fcfe: Sequence[Fraction], shares: Fraction, r: Fraction, g: Fraction) -> Fraction:
    if not fcfe:
        raise ValueError("fcfe sequence must not be empty")
    if shares <= 0:
        raise ValueError("shares count must be strictly positive")
    if r <= g:
        raise ValueError("r must be strictly greater than g")
    if r <= -1:
        raise ValueError("r must be strictly greater than -1")

    factor = Fraction(1) + r
    disc = Fraction(1)
    pv = Fraction(0)
    for f in fcfe:
        disc *= factor
        pv += f / disc

    n = len(fcfe)
    terminal_fcfe = fcfe[-1] * (Fraction(1) + g)
    tv = terminal_fcfe / (r - g)
    pv_tv = tv / (factor**n)
    total_equity = pv + pv_tv
    return total_equity / shares


def residual_income_value(
    book_value_0: Fraction, earnings: Sequence[Fraction], dividends: Sequence[Fraction], r: Fraction
) -> Fraction:
    if not earnings:
        raise ValueError("earnings sequence must not be empty")
    if len(earnings) != len(dividends):
        raise ValueError("earnings and dividends must have the same length")
    if r <= -1:
        raise ValueError("r must be strictly greater than -1")

    factor = Fraction(1) + r
    disc = Fraction(1)
    pv_ri = Fraction(0)
    b_prev = book_value_0

    for ni, d in zip(earnings, dividends, strict=True):
        ri = ni - r * b_prev
        disc *= factor
        pv_ri += ri / disc
        b_prev = b_prev + ni - d

    return book_value_0 + pv_ri


def scenario_price_target_cents(scenarios: Sequence[tuple[Fraction, int]]) -> int:
    if not scenarios:
        raise ValueError("scenarios sequence must not be empty")

    total_prob = Fraction(0)
    expected_cents = Fraction(0)

    for p, v in scenarios:
        if p < 0:
            raise ValueError("probability must be non-negative")
        if v < 0:
            raise ValueError("scenario value must be non-negative")
        total_prob += p
        expected_cents += p * v

    if total_prob != Fraction(1):
        raise ValueError("probabilities must sum to exactly 1")

    num = 2 * expected_cents.numerator + expected_cents.denominator
    den = 2 * expected_cents.denominator
    return num // den

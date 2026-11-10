"""Alternative implementation 1: Procedural loops with local discount factor."""

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

    val = Fraction(0)
    df = Fraction(1)
    one_plus_r = Fraction(1) + r
    for d in dividends:
        df /= one_plus_r
        val += d * df

    tv = (dividends[-1] * (Fraction(1) + g)) / (r - g)
    val += tv * df
    return val


def fcfe_value_per_share(fcfe: Sequence[Fraction], shares: Fraction, r: Fraction, g: Fraction) -> Fraction:
    if not fcfe:
        raise ValueError("fcfe sequence must not be empty")
    if shares <= 0:
        raise ValueError("shares count must be strictly positive")
    if r <= g:
        raise ValueError("r must be strictly greater than g")
    if r <= -1:
        raise ValueError("r must be strictly greater than -1")

    val = Fraction(0)
    df = Fraction(1)
    one_plus_r = Fraction(1) + r
    for f in fcfe:
        df /= one_plus_r
        val += f * df

    tv = (fcfe[-1] * (Fraction(1) + g)) / (r - g)
    val += tv * df
    return val / shares


def residual_income_value(
    book_value_0: Fraction, earnings: Sequence[Fraction], dividends: Sequence[Fraction], r: Fraction
) -> Fraction:
    if not earnings:
        raise ValueError("earnings sequence must not be empty")
    if len(earnings) != len(dividends):
        raise ValueError("earnings and dividends must have the same length")
    if r <= -1:
        raise ValueError("r must be strictly greater than -1")

    val = book_value_0
    b = book_value_0
    df = Fraction(1)
    one_plus_r = Fraction(1) + r
    for i in range(len(earnings)):
        df /= one_plus_r
        ri = earnings[i] - r * b
        val += ri * df
        b = b + earnings[i] - dividends[i]
    return val


def scenario_price_target_cents(scenarios: Sequence[tuple[Fraction, int]]) -> int:
    if not scenarios:
        raise ValueError("scenarios sequence must not be empty")

    tot_p = Fraction(0)
    expected = Fraction(0)
    for p, v in scenarios:
        if p < 0 or v < 0:
            raise ValueError("probability and value must be non-negative")
        tot_p += p
        expected += p * v
    if tot_p != Fraction(1):
        raise ValueError("probabilities must sum to 1")

    half = Fraction(1, 2)
    return int((expected + half).numerator // (expected + half).denominator)

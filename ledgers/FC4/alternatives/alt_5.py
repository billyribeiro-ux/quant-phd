"""Alternative implementation 5: Generator and math.floor style for half-up rounding."""

from __future__ import annotations

import math
from collections.abc import Sequence
from fractions import Fraction


def gordon_value(d1: Fraction, r: Fraction, g: Fraction) -> Fraction:
    if d1 < 0 or r <= g:
        raise ValueError("invalid inputs")
    return d1 / (r - g)


def ddm_value(dividends: Sequence[Fraction], r: Fraction, g: Fraction) -> Fraction:
    if not dividends or any(d < 0 for d in dividends) or r <= g or r <= -1:
        raise ValueError("invalid inputs")

    one_plus_r = Fraction(1) + r
    n = len(dividends)
    pv_stream = sum((d / (one_plus_r**t) for t, d in enumerate(dividends, 1)), Fraction(0))
    tv = (dividends[-1] * (Fraction(1) + g)) / (r - g)
    return pv_stream + tv / (one_plus_r**n)


def fcfe_value_per_share(fcfe: Sequence[Fraction], shares: Fraction, r: Fraction, g: Fraction) -> Fraction:
    if not fcfe or shares <= 0 or r <= g or r <= -1:
        raise ValueError("invalid inputs")

    one_plus_r = Fraction(1) + r
    n = len(fcfe)
    pv_stream = sum((f / (one_plus_r**t) for t, f in enumerate(fcfe, 1)), Fraction(0))
    tv = (fcfe[-1] * (Fraction(1) + g)) / (r - g)
    return (pv_stream + tv / (one_plus_r**n)) / shares


def residual_income_value(
    book_value_0: Fraction, earnings: Sequence[Fraction], dividends: Sequence[Fraction], r: Fraction
) -> Fraction:
    if not earnings or len(earnings) != len(dividends) or r <= -1:
        raise ValueError("invalid inputs")

    one_plus_r = Fraction(1) + r

    def generate_ri() -> list[Fraction]:
        b = book_value_0
        out: list[Fraction] = []
        for ni, d in zip(earnings, dividends, strict=True):
            out.append(ni - r * b)
            b = b + ni - d
        return out

    ris = generate_ri()
    pv_ri = sum((ri / (one_plus_r**t) for t, ri in enumerate(ris, 1)), Fraction(0))
    return book_value_0 + pv_ri


def scenario_price_target_cents(scenarios: Sequence[tuple[Fraction, int]]) -> int:
    if not scenarios or any(p < 0 or v < 0 for p, v in scenarios):
        raise ValueError("invalid inputs")
    if sum((p for p, _ in scenarios), Fraction(0)) != Fraction(1):
        raise ValueError("probabilities must sum to 1")

    ev = sum((p * v for p, v in scenarios), Fraction(0))
    # math.floor on exact Fraction shifted by 1/2
    shifted = ev + Fraction(1, 2)
    return math.floor(shifted.numerator / shifted.denominator)

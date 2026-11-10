"""Alternative implementation 4: Backward recursion style for DDM and FCFE."""

from __future__ import annotations

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
    # Terminal value at horizon N
    terminal_d = dividends[-1] * (Fraction(1) + g)
    v_curr = terminal_d / (r - g)

    # Backward recursion: V_{t-1} = (D_t + V_t) / (1 + r)
    for d in reversed(dividends):
        v_curr = (d + v_curr) / one_plus_r
    return v_curr


def fcfe_value_per_share(fcfe: Sequence[Fraction], shares: Fraction, r: Fraction, g: Fraction) -> Fraction:
    if not fcfe or shares <= 0 or r <= g or r <= -1:
        raise ValueError("invalid inputs")

    one_plus_r = Fraction(1) + r
    terminal_f = fcfe[-1] * (Fraction(1) + g)
    v_curr = terminal_f / (r - g)

    for f in reversed(fcfe):
        v_curr = (f + v_curr) / one_plus_r
    return v_curr / shares


def residual_income_value(
    book_value_0: Fraction, earnings: Sequence[Fraction], dividends: Sequence[Fraction], r: Fraction
) -> Fraction:
    if not earnings or len(earnings) != len(dividends) or r <= -1:
        raise ValueError("invalid inputs")

    one_plus_r = Fraction(1) + r
    # Dictionary keyed book roll
    books: dict[int, Fraction] = {0: book_value_0}
    for t in range(1, len(earnings) + 1):
        books[t] = books[t - 1] + earnings[t - 1] - dividends[t - 1]

    pv_ri = Fraction(0)
    for t in range(1, len(earnings) + 1):
        ri = earnings[t - 1] - r * books[t - 1]
        pv_ri += ri / (one_plus_r**t)
    return book_value_0 + pv_ri


def scenario_price_target_cents(scenarios: Sequence[tuple[Fraction, int]]) -> int:
    if not scenarios or any(p < 0 or v < 0 for p, v in scenarios):
        raise ValueError("invalid inputs")
    p_sum = sum((p for p, _ in scenarios), Fraction(0))
    if p_sum != Fraction(1):
        raise ValueError("probabilities must sum to 1")

    ev = sum((p * v for p, v in scenarios), Fraction(0))
    return int((ev + Fraction(1, 2)).numerator // (ev + Fraction(1, 2)).denominator)

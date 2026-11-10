"""Alternative implementation 2: Functional itertools and sum over zip."""

from __future__ import annotations

import itertools
from collections.abc import Sequence
from fractions import Fraction


def gordon_value(d1: Fraction, r: Fraction, g: Fraction) -> Fraction:
    if d1 < 0 or r <= g:
        raise ValueError("invalid d1 or r <= g")
    return d1 / (r - g)


def ddm_value(dividends: Sequence[Fraction], r: Fraction, g: Fraction) -> Fraction:
    if not dividends or any(d < 0 for d in dividends) or r <= g or r <= -1:
        raise ValueError("invalid ddm arguments")

    factor = Fraction(1) + r
    dfs = list(itertools.accumulate([Fraction(1) / factor] * len(dividends), lambda acc, x: acc * x))
    pv_divs = sum((d * df for d, df in zip(dividends, dfs, strict=True)), Fraction(0))
    tv = (dividends[-1] * (Fraction(1) + g)) / (r - g)
    return pv_divs + tv * dfs[-1]


def fcfe_value_per_share(fcfe: Sequence[Fraction], shares: Fraction, r: Fraction, g: Fraction) -> Fraction:
    if not fcfe or shares <= 0 or r <= g or r <= -1:
        raise ValueError("invalid fcfe arguments")

    factor = Fraction(1) + r
    dfs = list(itertools.accumulate([Fraction(1) / factor] * len(fcfe), lambda acc, x: acc * x))
    pv_fcfe = sum((f * df for f, df in zip(fcfe, dfs, strict=True)), Fraction(0))
    tv = (fcfe[-1] * (Fraction(1) + g)) / (r - g)
    return (pv_fcfe + tv * dfs[-1]) / shares


def residual_income_value(
    book_value_0: Fraction, earnings: Sequence[Fraction], dividends: Sequence[Fraction], r: Fraction
) -> Fraction:
    if not earnings or len(earnings) != len(dividends) or r <= -1:
        raise ValueError("invalid ri arguments")

    factor = Fraction(1) + r
    dfs = list(itertools.accumulate([Fraction(1) / factor] * len(earnings), lambda acc, x: acc * x))

    # Roll book values
    b_history = [book_value_0]
    for ni, d in zip(earnings[:-1], dividends[:-1], strict=True):
        b_history.append(b_history[-1] + ni - d)

    ris = [ni - r * b for ni, b in zip(earnings, b_history, strict=True)]
    pv_ri = sum((ri * df for ri, df in zip(ris, dfs, strict=True)), Fraction(0))
    return book_value_0 + pv_ri


def scenario_price_target_cents(scenarios: Sequence[tuple[Fraction, int]]) -> int:
    if not scenarios or any(p < 0 or v < 0 for p, v in scenarios):
        raise ValueError("invalid scenarios")
    probs = [p for p, _ in scenarios]
    if sum(probs, Fraction(0)) != Fraction(1):
        raise ValueError("probabilities must sum to 1")

    ev = sum((p * v for p, v in scenarios), Fraction(0))
    return (2 * ev.numerator + ev.denominator) // (2 * ev.denominator)

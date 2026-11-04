"""Alternative correct scanner: validates everything up front and uses itertools.accumulate for the chord sums."""
from __future__ import annotations
import itertools
from fractions import Fraction
from typing import Any

PPM = 1_000_000


def _rh(x: Fraction) -> int:
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def _validate(strikes: list[int], calls: list[int], puts: list[int] | None, df: int) -> None:
    if not 1 <= df <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(k <= 0 for k in strikes) or any(b <= a for a, b in itertools.pairwise(strikes)):
        raise ValueError("strikes must be strictly increasing and positive")
    if len(calls) != len(strikes) or (puts is not None and len(puts) != len(strikes)):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts) if puts is not None else len(strikes)} puts")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _validate([strike_cents], [call_cents], [put_cents], df_ppm)
    return _rh(Fraction(call_cents - put_cents - spot_cents) + Fraction(strike_cents * df_ppm, PPM))


def _diff(strikes: list[int], calls: list[int], j: int) -> Fraction:
    a, b, c = strikes[j - 1], strikes[j], strikes[j + 1]
    return Fraction(c - b, c - a) * calls[j - 1] + Fraction(b - a, c - a) * calls[j + 1] - calls[j]


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _validate(strikes_cents, calls_cents, None, df_ppm)
    return [j for j in range(1, len(strikes_cents) - 1) if _diff(strikes_cents, calls_cents, j) < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = chain["strikes_cents"], chain["call_cents"], chain["put_cents"]
    df, spot = chain["df_ppm"], chain["spot_cents"]
    fee, half = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    _validate(list(strikes), list(calls), list(puts), df)
    if fee < 0 or half < 0:
        raise ValueError("cost terms must be non-negative")
    per = 3 * (fee + half)
    res: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        g = Fraction(calls[k] - puts[k] - spot) + Fraction(strike * df, PPM)
        gross = _rh(abs(g))
        if gross > per:
            res.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - per,
                        "explanation": "parity relation with P1, P2, P3, P4 and P6 named; the net is after three legs."})
    for j in convexity_violations(strikes, calls, df):
        gross = _rh(-_diff(strikes, calls, j))
        if gross > per:
            res.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - per,
                        "explanation": "convexity in strike with P1, P2, P5 and P6 named; the net is after three legs."})
    return res

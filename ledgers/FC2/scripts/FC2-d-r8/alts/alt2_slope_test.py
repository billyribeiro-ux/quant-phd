"""Alternative correct scanner: convexity tested by comparing adjacent slopes, Fractions, validation after the scan."""
from __future__ import annotations
from fractions import Fraction
from typing import Any

PPM = 1_000_000


def _half_up_mag(x: Fraction) -> int:
    x = abs(x)
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def _half_up(x: Fraction) -> int:
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    if strike_cents <= 0:
        raise ValueError("strikes must be strictly increasing and positive")
    if not 1 <= df_ppm <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    return _half_up(Fraction(call_cents - put_cents) - Fraction(spot_cents) + Fraction(strike_cents * df_ppm, PPM))


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    if not 1 <= df_ppm <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(f"calls need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls")
    if any(k <= 0 for k in strikes_cents) or any(b <= a for a, b in zip(strikes_cents, strikes_cents[1:])):
        raise ValueError("strikes must be strictly increasing and positive")
    out = []
    for j in range(1, len(strikes_cents) - 1):
        s_left = Fraction(calls_cents[j] - calls_cents[j - 1], strikes_cents[j] - strikes_cents[j - 1])
        s_right = Fraction(calls_cents[j + 1] - calls_cents[j], strikes_cents[j + 1] - strikes_cents[j])
        if s_left > s_right:
            out.append(j)
    return out


def _gross_convexity(strikes: list[int], calls: list[int], j: int) -> Fraction:
    lo, mi, hi = strikes[j - 1], strikes[j], strikes[j + 1]
    chord = Fraction(hi - mi, hi - lo) * calls[j - 1] + Fraction(mi - lo, hi - lo) * calls[j + 1]
    return chord - calls[j]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = chain["strikes_cents"], chain["call_cents"], chain["put_cents"]
    spot, df = chain["spot_cents"], chain["df_ppm"]
    fee, half = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    if fee < 0 or half < 0:
        raise ValueError("cost terms must be non-negative")
    per = 3 * (fee + half)
    if len(puts) != len(strikes) or len(calls) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts) if puts is not None else len(strikes)} puts")
    found: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gross = _half_up_mag(Fraction(calls[k] - puts[k]) - Fraction(spot) + Fraction(strike * df, PPM))
        if gross - per > 0:
            found.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - per,
                          "explanation": "parity: P1, P2, P3, P4 and P6 apply; the cost is three legs of fee plus half-spread."})
    for j in convexity_violations(strikes, calls, df):
        gross = _half_up_mag(_gross_convexity(strikes, calls, j))
        if gross - per > 0:
            found.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - per,
                          "explanation": "convexity in strike: P1, P2, P5 and P6 apply; three calls at the cost of three legs."})
    return found

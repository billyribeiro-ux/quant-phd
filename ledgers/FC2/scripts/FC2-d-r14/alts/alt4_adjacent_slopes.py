"""Alternative 4 (r14): convexity found by comparing adjacent chord slopes (unequal grid handled); exact Fractions for money."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

PPM = 1_000_000
LEGS = 3


def _half_up(x: Fraction) -> int:
    return int((x + Fraction(1, 2)) // 1)


def _check(strikes: list[int], df: int) -> None:
    if isinstance(df, bool) or not isinstance(df, int) or not 1 <= df <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(isinstance(k, bool) or not isinstance(k, int) or k <= 0 for k in strikes):
        raise ValueError("strikes must be strictly increasing and positive")
    if any(b <= a for a, b in zip(strikes, strikes[1:])):
        raise ValueError("strikes must be strictly increasing and positive")


def _slope(strikes: list[int], calls: list[int], i: int) -> Fraction:
    return Fraction(calls[i + 1] - calls[i], strikes[i + 1] - strikes[i])


def _excess(strikes: list[int], calls: list[int], j: int) -> Fraction:
    """call at j minus the chord at strike j, computed from the chord through the neighbours' slope form."""
    lo, hi = strikes[j - 1], strikes[j + 1]
    chord = Fraction(calls[j - 1]) + _slope_span(strikes, calls, j - 1, j + 1) * (strikes[j] - lo)
    return Fraction(calls[j]) - chord


def _slope_span(strikes: list[int], calls: list[int], a: int, b: int) -> Fraction:
    return Fraction(calls[b] - calls[a], strikes[b] - strikes[a])


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check(strikes_cents, df_ppm)
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(f"calls need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls")
    out = []
    for j in range(1, len(strikes_cents) - 1):
        # convexity fails at j exactly when the slope into j exceeds the slope out of j
        if _slope(strikes_cents, calls_cents, j - 1) > _slope(strikes_cents, calls_cents, j):
            out.append(j)
    return out


def _gap(call: int, put: int, spot: int, strike: int, df: int) -> Fraction:
    return Fraction(call - put) - (Fraction(spot) - Fraction(strike * df, PPM))


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check([strike_cents], df_ppm)
    return _half_up(_gap(call_cents, put_cents, spot_cents, strike_cents, df_ppm))


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    df = chain["df_ppm"]
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    _check(strikes, df)
    if len(calls) != len(strikes) or len(puts) != len(strikes):
        raise ValueError(
            f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts"
        )
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = LEGS * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        g = _gap(calls[k], puts[k], chain["spot_cents"], strike, df)
        gross = _half_up(abs(g))
        net = gross - cost
        if net > 0:
            out.append(
                {
                    "kind": "parity",
                    "strike_cents": strike,
                    "gross_cents": gross,
                    "net_cents": net,
                    "explanation": "put-call parity (P1, P2, P3, P4, P6): the gap at this strike; "
                    f"net {net} after {LEGS} legs.",
                }
            )
    for j in convexity_violations(strikes, calls, df):
        gross = _half_up(_excess(strikes, calls, j))
        net = gross - cost
        if net > 0:
            out.append(
                {
                    "kind": "convexity",
                    "strike_cents": strikes[j],
                    "gross_cents": gross,
                    "net_cents": net,
                    "explanation": "convexity in strike (P1, P2, P5, P6): the call is above the chord; "
                    f"net {net} after {LEGS} legs.",
                }
            )
    return out

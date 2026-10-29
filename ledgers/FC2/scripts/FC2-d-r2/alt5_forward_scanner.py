"""Alternative correct implementation 5 (round 2): parity through the forward price F = S / df."""

from __future__ import annotations

from fractions import Fraction
from math import floor
from typing import Any


def _check_df(df_ppm: int) -> None:
    if type(df_ppm) is not int or not 1 <= df_ppm <= 1_000_000:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _check_strikes(strikes: list[int]) -> None:
    if any(type(k) is not int or k <= 0 for k in strikes):
        raise ValueError("strikes must be strictly increasing and positive")
    if any(strikes[i] >= strikes[i + 1] for i in range(len(strikes) - 1)):
        raise ValueError("strikes must be strictly increasing and positive")


def _check_lengths(strikes: list[int], *others: list[int]) -> None:
    for other in others:
        if len(other) != len(strikes):
            raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(other)} quotes")


def _parity_exact(call: int, put: int, spot: int, strike: int, df_ppm: int) -> Fraction:
    """C - P - (S - K df), written as (C - P) - (F - K) df with the forward F = S / df."""
    df = Fraction(df_ppm, 1_000_000)
    forward = Fraction(spot) / df
    return (Fraction(call) - Fraction(put)) - (forward - strike) * df


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check_df(df_ppm)
    if type(strike_cents) is not int or strike_cents <= 0:
        raise ValueError("strikes must be strictly increasing and positive")
    return floor(_parity_exact(call_cents, put_cents, spot_cents, strike_cents, df_ppm) + Fraction(1, 2))


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check_df(df_ppm)
    _check_strikes(strikes_cents)
    _check_lengths(strikes_cents, calls_cents)
    flagged = []
    for j in range(1, len(strikes_cents) - 1):
        lo, mid, hi = strikes_cents[j - 1], strikes_cents[j], strikes_cents[j + 1]
        chord = Fraction(hi - mid, hi - lo) * calls_cents[j - 1] + Fraction(mid - lo, hi - lo) * calls_cents[j + 1]
        if chord - calls_cents[j] < 0:
            flagged.append(j)
    return flagged


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    spot = chain["spot_cents"]
    df_ppm = chain["df_ppm"]
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    _check_df(df_ppm)
    _check_strikes(strikes)
    _check_lengths(strikes, calls, puts)
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gross = floor(abs(_parity_exact(calls[k], puts[k], spot, strike, df_ppm)) + Fraction(1, 2))
        if gross - cost > 0:
            out.append(
                {
                    "kind": "parity",
                    "strike_cents": strike,
                    "gross_cents": gross,
                    "net_cents": gross - cost,
                    "explanation": "put-call parity (P1, P2, P3, P4, P6): the parity gap exceeds the cost",
                }
            )
    for j in convexity_violations(strikes, calls, df_ppm):
        lo, mid, hi = strikes[j - 1], strikes[j], strikes[j + 1]
        chord = Fraction(hi - mid, hi - lo) * calls[j - 1] + Fraction(mid - lo, hi - lo) * calls[j + 1]
        gross = floor(-(chord - calls[j]) + Fraction(1, 2))
        if gross - cost > 0:
            out.append(
                {
                    "kind": "convexity",
                    "strike_cents": strikes[j],
                    "gross_cents": gross,
                    "net_cents": gross - cost,
                    "explanation": "convexity in strike (P1, P2, P5, P6): the middle call is above its chord",
                }
            )
    return out

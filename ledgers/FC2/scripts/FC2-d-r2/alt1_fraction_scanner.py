"""Alternative correct implementation 1 (round 2): exact Fractions, validation written independently."""

from __future__ import annotations

from fractions import Fraction
from itertools import pairwise
from math import floor
from typing import Any

HALF = Fraction(1, 2)


def _to_cents(exact: Fraction) -> int:
    return floor(exact + HALF)


def _validate_df(df_ppm: int) -> None:
    if type(df_ppm) is not int or df_ppm < 1 or df_ppm > 1_000_000:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _validate_strikes(strikes: list[int]) -> None:
    for k in strikes:
        if type(k) is not int or k <= 0:
            raise ValueError("strikes must be strictly increasing and positive")
    for lo, hi in pairwise(strikes):
        if not lo < hi:
            raise ValueError("strikes must be strictly increasing and positive")


def _validate_lengths(strikes: list[int], *others: list[int]) -> None:
    for other in others:
        if len(other) != len(strikes):
            raise ValueError(
                f"calls and puts need one quote per strike: {len(strikes)} strikes, "
                f"{len(strikes)} and {len(other)} quotes"
            )


def _validate_cost(fee: int, spread: int) -> None:
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _validate_df(df_ppm)
    if type(strike_cents) is not int or strike_cents <= 0:
        raise ValueError("strikes must be strictly increasing and positive")
    df = Fraction(df_ppm, 1_000_000)
    exact = Fraction(call_cents) - Fraction(put_cents) - (Fraction(spot_cents) - strike_cents * df)
    return _to_cents(exact)


def _chord_minus_call(strikes: list[int], calls: list[int], j: int) -> Fraction:
    k_lo, k_mid, k_hi = strikes[j - 1], strikes[j], strikes[j + 1]
    weight_lo = Fraction(k_hi - k_mid, k_hi - k_lo)
    weight_hi = Fraction(k_mid - k_lo, k_hi - k_lo)
    chord = weight_lo * calls[j - 1] + weight_hi * calls[j + 1]
    return chord - calls[j]


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _validate_df(df_ppm)
    _validate_strikes(strikes_cents)
    _validate_lengths(strikes_cents, calls_cents)
    return [j for j in range(1, len(strikes_cents) - 1) if _chord_minus_call(strikes_cents, calls_cents, j) < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    spot = chain["spot_cents"]
    df_ppm = chain["df_ppm"]
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    _validate_df(df_ppm)
    _validate_strikes(strikes)
    _validate_lengths(strikes, calls, puts)
    _validate_cost(fee, spread)
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gap = parity_gap_cents(calls[k], puts[k], spot, strike, df_ppm)
        exact_gap = Fraction(calls[k]) - Fraction(puts[k]) - (Fraction(spot) - strike * Fraction(df_ppm, 1_000_000))
        gross = _to_cents(abs(exact_gap))
        if gross - cost > 0:
            out.append(
                {
                    "kind": "parity",
                    "strike_cents": strike,
                    "gross_cents": gross,
                    "net_cents": gross - cost,
                    "explanation": f"put-call parity (P1, P2, P3, P4, P6): gap {gap} cents",
                }
            )
    for j in convexity_violations(strikes, calls, df_ppm):
        gross = _to_cents(-_chord_minus_call(strikes, calls, j))
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

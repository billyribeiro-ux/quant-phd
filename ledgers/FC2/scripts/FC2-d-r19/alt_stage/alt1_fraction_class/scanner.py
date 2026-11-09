"""Alternative 1 (r14): Fraction throughout, written as a small Money-style helper; half-up by floor(x + 1/2)."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any

PPM = 1_000_000
LEGS = 3
HALF = Fraction(1, 2)


class Cents:
    """An exact amount of cents; rounds once, half up, when asked for an integer."""

    def __init__(self, value: Fraction) -> None:
        self.value = value

    def rounded(self) -> int:
        return math.floor(self.value + HALF)

    def magnitude_rounded(self) -> int:
        return math.floor(abs(self.value) + HALF)


def _need_df(df: Any) -> None:
    if isinstance(df, bool) or not isinstance(df, int) or not (1 <= df <= PPM):
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _need_strikes(strikes: Any) -> None:
    for k in strikes:
        if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
            raise ValueError("strikes must be strictly increasing and positive")
    for a, b in zip(strikes, strikes[1:]):
        if not b > a:
            raise ValueError("strikes must be strictly increasing and positive")


def _need_length(strikes: Any, quotes: Any, label: str) -> None:
    if len(quotes) != len(strikes):
        raise ValueError(
            f"{label} need one quote per strike: {len(strikes)} strikes, {len(quotes)} {label}"
        )


def _need_cost(fee: Any, spread: Any) -> None:
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")


def _gap(call: int, put: int, spot: int, strike: int, df: int) -> Fraction:
    discount = Fraction(df, PPM)
    return Fraction(call - put) - (Fraction(spot) - Fraction(strike) * discount)


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _need_df(df_ppm)
    _need_strikes([strike_cents])
    return Cents(_gap(call_cents, put_cents, spot_cents, strike_cents, df_ppm)).rounded()


def _chord_gap(strikes: list[int], calls: list[int], j: int) -> Fraction:
    lo, mid, hi = strikes[j - 1], strikes[j], strikes[j + 1]
    span = Fraction(hi - lo)
    chord = calls[j - 1] * Fraction(hi - mid) / span + calls[j + 1] * Fraction(mid - lo) / span
    return chord - calls[j]


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _need_df(df_ppm)
    _need_strikes(strikes_cents)
    _need_length(strikes_cents, calls_cents, "calls")
    return [j for j in range(1, len(strikes_cents) - 1) if _chord_gap(strikes_cents, calls_cents, j) < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    spot = chain["spot_cents"]
    df = chain["df_ppm"]
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    _need_df(df)
    _need_strikes(strikes)
    _need_length(strikes, calls, "calls")
    _need_length(strikes, puts, "puts")
    _need_cost(fee, spread)
    cost = LEGS * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        g = _gap(calls[k], puts[k], spot, strike, df)
        gross = Cents(g).magnitude_rounded()
        net = gross - cost
        if net > 0:
            out.append(
                {
                    "kind": "parity",
                    "strike_cents": strike,
                    "gross_cents": gross,
                    "net_cents": net,
                    "explanation": "put-call parity (P1, P2, P3, P4, P6): the gap is "
                    f"{Cents(g).rounded()} cents; net {net} after {LEGS} legs at fee {fee} and half-spread {spread}.",
                }
            )
    for j in convexity_violations(strikes, calls, df):
        gross = Cents(-_chord_gap(strikes, calls, j)).magnitude_rounded()
        net = gross - cost
        if net > 0:
            out.append(
                {
                    "kind": "convexity",
                    "strike_cents": strikes[j],
                    "gross_cents": gross,
                    "net_cents": net,
                    "explanation": "convexity in strike (P1, P2, P5, P6): the call is above the chord; "
                    f"net {net} after {LEGS} legs at fee {fee} and half-spread {spread}.",
                }
            )
    return out

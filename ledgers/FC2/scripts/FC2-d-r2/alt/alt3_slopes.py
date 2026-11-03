"""Alternative 3 (slopes): convexity flagged by comparing the two neighbouring slopes; Fractions; floor-based rounding."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any

PPM = 1_000_000


def _check_df(df_ppm: int) -> None:
    if isinstance(df_ppm, bool) or not isinstance(df_ppm, int) or df_ppm < 1 or df_ppm > PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _check_strikes(strikes: list[int]) -> None:
    for k in strikes:
        if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
            raise ValueError("strikes must be strictly increasing and positive")
    for i in range(len(strikes) - 1):
        if strikes[i + 1] <= strikes[i]:
            raise ValueError("strikes must be strictly increasing and positive")


def _check_lengths(strikes: list[int], calls: list[int], puts: list[int] | None) -> None:
    bad_calls = len(calls) != len(strikes)
    bad_puts = puts is not None and len(puts) != len(strikes)
    if bad_calls or bad_puts:
        p = len(strikes) if puts is None else len(puts)
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {p} puts")


def _nearest_up(x: Fraction) -> int:
    """floor(x) plus one when the fractional part is at least one half: a tie goes toward +infinity."""
    base = math.floor(x)
    return base + 1 if x - base >= Fraction(1, 2) else base


def _magnitude(x: Fraction) -> int:
    return _nearest_up(abs(x))


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check_df(df_ppm)
    _check_strikes([strike_cents])
    gap = Fraction(call_cents - put_cents) - (Fraction(spot_cents) - Fraction(strike_cents * df_ppm, PPM))
    return _nearest_up(gap)


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check_df(df_ppm)
    _check_strikes(strikes_cents)
    _check_lengths(strikes_cents, calls_cents, None)
    flagged = []
    for j in range(1, len(strikes_cents) - 1):
        k0, k1, k2 = strikes_cents[j - 1], strikes_cents[j], strikes_cents[j + 1]
        left = Fraction(calls_cents[j] - calls_cents[j - 1], k1 - k0)
        right = Fraction(calls_cents[j + 1] - calls_cents[j], k2 - k1)
        if left > right:  # the call sits above the chord exactly when the slope into it exceeds the slope out
            flagged.append(j)
    return flagged


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    _check_df(chain["df_ppm"])
    _check_strikes(strikes)
    _check_lengths(strikes, calls, puts)
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gap = Fraction(calls[k] - puts[k]) - (Fraction(chain["spot_cents"]) - Fraction(strike * chain["df_ppm"], PPM))
        gross = _magnitude(gap)
        net = gross - cost
        if net > 0:
            rule = "the call is rich" if gap > 0 else "the call is cheap"
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": net,
                        "explanation": f"Parity (P1, P2, P3, P4, P6): {rule}; net {net} cents."})
    for j in convexity_violations(strikes, calls, chain["df_ppm"]):
        k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
        chord = Fraction(calls[j - 1] * (k2 - k1) + calls[j + 1] * (k1 - k0), k2 - k0)
        gross = _magnitude(chord - calls[j])
        net = gross - cost
        if net > 0:
            out.append({"kind": "convexity", "strike_cents": k1, "gross_cents": gross, "net_cents": net,
                        "explanation": f"Convexity (P1, P2, P5, P6): the middle call is above its chord; net {net} cents."})
    return out

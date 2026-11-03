"""Alternative 1 (plan 5.5(1)): exact Fraction arithmetic, written independently of reference.py, all three functions."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

PPM = 1_000_000


def _round_half_up(x: Fraction) -> int:
    return int((x + Fraction(1, 2)).__floor__())


def _validate_df(df_ppm: int) -> None:
    if not (1 <= df_ppm <= PPM) or isinstance(df_ppm, bool):
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _validate_strikes(strikes: list[int]) -> None:
    if any(k <= 0 for k in strikes) or any(b <= a for a, b in zip(strikes, strikes[1:], strict=False)):
        raise ValueError("the strikes must be strictly increasing and positive")


def _validate_quotes(strikes: list[int], calls: list[int], puts: list[int] | None) -> None:
    n = len(strikes)
    if len(calls) != n:
        raise ValueError(f"need one call per strike: {n} strikes but {len(calls)} calls")
    if puts is not None and len(puts) != n:
        raise ValueError(f"need one put per strike: {n} strikes but {len(puts)} puts")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _validate_df(df_ppm)
    if strike_cents <= 0:
        raise ValueError("the strikes must be strictly increasing and positive")
    gap = Fraction(call_cents - put_cents) - (Fraction(spot_cents) - Fraction(strike_cents * df_ppm, PPM))
    return _round_half_up(gap)


def _chord_less_call(strikes: list[int], calls: list[int], j: int) -> Fraction:
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    wl = Fraction(k2 - k1, k2 - k0)
    wh = Fraction(k1 - k0, k2 - k0)
    return wl * calls[j - 1] + wh * calls[j + 1] - calls[j]


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _validate_df(df_ppm)
    _validate_strikes(strikes_cents)
    _validate_quotes(strikes_cents, calls_cents, None)
    return [j for j in range(1, len(strikes_cents) - 1) if _chord_less_call(strikes_cents, calls_cents, j) < 0]


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
    _validate_quotes(strikes, calls, puts)
    if fee < 0 or spread < 0:
        raise ValueError("the cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gap = Fraction(calls[k] - puts[k]) - (Fraction(spot) - Fraction(strike * df_ppm, PPM))
        gross = _round_half_up(abs(gap))
        if gross - cost > 0:
            out.append(
                {
                    "kind": "parity",
                    "strike_cents": strike,
                    "gross_cents": gross,
                    "net_cents": gross - cost,
                    "explanation": "parity (P1, P2, P3, P4, P6): the call less the put differs from the synthetic forward"
                    f"; net after 3 legs at {fee} plus {spread}",
                }
            )
    for j in convexity_violations(strikes, calls, df_ppm):
        gross = _round_half_up(-_chord_less_call(strikes, calls, j))
        if gross - cost > 0:
            out.append(
                {
                    "kind": "convexity",
                    "strike_cents": strikes[j],
                    "gross_cents": gross,
                    "net_cents": gross - cost,
                    "explanation": "convexity in strike (P1, P2, P5, P6): the call sits above the chord; "
                    f"net after 3 legs at {fee} plus {spread}",
                }
            )
    return out

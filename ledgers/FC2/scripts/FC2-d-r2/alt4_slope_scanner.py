"""Alternative correct implementation 4 (round 2): convexity by comparing adjacent slopes."""

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


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check_df(df_ppm)
    if type(strike_cents) is not int or strike_cents <= 0:
        raise ValueError("strikes must be strictly increasing and positive")
    exact = Fraction(call_cents - put_cents) - (spot_cents - Fraction(strike_cents * df_ppm, 1_000_000))
    return floor(exact + Fraction(1, 2))


def _slope_test(strikes: list[int], calls: list[int], j: int) -> tuple[int, int, int]:
    """Returns (a, b, excess) with a = K_mid - K_lo, b = K_hi - K_mid, excess = b*(C_mid - C_lo) - a*(C_hi - C_mid).

    The chord less the call equals (a*(C_hi - C_mid) - b*(C_mid - C_lo)) / (a + b), so a positive excess is a violation.
    """
    a = strikes[j] - strikes[j - 1]
    b = strikes[j + 1] - strikes[j]
    excess = b * (calls[j] - calls[j - 1]) - a * (calls[j + 1] - calls[j])
    return a, b, excess


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check_df(df_ppm)
    _check_strikes(strikes_cents)
    _check_lengths(strikes_cents, calls_cents)
    flagged = []
    for j in range(1, len(strikes_cents) - 1):
        _a, _b, excess = _slope_test(strikes_cents, calls_cents, j)
        if excess > 0:
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
        exact = Fraction(calls[k] - puts[k]) - (spot - Fraction(strike * df_ppm, 1_000_000))
        gross = floor(abs(exact) + Fraction(1, 2))
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
        a, b, excess = _slope_test(strikes, calls, j)
        gross = floor(Fraction(excess, a + b) + Fraction(1, 2))
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

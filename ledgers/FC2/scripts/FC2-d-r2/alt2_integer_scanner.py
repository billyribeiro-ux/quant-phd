"""Alternative correct implementation 2 (round 2): integer-only arithmetic with an explicit half-up division helper."""

from __future__ import annotations

from typing import Any

PPM = 1_000_000


def _div_half_up(numerator: int, denominator: int) -> int:
    """numerator / denominator for denominator > 0, rounded to the nearest integer, a tie toward plus infinity."""
    return (2 * numerator + denominator) // (2 * denominator)


def _check_df(df_ppm: int) -> None:
    if type(df_ppm) is not int or not 1 <= df_ppm <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _check_strikes(strikes: list[int]) -> None:
    if any(type(k) is not int or k <= 0 for k in strikes):
        raise ValueError("strikes must be strictly increasing and positive")
    if any(strikes[i] >= strikes[i + 1] for i in range(len(strikes) - 1)):
        raise ValueError("strikes must be strictly increasing and positive")


def _check_lengths(strikes: list[int], calls: list[int], puts: list[int] | None) -> None:
    lengths = [len(strikes), len(calls)] + ([] if puts is None else [len(puts)])
    if len(set(lengths)) != 1:
        raise ValueError(f"calls and puts need one quote per strike, lengths were {lengths}")


def _gap_numerator(call: int, put: int, spot: int, strike: int, df_ppm: int) -> int:
    """PPM times the parity gap C - P - (S - K df), an integer: K df = strike * df_ppm / PPM."""
    return (call - put - spot) * PPM + strike * df_ppm


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check_df(df_ppm)
    if type(strike_cents) is not int or strike_cents <= 0:
        raise ValueError("strikes must be strictly increasing and positive")
    return _div_half_up(_gap_numerator(call_cents, put_cents, spot_cents, strike_cents, df_ppm), PPM)


def _chord_numerator(strikes: list[int], calls: list[int], j: int) -> tuple[int, int]:
    """(numerator, denominator) of chord-less-call at strike j; the denominator is the neighbour distance."""
    lo, mid, hi = strikes[j - 1], strikes[j], strikes[j + 1]
    span = hi - lo
    numerator = (hi - mid) * calls[j - 1] + (mid - lo) * calls[j + 1] - span * calls[j]
    return numerator, span


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check_df(df_ppm)
    _check_strikes(strikes_cents)
    _check_lengths(strikes_cents, calls_cents, None)
    flagged = []
    for j in range(1, len(strikes_cents) - 1):
        numerator, _span = _chord_numerator(strikes_cents, calls_cents, j)
        if numerator < 0:
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
        gross = _div_half_up(abs(_gap_numerator(calls[k], puts[k], spot, strike, df_ppm)), PPM)
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
        numerator, span = _chord_numerator(strikes, calls, j)
        gross = _div_half_up(-numerator, span)
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

"""Alternative correct scanner 10: Fraction-free parity with Decimal rounding by quantize, convexity by slope comparison."""
from __future__ import annotations

from decimal import ROUND_FLOOR, Decimal
from typing import Any

PPM = 1_000_000


def _ok_df(df: int) -> None:
    if isinstance(df, bool) or not isinstance(df, int) or df < 1 or df > PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _ok_strikes(strikes: list[int]) -> None:
    if any(isinstance(k, bool) or not isinstance(k, int) or k <= 0 for k in strikes):
        raise ValueError("strikes must be strictly increasing and positive")
    if any(b <= a for a, b in zip(strikes, strikes[1:])):
        raise ValueError("strikes must be strictly increasing and positive")


def _dec_round(num: int, den: int) -> int:
    # nearest integer to num/den, tie toward +inf: floor(num/den + 1/2) computed with Decimal at high precision
    value = (Decimal(2 * num) + Decimal(den)) / (Decimal(2) * Decimal(den))
    return int(value.to_integral_value(rounding=ROUND_FLOOR))


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _ok_df(df_ppm)
    _ok_strikes([strike_cents])
    # gap = (C - P - S) + K df / 1e6 = num / PPM
    num = (call_cents - put_cents - spot_cents) * PPM + strike_cents * df_ppm
    return _dec_round(num, PPM)


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _ok_df(df_ppm)
    _ok_strikes(strikes_cents)
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(f"calls need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls")
    flagged: list[int] = []
    for j in range(1, len(strikes_cents) - 1):
        k0, k1, k2 = strikes_cents[j - 1 : j + 2]
        c0, c1, c2 = calls_cents[j - 1 : j + 2]
        # slope from left to middle exceeds slope from middle to right  <=>  the middle call is above the chord
        if (c1 - c0) * (k2 - k1) > (c2 - c1) * (k1 - k0):
            flagged.append(j)
    return flagged


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    _ok_df(chain["df_ppm"])
    _ok_strikes(strikes)
    if len(calls) != len(strikes) or len(puts) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts")
    fee, spread = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    df, spot = chain["df_ppm"], chain["spot_cents"]
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        num = (calls[k] - puts[k] - spot) * PPM + strike * df
        gross = _dec_round(abs(num), PPM)
        if gross - cost > 0:
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "parity: P1, P2, P3, P4 and P6 apply; the cost is three legs at fee plus half-spread."})
    for j in convexity_violations(strikes, calls, df):
        k0, k1, k2 = strikes[j - 1 : j + 2]
        c0, c1, c2 = calls[j - 1 : j + 2]
        num = (k2 - k0) * c1 - ((k2 - k1) * c0 + (k1 - k0) * c2)  # > 0 at a violation: call less chord, times span
        gross = _dec_round(num, k2 - k0)
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "convexity in strike: P1, P2, P5 and P6 apply; the cost is three legs at fee plus half-spread."})
    return out

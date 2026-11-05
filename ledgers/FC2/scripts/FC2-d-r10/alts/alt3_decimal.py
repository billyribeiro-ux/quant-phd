"""Alternative correct scanner: Decimal at 60 digits with ROUND_HALF_CEILING for signed gaps and ROUND_HALF_UP for magnitudes."""
from __future__ import annotations
from decimal import ROUND_FLOOR, ROUND_HALF_UP, Decimal, localcontext
from fractions import Fraction
from typing import Any

PPM = 1_000_000


def _dec_gap(call: int, put: int, spot: int, strike: int, df_ppm: int) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = 60
        return Decimal(call) - Decimal(put) - (Decimal(spot) - Decimal(strike) * Decimal(df_ppm) / Decimal(PPM))


def _check_df(df: int) -> None:
    if isinstance(df, bool) or not 1 <= df <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _check_strikes(strikes: list[int]) -> None:
    if any(k <= 0 for k in strikes) or any(b <= a for a, b in zip(strikes, strikes[1:])):
        raise ValueError("strikes must be strictly increasing and positive")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check_df(df_ppm)
    _check_strikes([strike_cents])
    shifted = _dec_gap(call_cents, put_cents, spot_cents, strike_cents, df_ppm) + Decimal("0.5")
    return int(shifted.to_integral_value(rounding=ROUND_FLOOR))


def _conv_gap(strikes: list[int], calls: list[int], j: int) -> Fraction:
    lo, mi, hi = strikes[j - 1], strikes[j], strikes[j + 1]
    return Fraction(hi - mi, hi - lo) * calls[j - 1] + Fraction(mi - lo, hi - lo) * calls[j + 1] - calls[j]


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check_df(df_ppm)
    _check_strikes(strikes_cents)
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(f"calls need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls")
    return [j for j in range(1, len(strikes_cents) - 1) if _conv_gap(strikes_cents, calls_cents, j) < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    df, spot = chain["df_ppm"], chain["spot_cents"]
    fee, half = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    _check_df(df)
    _check_strikes(strikes)
    if len(calls) != len(strikes) or len(puts) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts")
    if fee < 0 or half < 0:
        raise ValueError("cost terms must be non-negative")
    per = 3 * (fee + half)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        g = _dec_gap(calls[k], puts[k], spot, strike, df)
        gross = int(abs(g).quantize(Decimal(1), rounding=ROUND_HALF_UP))
        if gross - per > 0:
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - per,
                        "explanation": "put-call parity under P1, P2, P3, P4 and P6, net of three legs at fee plus half-spread."})
    for j in convexity_violations(strikes, calls, df):
        exact = -_conv_gap(strikes, calls, j)
        gross = int((Decimal(exact.numerator) / Decimal(exact.denominator)).quantize(Decimal(1), rounding=ROUND_HALF_UP))
        if gross - per > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - per,
                        "explanation": "convexity in strike under P1, P2, P5 and P6, net of three legs at fee plus half-spread."})
    return out

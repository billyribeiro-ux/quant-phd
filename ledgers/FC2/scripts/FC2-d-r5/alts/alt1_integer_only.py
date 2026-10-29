"""Alternative correct scanner: integer-only arithmetic, no Fraction (round half up with integer division)."""
from __future__ import annotations
from typing import Any

PPM = 1_000_000


def _check(strikes: list[int], calls: list[int], df: int) -> None:
    if not (isinstance(df, int) and 1 <= df <= PPM):
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(k <= 0 for k in strikes) or any(b <= a for a, b in zip(strikes, strikes[1:])):
        raise ValueError("strikes must be strictly increasing and positive")
    if len(calls) != len(strikes):
        raise ValueError(f"calls need one quote per strike: {len(strikes)} strikes, {len(calls)} calls")


def _round_signed(n: int, d: int) -> int:  # nearest integer to n/d, ties toward +inf, d > 0
    return (2 * n + d) // (2 * d)


def _round_mag(n: int, d: int) -> int:  # nearest integer to |n|/d, ties away from zero
    return (2 * abs(n) + d) // (2 * d)


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    if not (isinstance(df_ppm, int) and 1 <= df_ppm <= PPM):
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if strike_cents <= 0:
        raise ValueError("strikes must be strictly increasing and positive")
    numer = (call_cents - put_cents - spot_cents) * PPM + strike_cents * df_ppm
    return _round_signed(numer, PPM)


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check(strikes_cents, calls_cents, df_ppm)
    out: list[int] = []
    for j in range(1, len(strikes_cents) - 1):
        lo, mi, hi = strikes_cents[j - 1], strikes_cents[j], strikes_cents[j + 1]
        d = hi - lo
        n = (hi - mi) * calls_cents[j - 1] + (mi - lo) * calls_cents[j + 1] - d * calls_cents[j]
        if n < 0:
            out.append(j)
    return out


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    cost = chain["cost"]
    if cost["fee_cents_per_contract"] < 0 or cost["half_spread_cents"] < 0:
        raise ValueError("cost terms must be non-negative")
    if len(puts) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts")
    _check(strikes, calls, chain["df_ppm"])
    per = 3 * (cost["fee_cents_per_contract"] + cost["half_spread_cents"])
    df = chain["df_ppm"]
    spot = chain["spot_cents"]
    rows: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        numer = (calls[k] - puts[k] - spot) * PPM + strike * df
        gross = _round_mag(numer, PPM)
        net = gross - per
        if net > 0:
            rows.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": net,
                         "explanation": f"parity (P1, P2, P3, P4, P6): gap {_round_signed(numer, PPM)} cents, net {net} after {per} cents of cost"})
    for j in convexity_violations(strikes, calls, df):
        lo, mi, hi = strikes[j - 1], strikes[j], strikes[j + 1]
        d = hi - lo
        n = (hi - mi) * calls[j - 1] + (mi - lo) * calls[j + 1] - d * calls[j]
        gross = _round_mag(n, d)
        net = gross - per
        if net > 0:
            rows.append({"kind": "convexity", "strike_cents": mi, "gross_cents": gross, "net_cents": net,
                         "explanation": f"convexity in strike (P1, P2, P5, P6): the chord test fails, net {net} after {per} cents"})
    return rows

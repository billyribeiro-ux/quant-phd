"""Alternative 3: Decimal arithmetic at 60 digits with ROUND_HALF_CEILING (tie toward plus infinity); own cutoffs."""
from __future__ import annotations

from decimal import ROUND_FLOOR, ROUND_HALF_UP, Decimal, localcontext
from typing import Any

_CENT = Decimal("1")


def _check_df(df_ppm: int) -> None:
    if isinstance(df_ppm, bool) or not isinstance(df_ppm, int) or df_ppm < 1 or df_ppm > 1000000:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _check_strikes(strikes: list[int]) -> None:
    for k in strikes:
        if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
            raise ValueError("strikes must be strictly increasing and positive")
    for a, b in zip(strikes, strikes[1:]):
        if not a < b:
            raise ValueError("strikes must be strictly increasing and positive")


def _gap(call: int, put: int, spot: int, strike: int, df_ppm: int) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = 60
        df = Decimal(df_ppm) / Decimal(1000000)
        return Decimal(call) - Decimal(put) - (Decimal(spot) - Decimal(strike) * df)


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check_df(df_ppm)
    _check_strikes([strike_cents])
    return int((_gap(call_cents, put_cents, spot_cents, strike_cents, df_ppm) + Decimal("0.5")).to_integral_value(rounding=ROUND_FLOOR))


def _chord_less_call(strikes: list[int], calls: list[int], j: int) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = 60
        k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
        w0 = Decimal(k2 - k1) / Decimal(k2 - k0)
        w2 = Decimal(k1 - k0) / Decimal(k2 - k0)
        return w0 * Decimal(calls[j - 1]) + w2 * Decimal(calls[j + 1]) - Decimal(calls[j])


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check_df(df_ppm)
    _check_strikes(strikes_cents)
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls, 0 puts")
    return [j for j in range(1, len(strikes_cents) - 1) if _chord_less_call(strikes_cents, calls_cents, j) < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    df = chain["df_ppm"]
    _check_df(df)
    _check_strikes(strikes)
    if len(calls) != len(strikes) or len(puts) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts")
    fee, spread = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        g = _gap(calls[k], puts[k], chain["spot_cents"], strike, df)
        gross = int(abs(g).quantize(_CENT, rounding=ROUND_HALF_UP))
        if gross - cost > 0:
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "parity under P1, P2, P3 and the supplied discount factor P4; three legs at P6 cost."})
    for j in convexity_violations(strikes, calls, df):
        gross = int((-_chord_less_call(strikes, calls, j) + Decimal("0.5")).to_integral_value(rounding=ROUND_FLOOR)) if False else int((-_chord_less_call(strikes, calls, j)).quantize(_CENT, rounding=ROUND_HALF_UP))
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "convexity in strike under P1, P2 and P5 (present values); three calls at P6 cost."})
    return out

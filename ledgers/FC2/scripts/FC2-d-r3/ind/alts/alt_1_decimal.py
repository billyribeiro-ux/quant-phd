"""Alternative correct scanner 1: Decimal arithmetic at 80 digits, exact integer comparisons, ROUND_HALF_CEILING for signed gaps."""

from __future__ import annotations

from decimal import ROUND_FLOOR, ROUND_HALF_UP, Decimal, getcontext
from typing import Any

getcontext().prec = 80
PPM = 1_000_000
LEGS = 3


def _check(strikes: list[int], df_ppm: int) -> None:
    if isinstance(df_ppm, bool) or not isinstance(df_ppm, int) or not 1 <= df_ppm <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(k <= 0 for k in strikes) or any(b <= a for a, b in zip(strikes, strikes[1:])):
        raise ValueError("strikes must be strictly increasing and positive")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check([strike_cents], df_ppm)
    gap = Decimal(call_cents - put_cents - spot_cents) + Decimal(strike_cents * df_ppm) / Decimal(PPM)
    return int((gap + Decimal("0.5")).quantize(Decimal(1), rounding=ROUND_FLOOR))


def _num_den(strikes: list[int], calls: list[int], j: int) -> tuple[int, int]:
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    den = k2 - k0
    num = (k2 - k1) * calls[j - 1] + (k1 - k0) * calls[j + 1] - den * calls[j]
    return num, den


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check(strikes_cents, df_ppm)
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(f"calls need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls")
    return [j for j in range(1, len(strikes_cents) - 1) if _num_den(strikes_cents, calls_cents, j)[0] < 0]


def _half_up_mag(num: int, den: int) -> int:
    return int((Decimal(abs(num)) / Decimal(den)).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    df = chain["df_ppm"]
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    _check(strikes, df)
    if len(calls) != len(strikes) or len(puts) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts")
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = LEGS * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gap = Decimal(calls[k] - puts[k] - chain["spot_cents"]) + Decimal(strike * df) / Decimal(PPM)
        gross = int((abs(gap)).quantize(Decimal(1), rounding=ROUND_HALF_UP))
        if gross - cost > 0:
            side = "sell the call, buy the put and the underlying, borrow the discounted strike" if gap > 0 else "buy the call, sell the put and the underlying, lend the discounted strike"
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": f"Parity (P1, P2, P3, P4, P6): {side}; net {gross - cost}."})
    for j in convexity_violations(strikes, calls, df):
        num, den = _num_den(strikes, calls, j)
        gross = _half_up_mag(num, den)
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": f"Convexity in strike (P1, P2, P5, P6): the middle call is above the chord; net {gross - cost}."})
    return out

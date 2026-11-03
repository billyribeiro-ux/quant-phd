"""Alternative 3 (plan 5.5(3)): float arithmetic with half-up rounding applied to the float result (the spec demands exact fractions)."""

from __future__ import annotations

import math
from typing import Any


def _half_up(x: float) -> int:
    return math.floor(x + 0.5)


def _check(strikes: list[int], calls: list[int], puts: list[int] | None, df_ppm: int) -> None:
    if not 1 <= df_ppm <= 1_000_000:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(k <= 0 for k in strikes) or any(strikes[i + 1] <= strikes[i] for i in range(len(strikes) - 1)):
        raise ValueError("the strikes must be strictly increasing and positive")
    if len(calls) != len(strikes) or (puts is not None and len(puts) != len(strikes)):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(strikes) if puts is None else len(puts)} puts")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    if not 1 <= df_ppm <= 1_000_000:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if strike_cents <= 0:
        raise ValueError("the strikes must be strictly increasing and positive")
    gap = call_cents - put_cents - (spot_cents - strike_cents * (df_ppm / 1_000_000))
    return _half_up(gap)


def _chord_less_call(strikes: list[int], calls: list[int], j: int) -> float:
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    return (k2 - k1) / (k2 - k0) * calls[j - 1] + (k1 - k0) / (k2 - k0) * calls[j + 1] - calls[j]


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check(strikes_cents, calls_cents, None, df_ppm)
    return [j for j in range(1, len(strikes_cents) - 1) if _chord_less_call(strikes_cents, calls_cents, j) < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    _check(strikes, calls, puts, chain["df_ppm"])
    fee, spread = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("the cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gross = _half_up(abs(calls[k] - puts[k] - (chain["spot_cents"] - strike * chain["df_ppm"] / 1_000_000)))
        if gross - cost > 0:
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "parity: P1, P2, P3, P4 and P6 (the call less the put differs from the forward)"})
    for j in convexity_violations(strikes, calls, chain["df_ppm"]):
        gross = _half_up(-_chord_less_call(strikes, calls, j))
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "convexity in strike: P1, P2, P5 and P6 (the call sits above the chord)"})
    return out

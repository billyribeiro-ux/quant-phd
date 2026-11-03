"""Alternative 4 (plan 5.5(4)): convexity by comparing adjacent slopes (unequal spacing handled), exact Fraction gross."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

PPM = 1_000_000


def _half_up(x: Fraction) -> int:
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def _validate(strikes: list[int], calls: list[int], puts: list[int] | None, df_ppm: int) -> None:
    if not 1 <= df_ppm <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(k <= 0 for k in strikes) or any(strikes[i + 1] <= strikes[i] for i in range(len(strikes) - 1)):
        raise ValueError("the strikes must be strictly increasing and positive")
    if len(calls) != len(strikes):
        raise ValueError(f"the calls need one quote per strike: {len(strikes)} strikes, {len(calls)} calls")
    if puts is not None and len(puts) != len(strikes):
        raise ValueError(f"the puts need one quote per strike: {len(strikes)} strikes, {len(puts)} puts")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _validate([strike_cents], [call_cents], [put_cents], df_ppm)
    gap = Fraction(call_cents - put_cents) - Fraction(spot_cents) + Fraction(strike_cents * df_ppm, PPM)
    return _half_up(gap)


def _violation_gap(strikes: list[int], calls: list[int], j: int) -> Fraction | None:
    """The exact amount by which the call exceeds the chord, or None when the call does not exceed it."""
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    left = Fraction(calls[j] - calls[j - 1], k1 - k0)
    right = Fraction(calls[j + 1] - calls[j], k2 - k1)
    if left <= right:
        return None
    chord = Fraction(calls[j - 1]) + Fraction(calls[j + 1] - calls[j - 1]) * Fraction(k1 - k0, k2 - k0)
    return calls[j] - chord


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _validate(strikes_cents, calls_cents, None, df_ppm)
    return [j for j in range(1, len(strikes_cents) - 1) if _violation_gap(strikes_cents, calls_cents, j) is not None]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    df_ppm, spot = chain["df_ppm"], chain["spot_cents"]
    _validate(strikes, calls, puts, df_ppm)
    fee, spread = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("the cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gap = Fraction(calls[k] - puts[k]) - (Fraction(spot) - Fraction(strike * df_ppm, PPM))
        gross = _half_up(abs(gap))
        if gross - cost > 0:
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "parity: P1, P2, P3, P4 and P6 (the call less the put differs from the forward)"})
    for j in convexity_violations(strikes, calls, df_ppm):
        gross = _half_up(_violation_gap(strikes, calls, j))  # type: ignore[arg-type]
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "convexity in strike: P1, P2, P5 and P6 (the call sits above the chord)"})
    return out

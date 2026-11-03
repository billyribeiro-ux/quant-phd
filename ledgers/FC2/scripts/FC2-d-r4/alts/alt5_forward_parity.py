"""Alternative 5 (plan 5.5(5)): parity through the forward F = S / df, comparing (F - K) df with C - P, exact Fraction."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

PPM = 1_000_000


def _half_up(x: Fraction) -> int:
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def _check(strikes: list[int], calls: list[int], puts: list[int] | None, df_ppm: int) -> None:
    if not 1 <= df_ppm <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(k <= 0 for k in strikes) or any(b <= a for a, b in zip(strikes, strikes[1:], strict=False)):
        raise ValueError("the strikes must be strictly increasing and positive")
    if len(calls) != len(strikes):
        raise ValueError(f"calls: {len(calls)} quotes for {len(strikes)} strikes")
    if puts is not None and len(puts) != len(strikes):
        raise ValueError(f"puts: {len(puts)} quotes for {len(strikes)} strikes")


def _parity_exact(call: int, put: int, spot: int, strike: int, df_ppm: int) -> Fraction:
    df = Fraction(df_ppm, PPM)
    forward = Fraction(spot) / df  # F = S / df
    return Fraction(call - put) - (forward - strike) * df  # (F - K) df equals S - K df


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check([strike_cents], [call_cents], [put_cents], df_ppm)
    return _half_up(_parity_exact(call_cents, put_cents, spot_cents, strike_cents, df_ppm))


def _lagrange_gap(strikes: list[int], calls: list[int], j: int) -> Fraction:
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    l0 = Fraction(k1 - k2, k0 - k2)  # Lagrange basis polynomial of node k0, at k1
    l2 = Fraction(k1 - k0, k2 - k0)
    return calls[j] - (l0 * calls[j - 1] + l2 * calls[j + 1])


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check(strikes_cents, calls_cents, None, df_ppm)
    return [j for j in range(1, len(strikes_cents) - 1) if _lagrange_gap(strikes_cents, calls_cents, j) > 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    df_ppm, spot = chain["df_ppm"], chain["spot_cents"]
    _check(strikes, calls, puts, df_ppm)
    fee, spread = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("the cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gross = _half_up(abs(_parity_exact(calls[k], puts[k], spot, strike, df_ppm)))
        if gross - cost > 0:
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "parity: P1, P2, P3, P4 and P6 (the call less the put differs from the forward)"})
    for j in convexity_violations(strikes, calls, df_ppm):
        gross = _half_up(_lagrange_gap(strikes, calls, j))
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "convexity in strike: P1, P2, P5 and P6 (the call sits above the chord)"})
    return out

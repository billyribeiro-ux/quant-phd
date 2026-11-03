"""Alternative correct scanner 4: Lagrange basis weights for the chord; parity through the forward price (S / df) compared with the call less the put."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

PPM = 1_000_000


def _floor_half(x: Fraction) -> int:
    return (x + Fraction(1, 2)).__floor__()


def _need(strikes: list[int], df: int) -> None:
    if isinstance(df, bool) or not isinstance(df, int) or not (1 <= df <= PPM):
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(k <= 0 for k in strikes) or any(b <= a for a, b in zip(strikes, strikes[1:])):
        raise ValueError("strikes must be strictly increasing and positive")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _need([strike_cents], df_ppm)
    df = Fraction(df_ppm, PPM)
    forward = Fraction(spot_cents) / df  # the forward implied by spot and the factor
    gap = Fraction(call_cents - put_cents) - (forward - strike_cents) * df
    return _floor_half(gap)


def _lagrange_chord_minus_call(strikes: list[int], calls: list[int], j: int) -> Fraction:
    x0, x1, x2 = (Fraction(s) for s in strikes[j - 1 : j + 2])
    l0 = (x1 - x2) / (x0 - x2)
    l2 = (x1 - x0) / (x2 - x0)
    return Fraction(calls[j - 1]) * l0 + Fraction(calls[j + 1]) * l2 - Fraction(calls[j])


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _need(strikes_cents, df_ppm)
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(f"calls need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls")
    return [j for j in range(1, len(strikes_cents) - 1) if _lagrange_chord_minus_call(strikes_cents, calls_cents, j) < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    df_ppm = chain["df_ppm"]
    fee, spread = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    _need(strikes, df_ppm)
    if len(calls) != len(strikes) or len(puts) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts")
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        signed = Fraction(calls[k] - puts[k]) - (Fraction(chain["spot_cents"]) - Fraction(strike * df_ppm, PPM))
        gross = _floor_half(abs(signed))
        if gross - cost > 0:
            text = "the call is rich: sell the call, buy the put and the underlying" if signed > 0 else "the call is cheap: buy the call"
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": f"Parity with P1, P2, P3, P4 and P6: {text}; net {gross - cost}."})
    for j in convexity_violations(strikes, calls, df_ppm):
        gross = _floor_half(-_lagrange_chord_minus_call(strikes, calls, j))
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": f"convexity in strike with P1, P2, P5 and P6: the middle call sits above the chord; net {gross - cost}."})
    return out

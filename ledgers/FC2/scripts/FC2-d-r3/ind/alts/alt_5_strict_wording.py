"""Alternative correct scanner 5: same arithmetic as reference via Fractions, explanations that name the rule and labels only (no trade wording), as the page's Required outputs paragraph asks."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

PPM = 1_000_000


def _half(x: Fraction) -> int:
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def _checks(strikes: list[int], df: int) -> None:
    if isinstance(df, bool) or not isinstance(df, int) or not 1 <= df <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(k <= 0 for k in strikes) or any(strikes[i + 1] <= strikes[i] for i in range(len(strikes) - 1)):
        raise ValueError("strikes must be strictly increasing and positive")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _checks([strike_cents], df_ppm)
    return _half(Fraction(call_cents - put_cents) - (Fraction(spot_cents) - Fraction(strike_cents * df_ppm, PPM)))


def _chord_minus_call(strikes: list[int], calls: list[int], j: int) -> Fraction:
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    return Fraction(k2 - k1, k2 - k0) * calls[j - 1] + Fraction(k1 - k0, k2 - k0) * calls[j + 1] - calls[j]


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _checks(strikes_cents, df_ppm)
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(f"calls need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls")
    return [j for j in range(1, len(strikes_cents) - 1) if _chord_minus_call(strikes_cents, calls_cents, j) < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    df = chain["df_ppm"]
    fee, spread = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    _checks(strikes, df)
    if len(calls) != len(strikes) or len(puts) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts")
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        signed = Fraction(calls[k] - puts[k]) - (Fraction(chain["spot_cents"]) - Fraction(strike * df, PPM))
        gross = _half(abs(signed))
        if gross - cost > 0:
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "P1 European exercise, P2 one expiry, P3 no income, P4 supplied discount factor and P6 cost: the parity gap is outside the no-arbitrage band at this strike."})
    for j in convexity_violations(strikes, calls, df):
        gross = _half(-_chord_minus_call(strikes, calls, j))
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "Convexity in strike under P1 European exercise, P2 one expiry, P5 present-value quotes and P6 cost."})
    return out

"""Alternative correct scanner 3: convexity by comparing adjacent slopes; parity with Fractions; explanation says the call is expensive and to write it."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

PPM = 1_000_000


def _round_half_up_away(x: Fraction) -> int:
    """Nearest integer, a tie away from zero (used for magnitudes, which are non-negative here)."""
    return int(x + Fraction(1, 2)) if x >= 0 else -int(-x + Fraction(1, 2))


def _signed_round(x: Fraction) -> int:
    """Nearest integer, a tie toward plus infinity."""
    return (x + Fraction(1, 2)).__floor__()


def _check(strikes: list[int], df: int) -> None:
    if isinstance(df, bool) or not isinstance(df, int) or not 1 <= df <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(k <= 0 for k in strikes) or any(strikes[i] >= strikes[i + 1] for i in range(len(strikes) - 1)):
        raise ValueError("strikes must be strictly increasing and positive")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check([strike_cents], df_ppm)
    gap = Fraction(call_cents - put_cents) - (Fraction(spot_cents) - Fraction(strike_cents * df_ppm, PPM))
    return _signed_round(gap)


def _is_concave_kink(strikes: list[int], calls: list[int], j: int) -> bool:
    # call strictly above the chord  <=>  left slope strictly greater than right slope
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    return (calls[j] - calls[j - 1]) * (k2 - k1) > (calls[j + 1] - calls[j]) * (k1 - k0)


def _gross_over_chord(strikes: list[int], calls: list[int], j: int) -> Fraction:
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    # call minus chord, written with one denominator
    return Fraction(calls[j] * (k2 - k0) - calls[j - 1] * (k2 - k1) - calls[j + 1] * (k1 - k0), k2 - k0)


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check(strikes_cents, df_ppm)
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(f"calls need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls")
    return [j for j in range(1, len(strikes_cents) - 1) if _is_concave_kink(strikes_cents, calls_cents, j)]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    df = chain["df_ppm"]
    fee, spread = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    _check(strikes, df)
    if len(calls) != len(strikes) or len(puts) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts")
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gap = Fraction(calls[k] - puts[k]) - (Fraction(chain["spot_cents"]) - Fraction(strike * df, PPM))
        gross = _round_half_up_away(abs(gap))
        if gross - cost > 0:
            side = (
                "the call is expensive against the synthetic forward, so write the call and buy the put and the underlying"
                if gap > 0
                else "the call is dear against the reverse: buy it against selling the put and the underlying"
            )
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": f"Parity: P1, P2, P3, P4 and P6 apply; {side}; net {gross - cost}."})
    for j in convexity_violations(strikes, calls, df):
        gross = _round_half_up_away(_gross_over_chord(strikes, calls, j))
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": f"Convexity: P1, P2, P5 and P6; the middle quote sits above the line through its neighbours; net {gross - cost}."})
    return out

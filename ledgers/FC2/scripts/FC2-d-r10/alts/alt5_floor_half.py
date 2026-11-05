"""Alternative correct scanner: the reference algorithm with rounding by math.floor(x + 1/2) and Fraction throughout."""
import math
from fractions import Fraction
from typing import Any

PPM = 1_000_000


def _rnd(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def _mag(x: Fraction) -> int:
    return math.floor(abs(x) + Fraction(1, 2))


def _gap(c: int, p: int, s: int, k: int, df: int) -> Fraction:
    return Fraction(c) - Fraction(p) - (Fraction(s) - Fraction(k * df, PPM))


def _lessconv(strikes: list[int], calls: list[int], j: int) -> Fraction:
    lo, mi, hi = strikes[j - 1], strikes[j], strikes[j + 1]
    return Fraction(hi - mi, hi - lo) * calls[j - 1] + Fraction(mi - lo, hi - lo) * calls[j + 1] - calls[j]


def _checks(strikes: list[int], calls: list[int], puts: list[int] | None, df: int) -> None:
    if not 1 <= df <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(k <= 0 for k in strikes) or any(b <= a for a, b in zip(strikes, strikes[1:])):
        raise ValueError("strikes must be strictly increasing and positive")
    if len(calls) != len(strikes) or (puts is not None and len(puts) != len(strikes)):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts) if puts is not None else len(strikes)} puts")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _checks([strike_cents], [call_cents], [put_cents], df_ppm)
    return _rnd(_gap(call_cents, put_cents, spot_cents, strike_cents, df_ppm))


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _checks(strikes_cents, calls_cents, None, df_ppm)
    return [j for j in range(1, len(strikes_cents) - 1) if _lessconv(strikes_cents, calls_cents, j) < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    df = chain["df_ppm"]
    _checks(strikes, calls, puts, df)
    fee, half = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    if fee < 0 or half < 0:
        raise ValueError("cost terms must be non-negative")
    per = 3 * (fee + half)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gross = _mag(_gap(calls[k], puts[k], chain["spot_cents"], strike, df))
        if gross - per > 0:
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - per,
                        "explanation": "parity under P1, P2, P3, P4 and P6, with the cost of three legs netted."})
    for j in convexity_violations(strikes, calls, df):
        gross = _mag(_lessconv(strikes, calls, j))
        if gross - per > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - per,
                        "explanation": "convexity in strike under P1, P2, P5 and P6, with the cost of three legs netted."})
    return out

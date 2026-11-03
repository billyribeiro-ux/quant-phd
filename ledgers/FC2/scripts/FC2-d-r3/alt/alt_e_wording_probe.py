"""Alternative E (verifier round 3, wording probe): arithmetic identical to the reference in substance, with correct
explanations that also describe the other legs as cheap or rich (the put, the underlying) in the same sentence."""

from __future__ import annotations

import itertools
from fractions import Fraction
from typing import Any

PPM = 1_000_000
LEGS = 3


def _chk(df: Any, strikes: list[Any], calls: list[Any], puts: list[Any] | None) -> None:
    if isinstance(df, bool) or not isinstance(df, int) or not 1 <= df <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(isinstance(k, bool) or not isinstance(k, int) or k <= 0 for k in strikes) or any(
        b <= a for a, b in itertools.pairwise(strikes)
    ):
        raise ValueError("strikes must be strictly increasing and positive")
    n = len(strikes) if puts is None else len(puts)
    if len(calls) != len(strikes) or n != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {n} puts")


def _half_up(x: Fraction) -> int:
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _chk(df_ppm, [strike_cents], [call_cents], None)
    return _half_up(Fraction(call_cents - put_cents - spot_cents) + Fraction(strike_cents * df_ppm, PPM))


def _second(strikes: list[int], calls: list[int], j: int) -> Fraction:
    lo, m, hi = strikes[j - 1], strikes[j], strikes[j + 1]
    return Fraction(hi - m, hi - lo) * calls[j - 1] + Fraction(m - lo, hi - lo) * calls[j + 1] - calls[j]


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _chk(df_ppm, strikes_cents, calls_cents, None)
    return [j for j in range(1, len(strikes_cents) - 1) if _second(strikes_cents, calls_cents, j) < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    _chk(chain["df_ppm"], strikes, calls, puts)
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    per = LEGS * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        g = Fraction(calls[k] - puts[k] - chain["spot_cents"]) + Fraction(strike * chain["df_ppm"], PPM)
        gross = _half_up(abs(g))
        net = gross - per
        if net > 0:
            if g > 0:
                text = (f"Parity: the call is rich, not cheap, against the synthetic forward, so sell the call; "
                        f"buy the put and the underlying and borrow the discounted strike (P1, P2, P3, P4, P6). "
                        f"Net {net} cents after {LEGS} legs at fee {fee} plus half-spread {spread}.")
            else:
                text = (f"Parity: the call is cheap, not rich, against the synthetic forward, so buy the call; "
                        f"sell the put and the underlying and lend the discounted strike (P1, P2, P3, P4, P6). "
                        f"Net {net} cents after {LEGS} legs at fee {fee} plus half-spread {spread}.")
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": net,
                        "explanation": text})
    for j in convexity_violations(strikes, calls, chain["df_ppm"]):
        gross = _half_up(-_second(strikes, calls, j))
        net = gross - per
        if net > 0:
            text = (f"Convexity in strike (P1, P2, P5, P6): the middle call is above the chord of its neighbours, "
                    f"so sell it and buy the wings; the cost is {LEGS} legs at fee {fee} plus half-spread {spread}, "
                    f"net {net} cents.")
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": net,
                        "explanation": text})
    return out

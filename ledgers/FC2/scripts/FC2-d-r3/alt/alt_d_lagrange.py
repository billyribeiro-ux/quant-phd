"""Alternative D (verifier round 3, independent): Lagrange interpolation weights over the three neighbouring strikes,
math.floor for the half-up rounding. Explanations use the reference wording."""

from __future__ import annotations

import math
import itertools
from fractions import Fraction
from typing import Any

PPM = 1_000_000
LEGS = 3


def _valid_df(v: Any) -> None:
    if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _valid_strikes(s: list[Any]) -> None:
    if any(isinstance(k, bool) or not isinstance(k, int) or k <= 0 for k in s) or any(
        b <= a for a, b in itertools.pairwise(s)
    ):
        raise ValueError("strikes must be strictly increasing and positive")


def _valid_lengths(s: list[Any], c: list[Any], p: list[Any] | None) -> None:
    n = len(s) if p is None else len(p)
    if len(c) != len(s) or n != len(s):
        raise ValueError(f"calls and puts need one quote per strike: {len(s)} strikes, {len(c)} calls, {n} puts")


def _nearest(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _valid_df(df_ppm)
    _valid_strikes([strike_cents])
    return _nearest(Fraction(call_cents) - Fraction(put_cents) - Fraction(spot_cents)
                    + Fraction(strike_cents * df_ppm, PPM))


def _lagrange_at(xs: list[int], ys: list[int], x: int) -> Fraction:
    total = Fraction(0)
    for i, xi in enumerate(xs):
        basis = Fraction(1)
        for j, xj in enumerate(xs):
            if j != i:
                basis *= Fraction(x - xj, xi - xj)
        total += basis * ys[i]
    return total


def _second(strikes: list[int], calls: list[int], j: int) -> Fraction:
    xs = [strikes[j - 1], strikes[j + 1]]
    ys = [calls[j - 1], calls[j + 1]]
    return _lagrange_at(xs, ys, strikes[j]) - calls[j]


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _valid_df(df_ppm)
    _valid_strikes(strikes_cents)
    _valid_lengths(strikes_cents, calls_cents, None)
    return [j for j in range(1, len(strikes_cents) - 1) if _second(strikes_cents, calls_cents, j) < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    _valid_df(chain["df_ppm"])
    _valid_strikes(strikes)
    _valid_lengths(strikes, calls, puts)
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    per = LEGS * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        g = Fraction(calls[k]) - Fraction(puts[k]) - (Fraction(chain["spot_cents"])
                                                       - Fraction(strike * chain["df_ppm"], PPM))
        gross = _nearest(abs(g))
        net = gross - per
        if net > 0:
            signed = _nearest(g)
            if signed > 0:
                action = "sell the call, buy the put and the underlying, and borrow the discounted strike"
                direction = "the call less the put exceeds the spot less the discounted strike"
            else:
                action = "buy the call, sell the put and the underlying, and lend the discounted strike"
                direction = "the call less the put is below the spot less the discounted strike"
            text = (f"put-call parity (P1 European exercise, P2 one expiry, P3 no income, P4 the supplied discount "
                    f"factor): {direction}, so {action}; net {net} cents after {LEGS} legs at fee {fee} plus "
                    f"half-spread {spread} (P6).")
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": net,
                        "explanation": text})
    for j in convexity_violations(strikes, calls, chain["df_ppm"]):
        gross = _nearest(-_second(strikes, calls, j))
        net = gross - per
        if net > 0:
            text = (f"convexity in strike (P1 European exercise, P2 one expiry, P5 quotes are present values at the "
                    f"valuation date): the middle call sits above the chord of its two neighbours, so sell the middle "
                    f"call and buy the wings in the chord weights; net {net} cents after {LEGS} legs at fee {fee} plus "
                    f"half-spread {spread} (P6).")
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": net,
                        "explanation": text})
    return out

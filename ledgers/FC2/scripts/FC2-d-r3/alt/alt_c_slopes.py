"""Alternative C (verifier round 3, independent): convexity decided by comparing adjacent chord slopes. The parity
explanation uses the richness wording ('the call is rich') and the trade, and the gross is taken from the exact gap
(magnitude first, then one half-up rounding), not from the signed rounded gap."""

from __future__ import annotations

import itertools
from fractions import Fraction
from typing import Any

PPM = 1_000_000
LEGS = 3


def _df(v: Any) -> None:
    if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _strikes(s: list[Any]) -> None:
    if any(isinstance(k, bool) or not isinstance(k, int) or k <= 0 for k in s):
        raise ValueError("strikes must be strictly increasing and positive")
    if any(b <= a for a, b in itertools.pairwise(s)):
        raise ValueError("strikes must be strictly increasing and positive")


def _lens(s: list[Any], c: list[Any], p: list[Any] | None) -> None:
    np_ = len(s) if p is None else len(p)
    if len(c) != len(s) or np_ != len(s):
        raise ValueError(f"calls and puts need one quote per strike: {len(s)} strikes, {len(c)} calls, {np_} puts")


def _half_up(x: Fraction) -> int:
    return (x + Fraction(1, 2)).__floor__()


def _exact_gap(call: int, put: int, spot: int, strike: int, df: int) -> Fraction:
    return Fraction(call - put - spot) + Fraction(strike * df, PPM)


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _df(df_ppm)
    _strikes([strike_cents])
    return _half_up(_exact_gap(call_cents, put_cents, spot_cents, strike_cents, df_ppm))


def _is_above_chord(strikes: list[int], calls: list[int], j: int) -> bool:
    lo, m, hi = strikes[j - 1], strikes[j], strikes[j + 1]
    left_slope = Fraction(calls[j] - calls[j - 1], m - lo)
    right_slope = Fraction(calls[j + 1] - calls[j], hi - m)
    return left_slope > right_slope  # the middle call is above the chord exactly when the slope falls


def _excess(strikes: list[int], calls: list[int], j: int) -> Fraction:
    lo, m, hi = strikes[j - 1], strikes[j], strikes[j + 1]
    chord = Fraction(calls[j - 1] * (hi - m) + calls[j + 1] * (m - lo), hi - lo)
    return Fraction(calls[j]) - chord


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _df(df_ppm)
    _strikes(strikes_cents)
    _lens(strikes_cents, calls_cents, None)
    return [j for j in range(1, len(strikes_cents) - 1) if _is_above_chord(strikes_cents, calls_cents, j)]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    s = list(chain["strikes_cents"])
    c = list(chain["call_cents"])
    p = list(chain["put_cents"])
    _df(chain["df_ppm"])
    _strikes(s)
    _lens(s, c, p)
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    per = LEGS * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(s):
        exact = _exact_gap(c[k], p[k], chain["spot_cents"], strike, chain["df_ppm"])
        gross = _half_up(abs(exact))
        net = gross - per
        if net > 0:
            if exact > 0:
                exp = (f"Parity: the call is rich, so sell the call; buy the put and the underlying and borrow the "
                       f"discounted strike. P1, P2, P3, P4 and P6 apply. Net {net} cents after {LEGS} legs at fee "
                       f"{fee} plus half-spread {spread}.")
            else:
                exp = (f"Parity: the call is cheap, so buy the call; sell the put and the underlying and lend the "
                       f"discounted strike. P1, P2, P3, P4 and P6 apply. Net {net} cents after {LEGS} legs at fee "
                       f"{fee} plus half-spread {spread}.")
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": net,
                        "explanation": exp})
    for j in convexity_violations(s, c, chain["df_ppm"]):
        gross = _half_up(-(-_excess(s, c, j)))  # the excess over the chord, rounded once, half up
        net = gross - per
        if net > 0:
            exp = (f"Convexity in strike: the middle call is above the chord of its neighbours, so sell the middle "
                   f"call. P1, P2, P5 and P6 apply. Net {net} cents after {LEGS} legs at fee {fee} plus half-spread "
                   f"{spread}.")
            out.append({"kind": "convexity", "strike_cents": s[j], "gross_cents": gross, "net_cents": net,
                        "explanation": exp})
    return out

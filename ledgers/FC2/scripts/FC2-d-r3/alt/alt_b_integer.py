"""Alternative B (verifier round 3, independent): integer-only arithmetic. Values are scaled by 10^6 cents; rounding
half up is floor((2x + d) / (2d)) for d > 0, which is exact for negative x too (floor division)."""

from __future__ import annotations

import itertools
from typing import Any

PPM = 1_000_000
LEGS = 3


def _check_df(df_ppm: Any) -> None:
    if isinstance(df_ppm, bool) or not isinstance(df_ppm, int) or not 1 <= df_ppm <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _check_strikes(strikes: list[Any]) -> None:
    ok = all(not isinstance(k, bool) and isinstance(k, int) and k > 0 for k in strikes)
    if not ok or any(b <= a for a, b in itertools.pairwise(strikes)):
        raise ValueError("strikes must be strictly increasing and positive")


def _check_lengths(strikes: list[Any], calls: list[Any], puts: list[Any] | None) -> None:
    n_puts = len(strikes) if puts is None else len(puts)
    if len(calls) != len(strikes) or n_puts != len(strikes):
        raise ValueError(
            f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {n_puts} puts"
        )


def _half_up_ratio(num: int, den: int) -> int:
    """round(num / den) with a tie toward plus infinity, for den > 0, in integers only."""
    return (2 * num + den) // (2 * den)


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check_df(df_ppm)
    _check_strikes([strike_cents])
    scaled = (call_cents - put_cents - spot_cents) * PPM + strike_cents * df_ppm  # gap * 10^6
    return _half_up_ratio(scaled, PPM)


def _chord_numerator(strikes: list[int], calls: list[int], j: int) -> tuple[int, int]:
    low, mid, high = strikes[j - 1], strikes[j], strikes[j + 1]
    d = high - low
    return calls[j - 1] * (high - mid) + calls[j + 1] * (mid - low) - calls[j] * d, d


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check_df(df_ppm)
    _check_strikes(strikes_cents)
    _check_lengths(strikes_cents, calls_cents, None)
    found = []
    for j in range(1, len(strikes_cents) - 1):
        num, _ = _chord_numerator(strikes_cents, calls_cents, j)
        if num < 0:  # the second difference num / d is negative
            found.append(j)
    return found


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    spot = chain["spot_cents"]
    df = chain["df_ppm"]
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    _check_df(df)
    _check_strikes(strikes)
    _check_lengths(strikes, calls, puts)
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    per = LEGS * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        scaled = (calls[k] - puts[k] - spot) * PPM + strike * df
        gross = _half_up_ratio(abs(scaled), PPM)
        net = gross - per
        if net > 0:
            rich = scaled > 0
            trade = "sell the call, buy the put and the underlying" if rich else "buy the call, sell the put and the underlying"
            text = (
                f"Put-call parity: the call is {'rich' if rich else 'cheap'} against the synthetic forward, so {trade}; "
                f"the discounted strike is borrowed or lent. Labels P1, P2, P3, P4 and P6 apply. Net {net} cents after "
                f"three legs at fee {fee} plus half-spread {spread}."
            )
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": net,
                        "explanation": text})
    for j in convexity_violations(strikes, calls, df):
        num, d = _chord_numerator(strikes, calls, j)
        gross = _half_up_ratio(-num, d)
        net = gross - per
        if net > 0:
            text = (
                "Convexity: the middle call lies above the chord of its two neighbours; sell it and buy the wings. "
                f"Labels P1, P2, P5 and P6 apply. Net {net} cents after three legs at fee {fee} plus half-spread {spread}."
            )
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": net,
                        "explanation": text})
    return out

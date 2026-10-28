"""Convexity tested with the first difference: a violation is a call that falls between neighbours, not a second difference.

Mutant of the reference scanner: one change, everything else as in reference.py.
"""

from __future__ import annotations

import itertools
from fractions import Fraction
from typing import Any

PPM = 1_000_000
DF_MIN = 1
DF_MAX = PPM
LEGS_PER_FINDING = 3  # each finding trades three legs: parity uses call, put and underlying; convexity uses three calls


def _half_up(x: Fraction) -> int:
    """The nearest integer to x, a tie going toward plus infinity: floor(x + 1/2)."""
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)


def _check_df(df_ppm: int) -> None:
    if isinstance(df_ppm, bool) or not isinstance(df_ppm, int) or not DF_MIN <= df_ppm <= DF_MAX:
        raise ValueError("df_ppm must lie in 1..1000000")


def _check_strikes(strikes: list[int]) -> None:
    if any(isinstance(k, bool) or not isinstance(k, int) or k <= 0 for k in strikes) or any(
        b <= a for a, b in itertools.pairwise(strikes)
    ):
        raise ValueError("strikes must be strictly increasing and positive")


def _check_lengths(strikes: list[int], calls: list[int], puts: list[int] | None) -> None:
    """Every quote list has one entry per strike; the message names the lengths."""
    if len(calls) != len(strikes) or (puts is not None and len(puts) != len(strikes)):
        raise ValueError(
            f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, "
            f"{len(strikes) if puts is None else len(puts)} puts"
        )


def _check_cost(fee: int, spread: int) -> None:
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    """The parity gap C - P - (S - K df) in cents, with df = df_ppm / 1e6, rounded once, a tie going up."""
    _check_df(df_ppm)
    if isinstance(strike_cents, bool) or not isinstance(strike_cents, int) or strike_cents <= 0:
        raise ValueError("strikes must be strictly increasing and positive")
    gap = Fraction(call_cents) - Fraction(put_cents) - (Fraction(spot_cents) - Fraction(strike_cents * df_ppm, PPM))
    return _half_up(gap)


def _second_difference(strikes: list[int], calls: list[int], j: int) -> Fraction:
    """The chord of the two neighbours of strike j, at strike j, less the call at j: negative means convexity fails."""
    low, mid, high = strikes[j - 1], strikes[j], strikes[j + 1]
    w_low = Fraction(high - mid, high - low)
    w_high = Fraction(mid - low, high - low)
    return w_low * calls[j - 1] + w_high * calls[j + 1] - calls[j]


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    """The interior indices j at which the second difference in strike is negative (a convexity failure).

    The quotes are present values at the valuation date, so the test compares them without discounting, and the
    sign does not depend on df_ppm. df_ppm is validated and not used otherwise.
    """
    _check_df(df_ppm)
    _check_strikes(strikes_cents)
    _check_lengths(strikes_cents, calls_cents, None)
    return [j for j in range(1, len(strikes_cents) - 1) if calls_cents[j + 1] - calls_cents[j] < 0]


def _explain_parity(gap: int, net: int, fee: int, spread: int) -> str:
    if gap > 0:
        action = "sell the call, buy the put and the underlying, and borrow the discounted strike"
        direction = "the call less the put exceeds the spot less the discounted strike"
    else:
        action = "buy the call, sell the put and the underlying, and lend the discounted strike"
        direction = "the call less the put is below the spot less the discounted strike"
    return (
        f"put-call parity (P1 European exercise, P2 one expiry, P3 no income, P4 the supplied discount factor): "
        f"{direction}, so {action}; net {net} cents after {LEGS_PER_FINDING} legs at fee {fee} plus half-spread "
        f"{spread} (P6)."
    )


def _explain_convexity(net: int, fee: int, spread: int) -> str:
    return (
        "convexity in strike (P1 European exercise, P2 one expiry, "
        "P5 quotes are present values at the valuation date): "
        "the middle call sits above the chord of its two neighbours, so sell the middle call and buy the wings in "
        f"the chord weights; net {net} cents after {LEGS_PER_FINDING} legs at fee {fee} plus half-spread {spread} (P6)."
    )


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    """One record per finding whose net amount is strictly positive: parity findings, then convexity findings."""
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    spot = chain["spot_cents"]
    df_ppm = chain["df_ppm"]
    cost = chain["cost"]
    fee = cost["fee_cents_per_contract"]
    spread = cost["half_spread_cents"]
    _check_df(df_ppm)
    _check_strikes(strikes)
    _check_lengths(strikes, calls, puts)
    _check_cost(fee, spread)
    per_finding = LEGS_PER_FINDING * (fee + spread)
    findings: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gap = Fraction(calls[k]) - Fraction(puts[k]) - (Fraction(spot) - Fraction(strike * df_ppm, PPM))
        gross = _half_up(abs(gap))
        net = gross - per_finding
        if net > 0:
            findings.append(
                {
                    "kind": "parity",
                    "strike_cents": strike,
                    "gross_cents": gross,
                    "net_cents": net,
                    "explanation": _explain_parity(_half_up(gap), net, fee, spread),
                }
            )
    for j in convexity_violations(strikes, calls, df_ppm):
        gross = _half_up(-_second_difference(strikes, calls, j))
        net = gross - per_finding
        if net > 0:
            findings.append(
                {
                    "kind": "convexity",
                    "strike_cents": strikes[j],
                    "gross_cents": gross,
                    "net_cents": net,
                    "explanation": _explain_convexity(net, fee, spread),
                }
            )
    return findings

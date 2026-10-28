"""Alternative 2 (alt1 with the page phrase in the length message): integer arithmetic in micro-cents, no Fraction; cross-multiplied chord test."""
from __future__ import annotations

from typing import Any

MICRO = 1_000_000


def _validate_df(df_ppm: int) -> None:
    if type(df_ppm) is not int or not (1 <= df_ppm <= MICRO):
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _validate_strikes(strikes: list[int]) -> None:
    if any(type(k) is not int or k <= 0 for k in strikes) or any(a >= b for a, b in zip(strikes, strikes[1:])):
        raise ValueError("strikes must be strictly increasing and positive")


def _round_micro(num_micro: int) -> int:
    # num_micro is an amount in units of 1e-6 cent; nearest cent, tie toward plus infinity
    return (num_micro + MICRO // 2) // MICRO


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _validate_df(df_ppm)
    if type(strike_cents) is not int or strike_cents <= 0:
        raise ValueError("strikes must be strictly increasing and positive")
    micro = (call_cents - put_cents - spot_cents) * MICRO + strike_cents * df_ppm
    return _round_micro(micro)


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _validate_df(df_ppm)
    _validate_strikes(strikes_cents)
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls")
    out = []
    for j in range(1, len(strikes_cents) - 1):
        k0, k1, k2 = strikes_cents[j - 1 : j + 2]
        c0, c1, c2 = calls_cents[j - 1 : j + 2]
        # chord(k1) - c1 = [c0 (k2-k1) + c2 (k1-k0) - c1 (k2-k0)] / (k2-k0); the denominator is positive
        if c0 * (k2 - k1) + c2 * (k1 - k0) - c1 * (k2 - k0) < 0:
            out.append(j)
    return out


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    df = chain["df_ppm"]
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    if len(calls) != len(strikes) or len(puts) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts")
    cost = 3 * (fee + spread)
    rows: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        micro = (calls[k] - puts[k] - chain["spot_cents"]) * MICRO + strike * df
        gross = (2 * abs(micro) + MICRO) // (2 * MICRO)  # nearest cent to the magnitude, a tie away from zero
        if gross - cost > 0:
            rows.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                         "explanation": "parity (P1, P2, P3, P4 the supplied discount factor, P6 cost): "
                                        "the gap is C - P - (S - K df) at this strike, net after three legs."})
    for j in convexity_violations(strikes, calls, df):
        k0, k1, k2 = strikes[j - 1 : j + 2]
        c0, c1, c2 = calls[j - 1 : j + 2]
        num = c1 * (k2 - k0) - (c0 * (k2 - k1) + c2 * (k1 - k0))  # positive for a violation, in units of 1/(k2-k0)
        gross = _half_up_frac(num, k2 - k0)
        if gross - cost > 0:
            rows.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                         "explanation": "convexity in strike (P1, P2, P5 present values, P6 cost): the call sits above "
                                        "its chord of the two neighbours."})
    return rows


def _half_up_frac(num: int, den: int) -> int:
    # nearest integer to num/den (den > 0), tie toward plus infinity
    return (2 * num + den) // (2 * den)

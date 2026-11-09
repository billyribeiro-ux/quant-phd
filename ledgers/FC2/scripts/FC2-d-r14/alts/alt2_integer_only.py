"""Alternative 2 (r14): integer-only arithmetic; every division is a half-up integer division helper."""

from __future__ import annotations

from typing import Any

PPM = 1_000_000
LEGS = 3


def _div_half_up(num: int, den: int) -> int:
    """num / den rounded half up (ties toward plus infinity) for den > 0, using integers only."""
    return (2 * num + den) // (2 * den)


def _mag_half_up(num: int, den: int) -> int:
    """|num| / den rounded half up in magnitude, for den > 0."""
    return (2 * abs(num) + den) // (2 * den)


def _check(strikes: list[int], df: int) -> None:
    if isinstance(df, bool) or not isinstance(df, int) or df < 1 or df > PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    for k in strikes:
        if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
            raise ValueError("strikes must be strictly increasing and positive")
    for i in range(1, len(strikes)):
        if strikes[i] <= strikes[i - 1]:
            raise ValueError("strikes must be strictly increasing and positive")


def _gap_num(call: int, put: int, spot: int, strike: int, df: int) -> int:
    # gap = (call - put - spot) + strike*df/PPM, scaled by PPM so the whole thing is an integer
    return (call - put - spot) * PPM + strike * df


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check([strike_cents], df_ppm)
    return _div_half_up(_gap_num(call_cents, put_cents, spot_cents, strike_cents, df_ppm), PPM)


def _conv_num(strikes: list[int], calls: list[int], j: int) -> tuple[int, int]:
    """(numerator, denominator) of chord-minus-call at strike j; denominator is the neighbour distance (> 0)."""
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    c0, c1, c2 = calls[j - 1], calls[j], calls[j + 1]
    num = (k2 - k1) * c0 + (k1 - k0) * c2 - (k2 - k0) * c1
    return num, k2 - k0


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check(strikes_cents, df_ppm)
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(
            f"calls need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls"
        )
    out = []
    for j in range(1, len(strikes_cents) - 1):
        num, _den = _conv_num(strikes_cents, calls_cents, j)
        if num < 0:
            out.append(j)
    return out


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    df = chain["df_ppm"]
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    _check(strikes, df)
    if len(calls) != len(strikes) or len(puts) != len(strikes):
        raise ValueError(
            f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts"
        )
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = LEGS * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        num = _gap_num(calls[k], puts[k], chain["spot_cents"], strike, df)
        gross = _mag_half_up(num, PPM)
        net = gross - cost
        if net > 0:
            out.append(
                {
                    "kind": "parity",
                    "strike_cents": strike,
                    "gross_cents": gross,
                    "net_cents": net,
                    "explanation": "put-call parity (P1, P2, P3, P4, P6): the parity gap is outside the "
                    f"cost; net {net} after {LEGS} legs.",
                }
            )
    for j in convexity_violations(strikes, calls, df):
        num, den = _conv_num(strikes, calls, j)
        gross = _mag_half_up(num, den)
        net = gross - cost
        if net > 0:
            out.append(
                {
                    "kind": "convexity",
                    "strike_cents": strikes[j],
                    "gross_cents": gross,
                    "net_cents": net,
                    "explanation": "convexity in strike (P1, P2, P5, P6): the call is above the chord; "
                    f"net {net} after {LEGS} legs.",
                }
            )
    return out

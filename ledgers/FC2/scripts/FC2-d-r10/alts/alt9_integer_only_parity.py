"""Alternative correct scanner 9: parity gap in integer ppm arithmetic, half-up by integer floor, net cutoff net >= 1."""
from __future__ import annotations

from typing import Any

PPM = 1_000_000
LEGS = 3


def _check_df(df: int) -> None:
    if isinstance(df, bool) or not isinstance(df, int) or not 1 <= df <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _check_strikes(strikes: list[int]) -> None:
    for k in strikes:
        if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
            raise ValueError("strikes must be strictly increasing and positive")
    for a, b in zip(strikes, strikes[1:]):
        if not b > a:
            raise ValueError("strikes must be strictly increasing and positive")


def _gap_ppm(call: int, put: int, spot: int, strike: int, df: int) -> int:
    # C - P - S + K*df, in units of 1e-6 cent, all integers
    return (call - put - spot) * PPM + strike * df


def _round_ppm(x_ppm: int) -> int:
    # nearest cent of x_ppm / 1e6, a tie toward plus infinity: floor((x + 0.5e6) / 1e6) in integers
    return (x_ppm + PPM // 2) // PPM


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check_df(df_ppm)
    _check_strikes([strike_cents])
    return _round_ppm(_gap_ppm(call_cents, put_cents, spot_cents, strike_cents, df_ppm))


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check_df(df_ppm)
    _check_strikes(strikes_cents)
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(f"calls need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls")
    out: list[int] = []
    for j in range(1, len(strikes_cents) - 1):
        k0, k1, k2 = strikes_cents[j - 1], strikes_cents[j], strikes_cents[j + 1]
        c0, c1, c2 = calls_cents[j - 1], calls_cents[j], calls_cents[j + 1]
        span = k2 - k0
        # call above the chord  <=>  span * c1 > (k2 - k1) * c0 + (k1 - k0) * c2
        if span * c1 > (k2 - k1) * c0 + (k1 - k0) * c2:
            out.append(j)
    return out


def _half_up_ratio(num: int, den: int) -> int:
    # nearest integer to num/den (den > 0), a tie toward plus infinity
    return (2 * num + den) // (2 * den)


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
    if len(calls) != len(strikes) or len(puts) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts")
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = LEGS * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        g = _gap_ppm(calls[k], puts[k], spot, strike, df)
        gross = _round_ppm(abs(g))
        net = gross - cost
        if net >= 1:
            sign = "sell the call, buy the put and the underlying" if g > 0 else "buy the call, sell the put and the underlying"
            out.append({
                "kind": "parity",
                "strike_cents": strike,
                "gross_cents": gross,
                "net_cents": net,
                "explanation": f"parity with P1, P2, P3, P4 (the supplied factor) and P6 (cost): {sign}; net {net}.",
            })
    for j in convexity_violations(strikes, calls, df):
        k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
        c0, c1, c2 = calls[j - 1], calls[j], calls[j + 1]
        span = k2 - k0
        excess_num = span * c1 - ((k2 - k1) * c0 + (k1 - k0) * c2)  # > 0 at a violation, in units of 1/span cent
        gross = _half_up_ratio(excess_num, span)
        net = gross - cost
        if net >= 1:
            out.append({
                "kind": "convexity",
                "strike_cents": strikes[j],
                "gross_cents": gross,
                "net_cents": net,
                "explanation": f"convexity in strike with P1, P2, P5 and P6 (cost): the middle call sits above its chord; net {net}.",
            })
    return out

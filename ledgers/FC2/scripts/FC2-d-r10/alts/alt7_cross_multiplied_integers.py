"""Alternative 7 (verifier round 5): integers only, cross-multiplied convexity test and exact half-up division.

A correct implementation written independently of reference.py. Parity: the gap times df_ppm is kept as an integer
numerator over 1_000_000, and the cent is rounded with floor((2n + d) / (2d)). Convexity: for strikes K1 < K2 < K3 the
chord weights are (K3 - K2)/(K3 - K1) on C1 and (K2 - K1)/(K3 - K1) on C3, so the second difference is N/D with
N = (K3 - K2) C1 + (K2 - K1) C3 - D C2 and D = K3 - K1 > 0. The call is above the chord when N < 0, and the gross is
the magnitude N/D rounded half up, computed as floor((2|N| + D) / (2D)). Standard library only.
"""

from __future__ import annotations

from typing import Any

PPM = 1_000_000
LEGS = 3


def _half_up_div(num: int, den: int) -> int:
    """floor(num/den + 1/2) for den > 0, with integers only."""
    assert den > 0
    return (2 * num + den) // (2 * den)


def _need_df(df_ppm: int) -> None:
    if type(df_ppm) is not int or not 1 <= df_ppm <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _need_strikes(strikes: list[int]) -> None:
    if any(type(k) is not int or k <= 0 for k in strikes) or any(b <= a for a, b in zip(strikes, strikes[1:])):
        raise ValueError("strikes must be strictly increasing and positive")


def _need_lengths(strikes: list[int], calls: list[int], puts: list[int] | None) -> None:
    if len(calls) != len(strikes) or (puts is not None and len(puts) != len(strikes)):
        raise ValueError(f"need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, "
                         f"{len(strikes) if puts is None else len(puts)} puts")


def _gap_numerator(call: int, put: int, spot: int, strike: int, df_ppm: int) -> int:
    # C - P - S + K df, times PPM
    return (call - put - spot) * PPM + strike * df_ppm


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _need_df(df_ppm)
    _need_strikes([strike_cents])
    num = _gap_numerator(call_cents, put_cents, spot_cents, strike_cents, df_ppm)
    # floor(num/PPM + 1/2) for a signed numerator
    return (2 * num + PPM) // (2 * PPM)


def _convexity_numerator(strikes: list[int], calls: list[int], j: int) -> tuple[int, int]:
    k1, k2, k3 = strikes[j - 1], strikes[j], strikes[j + 1]
    c1, c2, c3 = calls[j - 1], calls[j], calls[j + 1]
    d = k3 - k1
    n = (k3 - k2) * c1 + (k2 - k1) * c3 - d * c2
    return n, d


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _need_df(df_ppm)
    _need_strikes(strikes_cents)
    _need_lengths(strikes_cents, calls_cents, None)
    out = []
    for j in range(1, len(strikes_cents) - 1):
        n, _ = _convexity_numerator(strikes_cents, calls_cents, j)
        if n < 0:
            out.append(j)
    return out


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    spot = chain["spot_cents"]
    df_ppm = chain["df_ppm"]
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    _need_df(df_ppm)
    _need_strikes(strikes)
    _need_lengths(strikes, calls, puts)
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = LEGS * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        num = _gap_numerator(calls[k], puts[k], spot, strike, df_ppm)
        gross = _half_up_div(abs(num), PPM)
        net = gross - cost
        if net > 0:
            sign = "parity gap positive" if num > 0 else "parity gap negative"
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": net,
                        "explanation": f"parity (P1 European, P2 one expiry, P3 no income, P4 supplied factor, "
                                       f"P6 cost): {sign}; net {net} after {LEGS} legs."})
    for j in convexity_violations(strikes, calls, df_ppm):
        n, d = _convexity_numerator(strikes, calls, j)
        gross = _half_up_div(-n, d)
        net = gross - cost
        if net > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": net,
                        "explanation": f"convexity in strike (P1 European, P2 one expiry, P5 present values, "
                                       f"P6 cost): net {net} after {LEGS} legs."})
    return out

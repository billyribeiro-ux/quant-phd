"""Alternative correct scanner 2: integer-only arithmetic, scaled by 1e6 and by the strike span, with a floor-division half-up helper."""

from __future__ import annotations

from typing import Any

PPM = 1_000_000


def _floor_half_up(num: int, den: int) -> int:
    """Nearest integer to num/den, ties toward plus infinity, den > 0."""
    return (2 * num + den) // (2 * den)


def _validate(strikes: list[int], df: int) -> None:
    if not isinstance(df, int) or isinstance(df, bool) or df < 1 or df > PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(k <= 0 for k in strikes) or any(strikes[i + 1] <= strikes[i] for i in range(len(strikes) - 1)):
        raise ValueError("strikes must be strictly increasing and positive")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _validate([strike_cents], df_ppm)
    scaled = (call_cents - put_cents - spot_cents) * PPM + strike_cents * df_ppm  # gap * 1e6
    return _floor_half_up(scaled, PPM)


def _scaled_second_difference(strikes: list[int], calls: list[int], j: int) -> tuple[int, int]:
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    den = k2 - k0
    return (k2 - k1) * calls[j - 1] + (k1 - k0) * calls[j + 1] - den * calls[j], den


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _validate(strikes_cents, df_ppm)
    if len(calls_cents) != len(strikes_cents):
        raise ValueError(f"calls need one quote per strike: {len(strikes_cents)} strikes, {len(calls_cents)} calls")
    return [j for j in range(1, len(strikes_cents) - 1) if _scaled_second_difference(strikes_cents, calls_cents, j)[0] < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    df = chain["df_ppm"]
    fee, spread = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    _validate(strikes, df)
    if len(calls) != len(strikes) or len(puts) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {len(puts)} puts")
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        scaled = (calls[k] - puts[k] - chain["spot_cents"]) * PPM + strike * df
        gross = _floor_half_up(abs(scaled), PPM)
        if gross - cost > 0:
            text = ("Parity (P1, P2, P3, P4, P6): the call is rich against the synthetic forward; sell the call"
                    if scaled > 0 else
                    "Parity (P1, P2, P3, P4, P6): the call is cheap against the synthetic forward; buy the call")
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": f"{text}, net {gross - cost}."})
    for j in convexity_violations(strikes, calls, df):
        num, den = _scaled_second_difference(strikes, calls, j)
        gross = _floor_half_up(-num, den)
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": f"Convexity in strike (P1, P2, P5, P6): the middle call is above its chord; net {gross - cost}."})
    return out

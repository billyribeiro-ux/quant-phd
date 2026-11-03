"""Alternative 2 (plan 5.5(2)): integer-only arithmetic with an explicit half-up division helper, no Fraction anywhere."""

from __future__ import annotations

from typing import Any

PPM = 1_000_000


def _half_up_div(numer: int, denom: int) -> int:
    """floor(numer / denom + 1/2) for denom > 0, in integers only."""
    return (2 * numer + denom) // (2 * denom)


def _check_df(df_ppm: int) -> None:
    if isinstance(df_ppm, bool) or not 1 <= df_ppm <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _check_strikes(strikes: list[int]) -> None:
    if any(k <= 0 for k in strikes) or any(strikes[i + 1] <= strikes[i] for i in range(len(strikes) - 1)):
        raise ValueError("the strikes must be strictly increasing and positive")


def _check_lengths(strikes: list[int], calls: list[int], puts: list[int] | None) -> None:
    lens = [len(strikes), len(calls)] + ([len(puts)] if puts is not None else [])
    if any(n != len(strikes) for n in lens):
        raise ValueError(f"quote lists must match the strikes: strikes {len(strikes)}, calls {len(calls)}, puts {lens[2] if puts is not None else 'none'}")


def _gap_times_ppm(call: int, put: int, spot: int, strike: int, df_ppm: int) -> int:
    # C - P - (S - K df), multiplied by 1e6 so every term is an integer: (C-P-S)*1e6 + K*df_ppm
    return (call - put - spot) * PPM + strike * df_ppm


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check_df(df_ppm)
    if strike_cents <= 0:
        raise ValueError("the strikes must be strictly increasing and positive")
    num = _gap_times_ppm(call_cents, put_cents, spot_cents, strike_cents, df_ppm)
    return _half_up_div(num, PPM)


def _convex_numer(strikes: list[int], calls: list[int], j: int) -> tuple[int, int]:
    """Return (numerator, denominator) with denominator > 0 such that chord-less-call = numerator / denominator."""
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    c0, c1, c2 = calls[j - 1], calls[j], calls[j + 1]
    den = k2 - k0
    numer = (k2 - k1) * c0 + (k1 - k0) * c2 - den * c1
    return numer, den


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check_df(df_ppm)
    _check_strikes(strikes_cents)
    _check_lengths(strikes_cents, calls_cents, None)
    out = []
    for j in range(1, len(strikes_cents) - 1):
        numer, _ = _convex_numer(strikes_cents, calls_cents, j)
        if numer < 0:
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
    _check_df(df_ppm)
    _check_strikes(strikes)
    _check_lengths(strikes, calls, puts)
    if fee < 0 or spread < 0:
        raise ValueError("the cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        num = _gap_times_ppm(calls[k], puts[k], spot, strike, df_ppm)
        gross = _half_up_div(abs(num), PPM)
        if gross - cost > 0:
            out.append(
                {
                    "kind": "parity",
                    "strike_cents": strike,
                    "gross_cents": gross,
                    "net_cents": gross - cost,
                    "explanation": "parity: P1, P2, P3, P4 and P6 (the call less the put differs from the forward)",
                }
            )
    for j in convexity_violations(strikes, calls, df_ppm):
        numer, den = _convex_numer(strikes, calls, j)
        gross = _half_up_div(-numer, den)
        if gross - cost > 0:
            out.append(
                {
                    "kind": "convexity",
                    "strike_cents": strikes[j],
                    "gross_cents": gross,
                    "net_cents": gross - cost,
                    "explanation": "convexity in strike: P1, P2, P5 and P6 (the call sits above the chord)",
                }
            )
    return out

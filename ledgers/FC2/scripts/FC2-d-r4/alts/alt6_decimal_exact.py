"""Alternative 6 (replaces the float alternative, plan 5.5(3), which the page's exact-fraction rule rules out): exact decimal arithmetic."""

from __future__ import annotations

from decimal import ROUND_FLOOR, Decimal, getcontext
from typing import Any

getcontext().prec = 60
PPM = 1_000_000


def _half_up(x: Decimal) -> int:
    return int((x + Decimal("0.5")).to_integral_value(rounding=ROUND_FLOOR))


def _check(strikes: list[int], calls: list[int], puts: list[int] | None, df_ppm: int) -> None:
    if not 1 <= df_ppm <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(k <= 0 for k in strikes) or any(b <= a for a, b in zip(strikes, strikes[1:], strict=False)):
        raise ValueError("the strikes must be strictly increasing and positive")
    if len(calls) != len(strikes) or (puts is not None and len(puts) != len(strikes)):
        raise ValueError(
            f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, "
            f"{len(strikes) if puts is None else len(puts)} puts"
        )


def _gap(call: int, put: int, spot: int, strike: int, df_ppm: int) -> Decimal:
    discounted = Decimal(strike) * Decimal(df_ppm) / Decimal(PPM)  # exact: at most 6 extra decimal digits
    return Decimal(call) - Decimal(put) - (Decimal(spot) - discounted)


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check([strike_cents], [call_cents], [put_cents], df_ppm)
    return _half_up(_gap(call_cents, put_cents, spot_cents, strike_cents, df_ppm))


def _chord_less_call(strikes: list[int], calls: list[int], j: int) -> tuple[int, int]:
    """(numerator, denominator), denominator > 0, of chord-less-call, in integers."""
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    c0, c1, c2 = calls[j - 1], calls[j], calls[j + 1]
    den = k2 - k0
    return (k2 - k1) * c0 + (k1 - k0) * c2 - den * c1, den


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check(strikes_cents, calls_cents, None, df_ppm)
    return [j for j in range(1, len(strikes_cents) - 1) if _chord_less_call(strikes_cents, calls_cents, j)[0] < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    df_ppm, spot = chain["df_ppm"], chain["spot_cents"]
    _check(strikes, calls, puts, df_ppm)
    fee, spread = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("the cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gross = _half_up(abs(_gap(calls[k], puts[k], spot, strike, df_ppm)))
        if gross - cost > 0:
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "parity: P1, P2, P3, P4 and P6 (the call less the put differs from the forward)"})
    for j in convexity_violations(strikes, calls, df_ppm):
        numer, den = _chord_less_call(strikes, calls, j)
        gross = _half_up(-Decimal(numer) / Decimal(den))
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": "convexity in strike: P1, P2, P5 and P6 (the call sits above the chord)"})
    return out

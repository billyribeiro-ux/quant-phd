"""Alternative 1 (Decimal): exact Decimal arithmetic; signed ties toward +infinity (ROUND_HALF_CEILING), magnitudes half up."""

from __future__ import annotations

from decimal import ROUND_FLOOR, ROUND_HALF_UP, Decimal
from typing import Any

PPM = 1_000_000
ONE = Decimal(1)


def _bad_df(df_ppm: Any) -> bool:
    return isinstance(df_ppm, bool) or not isinstance(df_ppm, int) or not 1 <= df_ppm <= PPM


def _check(strikes: list[int], calls: list[int], puts: list[int] | None, df_ppm: int) -> None:
    if _bad_df(df_ppm):
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(isinstance(k, bool) or not isinstance(k, int) or k <= 0 for k in strikes) or any(
        b <= a for a, b in zip(strikes, strikes[1:], strict=False)
    ):
        raise ValueError("strikes must be strictly increasing and positive")
    if len(calls) != len(strikes) or (puts is not None and len(puts) != len(strikes)):
        n_puts = len(strikes) if puts is None else len(puts)
        raise ValueError(
            f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {n_puts} puts"
        )


def _check_cost(fee: int, spread: int) -> None:
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")


def _signed_cents(x: Decimal) -> int:
    """floor(x + 1/2): a tie goes toward +infinity (decimal has no half-toward-+inf mode)."""
    return int((x + Decimal("0.5")).to_integral_value(rounding=ROUND_FLOOR))


def _magnitude_cents(x: Decimal) -> int:
    return int(abs(x).quantize(ONE, rounding=ROUND_HALF_UP))


def _gap(call: int, put: int, spot: int, strike: int, df_ppm: int) -> Decimal:
    return Decimal(call) - Decimal(put) - (Decimal(spot) - Decimal(strike) * Decimal(df_ppm) / Decimal(PPM))


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _check([strike_cents], [call_cents], None, df_ppm)
    return _signed_cents(_gap(call_cents, put_cents, spot_cents, strike_cents, df_ppm))


def _chord_numerator(strikes: list[int], calls: list[int], j: int) -> tuple[int, int]:
    """Integer N and D > 0 with chord-minus-call = N / D (exact, no fractions)."""
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    n = (k2 - k1) * calls[j - 1] + (k1 - k0) * calls[j + 1] - (k2 - k0) * calls[j]
    return n, k2 - k0


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _check(strikes_cents, calls_cents, None, df_ppm)
    flagged = []
    for j in range(1, len(strikes_cents) - 1):
        n, _ = _chord_numerator(strikes_cents, calls_cents, j)
        if n < 0:
            flagged.append(j)
    return flagged


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    df_ppm = chain["df_ppm"]
    _check(strikes, calls, puts, df_ppm)
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    _check_cost(fee, spread)
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gap = _gap(calls[k], puts[k], chain["spot_cents"], strike, df_ppm)
        gross = _magnitude_cents(gap)
        net = gross - cost
        if net > 0:
            side = "sell the call, buy the put and the underlying, and borrow the discounted strike"
            if gap < 0:
                side = "buy the call, sell the put and the underlying, and lend the discounted strike"
            out.append(
                {
                    "kind": "parity",
                    "strike_cents": strike,
                    "gross_cents": gross,
                    "net_cents": net,
                    "explanation": (
                        f"Put-call parity holds by P1, P2, P3 (no income), P4 (supplied discount factor) "
                        f"and P6 (cost); the trade is to {side}; net {net} cents."
                    ),
                }
            )
    for j in convexity_violations(strikes, calls, df_ppm):
        n, d = _chord_numerator(strikes, calls, j)
        gross = _magnitude_cents(Decimal(-n) / Decimal(d))
        net = gross - cost
        if net > 0:
            out.append(
                {
                    "kind": "convexity",
                    "strike_cents": strikes[j],
                    "gross_cents": gross,
                    "net_cents": net,
                    "explanation": (
                        f"Convexity in strike, by P1, P2, P5 (present values) and P6 (cost): the middle call is above "
                        f"the chord of its neighbours; net {net} cents."
                    ),
                }
            )
    return out

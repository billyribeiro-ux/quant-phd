"""Alternative 4 (Lagrange): chord by Lagrange basis weights; ties resolved as ceil(x - 1/2) on the negated value."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any

PPM = 1_000_000


def _ok_int(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def _half_down_ceiling(x: Fraction) -> int:
    """ceil(x - 1/2): a tie goes toward -infinity."""
    return math.ceil(x - Fraction(1, 2))


def _round_toward_plus_inf(x: Fraction) -> int:
    """Nearest integer with a tie toward +infinity, expressed through the tie-down rule on -x."""
    return -_half_down_ceiling(-x)


def _validate(strikes: list[int], calls: list[int], puts: list[int] | None, df_ppm: Any) -> None:
    if not _ok_int(df_ppm) or not 1 <= df_ppm <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if not all(_ok_int(k) and k > 0 for k in strikes) or any(strikes[i] >= strikes[i + 1] for i in range(len(strikes) - 1)):
        raise ValueError("strikes must be strictly increasing and positive")
    if len(calls) != len(strikes) or (puts is not None and len(puts) != len(strikes)):
        puts_n = len(strikes) if puts is None else len(puts)
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {puts_n} puts")


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _validate([strike_cents], [call_cents], None, df_ppm)
    return _round_toward_plus_inf(
        Fraction(call_cents) - Fraction(put_cents) - Fraction(spot_cents) + Fraction(strike_cents) * Fraction(df_ppm, PPM)
    )


def _lagrange_chord(strikes: list[int], calls: list[int], j: int) -> Fraction:
    """Value at K_j of the Lagrange interpolant through the two neighbours."""
    x0, x1, x2 = strikes[j - 1], strikes[j], strikes[j + 1]
    basis0 = Fraction(x1 - x2, x0 - x2)
    basis2 = Fraction(x1 - x0, x2 - x0)
    return calls[j - 1] * basis0 + calls[j + 1] * basis2


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: Any) -> list[int]:
    _validate(strikes_cents, calls_cents, None, df_ppm)
    return [j for j in range(1, len(strikes_cents) - 1) if _lagrange_chord(strikes_cents, calls_cents, j) < calls_cents[j]]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    _validate(strikes, calls, puts, chain["df_ppm"])
    fee, spread = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (fee + spread)
    rows: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        gap = Fraction(calls[k]) - Fraction(puts[k]) - (Fraction(chain["spot_cents"]) - Fraction(strike * chain["df_ppm"], PPM))
        gross = _round_toward_plus_inf(abs(gap))
        if gross - cost > 0:
            side = ("sell the call, buy the put and the underlying, and borrow the discounted strike" if gap > 0
                    else "buy the call, sell the put and the underlying, and lend the discounted strike")
            rows.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": gross - cost,
                         "explanation": f"P1, P2, P3, P4 and P6 (put-call parity): {side}; the net is {gross - cost} cents."})
    for j in convexity_violations(strikes, calls, chain["df_ppm"]):
        gross = _round_toward_plus_inf(Fraction(calls[j]) - _lagrange_chord(strikes, calls, j))
        if gross - cost > 0:
            rows.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": gross - cost,
                         "explanation": f"P1, P2, P5 and P6 (convexity in strike): net {gross - cost} cents."})
    return rows

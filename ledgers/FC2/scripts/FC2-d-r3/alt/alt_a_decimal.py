"""Alternative A (verifier round 3, independent): exact Decimal arithmetic at 60 digits, integer decisions for signs."""

from __future__ import annotations

import itertools
from decimal import ROUND_FLOOR, Decimal, getcontext
from typing import Any

getcontext().prec = 60
PPM = 1_000_000
LEGS = 3


def _df(df_ppm: Any) -> None:
    if isinstance(df_ppm, bool) or not isinstance(df_ppm, int) or not 1 <= df_ppm <= PPM:
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _strikes(strikes: list[Any]) -> None:
    for k in strikes:
        if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
            raise ValueError("strikes must be strictly increasing and positive")
    if any(b <= a for a, b in itertools.pairwise(strikes)):
        raise ValueError("strikes must be strictly increasing and positive")


def _lengths(strikes: list[Any], calls: list[Any], puts: list[Any] | None) -> None:
    n_puts = len(strikes) if puts is None else len(puts)
    if len(calls) != len(strikes) or n_puts != len(strikes):
        raise ValueError(
            f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, {n_puts} puts"
        )


def _round_half_up_signed(x: Decimal) -> int:
    return int((x + Decimal("0.5")).to_integral_value(rounding=ROUND_FLOOR))


def _gap(call: int, put: int, spot: int, strike: int, df: int) -> Decimal:
    forward = Decimal(spot) - Decimal(strike) * Decimal(df).scaleb(-6)
    return Decimal(call) - Decimal(put) - forward


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _df(df_ppm)
    _strikes([strike_cents])
    return _round_half_up_signed(_gap(call_cents, put_cents, spot_cents, strike_cents, df_ppm))


def _sd_sign_and_gross(strikes: list[int], calls: list[int], j: int) -> tuple[int, int]:
    low, mid, high = strikes[j - 1], strikes[j], strikes[j + 1]
    d = high - low
    numerator = calls[j - 1] * (high - mid) + calls[j + 1] * (mid - low) - calls[j] * d  # = d * second difference
    # the second difference is numerator / d; a convexity failure is a negative second difference
    gross_value = -Decimal(numerator) / Decimal(d)
    return numerator, _round_half_up_signed(gross_value)


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _df(df_ppm)
    _strikes(strikes_cents)
    _lengths(strikes_cents, calls_cents, None)
    out = []
    for j in range(1, len(strikes_cents) - 1):
        numerator, _ = _sd_sign_and_gross(strikes_cents, calls_cents, j)
        if numerator < 0:
            out.append(j)
    return out


def _explain(kind: str, gap_sign: int, net: int, fee: int, spread: int) -> str:
    if kind == "parity":
        if gap_sign > 0:
            body = "Parity: the call is rich against the synthetic forward, so sell the call and buy the put and the underlying"
        else:
            body = "Parity: the call is cheap against the synthetic forward, so buy the call and sell the put and the underlying"
        head = "P1, P2, P3, P4 and P6 apply"
    else:
        body = "Convexity in strike: the middle call sits above the chord of its neighbours, so sell the middle call"
        head = "P1, P2, P5 and P6 apply"
    return f"{body}; {head}; net {net} cents after {LEGS} legs at fee {fee} plus half-spread {spread}."


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    _df(chain["df_ppm"])
    _strikes(strikes)
    _lengths(strikes, calls, puts)
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    per = LEGS * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        g = _gap(calls[k], puts[k], chain["spot_cents"], strike, chain["df_ppm"])
        gross = _round_half_up_signed(abs(g))
        net = gross - per
        if net > 0:
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": net,
                        "explanation": _explain("parity", 1 if g > 0 else -1, net, fee, spread)})
    for j in range(1, len(strikes) - 1):
        numerator, gross = _sd_sign_and_gross(strikes, calls, j)
        if numerator < 0:
            net = gross - per
            if net > 0:
                out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": net,
                            "explanation": _explain("convexity", 0, net, fee, spread)})
    return out

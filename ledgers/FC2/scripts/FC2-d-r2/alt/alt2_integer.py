"""Alternative 2 (integers only): no Fraction or Decimal; parity scaled by 10^6, convexity by cross-multiplication."""

from __future__ import annotations

from typing import Any

PPM = 1_000_000


def _df_ok(df_ppm: Any) -> bool:
    return not (isinstance(df_ppm, bool) or not isinstance(df_ppm, int)) and 1 <= df_ppm <= PPM


def _validate(strikes: list[int], calls: list[int], puts: list[int] | None, df_ppm: int) -> None:
    if not _df_ok(df_ppm):
        raise ValueError("df_ppm must lie in 1 to 1000000")
    for k in strikes:
        if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
            raise ValueError("strikes must be strictly increasing and positive")
    for a, b in zip(strikes, strikes[1:], strict=False):
        if not a < b:
            raise ValueError("strikes must be strictly increasing and positive")
    if len(calls) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, "
                         f"{len(strikes) if puts is None else len(puts)} puts")
    if puts is not None and len(puts) != len(strikes):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, "
                         f"{len(puts)} puts")


def _round_scaled(numer: int, scale: int) -> int:
    """Nearest integer to numer / scale, a tie toward +infinity, for scale > 0 (floor of x + 1/2)."""
    return (2 * numer + scale) // (2 * scale)


def _half_up_magnitude(numer: int, scale: int) -> int:
    """Nearest integer to |numer| / scale, a tie away from zero (magnitude half up)."""
    return _round_scaled(abs(numer), scale)


def parity_gap_cents(call_cents: int, put_cents: int, spot_cents: int, strike_cents: int, df_ppm: int) -> int:
    _validate([strike_cents], [call_cents], None, df_ppm)
    # gap * 10^6 = (C - P - S) * 10^6 + K * df
    scaled = (call_cents - put_cents - spot_cents) * PPM + strike_cents * df_ppm
    return _round_scaled(scaled, PPM)


def _violation_numerator(strikes: list[int], calls: list[int], j: int) -> int:
    """Negative exactly when the call at j is above its chord; equals (chord - call) * (K[j+1] - K[j-1])."""
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    return (k2 - k1) * calls[j - 1] + (k1 - k0) * calls[j + 1] - (k2 - k0) * calls[j]


def convexity_violations(strikes_cents: list[int], calls_cents: list[int], df_ppm: int) -> list[int]:
    _validate(strikes_cents, calls_cents, None, df_ppm)
    return [j for j in range(1, len(strikes_cents) - 1) if _violation_numerator(strikes_cents, calls_cents, j) < 0]


def scan(chain: dict[str, Any]) -> list[dict[str, Any]]:
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    df_ppm = chain["df_ppm"]
    _validate(strikes, calls, puts, df_ppm)
    fee, spread = chain["cost"]["fee_cents_per_contract"], chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out: list[dict[str, Any]] = []
    for k, strike in enumerate(strikes):
        scaled = (calls[k] - puts[k] - chain["spot_cents"]) * PPM + strike * df_ppm
        gross = _half_up_magnitude(scaled, PPM)
        net = gross - cost
        if net > 0:
            sign_side = "sell the call and buy the put" if scaled > 0 else "buy the call and sell the put"
            out.append({"kind": "parity", "strike_cents": strike, "gross_cents": gross, "net_cents": net,
                        "explanation": f"parity by P1, P2, P3, P4 and P6: {sign_side}; net {net} cents."})
    for j in convexity_violations(strikes, calls, df_ppm):
        num = _violation_numerator(strikes, calls, j)
        den = strikes[j + 1] - strikes[j - 1]
        gross = _half_up_magnitude(-num, den)
        net = gross - cost
        if net > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross, "net_cents": net,
                        "explanation": f"convexity in strike by P1, P2, P5 and P6: net {net} cents."})
    return out

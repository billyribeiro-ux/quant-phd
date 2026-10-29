"""Alternative correct implementation 1: Fraction throughout, written independently of reference.py."""
import math
from fractions import Fraction

PPM = 1_000_000


def _round(x):
    return math.floor(x + Fraction(1, 2))


def _validate_df(df):
    if not (type(df) is int and 1 <= df <= PPM):
        raise ValueError("df_ppm must lie in 1 to 1000000")


def _validate_strikes(strikes):
    for k in strikes:
        if not (type(k) is int and k > 0):
            raise ValueError("strikes must be strictly increasing and positive")
    for a, b in zip(strikes, strikes[1:]):
        if not b > a:
            raise ValueError("strikes must be strictly increasing and positive")


def _validate_lengths(strikes, calls, puts=None):
    n = len(strikes)
    if len(calls) != n or (puts is not None and len(puts) != n):
        raise ValueError(f"calls and puts need one quote per strike: {n} strikes, {len(calls)} calls, "
                         f"{n if puts is None else len(puts)} puts")


def parity_gap_cents(call_cents, put_cents, spot_cents, strike_cents, df_ppm):
    _validate_df(df_ppm)
    if not (type(strike_cents) is int and strike_cents > 0):
        raise ValueError("strikes must be strictly increasing and positive")
    df = Fraction(df_ppm, PPM)
    return _round(Fraction(call_cents - put_cents) - (Fraction(spot_cents) - strike_cents * df))


def _chord_gap(strikes, calls, j):
    k0, k1, k2 = strikes[j - 1], strikes[j], strikes[j + 1]
    t = Fraction(k1 - k0, k2 - k0)
    chord = Fraction(calls[j - 1]) + t * (calls[j + 1] - calls[j - 1])
    return chord - calls[j]


def convexity_violations(strikes_cents, calls_cents, df_ppm):
    _validate_df(df_ppm)
    _validate_strikes(strikes_cents)
    _validate_lengths(strikes_cents, calls_cents)
    return [j for j in range(1, len(strikes_cents) - 1) if _chord_gap(strikes_cents, calls_cents, j) < 0]


def scan(chain):
    strikes = list(chain["strikes_cents"])
    calls = list(chain["call_cents"])
    puts = list(chain["put_cents"])
    _validate_df(chain["df_ppm"])
    _validate_strikes(strikes)
    _validate_lengths(strikes, calls, puts)
    fee = chain["cost"]["fee_cents_per_contract"]
    spread = chain["cost"]["half_spread_cents"]
    if fee < 0 or spread < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (fee + spread)
    out = []
    for k, K in enumerate(strikes):
        g = parity_gap_cents(calls[k], puts[k], chain["spot_cents"], K, chain["df_ppm"])
        exact = Fraction(calls[k] - puts[k]) - (Fraction(chain["spot_cents"]) - K * Fraction(chain["df_ppm"], PPM))
        gross = _round(abs(exact))
        if gross - cost > 0:
            side = "call rich" if exact > 0 else "call cheap"
            out.append({"kind": "parity", "strike_cents": K, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": f"parity (P1, P2, P3, P4, P6): {side}; cost {cost}."})
    for j in convexity_violations(strikes, calls, chain["df_ppm"]):
        gross = _round(-_chord_gap(strikes, calls, j))
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross,
                        "net_cents": gross - cost,
                        "explanation": f"convex in strike (P1, P2, P5, P6): cost {cost}."})
    return out

"""Alternative correct implementation 5: parity through the forward F = S/df, comparing (F - K) df with C - P."""
import math
from fractions import Fraction


def _round(x):
    return math.floor(x + Fraction(1, 2))


def _check(strikes, calls, puts, df_ppm):
    if not (type(df_ppm) is int and 1 <= df_ppm <= 1_000_000):
        raise ValueError("df_ppm must lie in 1 to 1000000")
    if any(type(k) is not int or k <= 0 for k in strikes) or any(b <= a for a, b in zip(strikes, strikes[1:])):
        raise ValueError("strikes must be strictly increasing and positive")
    if len(calls) != len(strikes) or (puts is not None and len(puts) != len(strikes)):
        raise ValueError(f"calls and puts need one quote per strike: {len(strikes)} strikes, {len(calls)} calls, "
                         f"{len(strikes) if puts is None else len(puts)} puts")


def parity_gap_cents(call_cents, put_cents, spot_cents, strike_cents, df_ppm):
    _check([strike_cents], [call_cents], [put_cents], df_ppm)
    df = Fraction(df_ppm, 1_000_000)
    forward = Fraction(spot_cents) / df
    return _round(Fraction(call_cents - put_cents) - (forward - strike_cents) * df)


def _chord_times_span(strikes, calls, j):
    k1, k2, k3 = strikes[j - 1], strikes[j], strikes[j + 1]
    return Fraction(calls[j - 1] * (k3 - k2) + calls[j + 1] * (k2 - k1), k3 - k1)


def convexity_violations(strikes_cents, calls_cents, df_ppm):
    _check(strikes_cents, calls_cents, None, df_ppm)
    return [j for j in range(1, len(strikes_cents) - 1) if _chord_times_span(strikes_cents, calls_cents, j) < calls_cents[j]]


def scan(chain):
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    _check(strikes, calls, puts, chain["df_ppm"])
    ct = chain["cost"]
    if ct["fee_cents_per_contract"] < 0 or ct["half_spread_cents"] < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (ct["fee_cents_per_contract"] + ct["half_spread_cents"])
    out = []
    for k, K in enumerate(strikes):
        df = Fraction(chain["df_ppm"], 1_000_000)
        exact = Fraction(calls[k] - puts[k]) - (Fraction(chain["spot_cents"]) / df - K) * df
        g = _round(abs(exact))
        if g - cost > 0:
            out.append({"kind": "parity", "strike_cents": K, "gross_cents": g, "net_cents": g - cost,
                        "explanation": f"parity rule (P1, P2, P3, P4, P6, cost {cost})."})
    for j in convexity_violations(strikes, calls, chain["df_ppm"]):
        gross = _round(Fraction(calls[j]) - _chord_times_span(strikes, calls, j))
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross,
                        "net_cents": gross - cost, "explanation": f"convexity in strike (P1, P2, P5, P6, cost {cost})."})
    return out

"""Alternative correct implementation 4: convexity by adjacent slopes on the strike grid (valid for unequal spacing)."""
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
    return _round(Fraction(call_cents - put_cents) - Fraction(spot_cents) + Fraction(strike_cents * df_ppm, 1_000_000))


def _slope_break(strikes, calls, j):
    s_left = Fraction(calls[j] - calls[j - 1], strikes[j] - strikes[j - 1])
    s_right = Fraction(calls[j + 1] - calls[j], strikes[j + 1] - strikes[j])
    return s_right - s_left


def convexity_violations(strikes_cents, calls_cents, df_ppm):
    _check(strikes_cents, calls_cents, None, df_ppm)
    return [j for j in range(1, len(strikes_cents) - 1) if _slope_break(strikes_cents, calls_cents, j) < 0]


def scan(chain):
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    _check(strikes, calls, puts, chain["df_ppm"])
    ct = chain["cost"]
    if ct["fee_cents_per_contract"] < 0 or ct["half_spread_cents"] < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (ct["fee_cents_per_contract"] + ct["half_spread_cents"])
    out = []
    for k, K in enumerate(strikes):
        exact = Fraction(calls[k] - puts[k]) - (Fraction(chain["spot_cents"]) - K * Fraction(chain["df_ppm"], 1_000_000))
        g = _round(abs(exact))
        if g - cost > 0:
            out.append({"kind": "parity", "strike_cents": K, "gross_cents": g, "net_cents": g - cost,
                        "explanation": f"parity rule (P1, P2, P3, P4, P6, cost {cost})."})
    for j in convexity_violations(strikes, calls, chain["df_ppm"]):
        k1, k2, k3 = strikes[j - 1], strikes[j], strikes[j + 1]
        chord = Fraction(calls[j - 1]) * Fraction(k3 - k2, k3 - k1) + Fraction(calls[j + 1]) * Fraction(k2 - k1, k3 - k1)
        gross = _round(Fraction(calls[j]) - chord)
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": k2, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": f"convexity in strike (P1, P2, P5, P6, cost {cost})."})
    return out

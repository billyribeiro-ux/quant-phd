"""Alternative correct implementation 2: integer-only arithmetic with an explicit half-up division helper."""


def _half_up_div(num, den):
    # nearest integer to num/den, tie toward plus infinity, den > 0
    return (2 * num + den) // (2 * den)


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
    num = (call_cents - put_cents - spot_cents) * 1_000_000 + strike_cents * df_ppm
    return _half_up_div(num, 1_000_000)


def _chord_num(strikes, calls, j):
    k1, k2, k3 = strikes[j - 1], strikes[j], strikes[j + 1]
    c1, c2, c3 = calls[j - 1], calls[j], calls[j + 1]
    den = k3 - k1
    return (k3 - k2) * c1 + (k2 - k1) * c3 - den * c2, den


def convexity_violations(strikes_cents, calls_cents, df_ppm):
    _check(strikes_cents, calls_cents, None, df_ppm)
    return [j for j in range(1, len(strikes_cents) - 1) if _chord_num(strikes_cents, calls_cents, j)[0] < 0]


def scan(chain):
    strikes, calls, puts = list(chain["strikes_cents"]), list(chain["call_cents"]), list(chain["put_cents"])
    ct = chain["cost"]
    _check(strikes, calls, puts, chain["df_ppm"])
    if ct["fee_cents_per_contract"] < 0 or ct["half_spread_cents"] < 0:
        raise ValueError("cost terms must be non-negative")
    cost = 3 * (ct["fee_cents_per_contract"] + ct["half_spread_cents"])
    out = []
    for k, K in enumerate(strikes):
        num = (calls[k] - puts[k] - chain["spot_cents"]) * 1_000_000 + K * chain["df_ppm"]
        gross = _half_up_div(abs(num), 1_000_000)
        if gross - cost > 0:
            out.append({"kind": "parity", "strike_cents": K, "gross_cents": gross, "net_cents": gross - cost,
                        "explanation": f"parity rule (P1, P2, P3, P4 supplied df, P6 cost {cost})."})
    for j in convexity_violations(strikes, calls, chain["df_ppm"]):
        num, den = _chord_num(strikes, calls, j)
        gross = _half_up_div(-num, den)
        if gross - cost > 0:
            out.append({"kind": "convexity", "strike_cents": strikes[j], "gross_cents": gross,
                        "net_cents": gross - cost, "explanation": f"convexity in strike (P1, P2, P5, P6 cost {cost})."})
    return out

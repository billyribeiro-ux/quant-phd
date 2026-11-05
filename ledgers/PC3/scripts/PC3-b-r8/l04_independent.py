"""Independent re-derivation of the PC3 L04 numbers (verifier round 8). Written from the page text, not from the twin.

Run as: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r8/l04_independent.py
Prints one line per check; every check prints its observed value so the ledger can quote it.
"""

from __future__ import annotations

import random
from fractions import Fraction

N = 20
V0 = 10000
STEP = 5
LIMIT = 10
H = 10  # half-spread of the Example 1.3 rule (cents)


def path_and_arrivals(seed: int) -> tuple[list[int], list[str]]:
    # Draw order as stated in the twin docstring: per turn, one draw for the move, one for the arrival.
    rng = random.Random(seed)
    v = [V0]
    arr: list[str] = []
    for _ in range(N):
        u = rng.random()
        v.append(v[-1] + (STEP if u < 0.5 else -STEP))
        w = rng.random()
        arr.append("UB" if w < 0.25 else ("US" if w < 0.5 else "I"))
    return v, arr


def play_rule(seed: int, p_unused: int = 0) -> dict[str, object]:
    v, arr = path_and_arrivals(seed)
    inv = 0
    cash = 0
    mid = V0
    fills = 0
    cash_flow = 0
    max_abs = 0
    mids: list[int] = []
    mid_ok = True
    for t in range(1, N + 1):
        # Claim (page L05-side, Example 1.3 and mid paragraph): mid at turn t equals 10000 - 10 I_{t-1}.
        mids.append(mid)
        if mid != V0 - 10 * inv:
            mid_ok = False
        a, b = mid + H, mid - H
        fair = v[t]
        a_arr = arr[t - 1]
        side = 0
        if a_arr == "UB":
            side = -1
        elif a_arr == "US":
            side = 1
        else:
            if fair > a:
                side = -1
            elif fair < b:
                side = 1
        if side != 0 and abs(inv + side) <= LIMIT:
            price = a if side < 0 else b
            cash += -side * price
            cash_flow += -side * price
            inv += side
            fills += 1
            mid = price
        max_abs = max(max_abs, abs(inv))
    settle = v[N]
    pnl = cash + inv * settle
    return {
        "fills": fills,
        "cash_flow": cash_flow,
        "inv_end": inv,
        "settle": settle,
        "pnl": pnl,
        "identity": pnl == cash_flow + inv * settle,
        "max_abs_inv": max_abs,
        "mid_eq_10000_minus_10I": mid_ok,
        "informed_count": sum(1 for x in arr if x == "I"),
    }


def main() -> None:
    s0 = play_rule(0)
    print("seed0 rule-play:", s0)
    s1 = play_rule(1)
    print("E1 seed1 fills, cash_flow, inv_end, settle, pnl:", s1["fills"], s1["cash_flow"], s1["inv_end"], s1["settle"], s1["pnl"])
    print("E2 seed0 informed arrivals among 20:", s0["informed_count"])
    se = (0.25 / 20) ** 0.5
    z = (13 / 20 - 0.5) / se
    print("E2 standard error, z:", round(se, 6), round(z, 6))
    bad = [s for s in range(200) if not play_rule(s)["identity"] or not play_rule(s)["mid_eq_10000_minus_10I"]]
    print("identity and mid=10000-10I over seeds 0..199: failing seeds =", bad)
    fills_range = sorted({play_rule(s)["fills"] for s in range(200)})
    print("fill counts seen over seeds 0..199 (min,max):", min(fills_range), max(fills_range))

    # Exact one-turn expectation, general p, from inventory zero, fixed quote (a,b) = (m-h, m+h).
    def e_trade(v: int, a: int, b: int, p: Fraction) -> Fraction:
        tot = Fraction(0)
        # uninformed buy (customer buys at ask): maker sells, sigma=-1, cash +a, fill (inv 0 -> -1 allowed)
        tot += (1 - p) / 2 * (a - v)
        # uninformed sell: sigma=+1, cash -b
        tot += (1 - p) / 2 * (v - b)
        # informed
        if v > a:
            tot += p * (a - v)
        elif v < b:
            tot += p * (v - b)
        return tot

    def closed(v: int, a: int, b: int, p: Fraction) -> Fraction:
        h = Fraction(a - b, 2)
        return (1 - p) * h - p * (max(v - a, 0) + max(b - v, 0))

    ok = True
    count = 0
    for a in range(9000, 11001, 7):
        for half in range(1, 40, 3):
            b = a - 2 * half
            for p in (Fraction(0), Fraction(1, 5), Fraction(1, 2), Fraction(3, 5), Fraction(1)):
                for v in range(a - 150, a + 150, 11):
                    count += 1
                    if e_trade(v, a, b, p) != closed(v, a, b, p):
                        ok = False
    print("Prop 3.1 closed form equals one-turn enumeration, general p, cases:", count, "all equal:", ok)

    # Remark 4.2 example and Example 3.2 numbers, exact.
    print("Example 3.2 at p=1/2, a=10010 b=9990: v=10000,10020,9985 ->",
          closed(10000, 10010, 9990, Fraction(1, 2)), closed(10020, 10010, 9990, Fraction(1, 2)),
          closed(9985, 10010, 9990, Fraction(1, 2)))
    # Remark 4.2: at I=10, v=10000, quote 9990/10010, p=1/2. Informed: inside quote, no trade.
    # Uninformed buy: maker sells at ask 10010, inventory 10->9, fill, contribution a - v = 10, prob 1/4.
    # Uninformed sell: refused (inventory would be 11). Informed: no trade.
    at10 = Fraction(1, 4) * (10010 - 10000)
    print("Remark 4.2 expected trade term at I=10, v=10000 (cents):", at10)

    # Corollary 3.3: p=1/2, v>=a: E=0 iff v=a+h, checked for h in 1..30.
    cor_ok = True
    for h in range(1, 31):
        a = 10000 + h
        b = a - 2 * h
        for v in range(a, a + 80):
            zero = closed(v, a, b, Fraction(1, 2)) == 0
            if zero != (v == a + h):
                cor_ok = False
    print("Corollary 3.3 zero iff v=a+h for h=1..30, v in [a,a+80):", cor_ok)

    # R1: d = (1-p)h/p at p=3/5, h=10.
    p = Fraction(3, 5)
    d = (1 - p) * 10 / p
    print("R1 d at p=3/5, h=10:", d, float(d))
    print("R1 check E(v=a+20/3):", e_trade_exact(Fraction(10010) + Fraction(20, 3), Fraction(10010), Fraction(9990), p))

    # R2: E at v=m is (1-p)h for every h, p in (0,1), inventory zero.
    m = 10000
    r2 = all(closed(m, m + h, m - h, Fraction(3, 5)) == Fraction(2, 5) * h for h in range(1, 40))
    print("R2 E at mid equals (1-p)h with p=3/5, h=1..39:", r2)

    # R3: 25 I^2 < 100 gives |I| <= 1 as the largest integer.
    print("R3 integers I with 25 I^2 < 100 in -10..10:", [i for i in range(-10, 11) if 25 * i * i < 100])

    # Exact DP check of Prop 3.1 with the conditioning event {I_{t-1}=0, v_t=v} on a fixed quote for all turns.
    dp_ok = dp_check()
    print("DP conditional check of Prop 3.1 (fixed quote all turns, t=1..20, all v_t values):", dp_ok)


def e_trade_exact(v: Fraction, a: Fraction, b: Fraction, p: Fraction) -> Fraction:
    tot = (1 - p) / 2 * (a - v) + (1 - p) / 2 * (v - b)
    if v > a:
        tot += p * (a - v)
    elif v < b:
        tot += p * (v - b)
    return tot


def dp_check() -> str:
    """Fixed quote (a,b)=(9990,10010), p=1/2, enumerate the full game: state (inventory, fair value) with probability.

    For each turn t and each fair value v_t, compute E[c_t + sigma_t v_t | I_{t-1}=0, v_t=v] exactly and compare with
    Proposition 3.1. The fixed quote is used at every turn; the inventory limit is enforced.
    """
    a, b = 10010, 9990
    p = Fraction(1, 2)
    h = Fraction(a - b, 2)
    # distribution over (inventory, fair value) after each turn; start: inventory 0, fair value 10000.
    dist: dict[tuple[int, int], Fraction] = {(0, V0): Fraction(1)}
    worst = Fraction(0)
    checked = 0
    for t in range(1, N + 1):
        # For each (I_{t-1}, v_{t-1}) state, the fair value v_t is v_{t-1} +- 5 with prob 1/2.
        # Condition on I_{t-1}=0 and v_t=v: sum over v_{t-1} of P(I_{t-1}=0, v_{t-1}) * 1/2 for v=v_{t-1}+-5.
        mass_inv0: dict[int, Fraction] = {}
        for (i, vprev), pr in dist.items():
            if i == 0:
                for step in (STEP, -STEP):
                    vt = vprev + step
                    mass_inv0[vt] = mass_inv0.get(vt, Fraction(0)) + pr / 2
        for vt, mass in mass_inv0.items():
            # arrival at t independent of the past and of v_t: outcomes keep probabilities
            tot = Fraction(0)
            for arr_p, kind in ((Fraction(1, 2) * (1 - p), "UB"), (Fraction(1, 2) * (1 - p), "US"), (p, "I")):
                if kind == "UB":
                    tot += arr_p * (a - vt)
                elif kind == "US":
                    tot += arr_p * (vt - b)
                else:
                    if vt > a:
                        tot += arr_p * (a - vt)
                    elif vt < b:
                        tot += arr_p * (vt - b)
            cf = (1 - p) * h - p * (max(vt - a, 0) + max(b - vt, 0))
            worst = max(worst, abs(tot - cf))
            checked += 1
        # advance the full distribution one turn (fixed quote)
        new: dict[tuple[int, int], Fraction] = {}
        for (i, vprev), pr in dist.items():
            for step in (STEP, -STEP):
                vt = vprev + step
                base = pr / 2
                # arrival outcomes
                outs = [
                    (Fraction(1, 2) * (1 - p), -1, "UB"),
                    (Fraction(1, 2) * (1 - p), 1, "US"),
                    (p, 0, "I"),
                ]
                for pa, _, kind in outs:
                    side = 0
                    if kind == "UB":
                        side = -1
                    elif kind == "US":
                        side = 1
                    else:
                        if vt > a:
                            side = -1
                        elif vt < b:
                            side = 1
                    ni = i
                    if side != 0 and abs(i + side) <= LIMIT:
                        ni = i + side
                    key = (ni, vt)
                    new[key] = new.get(key, Fraction(0)) + base * pa
        dist = new
    total = sum(dist.values())
    return f"cases checked={checked}, max |difference| = {worst}, total probability = {total}"


if __name__ == "__main__":
    main()

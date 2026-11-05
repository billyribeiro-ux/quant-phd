"""Independent re-derivation of the L04 numbers (PC3-b round 10). Standard library only.

Written from the rules stated in course/modules/PC/PC3/L04.html (Definition 1.1, A1-A6), not from the lab code.
Run as: python -I -W error ledgers/PC3/scripts/PC3-b-r10/l04_indep.py  (from the checkout root)
"""

from __future__ import annotations

import itertools
import random
from fractions import Fraction

P = Fraction(1, 2)  # informed probability (A1, lab/project)
LIMIT = 10
ARR = {"ub": (1 - P) / 2, "us": (1 - P) / 2, "inf": P}


def trade_term_outcomes(a: int, b: int, v: Fraction, inventory: int, size: int = 1):
    """Yield (probability, contribution c + sigma*v) for the three arrival outcomes, one turn, fixed quote."""
    out = []
    for name, prob in ARR.items():
        if name == "ub":
            side = -1  # customer buys: maker sells at ask
            price = a
        elif name == "us":
            side = 1  # customer sells: maker buys at bid
            price = b
        else:
            if v > a:
                side, price = -1, a
            elif v < b:
                side, price = 1, b
            else:
                side, price = 0, 0
        filled = side != 0 and size >= 1 and abs(inventory + side) <= LIMIT
        if not filled:
            out.append((prob, Fraction(0)))
            continue
        cash = -side * price
        out.append((prob, cash + side * v))
    return out


def expected_term(a: int, b: int, v: Fraction, inventory: int) -> Fraction:
    return sum((p * c for p, c in trade_term_outcomes(a, b, v, inventory)), Fraction(0))


def closed_form(a: int, b: int, v: Fraction) -> Fraction:
    h = Fraction(a - b, 2)
    return (1 - P) * h - P * (max(v - a, 0) + max(b - v, 0))


def main() -> None:
    # Prop 3.1: closed form equals enumeration on many fair values and quotes, from inventory 0.
    checks = 0
    bad = []
    for a, b in [(10010, 9990), (10020, 9980), (10005, 9995), (10100, 9900), (10002, 9998), (10000, 9998)]:
        for vnum in range(9950, 10051):  # cents, integer and half-cent steps
            for frac in (Fraction(0), Fraction(1, 2)):
                v = Fraction(vnum) + frac
                e = expected_term(a, b, v, 0)
                if e != closed_form(a, b, v):
                    bad.append((a, b, str(v)))
                checks += 1
    print(f"Prop 3.1 enumeration vs closed form, inventory 0: {checks} points, mismatches {len(bad)}")

    # Example 3.2 values
    for v in (10000, 10020, 9985):
        print(f"Example 3.2 v={v}: E = {expected_term(10010, 9990, Fraction(v), 0)}")

    # Corollary 3.3: with p = 1/2 and v >= a, E = h/2 - (v-a)/2; zero exactly at v = a + h.
    zeros = [v for v in range(10010, 10041) if expected_term(10010, 9990, Fraction(v), 0) == 0]
    print(f"Corollary 3.3 zeros for v in 10010..10040 with quote 9990/10010: {zeros}")

    # Remark 4.2: |I| <= 9 gives the same trade term as inventory 0; I = 10 gives 5/2 at v = 10000.
    same = all(
        expected_term(10010, 9990, Fraction(v), inv) == expected_term(10010, 9990, Fraction(v), 0)
        for inv in range(-9, 10)
        for v in range(9980, 10025, 5)
    )
    print(f"Remark 4.2 trade term equal to inventory-0 value for |I| <= 9 on grid: {same}")
    print(f"Remark 4.2 I=10, v=10000 expected trade term: {expected_term(10010, 9990, Fraction(10000), 10)}")
    print(f"Remark 4.2 I=-10, v=10000 expected trade term: {expected_term(10010, 9990, Fraction(10000), -10)}")

    # R1: d = (1-p) h / p at p = 3/5, h = 10
    p = Fraction(3, 5)
    d = (1 - p) * 10 / p
    print(f"R1 d = {d} = {float(d):.4f}")
    # R2: E at the mid is (1-p)h for any h; zero only if p = 1
    print("R2 at v = mid, E = (1-p)h, e.g. h=10, p=1/2:", expected_term(10010, 9990, Fraction(10000), 0))

    # E2 numbers
    se = (0.25 / 20) ** 0.5
    z = (13 / 20 - 0.5) / se
    print(f"E2 standard error = {se:.6f}, z = {z:.4f}")

    # Game: independent implementation on seed 0 and seed 1 with the draw order documented in the lab.
    def game(seed: int):
        rng = random.Random(seed)
        fair = 10000
        last_fill = None
        inv = 0
        cash = 0
        fills = 0
        informed = 0
        flows = 0
        path = [fair]
        log = []
        for t in range(1, 21):
            move = 5 if rng.random() < 0.5 else -5
            fair += move
            path.append(fair)
            draw = rng.random()
            arrival = "ub" if draw < 0.25 else ("us" if draw < 0.5 else "inf")
            if arrival == "inf":
                informed += 1
            mid = 10000 if last_fill is None else last_fill
            a, b = mid + 10, mid - 10
            if arrival == "ub":
                side = -1
            elif arrival == "us":
                side = 1
            elif fair > a:
                side = -1
            elif fair < b:
                side = 1
            else:
                side = 0
            filled = side != 0 and abs(inv + side) <= LIMIT
            if filled:
                price = a if side < 0 else b
                cash += -side * price
                flows += -side * price
                inv += side
                fills += 1
                last_fill = price
            log.append((t, mid, filled, inv, mid - 10 * inv))
            # mid before turn t+1 must equal 10000 - 10 * inventory (induction claim in L04 Section 5)
        settle = path[20]
        return dict(fills=fills, informed=informed, flows=flows, inv=inv, settle=settle,
                    pnl=cash + inv * settle, identity=(cash + inv * settle) == flows + inv * settle, log=log)

    g0 = game(0)
    g1 = game(1)
    print("seed0:", {k: v for k, v in g0.items() if k != "log"})
    print("seed1:", {k: v for k, v in g1.items() if k != "log"})
    # mid induction: at each turn, mid_t == 10000 - 10 * I_{t-1}
    ok = True
    for seed in range(0, 200):
        rng_game = game(seed)
        inv_prev = 0
        for t, mid, filled, inv, _ in rng_game["log"]:
            if mid != 10000 - 10 * inv_prev:
                ok = False
            inv_prev = inv
    print(f"Section 5 mid claim mid_t = 10000 - 10*I_(t-1) on seeds 0..199, all turns: {ok}")
    # Remark 2.4 / E3: seed 0 mid before turn 20 and settlement
    last = g0["log"][-1]
    print(f"seed0 turn-20 mid = {last[1]}, settlement = {g0['settle']}, inventory after 20 = {g0['inv']}")
    print(f"E3 P&L at settlement = {g0['flows'] + g0['inv'] * g0['settle']}, at mid = {g0['flows'] + g0['inv'] * last[1]}")


if __name__ == "__main__":
    main()

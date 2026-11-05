"""Independent recomputation of L04 numbers: seed-0 and seed-1 games (own code, stdlib only),
Proposition 3.1 for general p by brute enumeration over random quotes and fair values, Corollary 3.3,
Remark 4.2 (I = 10 case), Problems R1, P2, E2 arithmetic, Remark 2.4 and E3 values.
Usage: python -I l04_indep.py
"""
import random
from fractions import Fraction as F
import math
import statistics

def game(seed):
    rng = random.Random(seed)
    v = [10000]
    arr = []
    for _ in range(20):
        v.append(v[-1] + (5 if rng.random() < 0.5 else -5))
        u = rng.random()
        arr.append("ub" if u < 0.25 else ("us" if u < 0.5 else "inf"))
    inv, cash, last = 0, 0, None
    fills = []
    for t in range(1, 21):
        mid = 10000 if last is None else last
        bid, ask = mid - 10, mid + 10
        kind = arr[t - 1]
        fair = v[t]
        if kind == "ub":
            side = -1          # customer buys -> maker sells at ask
        elif kind == "us":
            side = +1          # customer sells -> maker buys at bid
        elif fair > ask:
            side = -1
        elif fair < bid:
            side = +1
        else:
            side = 0
        if side != 0 and abs(inv + side) <= 10:
            px = ask if side == -1 else bid
            cash += -side * px
            inv += side
            last = px
            fills.append(px)
    settle = v[20]
    return dict(fills=len(fills), cash=cash, inv=inv, settle=settle, pnl=cash + inv * settle,
                informed=sum(1 for a in arr if a == "inf"))

print("seed0", game(0))
print("seed1", game(1))

# Proposition 3.1 for general p: enumerate the three arrival outcomes exactly.
def trade_term(p, a, b, v):
    tot = F(0)
    for outcome, prob in (("ub", F(1, 2) * (1 - p)), ("us", F(1, 2) * (1 - p)), ("inf", p)):
        if outcome == "ub":
            c, s = a, -1
        elif outcome == "us":
            c, s = -b, +1
        else:
            if v > a:
                c, s = a, -1
            elif v < b:
                c, s = -b, +1
            else:
                tot += 0
                continue
        tot += prob * (c + s * v)
    return tot

def closed(p, a, b, v):
    h = F(a - b, 2)
    return (1 - p) * h - p * (max(v - a, 0) + max(b - v, 0))

import itertools
ok = True
count = 0
for p in (F(0), F(1, 5), F(1, 2), F(3, 5), F(1)):
    for h in range(1, 8):
        for mid in (9990, 10000, 10003):
            a, b = mid + h, mid - h
            for v in range(mid - 40, mid + 41, 1):
                count += 1
                if trade_term(p, a, b, v) != closed(p, a, b, v):
                    ok = False
print("Prop 3.1 closed form equals enumeration on", count, "cases:", ok)

# Corollary 3.3: p = 1/2, v >= a: E = h/2 - (v-a)/2 ; zero iff v = a + h
ok3 = all(closed(F(1, 2), mid + h, mid - h, mid + h + d) == F(h, 2) - F(d, 2)
          for h in range(1, 8) for mid in (10000,) for d in range(0, 30))
zero = [d for d in range(0, 30) if closed(F(1, 2), 10000 + 10 + 0, 10000 - 10, 10020 + d - 20 + 0) == 0]
print("Corollary 3.3 identity holds:", ok3)

# Remark 4.2: I = 10, quote 9990/10010, v = 10000, p = 1/2: uninformed buy only, 10 cents with prob 1/4
print("Remark 4.2 I=10 expected trade term =", F(1, 4) * 10, "(= 5/2)")
print("Remark 4.2 I=0 expected trade term =", closed(F(1, 2), 10010, 9990, 10000))

# Problem R1: d = (1-p) h / p at p = 3/5, h = 10 ; check closed form zero
p = F(3, 5); h = 10
d = (1 - p) * h / p
print("R1 d =", d, float(d), "check zero:", closed(p, 10010 + 0, 9990, 10010 + d) == 0 or None)
print("R1 check with a=10010 and v=a+d:", closed(p, 10010, 9990, 10010 + d))

# Problem E2: standard error and standardised distance
se = math.sqrt(0.5 * 0.5 / 20)
z = (13 / 20 - 0.5) / se
print("E2 se =", round(se, 4), "z =", round(z, 4), "z crit", round(statistics.NormalDist().inv_cdf(0.975), 6))

# Problem E3 and Remark 2.4 (seed 0 last quote 9980/10000, mid 9990, settlement 9980, inventory 1, cash -9950)
print("E3 marked at settlement", -9950 + 1 * 9980, "at mid", -9950 + 1 * 9990, "difference", 9990 - 9980)

# Example 3.2 values
for v in (10000, 10020, 9985):
    print("Example 3.2 v", v, closed(F(1, 2), 10010, 9990, v))

# P2 at v = a and v = a+h
for hh in (1, 5, 10):
    a, b = 10000 + hh, 10000 - hh
    print("P2 h", hh, "E(v=a)", closed(F(1, 2), a, b, a), "E(v=a+h)", closed(F(1, 2), a, b, a + hh))

# Proposition 4.1 mean/variance by enumeration
for I in (-4, 0, 1, 3, 10):
    vals = [I * 5, I * -5]
    mean = F(sum(vals), 2)
    var = F(sum((x - mean) ** 2 for x in vals), 2)
    print("Prop 4.1 I", I, "mean", mean, "var", var, "== 25 I^2:", var == 25 * I * I)

# Remark 4.2 std of 3 and 10 units
print("sd at 3 units", math.sqrt(25 * 9), "sd at 10", math.sqrt(25 * 100))

# R3: strict bound
print("R3 variances", [(i, 25 * i * i) for i in range(0, 4)])

# Lab grid: nine fair values 9980..10020 step 5 with the quote 9990/10010
print("grid values", list(range(9980, 10025, 5)), len(list(range(9980, 10025, 5))))
print("expected trade term on grid", [str(closed(F(1, 2), 10010, 9990, v)) for v in range(9980, 10025, 5)])

# Section 5 claim: mid at turn t equals 10000 - 10 I_{t-1} along the seed-0 path (recomputed in game())

# Section 5 claim: mid at turn t equals 10000 - 10 * I_{t-1} on seeds 0..49 (own game code above, re-run)
def mid_check(seed):
    rng = random.Random(seed)
    v = [10000]
    arr = []
    for _ in range(20):
        v.append(v[-1] + (5 if rng.random() < 0.5 else -5))
        u = rng.random()
        arr.append("ub" if u < 0.25 else ("us" if u < 0.5 else "inf"))
    inv, last = 0, None
    for t in range(1, 21):
        mid = 10000 if last is None else last
        if mid != 10000 - 10 * inv:
            return False
        bid, ask = mid - 10, mid + 10
        kind = arr[t - 1]
        fair = v[t]
        if kind == "ub":
            side = -1
        elif kind == "us":
            side = +1
        elif fair > ask:
            side = -1
        elif fair < bid:
            side = +1
        else:
            side = 0
        if side != 0 and abs(inv + side) <= 10:
            px = ask if side == -1 else bid
            inv += side
            last = px
    return True

print("Section 5 mid identity holds on seeds 0..49:", all(mid_check(s) for s in range(50)))

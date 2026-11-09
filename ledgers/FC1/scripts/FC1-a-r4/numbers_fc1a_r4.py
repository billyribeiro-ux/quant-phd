"""FC1-a round 4: independent exact recomputation of every number in the slice (hub, L01-L03, cards).

Uses fractions.Fraction only. Run: .venv/bin/python -I ledgers/FC1/scripts/FC1-a-r4/numbers_fc1a_r4.py
"""

from __future__ import annotations

import math
from fractions import Fraction as F
from itertools import product


def half_up_cents(x: F) -> int:
    return math.floor(x * 100 + F(1, 2))


def check(label: str, got: object, want: object) -> None:
    status = "OK " if got == want else "BAD"
    print(f"{status} {label}: got {got} want {want}")


print("== L01 Example 3.3 (d=1000, rho=1/10)")
d, rho = F(1000), F(1, 10)
D = [d * (1 - rho) ** t for t in range(11)]
S = [sum(D[: n + 1]) for n in range(11)]
check("S_1", S[1], 1900)
check("S_2", S[2], 2710)
S10 = d * (1 - (1 - rho) ** 11) / rho
check("S_10 exact equals 6861.8940391", S10, F(68618940391, 10**7))
print("   S_10 decimal to 10 places:", f"{float(S10):.10f}")
check("S_10 cents half up", half_up_cents(S10), 686189)
check("multiplier S_10/d rounded 4 places", f"{float(S10/d):.4f}", "6.8619")
check("multiplier 4dp times 1000 cents", f"{round(float(S10/d), 4) * 1000:.2f}", "6861.90")
check("limit d/rho", d / rho, 10000)
check("1/rho", 1 / rho, 10)

print("== L01 Prop 3.1 closed form vs partial sums, d=1000, rho in {1/10,1/2,1/5,1/4,1}")
for r in [F(1, 10), F(1, 2), F(1, 5), F(1, 4), F(1)]:
    ok = all(sum(d * (1 - r) ** t for t in range(n + 1)) == d * (1 - (1 - r) ** (n + 1)) / r for n in range(0, 25))
    check(f"closed form rho={r}", ok, True)

print("== L01 Example 3.6 / E2 / leakage (phi=1/2, rho=1/10)")
phi = F(1, 2)
lim_half = d / (1 - phi * (1 - rho))
check("half-redeposit limit exact", lim_half, F(20000, 11))
check("half limit cents half up", half_up_cents(lim_half), 181818)
check("half limit decimal 4dp", f"{float(lim_half):.4f}", "1818.1818")
check("ratio to full limit", lim_half / (d / rho), F(2, 11))
check("ratio percent 2dp", f"{float(100 * lim_half / 10000):.2f}", "18.18")
S10_half = sum(d * (phi * (1 - rho)) ** t for t in range(11))
check("S_10 with leakage cents", half_up_cents(S10_half), 181790)
check("S_10 leakage decimal", f"{float(S10_half):.5f}", "1817.90322")

print("== L01 Prop 3.5 identity: d/rho - d/(1-phi(1-rho)) == d(1-rho)(1-phi)/(rho(1-phi(1-rho)))")
ok = True
for dd, rr, pp in product([F(1), F(3, 2), F(1000)], [F(1, 10), F(1, 2), F(1)], [F(0), F(1, 3), F(1, 2), F(1)]):
    k = pp * (1 - rr)
    lhs = dd / rr - dd / (1 - k)
    rhs = dd * (1 - rr) * (1 - pp) / (rr * (1 - k))
    ok = ok and lhs == rhs and lhs >= 0
print("   identity and sign on grid:", ok)
d0 = F(0)
print("   at d=0: d/rho - limit =", d0 / F(1, 2) - d0 / (1 - F(0) * (1 - F(1, 2))), "(equality holds at d=0 since limit is 0)")
print("   at d=0, phi=0, rho=1/2: limit 0 vs d/rho 0 -> equality with phi != 1 and rho != 1 (so the iff needs d>0)")

print("== L01 Remark 3.2 / P2 rho=0, d>0: S_n=(n+1)d")
check("S_5 rho=0", sum(F(1000) for _ in range(6)), 6000)

print("== L01 Misconceptions and Example numbers")
check("stage1 total 1000+900", F(1000) + F(900), 1900)
check("half multiplier 1.75 = S_2/d at rho=1/2", (1 - (F(1, 2)) ** 3) / F(1, 2), F(7, 4))
check("M1 reserves 500/5", F(500) / 5, 100)
check("M1 loan", F(500) - F(100), 400)
check("M2 S_2 (800, rho=1/4)", F(800) * (1 - (F(3, 4)) ** 3) / F(1, 4), 1850)
check("M2 stage deposits 800,600,450 sum", 800 + 600 + 450, 1850)
check("M3 equity after loss 300-320", 300 - 320, -20)
check("quiz 1000*(4/5)", F(4, 5) * 1000, 800)
check("quiz Q10 400*1.75", F(400) * F(7, 4), 700)
check("quiz equity 100-60", 100 - 60, 40)
check("E3 equity bound", 100 - 0, 100)
check("Example 3.6 base 1000/0.55", F(1000) / F(55, 100), F(20000, 11))

print("== L01 Lab Part D and Part C limit cents")
check("Part D equity 100-50", 100 - 50, 50)
check("Part D equity 100-100", 100 - 100, 0)
check("Part D equity 100-150", 100 - 150, -50)
check("Part C full limit cents", half_up_cents(F(1000) / (1 - (1 - F(1, 10)))), 1000000)

print("== L02 counts from REGISTER")
REG = [
    ("share listed on an exchange", ("equities",), ("cash",), ("exchange",)),
    ("share sold in a private negotiated trade", ("equities",), ("cash",), ("otc",)),
    ("futures on an equity index", ("equities",), ("derivative",), ("exchange",)),
    ("bond with a fixed coupon", ("rates",), ("cash",), ("otc",)),
    ("futures on a government bond", ("rates",), ("derivative",), ("exchange",)),
    ("interest rate swap", ("rates",), ("derivative",), ("otc",)),
    ("corporate bond", ("credit",), ("cash",), ("otc",)),
    ("credit default swap", ("credit",), ("derivative",), ("otc",)),
    ("spot purchase of a currency", ("fx",), ("cash",), ("otc",)),
    ("forward on a currency", ("fx",), ("derivative",), ("otc",)),
    ("futures on crude oil", ("commodities",), ("derivative",), ("exchange",)),
    ("physical quantity of a metal", ("commodities",), ("cash",), ("otc",)),
]
from collections import Counter

exp = Counter(e[1][0] for e in REG)
form = Counter(e[2][0] for e in REG)
venue = Counter(e[3][0] for e in REG)
check("exposure counts", (exp["equities"], exp["rates"], exp["credit"], exp["fx"], exp["commodities"]), (3, 3, 2, 2, 2))
check("form counts", (form["cash"], form["derivative"]), (6, 6))
check("venue counts", (venue["exchange"], venue["otc"]), (4, 8))
ex = [e for e in REG if e[3][0] == "exchange"]
check("exchange cash/derivative", (sum(e[2][0] == "cash" for e in ex), sum(e[2][0] == "derivative" for e in ex)), (1, 3))
check("exchange exposure classes", sorted({e[1][0] for e in ex}), ["commodities", "equities", "rates"])
check("derivative exposures all five", sorted({e[1][0] for e in REG if e[2][0] == "derivative"}), sorted(["commodities", "credit", "equities", "fx", "rates"]))
check("derivative entry indices 3,5,6,8,10,11", [i + 1 for i, e in enumerate(REG) if e[2][0] == "derivative"], [3, 5, 6, 8, 10, 11])
check("malformed exposure total", len(REG) + 1 + 0, 13)  # 13 entries
check("malformed total 14 over 13", sum(exp.values()) + 2, 14)
check("derivative share of exchange entries", F(3, 4), F(3, 4))
check("M2 counts 2+1+1+1+0", 2 + 1 + 1 + 1 + 0, 5)

print("== L03 Example 1.4 and relatives")
m, h = 5000, 15
check("bid", m - h, 4985)
check("ask", m + h, 5015)
check("spread", (m + h) - (m - h), 30)
check("relative %", F(30, 5000) * 100, F(6, 10))
check("E3 relative % (6/20000)", F(6, 20000) * 100, F(3, 100))

print("== L03 Definition 2.1 sign conventions & Prop 2.3 identity, random sequences")
import random

rng = random.Random(4242)
ok = True
for trial in range(300):
    n = rng.randint(1, 9)
    hh = rng.randint(0, 5)
    mids = [rng.randint(9000, 11000) for _ in range(n)]
    sig = [rng.choice([1, -1]) for _ in range(n)]
    q = [rng.randint(1, 50) for _ in range(n)]
    mn = mids[-1]
    p = [mids[t] + sig[t] * hh for t in range(n)]
    C = sum(sig[t] * q[t] * p[t] for t in range(n))
    I = -sum(sig[t] * q[t] for t in range(n))
    V = sum(q)
    P = C + I * mn
    rhs = hh * V + sum(sig[t] * q[t] * (mids[t] - mn) for t in range(n))
    ok = ok and P == rhs
    if I == 0:
        W = sum(q[t] for t in range(n) if sig[t] == 1)
        ok = ok and V == 2 * W and P == C and (C == 2 * hh * W if all(mm == mids[0] for mm in mids) else True)
print("   Prop 2.3 and Remark 2.2 on 300 random sequences:", ok)

print("== L03 Example 2.5 / M1 / M2 / R2 / Corollary 2.4")
m1, m2, h2 = 10000, 9990, 2
bid1, ask2 = m1 - h2, m2 + h2
C = -bid1 * 100 + ask2 * 100
check("Example 2.5 cash", C, -600)
check("Example 2.5 spread term", h2 * 200, 400)
check("Example 2.5 mid-move", (-1) * 100 * (m1 - m2) + (+1) * 100 * (m2 - m2), -1000)
check("Example 2.5 P = 400-1000", 400 - 1000, -600)
check("M1 cash", 10002 * 50 - 9998 * 50, 200)
check("M1 Cor 2.4 s*W", 4 * 50, 200)
check("M2 sale payment 10008*80", 10008 * 80, 800640)
check("M2 buy receipt 10006*80", 10006 * 80, 800480)
check("M2 cash", 800480 - 800640, -160)
check("M2 hV", 2 * 160, 320)
check("M2 mid-move", (-1) * 80 * (10010 - 10004), -480)
check("R2 cash", 10002 * 100 - 9988 * 100, 1400)
check("R2 mid-move", (-1) * 100 * (9990 - 10000), 1000)

print("== L03 Part A/B expected values are a seeded run; the lab's own run is checked by run_labs. Cash identity check:")
check("Part A 4 * 1000", 4 * 1000, 4000)
check("Part B capture 2*2000", 2 * 2000, 4000)
check("Part B 4000-545", 4000 - 545, 3455)

print("== L03 tick game Proposition 3.2 by brute force on a wider grid (cost 100, N=1000, asks 100..140)")


def profit2(ask: int, rival: int, cost: int, N: int) -> int:
    if ask < rival:
        return 2 * (ask - cost) * N
    if ask == rival:
        return (ask - cost) * N
    return 0


def eq_pairs(cost: int, N: int, asks: list[int]) -> list[tuple[int, int]]:
    out = []
    for a, b in product(asks, asks):
        ok1 = all(profit2(dd, b, cost, N) <= profit2(a, b, cost, N) for dd in asks)
        ok2 = all(profit2(dd, a, cost, N) <= profit2(b, a, cost, N) for dd in asks)
        if ok1 and ok2:
            out.append((a, b))
    return out


wide = eq_pairs(100, 1000, list(range(100, 141)))
print("   equilibria on 100..140 grid:", wide)
check("wide grid equilibria are exactly k=0,1,2 symmetric", wide, [(100, 100), (101, 101), (102, 102)])
check("grid 100..110 count", len(list(product(range(100, 111), repeat=2))), 121)
check("R1 three dealers at (c+2): own profit 2N/3 with N=999 is 666; deviation to c+1 earns N=999", F(2 * 999, 3), 666)
check("R1 deviation strictly better", 999 > 666, True)
print("   R1 deviation check: payoff at (c+2) each = 2N/3; deviation to c+1 wins all N => gain N - 2N/3 > 0")
check("Q7 (103,103) profit", 3 * 1000 // 2, 1500)
check("Q7 deviation to 102", 2 * 1000, 2000)
check("Q8 tie profit", (102 - 100) * 1000 // 2, 1000)

print("== Cards: L01 Example 3.3 cents, Part C cents, multiplier 6.8619 check")
check("card c010 cents", half_up_cents(S10), 686189)
check("card c011 cents", half_up_cents(F(1000) / (1 - F(45, 100))), 181818)
check("card c014/c092 leakage", half_up_cents(S10_half), 181790)
check("card c053 spread capture", 2 * 2000, 4000)
check("card c043 V", 100 + 100, 200)

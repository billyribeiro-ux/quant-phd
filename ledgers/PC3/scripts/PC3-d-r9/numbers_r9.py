"""Round-9 independent re-derivation of the numbers quoted in PC3 cards and lessons L01-L06 (slice d).

Exact fractions wherever the quantity is rational; math/float only where the lesson prints a log or a root.
Run with: .venv/bin/python -I ledgers/PC3/scripts/PC3-d-r9/numbers_r9.py
"""

import math
from fractions import Fraction as F
from itertools import product

rows: list[str] = []


def out(label: str, value: object) -> None:
    rows.append(f"{label}: {value}")


# ---- L01 ----
out("L01 product bounds", (20 * 2 * 300, 60 * 10 * 390))
out("L01 ratio", F(234000, 12000))
out("L01 ln 19.5 (10 dp)", f"{math.log(19.5):.10f}")
out("L01 factor widths", [f"{math.log(x):.10f}" for x in (3, 5, 1.3)])
out("L01 sum of factor widths (10 dp)", f"{math.log(3) + math.log(5) + math.log(1.3):.10f}")
out("L01 geometric midpoint sqrt(12000*234000) (4 dp)", f"{math.sqrt(12000 * 234000):.4f}")
base = math.log(19.5)
red_sym = math.log(3) - math.log(2)
red_q = math.log(5) - math.log(2)
red_m = math.log(1.3) - math.log(12 / 11)
out("L01 reductions sym/quote/min (10 dp)", f"{red_sym:.10f} {red_q:.10f} {red_m:.10f}")
out("L01 share quote % (to 1 dp)", f"{100 * red_q / base:.4f}")
out("L01 share minutes % (to 1 dp)", f"{100 * red_m / base:.4f}")
out("L01 totals after narrowing", f"{base - red_sym:.4f} {base - red_q:.4f} {base - red_m:.4f}")
out("L01 E1 ratio rem/bound (n=10,x=.01)", f"{0.0046221254 / 0.0048728552:.6f}")
x = F(1, 100)
rem = (1 + x) ** 10 - 1 - 10 * x
bnd = F(45) * (1 + x) ** 8 * x * x
out("L01 rem exact (10 dp float)", f"{float(rem):.10f}")
out("L01 bound exact (10 dp float)", f"{float(bnd):.10f}")
out("L01 1.01^10 (12 dp)", f"{float((1 + x) ** 10):.12f}")
out("L01 bound over rem - 1 (%)", f"{100 * (float(bnd) / float(rem) - 1):.3f}")
x20 = F(1, 20)
out("L01 1.05^10 (4 dp)", f"{float((1 + x20) ** 10):.6f}")
out("L01 miss share of exact (%)", f"{100 * float(((1 + x20) ** 10 - F(3, 2)) / (1 + x20) ** 10):.4f}")
out("L01 bound n=10 x=1/20 (4 dp)", f"{float(F(45) * (1 + x20) ** 8 * x20 * x20):.4f}")
out("L01 sqrt(2808000000) (4 dp)", f"{math.sqrt(2808000000):.4f}")
# Problem M1 / M2 / M3 and E3 / R1 of L01
out("L01 M1 ln 4.2 check", f"{math.log(21 / 5):.10f} vs {math.log(1.5) + math.log(1.4) + math.log(2):.10f}")
out("L01 E3 ln16.5 (4 dp)", f"{math.log(16.5):.4f} change {math.log(19.5) - math.log(16.5):.6f}")
out("L01 R1 half of total / ln5", f"{base / 2:.4f} {math.log(5):.4f}")

# ---- L02 ----
out("L02 M1 P(sum 7 | first 3)", F(1, 36) / F(6, 36))
out("L02 M2 P(B), P(A|B)", (F(3, 10) * F(1, 2) + F(7, 10) * F(1, 5), F(3, 10) * F(1, 2) / (F(3, 10) * F(1, 2) + F(7, 10) * F(1, 5))))
out("L02 M3 (4/6)(3/5)", F(4, 6) * F(3, 5))
out("L02 E1 57/64 by complement", 1 - F(1, 64) - F(6, 64))
out("L02 E3 2/3-1/2", F(2, 3) - F(1, 2))
out("L02 Monty rule A stay/switch", (F(1, 3), F(2, 3)))

# Monty Hall by independent enumeration of (car, pick, host) for rule B conditioned on goat reveal
w_stay = F(0)
w_sw = F(0)
w_tot = F(0)
for car, pick in product(range(3), range(3)):
    for opened in range(3):
        if opened == pick or opened == car:
            continue
        w = F(1, 9) * F(1, 2)
        w_tot += w
        other = [d for d in range(3) if d not in (pick, opened)][0]
        if pick == car:
            w_stay += w
        if other == car:
            w_sw += w
out("L02 Monty rule B (stay, switch | goat)", (w_stay / w_tot, w_sw / w_tot))

# ---- L03 ----
out("L03 E[face]*100", 100 * F(21, 6))
out("L03 reroll continuation", 100 * F(7, 2) - 100)
vals = [max(100 * f, 250) for f in range(1, 7)]
out("L03 backward induction value", F(sum(vals), 6))
out("L03 choice value", F(sum(vals), 6) - 350)
out("L03 Ex3.6 check 2300/6", F(2300, 6))


def stop_value(outcomes, rule, horizon=6):
    def rec(h):
        if len(h) == horizon or rule(h):
            return F(sum(h))
        return sum((p * rec(h + (x,)) for x, p in outcomes), F(0))

    return rec(())


biased = ((150, F(1, 2)), (-100, F(1, 2)))
rules = [
    ("all", lambda h: False),
    ("first win", lambda h: bool(h) and h[-1] > 0),
    ("first loss", lambda h: bool(h) and h[-1] < 0),
    ("reach 100", lambda h: sum(h) >= 100),
    ("200 either way", lambda h: sum(h) >= 200 or sum(h) <= -200),
]
for name, r in rules:
    out(f"L03 biased {name}", stop_value(biased, r))
fair = ((100, F(1, 2)), (-100, F(1, 2)))
out("L03 fair all rules zero", all(stop_value(fair, r) == 0 for _, r in rules))
out("L03 R1 two-turn look-ahead mean", F(200 + 100 + 0 - 100, 4))
out("L03 R2 gain at fee 1", F(sum(max(100 * f, 350 - 1) for f in range(1, 7)), 6) - 350)
out("L03 E2 625/8-150", F(625, 8) - 150)

# ---- L04 ----
p = F(1, 2)
h = 10
a, b = 10010, 9990


def trade_term(v):
    return (1 - p) * h - p * (max(v - a, 0) + max(b - v, 0))


out("L04 closed form at 10000, 10020, 9985", [trade_term(v) for v in (10000, 10020, 9985)])
out("L04 grid 9980..10020 step 5", [trade_term(v) for v in range(9980, 10025, 5)])
out("L04 Remark 4.2 at I=10, uninformed buy only (1/4 * 10)", F(1, 4) * 10)
out("L04 R1 d=(1-p)h/p at p=3/5,h=10", F(2, 5) * 10 / F(3, 5))
out("L04 E2 sd of 13/20 (4 dp)", f"{math.sqrt(0.25 / 20):.4f} z={(0.65 - 0.5) / math.sqrt(0.25 / 20):.4f}")
out("L04 E3 mid PnL", (-9950 + 9990, -9950 + 9980))
out("L04 E1 seed1 PnL", 20100 + (-2) * 10020)
out("L04 R3 25 I^2 < 100 threshold", [i for i in range(0, 5) if 25 * i * i < 100])

# ---- L05 ----
n, k = 200, 8
out("L05 naive count n=200 k=8", (n - k + 1) * (k - 1))
out("L05 naive count n=200 k=32", (n - 32 + 1) * (32 - 1))
out("L05 naive count n=200 k=101", (n - 101 + 1) * (101 - 1))
out("L05 E1 ratio 5239/382 (1 dp)", f"{5239 / 382:.4f}")
out("L05 heap bound n=200", 3 * 200 * math.floor(math.log2(200)))
out("L05 floor log2 200", math.floor(math.log2(200)))
out("L05 M1 n=10 k=4", (10 - 4 + 1) * (4 - 1))

# ---- L06 ----
def annuity(r):
    return sum((1 + r) ** -t for t in range(1, 4))


I = 15_000_000
m = 5_000
A10 = annuity(F(1, 10))
out("L06 A at 10%", A10)
out("L06 break-even 10% exact", I / (m * A10))
out("L06 break-even float 8/10/12", [f"{I / (m * float(annuity(F(r, 100)))):.4f}" for r in (8, 10, 12)])
out("L06 diffs unrounded 8->10, 10->12", (
    f"{I / (m * float(annuity(F(10, 100)))) - I / (m * float(annuity(F(8, 100)))):.4f}",
    f"{I / (m * float(annuity(F(12, 100)))) - I / (m * float(annuity(F(10, 100)))):.4f}",
))
out("L06 avg per point", f"{(I / (m * float(annuity(F(12, 100)))) - I / (m * float(annuity(F(8, 100))))) / 4:.4f}")
for r in (F(8, 100), F(10, 100), F(12, 100)):
    A = annuity(r)
    lo = -I + m * A * 200
    hi = -I + m * A * 1600
    out(f"L06 NPV at rate {r} lower/upper (float 2dp)", f"{float(lo):.2f} {float(hi):.2f}")
out("L06 NPV(200) exact", -I + m * A10 * 200)
out("L06 NPV(1600) exact float", float(-I + m * A10 * 1600))
out("L06 NPV(1200) exact", -I + m * A10 * 1200)
out("L06 NPV(1300) exact", -I + m * A10 * 1300)
out("L06 M2 NPV", -100 + F(60, 11) + F(60, 121) * 1)
out("L06 M3 break-even 100000/(400*A)", F(100000) / (400 * A10))
out("L06 R3 margin m* and fall %", (F(I) / (1600 * A10), 100 * (1 - float(F(I) / (1600 * A10)) / 5000)))
out("L06 P3 bounds", (2000 * 1 * F(1, 10), 4000 * 2 * F(1, 5)))
out("L06 E1 12% annuity float", f"{sum(1 / (1.12 ** t) for t in (1, 2, 3)):.5f}")
out("L06 Example 4.2 A exact", A10 == F(3310, 1331))
out("L06 Lab forward 9700/0.97", F(9700) / F(97, 100))
out("L06 M1 4900/0.98", F(4900) / F(98, 100))

print("\n".join(rows))

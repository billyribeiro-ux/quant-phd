"""Independent re-derivation of the numbers on LX1 slice-b pages (L01, L03, L04), round 18.

Run from the checkout root: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r18/rederive_numbers_r18.py
Exact Fractions for the model numbers; Decimal at 60 digits for ln and exp; the L04 log changes use
float(exact ratio) then math.log, the rule that the lab states. Each printed line names the page locator it checks.
"""

import csv
import math
import random
from decimal import ROUND_HALF_UP, Decimal, getcontext
from fractions import Fraction as F

getcontext().prec = 60


def rhu(x: F) -> int:
    return math.floor(x + F(1, 2))


def dec(x: F, places: int) -> str:
    q = Decimal(1).scaleb(-places)
    return str((Decimal(x.numerator) / Decimal(x.denominator)).quantize(q, rounding=ROUND_HALF_UP))


def fdec(x: float, places: int) -> str:
    return str(Decimal(x).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


def dq(x: Decimal, places: int) -> str:
    return str(x.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


print("== L01 (L01.html Lab 1, Proposition 2.2 witness, Problems, Quiz)")
r, g = F(9, 100), F(3, 100)
d1 = F(400)
F0 = d1 / (r - g)
q = (1 + g) / (1 + r)
print("F0 =", F0, "=", dec(F0, 6), "rounded", rhu(F0), "(lab Part A 6667)")
print("q =", q, "=", dec(q, 6), "(quiz 0.944954)")
for N in (10, 60, 200):
    S = sum(d1 * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1))
    print(f"N={N}: sum rounded {rhu(S)}; identity exact {S == F0 * (1 - q**N)}; F0 q^N rounded {rhu(F0 * q**N)}")
F2 = d1 * (1 + g) ** 2 / (r - g)
print("F2 =", dec(F2, 6), "rounded", rhu(F2), "(quiz 7072.67; lab t=2 7073)")
print("g* for benchmark = 6000:", dec(r - F(400, 6000), 6), "(Research 1 0.023333; quiz 0.023333)")
print("F(1%) =", 400 / (F(9, 100) - F(1, 100)), "; F(3%) =", 400 / (F(9, 100) - F(3, 100)),
      "; gap+ =", 6000 - F(400) / (F(9, 100) - F(1, 100)), "; gap- =", dec(6000 - F(400) / (F(9, 100) - F(3, 100)), 4))
print("Sec5 PV 400/1.09 =", dec(F(400) / F(109, 100), 4), "rounded", rhu(F(400) / F(109, 100)), "; 40000/109 =",
      F(40000, 109))
print("Mech1 F0=250/0.06 =", F(250) / F(6, 100), "=", dec(F(250) / F(6, 100), 4), "rounded",
      rhu(F(250) / F(6, 100)), "(page 4167)")
print("Mech2 1.04^3 =", F(104, 100) ** 3, "; 250*1.04^3 =", F(250) * F(104, 100) ** 3,
      "; F3 =", dec(F(250) * F(104, 100) ** 3 / F(6, 100), 4), "rounded", rhu(F(250) * F(104, 100) ** 3 / F(6, 100)),
      "(page 4687)")
S10 = sum(F(100) / F(105, 100) for _ in range(10))
print("Mech3 S10 =", S10, "=", dec(S10, 2), "; 20000/21 =", F(20000, 21), "; 1000/1.05 =", F(1000) / F(105, 100))
F9 = d1 * (1 + g) ** 9 / (r - g)
print("Emp3 F_9 exact =", dec(F9, 6), "rounded", rhu(F9), "; 0.25*F9 =", dec(F(1, 4) * F9, 6),
      "; 2175/8698 =", dec(F(2175, 8698) * 100, 6) + "%")
print("Emp1 9/13 =", dec(F(9, 13), 6), "; Emp2 13-9 =", 13 - 9)
print("Sec5/misc: 1-q at N=200 residual ok")

print("\n-- L01 lab Parts A-C re-run in exact arithmetic (rounding half up)")
SEED = 20261103
rng = random.Random(SEED)
gaps = []
for t in range(13):
    fund = F(400) * (1 + g) ** t / (r - g)
    w = F(rng.randint(-8, 25), 100)
    price = rhu(fund * (1 + w))
    gaps.append(price - rhu(fund))
    print(f"  t={t:2d} wedge {float(w):+.2f} fund {rhu(fund)} price {price} gap {gaps[-1]}")
print("  periods above:", sum(1 for x in gaps if x > 0), "of 13; largest gap", max(gaps), "at t =", gaps.index(max(gaps)))
rng = random.Random(SEED)
alt = 0
for t in range(13):
    w = F(rng.randint(-8, 25), 100)
    price = rhu(F(400) * (1 + g) ** t / (r - g) * (1 + w))
    altf = rhu(F(400) * (1 + F(1, 100)) ** t / (r - F(1, 100)))
    alt += (price - altf) > 0
print("  alternative (1%) periods above:", alt, "of 13 (page 13 of 13)")

print("\n== L03 (L03.html Lab 1, Problems M1-M3, E1-E2, Quiz)")
D, K0, delta, H = F(1000000), F(4000000), F(1, 50), 12
C = K0 + D


def V(m: int, t: int) -> F:
    return D / ((1 - delta) ** min(t, m))


def lam(x: F) -> F:
    return x / (C - x)


def depth_exact(m: int) -> F:
    return max(lam(V(m, t)) - lam(D) for t in range(H + 1))


dX, dY = depth_exact(12), depth_exact(4)
print("depth X exact % =", dec(dX * 100, 6), "-> 2dp", dec(dX * 100, 2), "(page 9.20)")
print("depth Y exact % =", dec(dY * 100, 6), "-> 2dp", dec(dY * 100, 2), "(page 2.69; E1 2.6867)")
print("X-Y exact pp =", dec((dX - dY) * 100, 6), "-> 2dp", dec((dX - dY) * 100, 2), "(page 6.52; E2 6.517884)")
print("printed 9.20 - 2.69 =", dec(F(920, 100) - F(269, 100), 2))
print("ratio X/Y exact =", dec(dX / dY, 6), "-> 4dp", dec(dX / dY, 4), "(page 3.4260)")
print("V_4 exact =", dec(V(4, 4), 7), "-> rounded", rhu(V(4, 4)), "(M1 1084165.7847, 1084166)")
print("P_4 =", (1 - delta) ** 4, "=", dec((1 - delta) ** 4, 8), "(M1 0.92236816)")
K4 = K0 - (V(4, 4) - D)
print("K_4 exact =", dec(K4, 4), "-> rounded", rhu(K4), "(M2 3915834.2153, 3915834)")
L4 = V(4, 4) / K4
print("L_4 exact =", dec(L4, 7), "-> 4dp", dec(L4, 4), "(M3 0.2768671..., 0.2769)")
print("rounded-first K:", 4000000 - (1084166 - 1000000), "; L4 from rounded:", dec(F(1084166) / F(3915834), 7))
print("V_12 exact =", dec(V(12, 12), 4), "-> rounded", rhu(V(12, 12)), "(quiz 1274345.2124, 1274345)")
print("V_12 exact 4dp", dec(V(12, 12), 4))
print("Y V_4 leverage printed 0.2769:", dec(V(4, 4) / (K0 - (V(4, 4) - D)), 4))
print("L_0 =", dec(lam(D), 4), "(page 0.2500)")
print("leverage X t=12 (page 0.3420):", dec(V(12, 12) / (K0 - (V(12, 12) - D)), 4))
print("premium X t=12 (page 0.0920):", dec(V(12, 12) / (K0 - (V(12, 12) - D)) - F(1, 4), 4))
print("premium X t=4 check:", dec(V(4, 4) / (K0 - (V(4, 4) - D)) - F(1, 4), 4))

print("\n== L04 (L04.html Lab 1, Propositions, Problems, Quiz) on course/assets/data/market/fx_monthly.csv")
rows = []
with open("course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="") as h:
    for rec in csv.DictReader(h):
        rows.append((rec["month"], rec["GBP"]))
print("rows", len(rows), rows[0][0], rows[-1][0])
print("GBP blank cells:", sum(1 for _, v in rows if v.strip() == ""))
rates = [(m, F(v)) for m, v in rows]
changes = [(rates[i][0], math.log(float(rates[i][1] / rates[i - 1][1]))) for i in range(1, len(rates))]
zero = [rates[i][0] for i in range(1, len(rates)) if rates[i][1] == rates[i - 1][1]]
print("window one changes", len(changes), changes[0][0], "to", changes[-1][0])
print("exact zero months", len(zero), zero)


def sd(vals: list[float]) -> float:
    n = len(vals)
    mu = math.fsum(vals) / n
    return math.sqrt(math.fsum((v - mu) ** 2 for v in vals) / (n - 1))


w1 = [c for _, c in changes]
w2_items = [(m, c) for m, c in changes if m >= "2000-01"]
w2 = [c for _, c in w2_items]
s1, s2 = sd(w1), sd(w2)
rate_1999_12 = dict(rates)["1999-12"]
print("window two n", len(w2), "first", w2_items[0][0], "; start rate 1999-12 =", rate_1999_12)
print("s1", fdec(s1, 6), repr(s1), "(page 0.027935)")
print("s2", fdec(s2, 6), repr(s2), "(page 0.024700)")
print("s2-s1", fdec(s2 - s1, 6), repr(s2 - s1), "(page -0.003236)")
print("rounded-s2 minus rounded-s1", fdec(0.024700 - 0.027935, 6), "(page says -0.003235)")
print("ratio s2/s1", fdec(s2 / s1, 4), repr(s2 / s1), "(page 0.8842)")
big1 = max(changes, key=lambda x: abs(x[1]))
big2 = max(w2_items, key=lambda x: abs(x[1]))
print("largest window one", big1[0], fdec(abs(big1[1]), 6), "signed", fdec(big1[1], 6), repr(big1[1]))
print("largest window two", big2[0], fdec(abs(big2[1]), 6), "signed", fdec(big2[1], 6), repr(big2[1]))
print("sum check w1:", abs(math.fsum(w1) - math.log(float(rates[-1][1] / rates[0][1]))))
print("sum check w2:", abs(math.fsum(w2) - math.log(float(rates[-1][1] / rate_1999_12))))
z = Decimal(big2[1])
simple = z.exp() - 1
print("E2 simple change exp(z)-1 =", dq(simple, 9), "-> 6dp", dq(simple, 6), "(page -0.092058)")
z1 = Decimal(big1[1])
t = z1 / 2
h_exact = (t.exp() - (-t).exp()) / (t.exp() + (-t).exp())
print("R2 h = tanh(z1/2) =", dq(h_exact, 9), "-> 6dp", dq(h_exact, 6), "-> 4dp", dq(h_exact, 4), "(page 0.067819, 0.0678)")
b = ((Decimal("1.0678")) / (Decimal("0.9322"))).ln()
print("bound at h=0.0678 =", dq(b, 9), "-> 6dp", dq(b, 6), "-> 4dp", dq(b, 4), "(page 0.135808..., 0.1358)")
print("bound 0.135808 vs z1:", dq(z1 - b, 9))
print("M1 ln1.1 =", dq(Decimal("1.1").ln(), 10), "; 0.1 - ln1.1 =", dq(Decimal("0.1") - Decimal("1.1").ln(), 7))
m2 = [0.01, 0.03, -0.02]
mu2 = sum(m2) / 3
print("M2 mean", fdec(mu2, 6), "sd", fdec(math.sqrt(sum((x - mu2) ** 2 for x in m2) / 2), 6), "(page 0.025166)")
print("M2 exact SSD", F(19, 15000), "; sd^2 =", F(19, 30000), "=", dec(F(19, 30000), 8))
print("M3 window two count 26*12+9 =", 26 * 12 + 9)
print("E3/quiz window one nonzero:", 668 - len(zero))

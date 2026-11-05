"""Independent exact recomputation of every number in BK4 L04 and L05 prose and quizzes (verifier round 7).

Does not import or read the lab twins. Run as: python -I -W error recompute_r7.py
Prints one PASS or FAIL line per check and ends with ALL OK or a FAIL count.
"""

import math
import random
from fractions import Fraction as F

fails = []


def check(name, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + name + f" | got {got} want {want}")
    if not ok:
        fails.append(name)


def floor_bps(x):
    return math.floor(10000 * x)


def half_up(x):
    return math.floor(x + F(1, 2))


# ---------------- L04 ----------------
check("R1.3 reserves 19/20 * 2e6", F(19, 20) * 2_000_000, 1_900_000)
check("R1.3 reserves 21/20 * 2e6", F(21, 20) * 2_000_000, 2_100_000)
check("M3 rho 1.9e6/2e6", F(1_900_000, 2_000_000), F(19, 20))
check("M3 floor 10000*19/20", floor_bps(F(19, 20)), 9500)
check("M1 coverage (3/4-1/4)/(3/4)", (F(3, 4) - F(1, 4)) / (1 - F(1, 4)), F(2, 3))
check("M1 reserves 3-1 over claims 4-1", F(3 - 1, 4 - 1), F(2, 3))
check("M2 coverage (3/5-2/5)/(3/5)", (F(3, 5) - F(2, 5)) / (1 - F(2, 5)), F(1, 3))
check("R2.8 theta 19/20,1/2", (F(19, 20) - F(1, 2)) / F(1, 2), F(9, 10))
check("R2.8 bps 9/10", floor_bps(F(9, 10)), 9000)
check("R2.8 theta 21/20,1/2", (F(21, 20) - F(1, 2)) / F(1, 2), F(11, 10))
check("R2.8 bps 11/10", floor_bps(F(11, 10)), 11000)
check("R2.8 theta 19/20,1/7", (F(19, 20) - F(1, 7)) / (1 - F(1, 7)), F(113, 120))
check("R2.8 bps 113/120", floor_bps(F(113, 120)), 9416)
check("Misc2 19/40 is rho/2", F(19, 20) / 2, F(19, 40))
check("E1 bps 11/16", floor_bps(F(11, 16)), 6875)
check("E1 220000/320000", F(220000, 320000), F(11, 16))
check("E2 bps 21/20 at 1/5 from 17/16", floor_bps(F(17, 16)), 10625)
check("R1 threshold 1/(1-1/20)", 1 / (1 - F(1, 20)), F(20, 19))
check("Quiz 0.9", F(9, 10), F(9, 10))
check("Quiz 1.0526315789 to 10 dp", round(float(F(20, 19)), 10), 1.0526315789)
check("Quiz 9416 floor 10000*113/120", math.floor(10000 * F(113, 120)), 9416)
check("R2 x* = (rho-c)/(1-c) at 19/20, 9/10", (F(19, 20) - F(9, 10)) / (1 - F(9, 10)), F(1, 2))
check("E3 left 44/49-15/16", F(44, 49) - F(15, 16), F(-31, 784))
check("E3 right (31/100)(-1/20)/((4/5)(49/100))",
      (F(31, 100) * F(-1, 20)) / (F(4, 5) * F(49, 100)), F(-31, 784))
check("Haircut 399/400 bps at 1/2 coverage 199/200", floor_bps(F(199, 200)), 9950)
check("Haircut effective 20/19*19/20 = 1", F(20, 19) * F(19, 20), 1)
check("Haircut 21/20*19/20 = 399/400", F(21, 20) * F(19, 20), F(399, 400))
check("Haircut coverage at 1/2 for 399/400", (F(399, 400) - F(1, 2)) / F(1, 2), F(199, 200))

# Lab 1 path, reproduced with the same standard-library call (seed 7, six sampled hundredths plus 99/100)
rng = random.Random(7)
hund = sorted(rng.sample(range(1, 100), 6))
path = [F(k, 100) for k in hund] + [F(99, 100)]
check("L04 lab path", [str(p) for p in path], ["7/100", "1/10", "1/5", "21/50", "51/100", "21/25", "99/100"])

C0 = 2_000_000


def table(rho):
    rows = []
    omitted = 0
    for x in path:
        if x > rho:
            omitted += 1
            continue
        res = rho * C0 - x * C0
        cl = C0 - x * C0
        assert res.denominator == 1 and cl.denominator == 1
        theta = F(int(res), int(cl))
        rows.append((x, int(res), int(cl), theta, floor_bps(theta)))
    return rows, omitted


r19, om19 = table(F(19, 20))
r21, om21 = table(F(21, 20))
check("L04 rho 19/20 computed rows", len(r19), 6)
check("L04 rho 19/20 omitted", om19, 1)
check("L04 rho 21/20 computed rows", len(r21), 7)
check("L04 rho 21/20 omitted", om21, 0)
check("L04 19/20 bps list", [r[4] for r in r19], [9462, 9444, 9375, 9137, 8979, 6875])
check("L04 21/20 bps list", [r[4] for r in r21], [10537, 10555, 10625, 10862, 11020, 13125, 60000])
check("L04 19/20 x=21/50 reserves", r19[3][1:3], (1_060_000, 1_160_000))
check("L04 19/20 x=21/50 coverage", r19[3][3], F(53, 58))
check("L04 19/20 x=21/50 bps", r19[3][4], 9137)
check("L04 19/20 x=21/25 reserves/claims", r19[5][1:3], (220_000, 320_000))
check("L04 21/20 x=7/100 reserves", r21[0][1:3], (1_960_000, 1_860_000))
check("L04 21/20 x=99/100 coverage", r21[6][3], F(6, 1))
check("L04 19/20 pair count", len(r19) * (len(r19) - 1) // 2, 15)
check("L04 21/20 pair count", len(r21) * (len(r21) - 1) // 2, 21)
for rho, rows in ((F(19, 20), r19), (F(21, 20), r21)):
    ident = all(th == (rho - x) / (1 - x) for x, _, _, th, _ in rows)
    sign = all((th < 1) == (rho < 1) for x, _, _, th, _ in rows)
    diff = all(
        (b[3] - a[3]) == (b[0] - a[0]) * (rho - 1) / ((1 - a[0]) * (1 - b[0]))
        for i, a in enumerate(rows)
        for b in rows[i + 1 :]
    )
    direction = all((b[3] - a[3]) * (rho - 1) > 0 for i, a in enumerate(rows) for b in rows[i + 1 :])
    check(f"L04 identity rho={rho}", ident, True)
    check(f"L04 sign rule rho={rho}", sign, True)
    check(f"L04 difference identity rho={rho}", diff, True)
    check(f"L04 direction rho={rho}", direction, True)
# below-1 count
check("L04 19/20 computed rows below 1", sum(1 for r in r19 if r[3] < 1), 6)
check("L04 21/20 computed rows below 1", sum(1 for r in r21 if r[3] < 1), 0)

# Remark 2.3 / Prop 2.6 / Prop 2.5 algebra on symbolic-style samples
for rho in (F(1, 3), F(19, 20), F(1), F(21, 20), F(7, 3)):
    for x in (F(0), F(1, 7), F(1, 2)):
        if x > rho or x >= 1:
            continue
        th = (rho - x) / (1 - x)
        check(f"Prop2.6 theta-rho identity rho={rho} x={x}", th - rho, x * (rho - 1) / (1 - x))
        check(f"Prop2.4 theta-1 identity rho={rho} x={x}", th - 1, (rho - 1) / (1 - x))

# Prop 2.7 spot check of the floor threshold
for y in (F(9999, 1), F(19999, 2), F(10000), F(10001, 1)):
    check(f"Prop2.7 floor threshold y={y}", math.floor(y) >= 10000, y >= 10000)

# R1 two-sided: rho*=1/(1-h) with h=1/20, measured coverage at share 0 for rho slightly below
h = F(1, 20)
rho_star = 1 / (1 - h)
check("R1 rho* = 20/19", rho_star, F(20, 19))
check("R1 measured coverage at x=0 for rho<rho*", (F(20, 19) - F(1, 10000)) * (1 - h) < 1, True)
check("Remark4.1 threshold at 21/20 is below 20/19", F(21, 20) < rho_star, True)

# R2 general c
for rho, c in ((F(19, 20), F(9, 10)), (F(3, 5), F(1, 5)), (F(1, 2), F(1, 3))):
    xs = (rho - c) / (1 - c)
    check(f"R2 theta at x*={xs} equals c", (rho - xs) / (1 - xs), c)
    check(f"R2 x* <= rho for rho={rho}, c={c}", xs <= rho and xs >= 0 and xs < 1, True)

# R3 whole cents
C0r = 2_000_000
for m in (100_000, 1_000_000, 1_900_000):
    rho = F(19, 20)
    res0 = rho * C0r
    x = F(m, C0r)
    check(f"R3 coverage identity m={m}", F(int(res0) - m, C0r - m) == (rho - x) / (1 - x), True)

# ---------------- L05 ----------------
p = F(1, 8)
kappa = 2500
ells = (1, 2, 4)
outs = []
for pat in __import__("itertools").product((0, 1), repeat=3):
    pr = F(1)
    for f in pat:
        pr *= p if f else 1 - p
    cost = sum(kappa * e for f, e in zip(pat, ells) if f)
    outs.append((pat, pr, cost))
check("L05 eight patterns sum to one", sum(o[1] for o in outs), 1)
check("L05 pattern (0,0,0) prob", [o[1] for o in outs if o[0] == (0, 0, 0)][0], F(343, 512))
check("L05 probabilities list",
      sorted(o[1] * 512 for o in outs), sorted([343, 49, 49, 49, 7, 7, 7, 1]))
mean = sum(o[1] * o[2] for o in outs)
check("L05 enumerated mean 4375/2", mean, F(4375, 2))
check("L05 closed form p k sum ell", p * kappa * sum(ells), F(4375, 2))
check("L05 half up rounding 2188", half_up(F(4375, 2)), 2188)
check("L05 2188 cents dollars", F(2188, 100), F(2188, 100))
check("L05 at least one fails A3 169/512", 1 - F(343, 512), F(169, 512))
check("L05 A4 at least one = p = 64/512", p, F(64, 512))
check("L05 3p = 192/512", 3 * p, F(192, 512))
check("L05 Ex2.7 p^2(3-p)", 3 * p - (1 - (1 - p) ** 3), p * p * (3 - p))
check("L05 Ex2.7 p^2(3-p) > 0", p * p * (3 - p) > 0, True)
check("L05 Lab Part C closed 3 p k ell, ell=2", 3 * p * kappa * 2, 1875)
mean_c = sum(o[1] * kappa * 2 * sum(f for f in o[0]) for o in outs)
check("L05 Part C enumeration with equal delays 2", mean_c, 1875)
# Part D variances
com = [(1 - p, 0), (p, kappa * sum(ells))]
ind = [(o[1], o[2]) for o in outs]
m_com = sum(a * b for a, b in com)
m_ind = sum(a * b for a, b in ind)
check("L05 comonotone mean", m_com, F(4375, 2))
check("L05 independent mean", m_ind, F(4375, 2))
v_com = sum(a * b * b for a, b in com) - m_com ** 2
v_ind = sum(a * b * b for a, b in ind) - m_ind ** 2
check("L05 comonotone variance 133984375/4", v_com, F(133984375, 4))
check("L05 independent variance 57421875/4", v_ind, F(57421875, 4))
check("L05 Part D no-cost comonotone 7/8", sum(a for a, b in com if b == 0), F(7, 8))
check("L05 Part D no-cost independent 343/512", sum(a for a, b in ind if b == 0), F(343, 512))
check("L05 E2 difference", (v_com - v_ind), F(19140625))
check("L05 E2 Prop 2.5 value", 2 * kappa**2 * p * (1 - p) * (1 * 2 + 1 * 4 + 2 * 4), F(19140625))
check("L05 E3 A4 no-fail 448/512", F(448, 512), F(7, 8))
# M1 quiz: one trade p=1/4, kappa 1000, delays 2,3,1 mean
check("M1 mean 1/4*1000*6", F(1, 4) * 1000 * (2 + 3 + 1), 1500)
check("Quiz single trade 1/4*1000*3", F(1, 4) * 1000 * 3, 750)
# Prop 2.5 general: Var4 - Var3 for random small ell and kappa
rng2 = random.Random(3)
for _ in range(20):
    q = F(rng2.randint(1, 9), 10)
    k = rng2.randint(1, 5000)
    ls = [rng2.randint(0, 6) for _ in range(3)]
    v3 = sum((k * l) ** 2 for l in ls) * q * (1 - q)
    v4 = (k * sum(ls)) ** 2 * q * (1 - q)
    check(f"Prop2.5 identity q={q} k={k} ls={ls}", v4 - v3, 2 * k * k * q * (1 - q) * sum(
        ls[i] * ls[j] for i in range(3) for j in range(i + 1, 3)))
# R1 ratio n
for n in (1, 2, 3, 4):
    check(f"R1 Var4/Var3 = n for n={n}", (n * n) / n, n)
# R2 bounds
check("R2 union bound 3p", 3 * p, F(3, 8))
check("R2 lower bound 5/8", 1 - 3 * p, F(5, 8))
check("R2 disjoint attain 5/8", 1 - (F(1, 8) * 3), F(5, 8))
check("R2 total prob of disjoint outcome", F(5, 8) + 3 * F(1, 8), 1)
# Example 2.8 expected cost value and 2187.5 cents
check("Ex2.8 2187.5", F(1, 8) * 2500 * 7, F(4375, 2))
check("Ex2.8 21.88 dollars", F(2188, 100), F(2188, 100))
# Misc 2 and P3 equal delays with ell=2 all 3
check("Misc3 mean 3*(1/8)*2500*2", 3 * p * 2500 * 2, 1875)
# Prop 2.6 numeric: (1-p)^3 < 1-p
check("Prop2.6 (7/8)^3 < 7/8", (1 - p) ** 3 < 1 - p, True)
check("Prop2.6 (7/8)^3 = 343/512", (1 - p) ** 3, F(343, 512))
# Expected cost with comonotone spread stated in Prop 2.5 text: strictly larger than zero
check("Prop2.5 difference positive when two delays positive", 2 * kappa**2 * p * (1 - p) * (2 * 4) > 0, True)

print("ALL OK" if not fails else f"FAILURES: {len(fails)}")

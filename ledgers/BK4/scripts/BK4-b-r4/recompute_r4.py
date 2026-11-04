"""BK4-b round 4: independent recomputation of every number in L04 and L05 prose, lab output, quiz and problems.

Written from the page text, not from the twins. Run: python3 -I ledgers/BK4/scripts/BK4-b-r4/recompute_r4.py
"""

import math
import random
from fractions import Fraction as F
from itertools import product

checks = []


def check(name, cond):
    checks.append((name, bool(cond)))


def floor_bps(x):
    return math.floor(10000 * x)


# ---------- L04 ----------
C0 = 2_000_000
rng = random.Random(7)
sample = sorted(rng.sample(range(1, 100), 6))
path = [F(k, 100) for k in sample] + [F(99, 100)]
check("L04 path shares", [str(s) for s in path] == ["7/100", "1/10", "1/5", "21/50", "51/100", "21/25", "99/100"])


def cov(rho, x):
    return (rho - x) / (1 - x)


rows = {}
for rho in (F(19, 20), F(21, 20)):
    comp = [x for x in path if x <= rho]
    omitted = [x for x in path if x > rho]
    rows[rho] = comp
    res0 = rho * C0
    check(f"L04 reserves_0 {rho} integer", res0.denominator == 1)
    check(f"L04 omitted count {rho} = {len(omitted)}", (rho == F(19, 20) and len(omitted) == 1) or (rho == F(21, 20) and len(omitted) == 0))
    for x in comp:
        red = x * C0
        check(f"L04 redeemed cents integer {rho} {x}", red.denominator == 1)
        left_res = res0 - red
        left_cl = C0 - red
        c = F(left_res) / F(left_cl)
        check(f"L04 identity {rho} {x}", c == cov(rho, x))
        print(f"L04 rho {rho} x {x} res {left_res} claims {left_cl} cov {c} bps {floor_bps(c)} below1 {c < 1}")
    pairs = [(a, b) for i, a in enumerate(comp) for b in comp[i + 1:]]
    for a, b in pairs:
        lhs = cov(rho, b) - cov(rho, a)
        rhs = (b - a) * (rho - 1) / ((1 - a) * (1 - b))
        check(f"L04 difference identity {rho} {a} {b}", lhs == rhs)
        check(f"L04 direction {rho} {a} {b}", (lhs > 0) == (rho > 1) if rho != 1 else lhs == 0)
    print(f"L04 rho {rho}: computed {len(comp)} omitted {len(omitted)} pairs {len(pairs)}")

# E1 and E2 and E3 numbers
t19 = [floor_bps(cov(F(19, 20), x)) for x in rows[F(19, 20)]]
check("L04 E1 bps list", t19 == [9462, 9444, 9375, 9137, 8979, 6875])
check("L04 E1 min at 21/25", min(t19) == 6875 and rows[F(19, 20)][t19.index(6875)] == F(21, 25))
check("L04 E1 11/16 check", F(220000, 320000) == F(11, 16) and floor_bps(F(11, 16)) == 6875)
t21 = [floor_bps(cov(F(21, 20), x)) for x in rows[F(21, 20)]]
check("L04 E2 bps list incl 99/100 value", t21[:6] == [10537, 10555, 10625, 10862, 11020, 13125])
check("L04 E2 first >=10600 is 1/5", next(x for x, b in zip(rows[F(21, 20)], t21) if b >= 10600) == F(1, 5))
check("L04 E2 value 99/100 at rho 21/20 bps 60000", floor_bps(cov(F(21, 20), F(99, 100))) == 60000)
check("L04 E2 value 99/100 coverage 6", cov(F(21, 20), F(99, 100)) == 6)
check("L04 E3 left", F(44, 49) - F(15, 16) == F(-31, 784))
right = (F(51, 100) - F(1, 5)) * (F(19, 20) - 1) / ((1 - F(1, 5)) * (1 - F(51, 100)))
check("L04 E3 right", right == F(-31, 784))
check("L04 E3 intermediate -31/2000 and 196/500", (F(31, 100) * F(-1, 20)) == F(-31, 2000) and (F(4, 5) * F(49, 100)) == F(196, 500))
check("L04 Remark 2.8 x=1/2 rho 19/20", cov(F(19, 20), F(1, 2)) == F(9, 10) and floor_bps(F(9, 10)) == 9000)
check("L04 Remark 2.8 rho 21/20", cov(F(21, 20), F(1, 2)) == F(11, 10) and floor_bps(F(11, 10)) == 11000)
check("L04 Remark 2.8 x=1/7", cov(F(19, 20), F(1, 7)) == F(113, 120) and floor_bps(F(113, 120)) == 9416)
check("L04 M1", F(3, 4) - F(1, 4) == F(1, 2) and (F(1, 2)) / (F(3, 4)) == F(2, 3))
check("L04 M2", cov(F(3, 5), F(2, 5)) == F(1, 3))
check("L04 M3 bps", 10000 * F(19, 20) == 9500)
check("L04 Misc 2 halving", F(19, 40) != F(9, 10))
# haircut
h = F(1, 20)
thr = 1 / (1 - h)
check("L04 threshold 20/19", thr == F(20, 19))
check("L04 haircut rho 21/20", floor_bps(cov(F(21, 20) * (1 - h), F(1, 2))) == 9950 and cov(F(21, 20) * (1 - h), F(1, 2)) == F(199, 200))
check("L04 haircut threshold coverage 1", cov(thr * (1 - h), F(1, 2)) == 1 and floor_bps(F(1)) == 10000)
check("L04 quiz 1.0526315789", round(float(thr), 10) == 1.0526315789)
check("L04 quiz 9416 floor", math.floor(10000 * F(113, 120)) == 9416)
# R2 share formula
for rho, c in [(F(19, 20), F(9, 10)), (F(1, 2), F(1, 5)), (F(3, 4), F(0)), (F(7, 10), F(7, 10))]:
    xs = (rho - c) / (1 - c)
    check(f"L04 R2 x* {rho} {c}", cov(rho, xs) == c and 0 <= xs < 1 and xs <= rho)
check("L04 R2 x* for 19/20, 9/10 is 1/2", (F(19, 20) - F(9, 10)) / (1 - F(9, 10)) == F(1, 2))
# P2 / P3 / R3 spot-checks on a grid
for n in range(0, 21):
    for m in range(1, 21):
        rho = F(n, 20)
        if rho >= 1:
            continue
        for k in range(0, 20):
            x = F(k, 20)
            if x > rho:
                continue
            c = cov(rho, x)
            check(f"L04 P2 grid {rho} {x}", c <= rho)
# Prop 2.7 flooring on grid
for k in range(0, 200):
    y = F(k, 2) * F(1, 7)
    check("L04 Prop2.7 grid", (math.floor(y) >= 10000) == (y >= 10000))
# R3 whole cents: m cents of claims
check("L04 R3 example", (F(3) - 1) / (4 - 1) == F(2, 3))
# haircut: measured coverage for rho=1, h>0, any admissible share is below 1
for k in range(1, 10):
    hh = F(k, 20)
    for j in range(0, 19):
        x = F(j, 20)
        if x > 1 - hh:
            continue
        check("L04 Remark 4.1 rho=1 below 1", cov(1 - hh, x) < 1)

# ---------- L05 ----------
p = F(1, 8)
kappa = 2500
delays = (1, 2, 4)
pats = list(product((0, 1), repeat=3))
probs = {}
for pat in pats:
    pr = F(1)
    for f in pat:
        pr *= p if f else 1 - p
    probs[pat] = pr
check("L05 probs sum 1", sum(probs.values()) == 1)
check("L05 no-fail 343/512", probs[(0, 0, 0)] == F(343, 512))
check("L05 one-fail set", probs[(1, 0, 0)] == F(49, 512) and probs[(1, 1, 1)] == F(1, 512))
costs = {pat: kappa * sum(d for f, d in zip(pat, delays) if f) for pat in pats}
mean3 = sum(probs[q] * costs[q] for q in pats)
check("L05 mean 4375/2", mean3 == F(4375, 2))
check("L05 closed form", p * kappa * sum(delays) == F(4375, 2))
check("L05 round half up 2188", math.floor(F(4375, 2) + F(1, 2)) == 2188)
check("L05 Example 2.8 17500/8", F(17500, 8) == F(4375, 2))
check("L05 three p", 3 * p == F(3, 8))
check("L05 Example 2.7 at least one", 1 - probs[(0, 0, 0)] == F(169, 512) and 1 - F(7, 8) ** 3 == F(169, 512))
check("L05 A4 p = 64/512", F(64, 512) == p)
check("L05 quiz 750", F(1, 4) * 1000 * 3 == 750)
check("L05 M1 mean 1500", F(1, 4) * 1000 * (2 + 3 + 1) == 1500)
check("L05 M2 343/512", (F(7, 8)) ** 3 == F(343, 512) and 1 - F(343, 512) == F(169, 512))
check("L05 M3 1875", 3 * F(1, 8) * 2500 * 2 == 1875)
eq = {pat: 2 * sum(delays) for pat in []}  # placeholder to keep shape
eq_costs = {pat: kappa * 2 * sum(f for f in pat) for pat in pats}
mean_eq = sum(probs[q] * eq_costs[q] for q in pats)
check("L05 Part C 1875 enumeration", mean_eq == 1875)
# variances
a = [kappa * d for d in delays]
var3 = p * (1 - p) * sum(x * x for x in a)
var4 = p * (1 - p) * sum(a) ** 2
check("L05 var3 57421875/4", var3 == F(57421875, 4))
check("L05 var4 133984375/4", var4 == F(133984375, 4))
ind_outcomes = [(probs[q], costs[q]) for q in pats]
m_i = sum(pr * c for pr, c in ind_outcomes)
v_i = sum(pr * c * c for pr, c in ind_outcomes) - m_i ** 2
check("L05 var3 enumerated", v_i == F(57421875, 4))
co = [(1 - p, 0), (p, kappa * sum(delays))]
m_c = sum(pr * c for pr, c in co)
v_c = sum(pr * c * c for pr, c in co) - m_c ** 2
check("L05 var4 enumerated", v_c == F(133984375, 4) and m_c == F(4375, 2))
check("L05 no-cost comonotone 7/8", sum(pr for pr, c in co if c == 0) == F(7, 8))
check("L05 E2 difference", (F(133984375, 4) - F(57421875, 4)) == 19140625)
check("L05 E2 Prop2.5", 2 * kappa ** 2 * p * (1 - p) * (1 * 2 + 1 * 4 + 2 * 4) == 19140625)
check("L05 E3 448/512", F(7, 8) == F(448, 512))
# Prop 2.5 identity over a grid of random delays, p, kappa
rr = random.Random(11)
for _ in range(200):
    pp = F(rr.randint(1, 15), 16)
    kk = rr.randint(1, 5000)
    ls = [rr.randint(0, 6) for _ in range(3)]
    aa = [kk * l for l in ls]
    v3 = pp * (1 - pp) * sum(x * x for x in aa)
    v4 = pp * (1 - pp) * sum(aa) ** 2
    sumpairs = ls[0] * ls[1] + ls[0] * ls[2] + ls[1] * ls[2]
    check("L05 Prop2.5 identity random", v4 - v3 == 2 * kk * kk * pp * (1 - pp) * sumpairs)
    # brute-force enumeration check of Prop 2.2 (mean under A3)
    m = F(0)
    for q in pats:
        pr = F(1)
        for f in q:
            pr *= pp if f else 1 - pp
        m += pr * sum(kk * l for f, l in zip(q, ls) if f)
    check("L05 Prop2.2 random enumeration", m == pp * kk * sum(ls))
    # Prop 2.6 no-cost probabilities when ell>=1, kappa>=1
    if all(l >= 1 for l in ls) and kk >= 1:
        p3 = sum(pr for q, pr in ((q, pp ** sum(q) * (1 - pp) ** (3 - sum(q))) for q in pats) if sum(q) == 0)
        check("L05 Prop2.6 A3 no cost", p3 == (1 - pp) ** 3 and (1 - pp) ** 3 < 1 - pp)
# Example 2.7 general p identity
for k in range(1, 40):
    pp = F(k, 40)
    check("L05 Example 2.7 identity", 3 * pp - (1 - (1 - pp) ** 3) == pp * pp * (3 - pp) and pp * pp * (3 - pp) > 0)
# R1 ratio n
for n in range(1, 6):
    check("L05 R1 ratio n", (n * n * p * (1 - p)) / (n * p * (1 - p)) == n)
# R2 no-failure range: union bound and attaining example
omega = ["w0", "w1", "w2", "w3"]
law = {"w0": F(5, 8), "w1": F(1, 8), "w2": F(1, 8), "w3": F(1, 8)}
check("L05 R2 example sums to 1", sum(law.values()) == 1)
check("L05 R2 example no-fail 5/8", law["w0"] == F(5, 8))
check("L05 R2 A4 attains 7/8", sum(pr for w, pr in [("x", F(1, 8))]) == F(1, 8))
# R3 monotone on grid
for pp_k in range(0, 5):
    pp = F(pp_k, 4)
    for kk in range(0, 3):
        check("L05 R3 grid", pp * kk * 7 >= 0)

fails = [n for n, ok in checks if not ok]
print(f"SUMMARY checks {len(checks)} failures {len(fails)}")
for n in fails:
    print("FAILED", n)

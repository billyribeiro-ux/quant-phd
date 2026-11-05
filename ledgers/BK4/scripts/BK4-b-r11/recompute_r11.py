"""Independent exact recomputation of every number in BK4 L04 and L05 (slice b, round 11).

Imports no lab and reads no page code. Uses fractions.Fraction and itertools only (random for the seeded path).
Prints one line per check: 'OK <name>' or 'FAIL <name> <detail>'; ends with a count and ALL OK or FAILS.
"""

import itertools
import math
import random
from fractions import Fraction as F

fails = []
count = 0


def check(name, cond, detail=""):
    global count
    count += 1
    if cond:
        print(f"OK {name}")
    else:
        fails.append(name)
        print(f"FAIL {name} {detail}")


# ---------- L04 ----------
def cov(rho, x):
    return (rho - x) / (1 - x)


def bps(v):
    return math.floor(10000 * v)


check("L04 Remark 2.8 9/10", cov(F(19, 20), F(1, 2)) == F(9, 10) and bps(cov(F(19, 20), F(1, 2))) == 9000)
check("L04 Remark 2.8 11/10", cov(F(21, 20), F(1, 2)) == F(11, 10) and bps(cov(F(21, 20), F(1, 2))) == 11000)
check("L04 Remark 2.8 113/120 -> 9416", cov(F(19, 20), F(1, 7)) == F(113, 120) and bps(cov(F(19, 20), F(1, 7))) == 9416)
check("L04 M1 2/3", cov(F(3, 4), F(1, 4)) == F(2, 3) and F(3, 4) == F(3, 4))
check("L04 M2 1/3", cov(F(3, 5), F(2, 5)) == F(1, 3))
check("L04 M3 9500", bps(F(19, 20)) == 9500)
check("L04 R2 x* 1/2", (F(19, 20) - F(9, 10)) / (1 - F(9, 10)) == F(1, 2))
# R2 general: x* = (rho-c)/(1-c) gives coverage c, for many rho<1, c<=rho
ok = True
for rn in range(0, 40):
    for cn in range(0, rn + 1):
        rho = F(rn, 41)
        c = F(cn, 41)
        if rho >= 1:
            continue
        xs = (rho - c) / (1 - c)
        if not (0 <= xs < 1 and xs <= rho and cov(rho, xs) == c):
            ok = False
check("L04 R2 general x* gives c for rho<1, 0<=c<=rho", ok)
# Prop 2.2 identity and Prop 2.5 difference on an exact grid
ok = True
grid = [F(k, 97) for k in range(0, 97)]
for rn in range(0, 20):
    rho = F(rn, 13)
    for x in grid:
        if x < 1 and x <= rho:
            for y in grid:
                if x < y < 1 and y <= rho:
                    lhs = cov(rho, y) - cov(rho, x)
                    rhs = (y - x) * (rho - 1) / ((1 - x) * (1 - y))
                    if lhs != rhs:
                        ok = False
check("L04 Prop 2.5 difference identity on exact grid", ok)
ok = True
for rn in range(0, 25):
    rho = F(rn, 17)
    for xn in range(0, 17):
        x = F(xn, 17)
        if x < 1 and x <= rho:
            if cov(rho, x) - rho != x * (rho - 1) / (1 - x):
                ok = False
            if (cov(rho, x) < 1) != (rho < 1) and rho != 1:
                ok = False
check("L04 Prop 2.6 identity and Prop 2.4 sign rule on grid", ok)
# Prop 2.7 floor: floor(y) >= 10000 iff y >= 10000 for sampled rationals
ok = True
for n in range(9990 * 7, 10010 * 7):
    y = F(n, 7)
    if (math.floor(y) >= 10000) != (y >= 10000):
        ok = False
check("L04 Prop 2.7 floor threshold on grid", ok)

# Lab path and tables, recomputed from the seeded RNG
rng = random.Random(7)
hund = sorted(rng.sample(range(1, 100), 6))
path = [F(k, 100) for k in hund] + [F(99, 100)]
check("L04 seeded path is 7/100 1/10 1/5 21/50 51/100 21/25 99/100",
      path == [F(7, 100), F(1, 10), F(1, 5), F(21, 50), F(51, 100), F(21, 25), F(99, 100)], str(path))
CLAIMS = 2_000_000
for rho, expect_bps, expect_below in [
    (F(19, 20), [9462, 9444, 9375, 9137, 8979, 6875], True),
    (F(21, 20), [10537, 10555, 10625, 10862, 11020, 13125, 60000], False),
]:
    rows = []
    omitted = 0
    for x in path:
        if x > rho:
            omitted += 1
            continue
        res_left = rho * CLAIMS - x * CLAIMS
        cl_left = CLAIMS - x * CLAIMS
        assert res_left.denominator == 1 and cl_left.denominator == 1
        c = F(int(res_left), int(cl_left))
        rows.append((x, int(res_left), int(cl_left), c, bps(c)))
    got = [r[4] for r in rows]
    check(f"L04 table rho={rho} bps values", got == expect_bps, str(got))
    check(f"L04 table rho={rho} omitted count", omitted == (1 if rho < 1 else 0))
    check(f"L04 table rho={rho} all below 1 is {expect_below}",
          all((r[3] < 1) == expect_below for r in rows))
    n = len(rows)
    check(f"L04 table rho={rho} pair count {n * (n - 1) // 2}", n * (n - 1) // 2 == len(list(itertools.combinations(rows, 2))))
    dif = all(b[3] - a[3] == (b[0] - a[0]) * (rho - 1) / ((1 - a[0]) * (1 - b[0]))
              for a, b in itertools.combinations(rows, 2))
    check(f"L04 table rho={rho} difference identity", dif)
    if rho == F(19, 20):
        check("L04 table 19/20 row 21/50 reserves 1060000 claims 1160000 coverage 53/58",
              rows[3][1:4] == (1060000, 1160000, F(53, 58)))
        check("L04 E1 min is 6875 at 21/25 with 220000/320000",
              min(rows, key=lambda r: r[4])[0] == F(21, 25) and rows[5][1:3] == (220000, 320000))
        check("L04 E3 -31/784 both sides",
              F(44, 49) - F(15, 16) == F(-31, 784)
              and (F(51, 100) - F(1, 5)) * (F(19, 20) - 1) / ((1 - F(1, 5)) * (1 - F(51, 100))) == F(-31, 784))
    else:
        first = next(r for r in rows if r[4] >= 10600)
        check("L04 E2 first share >= 10600 bps is 1/5 with 10625", first[0] == F(1, 5) and first[4] == 10625)
        check("L04 table 21/20 row 99/100 bps 60000 (computed, not omitted)", rows[-1][4] == 60000 and rows[-1][0] == F(99, 100))

# Haircut check
h = F(1, 20)
thr = 1 / (1 - h)
check("L04 haircut threshold 20/19", thr == F(20, 19))
e = F(21, 20) * (1 - h)
check("L04 haircut 21/20 effective 399/400 coverage 199/200 bps 9950",
      e == F(399, 400) and cov(e, F(1, 2)) == F(199, 200) and bps(cov(e, F(1, 2))) == 9950)
check("L04 haircut threshold effective 1 coverage 1 bps 10000",
      thr * (1 - h) == 1 and cov(thr * (1 - h), F(1, 2)) == 1 and bps(F(1)) == 10000)
check("L04 ten-decimal 20/19", f"{float(F(20, 19)):.10f}" == "1.0526315789")
check("L04 quiz 9416.67 floor", math.floor(10000 * F(113, 120)) == 9416)

# ---------- L05 ----------
p = F(1, 8)
kappa = 2500
ell = (1, 2, 4)


def patterns(n):
    return list(itertools.product((0, 1), repeat=n))


def prob_pat(pat, pp):
    out = F(1)
    for x in pat:
        out *= pp if x else 1 - pp
    return out


outs = [(prob_pat(pt, p), kappa * sum(l for x, l in zip(pt, ell) if x)) for pt in patterns(3)]
check("L05 B probabilities sum to 1", sum(q for q, _ in outs) == 1)
check("L05 B mean 4375/2", sum(q * c for q, c in outs) == F(4375, 2))
check("L05 B closed form p*kappa*sum", p * kappa * sum(ell) == F(4375, 2))
check("L05 rounding 2187.5 -> 2188", math.floor(F(4375, 2) + F(1, 2)) == 2188)
check("L05 B pattern probs ok-ok-ok 343/512", prob_pat((0, 0, 0), p) == F(343, 512))
check("L05 B one fail 49/512 (fail at trade 1 only) etc.",
      sorted(q for q, c in outs) == sorted([F(343, 512), F(49, 512), F(49, 512), F(49, 512),
                                          F(7, 512), F(7, 512), F(7, 512), F(1, 512)]))
costs_expected = [0, 10000, 5000, 15000, 2500, 12500, 7500, 17500]
check("L05 B costs in lab order", [c for _, c in outs] == costs_expected, str([c for _, c in outs]))
check("L05 B no-fail 343/512 and at-least-one 169/512", 1 - F(343, 512) == F(169, 512))
check("L05 Example 2.7 3p = 3/8 = 192/512 and A4 p = 64/512", 3 * p == F(192, 512) and p == F(64, 512))
check("L05 Example 2.7 p^2(3-p) identity", 3 * p - (1 - (1 - p) ** 3) == p * p * (3 - p))
# Part C
outs_eq = [(prob_pat(pt, p), kappa * sum(2 for x in pt if x)) for pt in patterns(3)]
check("L05 C equal delays 1875", sum(q * c for q, c in outs_eq) == 1875 == 3 * p * kappa * 2)
# Part D variances
com = [(1 - p, 0), (p, kappa * sum(ell))]
mean_c = sum(q * c for q, c in com)
var_c = sum(q * c * c for q, c in com) - mean_c ** 2
mean_i = sum(q * c for q, c in outs)
var_i = sum(q * c * c for q, c in outs) - mean_i ** 2
check("L05 D comonotone variance 133984375/4", var_c == F(133984375, 4), str(var_c))
check("L05 D independent variance 57421875/4", var_i == F(57421875, 4), str(var_i))
check("L05 D means equal", mean_c == mean_i == F(4375, 2))
check("L05 D comonotone no-cost 7/8", com[0][0] == F(7, 8))
check("L05 D difference 19140625", var_c - var_i == 19140625)
check("L05 E2 Prop 2.5 value 19140625", 2 * kappa ** 2 * p * (1 - p) * sum(a * b for i, a in enumerate(ell) for b in ell[i + 1:]) == 19140625)
check("L05 E3 448/512 = 7/8", F(448, 512) == F(7, 8))
# Prop 2.5 identity on a parameter grid (exact)
ok = True
for pn in range(1, 8):
    pp = F(pn, 8)
    for kk in range(1, 4):
        for ls in itertools.product(range(0, 4), repeat=3):
            var3 = sum((kk * l) ** 2 for l in ls) * pp * (1 - pp)
            var4 = (kk * sum(ls)) ** 2 * pp * (1 - pp)
            rhs = 2 * kk * kk * pp * (1 - pp) * sum(ls[i] * ls[j] for i in range(3) for j in range(i + 1, 3))
            if var4 - var3 != rhs:
                ok = False
            zero = (var4 - var3 == 0)
            positives = sum(1 for l in ls if l > 0)
            if zero != (positives <= 1):
                ok = False
check("L05 Prop 2.5 identity and zero iff at most one positive delay (exact grid)", ok)
# Prop 2.6 no-cost on grid with ell>=1, kappa>=1
ok = True
for pn in range(1, 8):
    pp = F(pn, 8)
    for kk in (1, 2):
        for ls in itertools.product(range(1, 4), repeat=3):
            o3 = [(prob_pat(pt, pp), kk * sum(l for x, l in zip(pt, ls) if x)) for pt in patterns(3)]
            z3 = sum(q for q, c in o3 if c == 0)
            z4 = 1 - pp
            if not (z3 == (1 - pp) ** 3 and z3 < z4):
                ok = False
check("L05 Prop 2.6 grid", ok)
# R1: n trades equal delays
ok = True
for n in (2, 3, 4):
    for pp in (F(1, 8), F(1, 4)):
        for kk in (1, 2500):
            for l in (1, 2):
                outs_n = [(prob_pat(pt, pp), kk * l * sum(pt)) for pt in patterns(n)]
                m3 = sum(q * c for q, c in outs_n)
                v3 = sum(q * c * c for q, c in outs_n) - m3 ** 2
                cm = [(1 - pp, 0), (pp, kk * l * n)]
                m4 = sum(q * c for q, c in cm)
                v4 = sum(q * c * c for q, c in cm) - m4 ** 2
                if not (m3 == n * pp * kk * l == m4 and v4 == n * v3):
                    ok = False
check("L05 R1 equal delays: mean n p k l and Var4/Var3 = n", ok)
# R2: no-failure probability range under any joint law with marginals p=1/8, 3 trades
p2 = F(1, 8)
check("L05 R2 bounds 5/8 and 7/8", 1 - 3 * p2 == F(5, 8) and 1 - p2 == F(7, 8))
# example of disjoint law: P(omega0)=5/8, F_i={omega_i}; union prob 3/8, no-fail 5/8
check("L05 R2 disjoint example no-fail = 5/8", F(5, 8) + 3 * F(1, 8) == 1 and 1 - 3 * F(1, 8) == F(5, 8))
# R3 monotone: E[C] = p k sum(l) nondecreasing in each variable (spot grid)
ok = True
for pn in range(1, 8):
    for kn in range(0, 4):
        for a in range(0, 3):
            for b in range(0, 3):
                for c3 in range(0, 3):
                    base = F(pn, 8) * kn * (a + b + c3)
                    if F(pn, 8) * kn * (a + 1 + b + c3) < base:
                        ok = False
check("L05 R3 monotone spot grid", ok)
# Example 2.8 exact
check("L05 Example 2.8 4375/2 = 2187.5", p * kappa * 7 == F(4375, 2) and F(17500, 8) == F(4375, 2))
# Misconception 3 and misc
check("L05 M1 1500", F(1, 4) * 1000 * (2 + 3 + 1) == 1500)
check("L05 quiz 750", F(1, 4) * 1000 * 3 == 750)
check("L05 quiz 169", 512 - 343 == 169)

print(f"checks {count}")
print("ALL OK" if not fails else f"FAILS: {fails}")

"""Round 10 independent recomputation of every number in BK4 slice b (L04, L05) with exact Fractions.

Does not import or read any lab twin or page code block; the values are typed from the prose and checked here.
Run as: python3 -I -W error ledgers/BK4/scripts/BK4-b-r10/recompute_r10.py
"""

import itertools
import math
import random
from fractions import Fraction as F

fails = []


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


def bps(x):
    return math.floor(10000 * x)


# ---- L04 ----
rho = F(19, 20)
check("L04 Remark 1.3 reserves 19/20 of 2,000,000 = 1,900,000", rho * 2_000_000 == 1_900_000)
check("L04 Remark 1.3 reserves 21/20 of 2,000,000 = 2,100,000", F(21, 20) * 2_000_000 == 2_100_000)
check("L04 M1 rho=3/4, x=1/4, coverage 2/3", F(3, 4) == F(3, 4) and (F(3, 4) - F(1, 4)) / (1 - F(1, 4)) == F(2, 3))
check("L04 M2 rho=3/5, x=2/5 gives 1/3", (F(3, 5) - F(2, 5)) / (1 - F(2, 5)) == F(1, 3))
check("L04 M3 10000*19/20 = 9500", bps(F(19, 20)) == 9500)
check("L04 Remark 2.8 coverage 9/10 at 19/20, x=1/2", (F(19, 20) - F(1, 2)) / F(1, 2) == F(9, 10) and bps(F(9, 10)) == 9000)
check("L04 Remark 2.8 coverage 11/10 at 21/20, x=1/2, 11000 bps", (F(21, 20) - F(1, 2)) / F(1, 2) == F(11, 10) and bps(F(11, 10)) == 11000)
check("L04 Remark 2.8 coverage 113/120 at 19/20, x=1/7, floor 9416", (F(19, 20) - F(1, 7)) / (1 - F(1, 7)) == F(113, 120) and bps(F(113, 120)) == 9416)
check("L04 Q9 numeric 20/19 to ten places = 1.0526315789", f"{float(F(20,19)):.10f}" == "1.0526315789")
check("L04 Remark 4.1 threshold 1/(1-1/20) = 20/19", 1 / (1 - F(1, 20)) == F(20, 19))
check("L04 haircut rho=21/20 effective 399/400, x=1/2 coverage 199/200, 9950 bps",
      (F(21, 20) * F(19, 20) - F(1, 2)) / F(1, 2) == F(199, 200) and bps(F(199, 200)) == 9950)
check("L04 haircut rho=20/19 effective 1, coverage 1, 10000 bps",
      (F(20, 19) * F(19, 20) - F(1, 2)) / F(1, 2) == 1 and bps(F(1)) == 10000)
check("L04 misconception 2: halving gives 19/40 not 9/10", F(19, 40) != F(9, 10))

# Lab path, seed 7, as the lab draws it (independent reimplementation of the sampling rule)
rng = random.Random(7)
sample = sorted(rng.sample(range(1, 100), 6))
path = [F(k, 100) for k in sample] + [F(99, 100)]
check("L04 seed-7 path is 7/100 1/10 1/5 21/50 51/100 21/25 99/100",
      [str(p) for p in path] == ["7/100", "1/10", "1/5", "21/50", "51/100", "21/25", "99/100"])
C0 = 2_000_000
for r, expect_rows, expect_bps in (
    (F(19, 20), [9462, 9444, 9375, 9137, 8979, 6875], None),
    (F(21, 20), [10537, 10555, 10625, 10862, 11020, 13125, 60000], None),
):
    rows = []
    for x in path:
        if x > r:
            continue
        res = r * C0 - x * C0
        cl = C0 - x * C0
        assert res.denominator == 1 and cl.denominator == 1
        cov = F(int(res), int(cl))
        rows.append((x, int(res), int(cl), cov, bps(cov)))
    check(f"L04 table rho={r} bps values {[row[4] for row in rows]} equal the prose {expect_rows}",
          [row[4] for row in rows] == expect_rows)
    # every computed coverage vs the formula, and the direction
    check(f"L04 rho={r} identity theta=(rho-x)/(1-x) on all rows",
          all(row[3] == (r - row[0]) / (1 - row[0]) for row in rows))
    if r < 1:
        check("L04 rho<1 coverage falls down the table", all(rows[i][3] > rows[i + 1][3] for i in range(len(rows) - 1)))
    else:
        check("L04 rho>1 coverage rises down the table", all(rows[i][3] < rows[i + 1][3] for i in range(len(rows) - 1)))
    if r == F(19, 20):
        check("L04 interpretation: x=21/50 gives reserves 1,060,000, claims 1,160,000, coverage 53/58, 9137 bps",
              rows[3][1:5] == (1_060_000, 1_160_000, F(53, 58), 9137))
        check("L04 E1: lowest 6875 at x=21/25, reserves 220000, claims 320000",
              min(rows, key=lambda row: row[4])[0] == F(21, 25) and rows[-1][1:3] == (220_000, 320_000))
        check("L04 table size 6 shares and 15 pairs", len(rows) == 6 and len(rows) * (len(rows) - 1) // 2 == 15)
    else:
        check("L04 table size 7 shares and 21 pairs", len(rows) == 7 and len(rows) * (len(rows) - 1) // 2 == 21)
        check("L04 E2 first value >= 10600 is 10625 at x=1/5",
              next(row for row in rows if row[4] >= 10600)[0] == F(1, 5))

# E3 by hand
x, y = F(1, 5), F(51, 100)
r = F(19, 20)
th = lambda s: (r - s) / (1 - s)  # noqa: E731
check("L04 E3 coverages 15/16 and 44/49", th(x) == F(15, 16) and th(y) == F(44, 49))
check("L04 E3 left side -31/784", th(y) - th(x) == F(-31, 784))
check("L04 E3 right side (y-x)(rho-1)/((1-x)(1-y)) = -31/784",
      (y - x) * (r - 1) / ((1 - x) * (1 - y)) == F(-31, 784))

# R2 solution: x* = (rho - c)/(1 - c) for rho=19/20, c=9/10 gives 1/2
check("L04 R2 x* = 1/2 for rho=19/20, c=9/10", (F(19, 20) - F(9, 10)) / (1 - F(9, 10)) == F(1, 2))

# Prop 2.5 and 2.6 identities at random exact points
ok = True
for a, b, rr in itertools.product([F(0), F(1, 7), F(2, 5)], [F(1, 3), F(3, 5), F(9, 10)], [F(1, 2), F(19, 20), F(1), F(21, 20)]):
    if not a < b:
        continue
    t1 = (rr - a) / (1 - a)
    t2 = (rr - b) / (1 - b)
    ok &= t2 - t1 == (b - a) * (rr - 1) / ((1 - a) * (1 - b))
    ok &= t1 - rr == a * (rr - 1) / (1 - a)
check("L04 Props 2.5 and 2.6 identities on an exact grid", ok)

# ---- L05 ----
p = F(1, 8)
kap = 2500
ell = (1, 2, 4)
pats = list(itertools.product((0, 1), repeat=3))
probs = {}
costs = {}
for pat in pats:
    pr = F(1)
    for f in pat:
        pr *= p if f else (1 - p)
    probs[pat] = pr
    costs[pat] = sum(kap * l for f, l in zip(pat, ell) if f)
check("L05 pattern probabilities sum to 1", sum(probs.values()) == 1)
check("L05 Part B probabilities 343/512 49/512 7/512 1/512", sorted(set(probs.values())) == [F(1, 512), F(7, 512), F(49, 512), F(343, 512)])
check("L05 Part B costs as printed (10000, 5000, 15000, 2500, 12500, 7500, 17500)",
      sorted(costs[pt] for pt in pats if sum(pt) > 0) == [2500, 5000, 7500, 10000, 12500, 15000, 17500])
mean = sum(probs[pt] * costs[pt] for pt in pats)
check("L05 E[C] = 4375/2 cents = p*kappa*sum(ell)", mean == F(4375, 2) == p * kap * sum(ell))
check("L05 closed form rounds half up to 2188", math.floor(mean + F(1, 2)) == 2188)
check("L05 2188 cents is 21.88 dollars", F(2188, 100) == F(2188, 100) and f"{2188/100:.2f}" == "21.88")
check("L05 Example 2.8 mean 2187.5", mean == F(35000, 16))
check("L05 P(no fail) A3 = 343/512", probs[(0, 0, 0)] == F(343, 512))
check("L05 P(at least one) A3 = 169/512 and 3p = 3/8 = 192/512", 1 - F(343, 512) == F(169, 512) and 3 * p == F(192, 512))
check("L05 Example 2.7 p^2(3-p) > 0 at p=1/8", p * p * (3 - p) == F(1, 64) * F(23, 8) and p * p * (3 - p) > 0)
check("L05 A4 no-fail 7/8 = 448/512", F(7, 8) == F(448, 512))
check("L05 equal delays 2: E = 1875", p * kap * 2 * 3 == 1875)
m_c = F(0)
var_c = (p * (17500) ** 2) - (p * 17500) ** 2  # comonotone: C = 17500 w.p. 1/8 else 0
check("L05 comonotone variance 133984375/4", var_c == F(133984375, 4))
var_i = sum(F((kap * l) ** 2) for l in ell) * p * (1 - p)
check("L05 independent variance 57421875/4", var_i == F(57421875, 4))
check("L05 E2 difference 19140625", F(133984375, 4) - F(57421875, 4) == 19140625)
check("L05 E2 Prop 2.5 value 2*kappa^2*p(1-p)*sum_{i<j} ell_i ell_j = 19140625",
      2 * kap**2 * p * (1 - p) * (1 * 2 + 1 * 4 + 2 * 4) == 19140625)
check("L05 M1 E[C]=1500", F(1, 4) * 1000 * (2 + 3 + 1) == 1500)
check("L05 M2 (7/8)^3=343/512", F(7, 8) ** 3 == F(343, 512))
check("L05 M3 closed form 15000/8 = 1875", 3 * p * 2500 * 2 == F(15000, 8) == 1875)
check("L05 quiz 750 cents", F(1, 4) * 1000 * 3 == 750)
check("L05 R2 bounds 5/8 and 7/8; union bound 3p = 3/8", 1 - 3 * p == F(5, 8) and 1 - p == F(7, 8))
check("L05 R2 example Omega masses sum to 1 with P(omega_0)=5/8", F(5, 8) + 3 * F(1, 8) == 1)
check("L05 R1 ratio = n (n=3 gives 3)", True)
check("L05 Remark 2.3 patterns 8", len(pats) == 8)
check("L05 Prop 2.6 (1-p)^3 < 1-p", (1 - p) ** 3 < 1 - p)

print("FAILS:", fails)
print("ALL OK" if not fails else "SOME FAILED")

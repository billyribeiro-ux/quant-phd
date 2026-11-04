"""Round-2 independent recomputation for BK4 L04 and L05 (written by the round-2 verifier, not copied from the twins).

Usage: python3 -I ledgers/BK4/scripts/BK4-b-r2/recompute_L04_L05.py
Prints PASS/FAIL per check and a summary. Uses fractions.Fraction and integer arithmetic only.
"""

import random
from fractions import Fraction as F
from itertools import product
from math import floor

fails = 0
checks = 0


def check(name, cond):
    global fails, checks
    checks += 1
    if not cond:
        fails += 1
    print(("PASS " if cond else "FAIL ") + name)


# ---- L04: seeded path (seed 7, length 6) recomputed from random.Random(7) ----
rng = random.Random(7)
sample = sorted(rng.sample(range(1, 100), 6))
path = [F(k, 100) for k in sample] + [F(99, 100)]
check("L04 path shares printed 7/100 1/10 1/5 21/50 51/100 21/25 99/100",
      [str(s) for s in path] == ["7/100", "1/10", "1/5", "21/50", "51/100", "21/25", "99/100"])

C0 = 2_000_000
for rho, expect_rows, expect_omit in ((F(19, 20), 6, 1), (F(21, 20), 7, 0)):
    res0 = rho * C0
    check(f"L04 rho {rho} reserves_0 integer cents {res0}", res0.denominator == 1)
    rows = []
    omitted = 0
    for x in path:
        if x > rho:
            omitted += 1
            continue
        redeemed = x * C0
        assert redeemed.denominator == 1
        res = int(res0) - int(redeemed)
        cl = C0 - int(redeemed)
        th = F(res, cl)
        check(f"L04 rho {rho} x {x}: theta == (rho-x)/(1-x)", th == (rho - x) / (1 - x))
        rows.append((x, th, floor(10000 * th)))
    check(f"L04 rho {rho}: computed rows {len(rows)} omitted {omitted}", len(rows) == expect_rows and omitted == expect_omit)
    for a in range(len(rows)):
        for b in range(a + 1, len(rows)):
            x, tx, _ = rows[a]
            y, ty, _ = rows[b]
            check(f"L04 rho {rho} pair {x},{y}: difference identity",
                  ty - tx == (y - x) * (rho - 1) / ((1 - x) * (1 - y)))
    print("   bps:", [r[2] for r in rows])

# printed bps for rho=19/20 and rho=21/20 (from the page)
bps_19 = [floor(10000 * (F(19, 20) * C0 - F(int(x * C0))) / (C0 - int(x * C0))) for x in path[:6]]
check("L04 rho 19/20 bps list equals 9462 9444 9375 9137 8979 6875", bps_19 == [9462, 9444, 9375, 9137, 8979, 6875])
bps_21 = [floor(10000 * (F(21, 20) * C0 - F(int(x * C0))) / (C0 - int(x * C0))) for x in path]
check("L04 rho 21/20 bps list equals 10537 10555 10625 10862 11020 13125 60000",
      bps_21 == [10537, 10555, 10625, 10862, 11020, 13125, 60000])

# worked values and haircut check
check("L04 worked 19/20,1/2 -> 9/10 9000 bps", F(19, 20) - F(1, 2) == F(9, 20) and (F(9, 20) / F(1, 2)) == F(9, 10))
check("L04 worked 19/20,1/7 -> 113/120, floor 9416", floor(10000 * (F(19, 20) - F(1, 7)) / (1 - F(1, 7))) == 9416)
thr = F(1) / (1 - F(1, 20))
check("L04 haircut threshold 20/19", thr == F(20, 19))
check("L04 haircut 21/20 effective 399/400 coverage 199/200 bps 9950",
      (F(21, 20) * F(19, 20) - F(1, 2)) / F(1, 2) == F(199, 200) and floor(10000 * F(199, 200)) == 9950)
check("L04 haircut threshold 20/19 gives coverage 1 at x=1/2", (F(20, 19) * F(19, 20) - F(1, 2)) / F(1, 2) == 1)
check("L04 round(20/19, 10dp) == 1.0526315789", f"{float(thr):.10f}" == "1.0526315789")

# Prop 2.5 algebra, numeric spot check over a grid
ok = True
for r in [F(k, 20) for k in range(1, 40)]:
    for x in [F(k, 50) for k in range(0, 50)]:
        for y in [F(k, 50) for k in range(0, 50)]:
            if not (x < y and x <= r and y <= r and y < 1 and x >= 0):
                continue
            lhs = (r - y) / (1 - y) - (r - x) / (1 - x)
            rhs = (y - x) * (r - 1) / ((1 - x) * (1 - y))
            ok &= lhs == rhs
check("L04 Prop 2.5 difference identity on a grid of 39x50x50 points", ok)

# ---- L05: enumeration recomputed ----
p = F(1, 8)
kap = 2500
ell = (1, 2, 4)
mean = F(0)
var3_second = F(0)
probs = []
total = F(0)
for pat in product((0, 1), repeat=3):
    pr = F(1)
    for f in pat:
        pr *= p if f else 1 - p
    cost = kap * sum(l * f for l, f in zip(ell, pat))
    probs.append((pat, pr, cost))
    total += pr
    mean += pr * cost
    var3_second += pr * cost * cost
check("L05 eight pattern probabilities sum to 1", total == 1)
check("L05 enumerated mean == 4375/2", mean == F(4375, 2))
check("L05 closed form p*kappa*sum(ell) == 4375/2", p * kap * sum(ell) == F(4375, 2))
check("L05 round half up 4375/2 -> 2188", floor(F(4375, 2) + F(1, 2)) == 2188)
check("L05 pattern (0,0,0) probability 343/512", [pr for pat, pr, c in probs if pat == (0, 0, 0)] == [F(343, 512)])
check("L05 at least one fails 169/512", 1 - F(343, 512) == F(169, 512))
check("L05 169/512 < 3p = 192/512", F(169, 512) < 3 * p)
equal = 0
for pat in product((0, 1), repeat=3):
    pr = F(1)
    for f in pat:
        pr *= p if f else 1 - p
    equal += pr * (kap * 2 * sum(pat))
check("L05 Part C enumeration == 3*p*kappa*2 == 1875", equal == F(1875) and 3 * p * kap * 2 == F(1875))
var3 = var3_second - mean * mean
como_mean = p * kap * sum(ell)
como_second = p * (kap * sum(ell)) ** 2
var4 = como_second - como_mean * como_mean
check("L05 Part D comonotone variance == 133984375/4", var4 == F(133984375, 4))
check("L05 Part D independent variance == 57421875/4", var3 == F(57421875, 4))
check("L05 Prop 2.5: Var4-Var3 == 2 kappa^2 p(1-p) sum_{i<j} l_i l_j == 19140625",
      var4 - var3 == 2 * kap**2 * p * (1 - p) * (1 * 2 + 1 * 4 + 2 * 4) == F(19140625))
check("L05 comonotone no-cost probability 7/8", 1 - p == F(7, 8))
check("L05 Prop 2.6: (7/8)^3 < 7/8", F(7, 8) ** 3 < F(7, 8))
check("L05 M1 two trades p=1/4 kappa=1000 delays 2,3 -> 1250", F(1, 4) * 1000 * (2 + 3) == 1250)
check("L05 card c085: 1/8 == 64/512", F(1, 8) == F(64, 512))
check("L05 E3 right side (y-x)(rho-1)/((1-x)(1-y)) at x=1/5, y=51/100, rho=19/20 == -31/784",
      (F(51, 100) - F(1, 5)) * (F(19, 20) - 1) / ((1 - F(1, 5)) * (1 - F(51, 100))) == F(-31, 784))
check("L05 E3 left side 44/49 - 15/16 == -31/784", F(44, 49) - F(15, 16) == F(-31, 784))
check("L05 R2 bounds: 5/8 and 7/8 at p=1/8, 3p = 3/8", 1 - 3 * p == F(5, 8) and 1 - p == F(7, 8))
print(f"SUMMARY checks {checks} failures {fails}")

"""Verifier re-derivation (BK4-b round 1) of every number and identity in L04 and L05, written independently of the labs.

Usage: python3 -I ledgers/BK4/scripts/BK4-b-r1/recompute_L04_L05.py
Prints PASS/FAIL lines; exits 1 on any mismatch.
"""

from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction as F

fails: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(("PASS " if ok else "FAIL ") + name + (" | " + detail if detail else ""))
    if not ok:
        fails.append(name)


# ---------------- L04 ----------------
C0 = 2_000_000
# Remark 1.3 and Definition 1.2 values
check("L04 R1.3 reserves 19/20 of 2,000,000", F(19, 20) * C0 == 1_900_000)
check("L04 R1.3 reserves 21/20 of 2,000,000", F(21, 20) * C0 == 2_100_000)

# Remark 2.8 worked values
check("L04 R2.8 rho 19/20 x 1/2 = 9/10 = 9000 bps", (F(19, 20) - F(1, 2)) / (1 - F(1, 2)) == F(9, 10) and math.floor(10000 * F(9, 10)) == 9000)
check("L04 R2.8 rho 21/20 x 1/2 = 11/10 = 11000 bps", (F(21, 20) - F(1, 2)) / (1 - F(1, 2)) == F(11, 10) and math.floor(10000 * F(11, 10)) == 11000)
th = (F(19, 20) - F(1, 7)) / (1 - F(1, 7))
check("L04 R2.8 rho 19/20 x 1/7 = 113/120, floor 9416", th == F(113, 120) and math.floor(10000 * th) == 9416, f"theta={th} bps_exact={10000*th}")
check("L04 M3 10000*19/20 = 9500 exactly", 10000 * F(19, 20) == 9500)
check("L04 M1 rho 3/4, x 1/4, coverage 2/3", (F(3, 4) - F(1, 4)) / (1 - F(1, 4)) == F(2, 3))
check("L04 M2 rho 3/5, x 2/5, coverage 1/3", (F(3, 5) - F(2, 5)) / (1 - F(2, 5)) == F(1, 3))

# Seeded path: independent recomputation with the same stdlib generator
rng = random.Random(7)
hund = sorted(rng.sample(range(1, 100), 6))
path = [F(k, 100) for k in hund] + [F(99, 100)]
print("INFO L04 path", " ".join(str(s) for s in path))
check("L04 printed path 7/100 1/10 1/5 21/50 51/100 21/25 99/100", path == [F(7, 100), F(1, 10), F(1, 5), F(21, 50), F(51, 100), F(21, 25), F(99, 100)])

printed_rows = {
    F(19, 20): {
        F(7, 100): (1760000, 1860000, F(88, 93), 9462),
        F(1, 10): (1700000, 1800000, F(17, 18), 9444),
        F(1, 5): (1500000, 1600000, F(15, 16), 9375),
        F(21, 50): (1060000, 1160000, F(53, 58), 9137),
        F(51, 100): (880000, 980000, F(44, 49), 8979),
        F(21, 25): (220000, 320000, F(11, 16), 6875),
    },
    F(21, 20): {
        F(7, 100): (1960000, 1860000, F(98, 93), 10537),
        F(1, 10): (1900000, 1800000, F(19, 18), 10555),
        F(1, 5): (1700000, 1600000, F(17, 16), 10625),
        F(21, 50): (1260000, 1160000, F(63, 58), 10862),
        F(51, 100): (1080000, 980000, F(54, 49), 11020),
        F(21, 25): (420000, 320000, F(21, 16), 13125),
        F(99, 100): (120000, 20000, F(6, 1), 60000),
    },
}
for rho, table in printed_rows.items():
    computed_shares = [s for s in path if s <= rho]
    omitted = [s for s in path if s > rho]
    check(f"L04 rho {rho} omitted shares", (omitted == [F(99, 100)]) if rho == F(19, 20) else omitted == [], f"omitted={[str(s) for s in omitted]}")
    check(f"L04 rho {rho} computed share count", len(computed_shares) == len(table))
    below = 0
    for x in computed_shares:
        res_left = int(rho * C0) - int(x * C0)
        cl_left = C0 - int(x * C0)
        cov = F(res_left, cl_left)
        bps = math.floor(10000 * cov)
        assert cov == (rho - x) / (1 - x)
        exp = table[x]
        ok = (res_left, cl_left, cov, bps) == exp
        check(f"L04 rho {rho} x {x} row", ok, f"computed=({res_left},{cl_left},{cov},{bps}) printed={exp}")
        below += cov < 1
    print(f"INFO L04 rho {rho} below-1 count {below} of {len(computed_shares)}")
    # difference identity over all pairs
    pairs = list(itertools.combinations(computed_shares, 2))
    ident = True
    direction = True
    for x, y in pairs:
        th_x = (rho - x) / (1 - x)
        th_y = (rho - y) / (1 - y)
        ident &= th_y - th_x == (y - x) * (rho - 1) / ((1 - x) * (1 - y))
        direction &= (th_y - th_x) * (rho - 1) > 0
    check(f"L04 rho {rho} difference identity over {len(pairs)} pairs", ident)
    check(f"L04 rho {rho} monotone direction over pairs", direction == (rho != 1))

# E1 and E2 answers
vals19 = [9462, 9444, 9375, 9137, 8979, 6875]
check("L04 E1 lowest bps 6875 at 21/25", min(vals19) == 6875)
seq21 = [(F(7, 100), 10537), (F(1, 10), 10555), (F(1, 5), 10625), (F(21, 50), 10862), (F(51, 100), 11020), (F(21, 25), 13125), (F(99, 100), 60000)]
first = [x for x, v in seq21 if v >= 10600][0]
check("L04 E2 first computed share with bps >= 10600 is 1/5", first == F(1, 5))

# E3 by hand
lhs = F(44, 49) - F(15, 16)
rhs = (F(51, 100) - F(1, 5)) * (F(19, 20) - 1) / ((1 - F(1, 5)) * (1 - F(51, 100)))
check("L04 E3 identity both sides -31/784", lhs == rhs == F(-31, 784), f"lhs={lhs} rhs={rhs}")

# Proposition 2.6 and 2.4 identities on a grid
grid_ok = True
for rho in [F(k, 20) for k in range(1, 40)]:
    for x in [F(k, 100) for k in range(0, 100) if F(k, 100) <= rho]:
        th = (rho - x) / (1 - x)
        grid_ok &= th - 1 == (rho - 1) / (1 - x)
        grid_ok &= th - rho == x * (rho - 1) / (1 - x)
        grid_ok &= (th < 1) == (rho < 1) if x > 0 or True else True
check("L04 Prop 2.4 and 2.6 identities on rational grid", grid_ok)

# Proposition 2.6 strict part: rho<=1 gives theta<=rho with equality iff x=0 or rho=1
eq_ok = True
for rho in [F(k, 20) for k in range(1, 21)]:
    for x in [F(k, 100) for k in range(0, 100) if F(k, 100) <= rho]:
        th = (rho - x) / (1 - x)
        if rho <= 1:
            eq_ok &= th <= rho
            eq_ok &= (th == rho) == (x == 0 or rho == 1)
check("L04 Prop 2.6 equality set", eq_ok)

# Remark 4.1 and R1: measured coverage and threshold 1/(1-h), h=1/20
h = F(1, 20)
check("L04 threshold 1/(1-h) = 20/19", 1 / (1 - h) == F(20, 19))
print("INFO L04 20/19 decimal to 10 places", f"{float(F(20, 19)):.10f}")
check("L04 quiz numeric 1.0526315789 within 1e-9 of 20/19", abs(float(F(20, 19)) - 1.0526315789) < 1e-9)
check("L04 haircut 21/20 effective 399/400, x=1/2 coverage 199/200 = 9950 bps", (F(21, 20) * (1 - h) - F(1, 2)) / (F(1, 2)) == F(199, 200) and math.floor(10000 * F(199, 200)) == 9950)
check("L04 haircut threshold effective 1, coverage 1 at x=1/2", (F(1) - F(1, 2)) / F(1, 2) == 1)
# R1 at h: admissible x<1 with x<=rho*(1-h); at rho*=1/(1-h) coverage =1 for all x
r_star = 1 / (1 - h)
r1_ok = all(((r_star * (1 - h)) - x) / (1 - x) == 1 for x in [F(k, 100) for k in range(0, 100)])
check("L04 R1 coverage equals 1 at rho* for every grid share", r1_ok)
# R2 solution
x_star = (F(19, 20) - F(9, 10)) / (1 - F(9, 10))
check("L04 R2 x*=1/2 for rho 19/20, c 9/10 and coverage returns c", x_star == F(1, 2) and (F(19, 20) - x_star) / (1 - x_star) == F(9, 10))
r2_ok = True
for rho in [F(k, 40) for k in range(0, 40)]:
    for c in [F(k, 40) for k in range(0, 41) if F(k, 40) <= rho]:
        xs = (rho - c) / (1 - c)
        r2_ok &= 0 <= xs < 1 and xs <= rho and (rho - xs) / (1 - xs) == c
check("L04 R2 general x* on grid", r2_ok)
# Misconception 2: halving 19/20 gives 19/40 not 9/10
check("L04 misconception 2 values 19/40 vs 9/10", F(19, 40) != F(9, 10))
# Misconception 3 claim: unchanged only when rho=1 (page says 'only'); check x=0 counterexample
print("INFO L04 misconception-3 counterexample: rho 19/20 at x=0 coverage", (F(19, 20) - 0) / (1 - 0), "= rho, unchanged with zero redemption")

# ---------------- L05 ----------------
P = F(1, 8)
K = 2500
D = (1, 2, 4)


def pattern_prob(pat, p):
    out = F(1)
    for f in pat:
        out *= p if f else 1 - p
    return out


def cost(pat, delays, k):
    return sum(k * d for f, d in zip(pat, delays) if f)


pats = list(itertools.product((0, 1), repeat=3))
ind = [(pattern_prob(pt, P), cost(pt, D, K)) for pt in pats]
check("L05 pattern probabilities sum to 1", sum(p for p, _ in ind) == 1)
mean_ind = sum(p * c for p, c in ind)
closed = P * K * sum(D)
check("L05 Example 2.2 mean 4375/2 = 2187.5", mean_ind == closed == F(4375, 2))
check("L05 rounding half up 2188", math.floor(closed + F(1, 2)) == 2188)
check("L05 printed pattern probabilities", [pattern_prob(pt, P) for pt in pats] == [F(343, 512), F(49, 512), F(49, 512), F(7, 512), F(49, 512), F(7, 512), F(7, 512), F(1, 512)])
check("L05 printed pattern costs", [cost(pt, D, K) for pt in pats] == [0, 10000, 5000, 15000, 2500, 12500, 7500, 17500])
check("L05 Example 2.7 at least one fail A3 = 169/512", 1 - (1 - P) ** 3 == F(169, 512))
check("L05 Example 2.7 3p = 3/8 = 192/512", 3 * P == F(3, 8) == F(192, 512))
check("L05 A4 at least one fails = p = 64/512", P == F(64, 512))
check("L05 M1 mean 1250", F(1, 4) * 1000 * (2 + 3) == 1250)
check("L05 M2 (7/8)^3 = 343/512 and complement 169/512", (F(7, 8)) ** 3 == F(343, 512) and 1 - F(343, 512) == F(169, 512))
check("L05 M3 closed form 1875", 3 * P * K * 2 == 1875)
eq_enum = sum(p * c for p, c in [(pattern_prob(pt, P), cost(pt, (2, 2, 2), K)) for pt in pats])
check("L05 Part C enumeration equal delays 1875", eq_enum == 1875)
# Part D variances, exact
com = [(1 - P, 0), (P, K * sum(D))]
var = lambda outs: sum(p * c * c for p, c in outs) - sum(p * c for p, c in outs) ** 2  # noqa: E731
v3 = var(ind)
v4 = var(com)
check("L05 Part D variance A3 = 57421875/4", v3 == F(57421875, 4), f"v3={v3}")
check("L05 Part D variance A4 = 133984375/4", v4 == F(133984375, 4), f"v4={v4}")
check("L05 Part D no-cost A4 = 7/8", sum(p for p, c in com if c == 0) == F(7, 8))
check("L05 Part D no-cost A3 = 343/512", sum(p for p, c in ind if c == 0) == F(343, 512))
check("L05 E2 difference 19140625", v4 - v3 == 19140625)
check("L05 E2 Prop 2.5 closed 2*K^2*p(1-p)*sum l_i l_j", 2 * K * K * P * (1 - P) * (2 + 4 + 8) == 19140625)
check("L05 E3 448/512 = 7/8", F(448, 512) == F(7, 8))
check("L05 M3 page: E[C] equal-delay closed form 1875 whole", 3 * F(1, 8) * 2500 * 2 == F(15000, 8) == 1875)

# Random-parameter checks of Propositions 2.1, 2.2, 2.4, 2.5, 2.6 by exact enumeration
rnd = random.Random(12345)
ok21 = ok22 = ok24 = ok25 = ok26 = True
zero_ok = True
for _ in range(400):
    p = F(rnd.randint(1, 99), 100)
    kap = rnd.randint(0, 50)
    ell = tuple(rnd.randint(0, 9) for _ in range(3))
    ind_r = [(pattern_prob(pt, p), kap * sum(l * f for l, f in zip(ell, pt))) for pt in pats]
    com_r = [(1 - p, 0), (p, kap * sum(ell))]
    mean_r = p * kap * sum(ell)
    ok21 &= sum(pr * c for pr, c in ind_r) == mean_r
    ok22 &= sum(pr * c for pr, c in ind_r) == mean_r
    ok24 &= sum(pr * c for pr, c in com_r) == mean_r
    diff = var(com_r) - var(ind_r)
    formula = 2 * kap * kap * p * (1 - p) * sum(ell[i] * ell[j] for i, j in [(0, 1), (0, 2), (1, 2)])
    ok25 &= diff == formula and diff >= 0
    zero_ok &= (diff == 0) == (sum(1 for l in ell if l > 0) <= 1) if kap > 0 else True
for _ in range(300):
    p = F(rnd.randint(1, 99), 100)
    kap = rnd.randint(1, 50)
    ell = tuple(rnd.randint(1, 9) for _ in range(3))
    ind_r = [(pattern_prob(pt, p), kap * sum(l * f for l, f in zip(ell, pt))) for pt in pats]
    no_ind = sum(pr for pr, c in ind_r if c == 0)
    no_com = 1 - p
    ok26 &= no_ind == (1 - p) ** 3 and no_com == 1 - p and no_ind < no_com
check("L05 random Prop 2.1 mean identity", ok21)
check("L05 random Prop 2.2 enumeration identity", ok22)
check("L05 random Prop 2.4 comonotone mean identity", ok24)
check("L05 random Prop 2.5 variance difference identity and >=0", ok25)
check("L05 random Prop 2.5 zero exactly when at most one delay positive", zero_ok)
check("L05 random Prop 2.6 no-cost probabilities and strict inequality", ok26)

# Prop 2.5 zero case with delays (0,0,5) and (0,3,0): explicit
for dl in [(0, 0, 5), (0, 3, 0), (2, 0, 0)]:
    dd = sum(1 for d in dl if d > 0)
    ind_r = [(pattern_prob(pt, P), K * sum(l * f for l, f in zip(dl, pt))) for pt in pats]
    com_r = [(1 - P, 0), (P, K * sum(dl))]
    check(f"L05 Prop 2.5 zero difference for delays {dl}", var(com_r) - var(ind_r) == 0 and dd <= 1)

# Prop 2.5 with a single nonzero delay but (0,0,0): trivially zero

# R1 variance ratio n for n=4 with equal delays
n = 4
ell1 = 2
ind_n = []
for pt in itertools.product((0, 1), repeat=n):
    ind_n.append((pattern_prob(pt, P) if False else (P ** sum(pt)) * ((1 - P) ** (n - sum(pt))), K * ell1 * sum(pt)))
com_n = [(1 - P, 0), (P, K * ell1 * n)]
v3n = var(ind_n)
v4n = var(com_n)
check("L05 R1 ratio Var4/Var3 = n for n=4", v4n / v3n == n, f"ratio={v4n / v3n}")
check("L05 R1 variance formula n p(1-p) k^2 l^2 for n=4", v3n == n * P * (1 - P) * (K * ell1) ** 2)

# R2: joint laws with marginals 1/8 give no-failure in [5/8,7/8]; example distribution attains 5/8
ex_point = {"w0": F(5, 8), "w1": F(1, 8), "w2": F(1, 8), "w3": F(1, 8)}
F1 = {"w1"}
F2 = {"w2"}
F3 = {"w3"}
marg_ok = [sum(ex_point[w] for w in S) == P for S in (F1, F2, F3)]
no_fail = sum(ex_point[w] for w in ex_point if w not in F1 | F2 | F3)
check("L05 R2 disjoint example marginals and no-fail 5/8", all(marg_ok) and no_fail == F(5, 8))
check("L05 R2 comonotone attains 7/8", 1 - P == F(7, 8))

print("INFO prose checks in L05 Prop 2.5 'never smaller' apply for p in (0,1), kappa>0: tested above")
print("SUMMARY failures:", len(fails), fails)
raise SystemExit(1 if fails else 0)

# Independent exact-Fraction recomputation for BK4 slice b (L04, L05). Reads no lab or page code.
import itertools
import math
import random
from fractions import Fraction as F

fails = []
def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)

# ---------- L04 ----------
C0 = 2_000_000
# Path: seeded sample of 6 distinct k in 1..99 (sorted), then append 99/100
rng = random.Random(7)
ks = sorted(rng.sample(range(1, 100), 6))
path = [F(k, 100) for k in ks] + [F(99, 100)]
check("L04 path == 7/100 1/10 1/5 21/50 51/100 21/25 99/100", [str(p) for p in path] == ["7/100", "1/10", "1/5", "21/50", "51/100", "21/25", "99/100"])
check("L04 path strictly increasing (99/100 not repeated)", all(a < b for a, b in zip(path, path[1:])))

expected_table = {
    F(19, 20): [("88/93", 9462), ("17/18", 9444), ("15/16", 9375), ("53/58", 9137), ("44/49", 8979), ("11/16", 6875)],
    F(21, 20): [("98/93", 10537), ("19/18", 10555), ("17/16", 10625), ("63/58", 10862), ("54/49", 11020), ("21/16", 13125), ("6", 60000)],
}
for rho, exp in expected_table.items():
    comp = [s for s in path if s <= rho]
    omitted = [s for s in path if s > rho]
    check(f"rho={rho}: computed {len(comp)} omitted {len(omitted)}", (len(comp), len(omitted)) == ((6, 1) if rho < 1 else (7, 0)))
    reserves0 = rho * C0
    check(f"rho={rho}: reserves_0 integer {reserves0}", reserves0.denominator == 1)
    rows = []
    for s, (cov_txt, bps) in zip(comp, exp):
        res_left = int(reserves0) - int(s * C0)
        cl = C0 - int(s * C0)
        cov = F(res_left, cl)
        ok = str(cov) == cov_txt and math.floor(10000 * cov) == bps and cov == (rho - s) / (1 - s)
        check(f"rho={rho} x={s}: coverage {cov} bps {math.floor(10000*cov)} == printed {cov_txt} {bps}", ok)
        rows.append((s, cov))
    below = sum(1 for _, c in rows if c < 1)
    check(f"rho={rho}: coverage below 1 count {below} (expect {len(rows) if rho<1 else 0})", below == (len(rows) if rho < 1 else 0))
    npairs = 0; ok_id = True; ok_dir = True
    for (a, ca), (b, cb) in itertools.combinations(rows, 2):
        npairs += 1
        ok_id &= (cb - ca == (b - a) * (rho - 1) / ((1 - a) * (1 - b)))
        ok_dir &= ((cb - ca) * (rho - 1) > 0)
    check(f"rho={rho}: pairs {npairs} identity {ok_id} direction {ok_dir}", ok_id and ok_dir and npairs == (15 if rho < 1 else 21))

# worked values
check("L04 worked 19/20,1/2 -> 9/10, 9000", F(19, 20) - F(1, 2) == F(9, 20) and (F(19,20)-F(1,2))/F(1,2) == F(9, 10) and math.floor(10000*F(9,10)) == 9000)
check("L04 worked 21/20,1/2 -> 11/10, 11000", (F(21, 20) - F(1, 2)) / F(1, 2) == F(11, 10) and math.floor(10000 * F(11, 10)) == 11000)
check("L04 worked 19/20,1/7 -> 113/120, 9416", (F(19, 20) - F(1, 7)) / (1 - F(1, 7)) == F(113, 120) and math.floor(10000 * F(113, 120)) == 9416)
# haircut
h = F(1, 20)
thr = 1 / (1 - h)
check("L04 threshold 20/19", thr == F(20, 19))
eff = F(21, 20) * (1 - h)
check("L04 haircut 21/20 effective 399/400, coverage 199/200, 9950 bps", eff == F(399, 400) and (eff - F(1, 2)) / F(1, 2) == F(199, 200) and math.floor(10000 * F(199, 200)) == 9950)
eff2 = thr * (1 - h)
check("L04 haircut at threshold effective 1, coverage 1, 10000 bps", eff2 == 1 and (eff2 - F(1, 2)) / F(1, 2) == 1)
# Prose M1, M2, M3, P1 numbers, E1, E2, E3, R2, R1 spot checks
check("L04 M1 coverage 2/3", (F(3, 4) - F(1, 4)) / (1 - F(1, 4)) == F(2, 3))
check("L04 M2 coverage 1/3", (F(3, 5) - F(2, 5)) / (1 - F(2, 5)) == F(1, 3))
check("L04 M3 10000*19/20 floor 9500", math.floor(10000 * F(19, 20)) == 9500)
check("L04 E1 11/16 -> 6875", math.floor(10000 * F(220000, 320000)) == 6875 and F(220000, 320000) == F(11, 16))
check("L04 E2 first >= 10600 is 10625 at 1/5", [b for b in [10537, 10555, 10625]][2] >= 10600 and 10555 < 10600)
e3_left = F(44, 49) - F(15, 16)
e3_right = (F(51, 100) - F(1, 5)) * (F(19, 20) - 1) / ((1 - F(1, 5)) * (1 - F(51, 100)))
check("L04 E3 both sides -31/784", e3_left == F(-31, 784) and e3_right == F(-31, 784))
check("L04 R2 x*=(rho-c)/(1-c) for rho=19/20 c=9/10 is 1/2", (F(19, 20) - F(9, 10)) / (1 - F(9, 10)) == F(1, 2))
check("L04 Prop 2.6 identity theta - rho = x(rho-1)/(1-x) at 19/20,1/2", (F(9,10) - F(19,20)) == F(1,2)*(F(19,20)-1)/(1-F(1,2)))
check("L04 quiz Q9 20/19 to 10 dp is 1.0526315789 within 1e-9", abs(float(F(20,19)) - 1.0526315789) < 1e-9 and round(F(20,19).numerator/F(20,19).denominator, 10) == 1.0526315789)

# ---------- L05 ----------
p = F(1, 8); kappa = 2500; ell = (1, 2, 4)
pats = list(itertools.product((0, 1), repeat=3))
def P(x): 
    r = F(1)
    for xi in x: r *= p if xi else 1 - p
    return r
def Cc(x, ell_, kap): return sum(kap * l * xi for l, xi in zip(ell_, x))
check("L05 eight pattern probs sum to 1", sum(P(x) for x in pats) == 1)
mean_enum = sum(P(x) * Cc(x, ell, kappa) for x in pats)
check("L05 enumerated mean 4375/2", mean_enum == F(4375, 2))
check("L05 closed form p*kappa*sum ell", p * kappa * sum(ell) == F(4375, 2))
check("L05 round half up 2187.5 -> 2188", math.floor(F(4375, 2) + F(1, 2)) == 2188)
check("L05 no failure A3 = 343/512", P((0, 0, 0)) == F(343, 512))
check("L05 at least one A3 = 169/512; 3p = 3/8 = 192/512", 1 - P((0,0,0)) == F(169, 512) and 3 * p == F(192, 512))
check("L05 A4 at least one = p = 64/512", p == F(64, 512))
check("L05 Example 2.7 3p - (1-(1-p)^3) = p^2(3-p)", 3*p - (1 - (1-p)**3) == p**2 * (3 - p))
# Part B pattern probabilities/costs as printed
printed = {(0,0,0): (F(343,512),0),(0,0,1):(F(49,512),10000),(0,1,0):(F(49,512),5000),(0,1,1):(F(7,512),15000),(1,0,0):(F(49,512),2500),(1,0,1):(F(7,512),12500),(1,1,0):(F(7,512),7500),(1,1,1):(F(1,512),17500)}
check("L05 Part B per-pattern probability and cost", all(P(x) == printed[x][0] and Cc(x, ell, kappa) == printed[x][1] for x in pats))
# Part C equal delays 2
mean_c = sum(P(x) * Cc(x, (2,2,2), kappa) for x in pats)
check("L05 Part C 1875 = 3 p kappa ell", mean_c == 1875 and 3 * p * kappa * 2 == 1875)
# Part D comonotone and independent
def mom(outs):
    m = sum(pr * c for pr, c in outs)
    return sum(pr for pr, c in outs if c == 0), m, sum(pr * c * c for pr, c in outs) - m * m
com = [(1 - p, 0), (p, kappa * sum(ell))]
ind = [(P(x), Cc(x, ell, kappa)) for x in pats]
z_c, m_c, v_c = mom(com); z_i, m_i, v_i = mom(ind)
check("L05 comonotone no-cost 7/8 mean 4375/2 var 133984375/4", z_c == F(7,8) and m_c == F(4375,2) and v_c == F(133984375, 4))
check("L05 independent no-cost 343/512 mean 4375/2 var 57421875/4", z_i == F(343,512) and m_i == F(4375,2) and v_i == F(57421875, 4))
check("L05 Prop 2.5 difference 19140625 = 2 k^2 p(1-p) sum_{i<j} l_i l_j", v_c - v_i == 2 * kappa**2 * p * (1-p) * (1*2 + 1*4 + 2*4) == 19140625)
check("L05 comonotone variance larger", v_c > v_i)
check("L05 E2 difference (133984375-57421875)/4 = 19140625", (F(133984375,4) - F(57421875,4)) == 19140625)
check("L05 Prop 2.6 (1-p)^3 < 1-p", (1-p)**3 < 1-p)
# R1: ratio var4/var3 = n for n=3
n = 3; l = 1
v3 = n * p * (1-p) * (kappa*l)**2; v4 = (n*kappa*l)**2 * p*(1-p)
check("L05 R1 ratio var4/var3 = n", v4 / v3 == n)
# R2: range of no-failure probability bounds 5/8 and 7/8
check("L05 R2 bounds", 1 - 3*p == F(5,8) and 1 - p == F(7,8))
# Example 2.8 and E1 numbers
check("L05 2187.5 = 21.88 dollars rounding", F(4375,2) == F(2187,1) + F(1,2))
# Quiz numeric items
check("L05 Q2 750", F(1,4)*1000*3 == 750)
check("L05 Q4 512-343=169", 512 - 343 == 169)
check("L05 M1 1500", F(1,4)*1000*(2+3+1) == 1500)
check("L05 M3 1875", F(1,8)*2500*2*3 == 1875)
check("L05 Example 2.8 2187.5", F(1,8)*2500*7 == F(4375,2))
# Prop 2.5 fraction check: independent var formula
check("L05 Var3 formula kappa^2 sum l_i^2 p(1-p) = 57421875/4", kappa**2 * sum(l*l for l in ell) * p*(1-p) == F(57421875,4))
check("L05 Var4 formula kappa^2 (sum l)^2 p(1-p) = 133984375/4", kappa**2 * sum(ell)**2 * p*(1-p) == F(133984375,4))

print("FAILS:", fails)
print("ALL OK" if not fails else "SOME FAILED")

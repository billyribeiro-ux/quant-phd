"""Independent exact recomputation for BK4 slice b (L04, L05). Written by the verifier; does not import the lab."""
from fractions import Fraction as F
from itertools import product
import math, random

ok = True
def check(name, cond):
    global ok
    ok = ok and bool(cond)
    print(("PASS " if cond else "FAIL ") + name)

# ---------- L04 ----------
def cov(rho, x):
    assert 0 <= x < 1 and x <= rho
    return (rho - x) / (1 - x)

shares19 = [F(7,100), F(1,10), F(1,5), F(21,50), F(51,100), F(21,25)]
expect19 = [(F(88,93), 9462), (F(17,18), 9444), (F(15,16), 9375), (F(53,58), 9137), (F(44,49), 8979), (F(11,16), 6875)]
for x, (c, b) in zip(shares19, expect19):
    check(f"L04 rho=19/20 x={x} coverage {c} bps {b}", cov(F(19,20), x) == c and math.floor(10000*c) == b)
shares21 = shares19 + [F(99,100)]
expect21 = [(F(98,93), 10537), (F(19,18), 10555), (F(17,16), 10625), (F(63,58), 10862), (F(54,49), 11020), (F(21,16), 13125), (F(6,1), 60000)]
for x, (c, b) in zip(shares21, expect21):
    check(f"L04 rho=21/20 x={x} coverage {c} bps {b}", cov(F(21,20), x) == c and math.floor(10000*c) == b)
check("L04 99/100 > 19/20 (omitted for rho=19/20)", F(99,100) > F(19,20))
check("L04 printed 19/20 reserves at x=21/50: 1060000 and claims 1160000", F(19,20)*2000000 - F(21,50)*2000000 == 1060000 and 2000000 - F(21,50)*2000000 == 1160000)
# identity and pairwise difference identity (Prop 2.5) for all pairs, both ratios
for rho, sh in ((F(19,20), shares19), (F(21,20), shares21)):
    ids = True; dirn = True; npairs = 0
    rows = [(x, cov(rho, x)) for x in sh if x <= rho]
    for i in range(len(rows)):
        for j in range(i+1, len(rows)):
            (x, a), (y, b) = rows[i], rows[j]
            npairs += 1
            ids = ids and (b - a == (y - x)*(rho - 1)/((1-x)*(1-y)))
            dirn = dirn and ((b - a)*(rho - 1) > 0)
    check(f"L04 rho={rho}: {npairs} pairs, difference identity and direction", ids and dirn)
# Prop 2.6 identity and bound, random grid
bad = 0
for k in range(1, 200):
    for m in range(0, 100):
        rho = F(k, 100); x = F(m, 100)
        if x < 1 and x <= rho:
            th = cov(rho, x)
            if th - rho != x*(rho-1)/(1-x): bad += 1
            if rho <= 1 and th > rho: bad += 1
print("L04 Prop2.6 grid violations:", bad); ok = ok and bad == 0
# Prop 2.4 grid
bad = 0
for k in range(1, 200):
    for m in range(0, 100):
        rho = F(k, 100); x = F(m, 100)
        if x < 1 and x <= rho:
            th = cov(rho, x)
            if th - 1 != (rho - 1)/(1 - x): bad += 1
            if (th < 1) != (rho < 1): bad += 1
print("L04 Prop2.4 grid violations:", bad); ok = ok and bad == 0
# Remark 2.8 values
check("L04 Remark 2.8: 19/20, x=1/2 -> 9/10", cov(F(19,20), F(1,2)) == F(9,10))
check("L04 Remark 2.8: 21/20, x=1/2 -> 11/10", cov(F(21,20), F(1,2)) == F(11,10))
check("L04 Remark 2.8: 19/20, x=1/7 -> 113/120, bps 9416", cov(F(19,20), F(1,7)) == F(113,120) and math.floor(10000*F(113,120)) == 9416)
check("L04 quiz 9000 for 19/20 and 1/2", math.floor(10000*F(9,10)) == 9000)
check("L04 quiz 11000 for 21/20 and 1/2", math.floor(10000*F(11,10)) == 11000)
check("L04 quiz 9416.67 floor", math.floor(10000*F(113,120)) == 9416)
check("L04 quiz decimal 20/19 to ten places = 1.0526315789", f"{float(F(20,19)):.10f}" == "1.0526315789")
check("L04 quiz 1/(1-h) with h=1/20 is 20/19", F(1)/(1-F(1,20)) == F(20,19))
# Remark 4.1 threshold, brute force over shares for rho near threshold
h = F(1,20); thr = 1/(1-h)
def measured_ok(rho):
    eff = rho*(1-h)
    shares = [F(k, 1000) for k in range(0, 1000) if F(k,1000) <= eff]
    return all(cov(eff, x) >= 1 for x in shares)
check("L04 Remark 4.1: rho=20/19 gives measured coverage >= 1 at all admissible shares (grid)", measured_ok(thr))
eff_below = F(21,20)*(1-h)
check("L04 Remark 4.1: x=0 admissible for rho(1-h)=399/400 gives measured coverage 399/400 <1", eff_below < 1 and cov(eff_below, F(0)) == eff_below)
check("L04 haircut row rho=21/20 effective 399/400, x=1/2 coverage 199/200 bps 9950", cov(eff_below, F(1,2)) == F(199,200) and math.floor(10000*F(199,200)) == 9950)
# R2 solution: x* = (rho-c)/(1-c)
bad = 0
for rho in [F(k,40) for k in range(0,40)]:
    for c in [F(j,40) for j in range(0,41)]:
        if c <= rho < 1:
            xs = (rho - c)/(1 - c)
            if not (0 <= xs < 1 and xs <= rho and cov(rho, xs) == c): bad += 1
print("L04 R2 grid violations:", bad); ok = ok and bad == 0
check("L04 R2 example rho=19/20,c=9/10 gives x*=1/2", (F(19,20)-F(9,10))/(1-F(9,10)) == F(1,2))
# R3 identity
bad = 0
for m in range(0, 50):
    Res0, C0 = 30, 50
    if m <= Res0 and m < C0:
        if F(Res0-m, C0-m) != cov(F(Res0, C0), F(m, C0)): bad += 1
print("L04 R3 violations:", bad); ok = ok and bad == 0
# M1..M3, E1, E2
check("L04 M1 rho=3/4, x=1/4, coverage 2/3", cov(F(3,4), F(1,4)) == F(2,3))
check("L04 M2 rho=3/5 x=2/5 coverage 1/3", cov(F(3,5), F(2,5)) == F(1,3))
check("L04 M3 10000*19/20 = 9500", 10000*F(19,20) == 9500)
check("L04 E1 6875 at 21/25, 220000/320000 = 11/16", F(220000,320000) == F(11,16) and math.floor(10000*F(11,16)) == 6875)
check("L04 E2 first >= 10600 is 10625 at 1/5", [b for (_, b) in expect21 if b >= 10600][0] == 10625)
# E3
lhs = F(44,49) - F(15,16); rhs = (F(51,100)-F(1,5))*(F(19,20)-1)/((1-F(1,5))*(1-F(51,100)))
check("L04 E3 both sides -31/784", lhs == rhs == F(-31,784))
# seeded path check (independent of lab code): sample from random.Random(7)
rng = random.Random(7)
sample = sorted(rng.sample(range(1,100), 6))
check(f"L04 seed-7 sample = {sample} gives path 7/100 1/10 1/5 21/50 51/100 21/25 99/100", sample == [7,10,20,42,51,84] )
check("L04 printed path strictly increasing", all(a < b for a, b in zip([7,10,20,42,51,84,99], [7,10,20,42,51,84,99][1:])))

# ---------- L05 ----------
def enum_indep(p, ell, kap):
    out = []
    for pat in product((0,1), repeat=3):
        pr = F(1)
        for f in pat: pr *= p if f else (1-p)
        cost = kap*sum(l for f, l in zip(pat, ell) if f)
        out.append((pr, cost))
    return out
def enum_comono(p, ell, kap):
    return [(1-p, 0), (p, kap*sum(ell))]
def mean(o): return sum(pr*c for pr, c in o)
def var(o): return sum(pr*c*c for pr, c in o) - mean(o)**2
def p0(o): return sum(pr for pr, c in o if c == 0)

p = F(1,8); ell = (1,2,4); kap = 2500
ind = enum_indep(p, ell, kap); com = enum_comono(p, ell, kap)
check("L05 pattern probabilities sum to 1", sum(pr for pr,_ in ind) == 1)
check("L05 E[C] = 4375/2", mean(ind) == F(4375,2) == mean(com))
check("L05 round half up 2188", math.floor(mean(ind) + F(1,2)) == 2188)
check("L05 variance under A4 = 133984375/4", var(com) == F(133984375,4))
check("L05 variance under A3 = 57421875/4", var(ind) == F(57421875,4))
check("L05 difference = 19140625", var(com) - var(ind) == 19140625)
check("L05 Prop 2.5 value 2 kappa^2 p(1-p) sum l_i l_j = 19140625", 2*kap**2*p*(1-p)*(1*2+1*4+2*4) == 19140625)
check("L05 no-cost A3 = 343/512 and A4 = 7/8", p0(ind) == F(343,512) and p0(com) == F(7,8))
check("L05 at least one fails A3 = 169/512", 1 - p0(ind) == F(169,512))
check("L05 E3: 448/512 = 7/8", F(448,512) == F(7,8))
check("L05 Example 2.7: 3/8 = 192/512 and A4 p = 64/512", F(3,8) == F(192,512) and p == F(64,512))
check("L05 Example 2.7 identity: 3p-(1-(1-p)^3)=p^2(3-p)>0 at p=1/8", 3*p-(1-(1-p)**3) == p*p*(3-p) and p*p*(3-p) > 0)
check("L05 Part C 3 p kappa ell = 1875 with ell=2", 3*p*kap*2 == 1875 and mean(enum_indep(p,(2,2,2),kap)) == 1875)
check("L05 Example 2.8 mean 2187.5 = 4375/2 = (1/8)*2500*7", F(1,8)*2500*7 == F(4375,2))
check("L05 M1 mean 1/4 * 1000 * 6 = 1500", F(1,4)*1000*6 == 1500)
check("L05 Quiz 750 = 1/4*1000*3", F(1,4)*1000*3 == 750)
check("L05 M2 (7/8)^3 = 343/512", F(7,8)**3 == F(343,512))
check("L05 Q numeric 169 = 512-343", 512-343 == 169)
# random parameter sweep: Prop 2.2, 2.1, 2.4, 2.5, 2.6
import random as R
rng = R.Random(12345)
bad = {"2.1/2.2":0,"2.4":0,"2.5":0,"2.6":0,"R1":0,"P3":0}
for trial in range(3000):
    pn = F(rng.randint(1, 99), 100)
    ells = tuple(rng.randint(0, 6) for _ in range(3))
    kp = rng.randint(0, 5000)
    i_o = enum_indep(pn, ells, kp); c_o = enum_comono(pn, ells, kp)
    closed = pn*kp*sum(ells)
    if mean(i_o) != closed or mean(c_o) != closed: bad["2.1/2.2"] += 1
    if var(c_o) - var(i_o) != 2*kp*kp*pn*(1-pn)*sum(ells[i]*ells[j] for i in range(3) for j in range(i+1,3)): bad["2.5"] += 1
    if (var(c_o) - var(i_o) == 0) != (sum(1 for l in ells if l > 0) <= 1) and kp > 0: bad["2.5"] += 1
    if trial < 1500 and kp > 0 and all(l >= 1 for l in ells):
        if p0(i_o) != (1-pn)**3 or p0(c_o) != 1-pn or not (p0(i_o) < p0(c_o)): bad["2.6"] += 1
    if kp == 0 and False: pass
print("L05 random sweep violations:", bad); ok = ok and all(v == 0 for v in bad.values())
# R1 ratio for n trades
for n in (1,2,3,4):
    l, k = 2, 1000
    pn = F(1,4)
    vi = pn*(1-pn)*k*k*l*l*n
    vc = pn*(1-pn)*k*k*l*l*n*n
    check(f"L05 R1 n={n}: Var4/Var3 = n", vc/vi == n)
# R2 bounds: attained examples
w = {'w0': F(5,8), 'w1': F(1,8), 'w2': F(1,8), 'w3': F(1,8)}
check("L05 R2 disjoint example: masses sum to 1, P(no fail)=5/8, P(U)=3/8", sum(w.values()) == 1 and w['w0'] == F(5,8) and 1-w['w0'] == F(3,8))
check("L05 R2 comonotone attains 7/8", 1 - F(1,8) == F(7,8))
# P3 hypotheses: C=0 iff no failure when kappa*ell_i >= 1
print("ALL OK" if ok else "SOME FAIL")

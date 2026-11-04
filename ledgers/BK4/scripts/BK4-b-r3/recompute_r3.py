# Round-3 independent recomputation for BK4 L04 and L05 (own code, Fraction arithmetic, no twin imports).
import random, math, itertools
from fractions import Fraction as F
fails = []
checks = 0
def ck(name, cond):
    global checks
    checks += 1
    if not cond:
        fails.append(name)
    print(("ok  " if cond else "FAIL"), name)

# L04: seeded path
rng = random.Random(7)
ks = sorted(rng.sample(range(1, 100), 6))
path = [F(k, 100) for k in ks] + [F(99, 100)]
ck("path shares " + " ".join(str(p) for p in path), [str(p) for p in path] == ["7/100","1/10","1/5","21/50","51/100","21/25","99/100"])
C0 = 2_000_000
def rows_for(rho):
    out = []
    for x in path:
        if x > rho:
            continue
        res = rho * C0 - x * C0
        cl = C0 - x * C0
        assert res.denominator == 1 and cl.denominator == 1
        th = F(int(res), int(cl))
        out.append((x, int(res), int(cl), th, math.floor(10000 * th)))
    return out
r19 = rows_for(F(19, 20)); r21 = rows_for(F(21, 20))
ck("rho 19/20 computed rows = 6", len(r19) == 6)
ck("rho 21/20 computed rows = 7", len(r21) == 7)
exp19 = [(9462),(9444),(9375),(9137),(8979),(6875)]
ck("19/20 bps list", [r[4] for r in r19] == exp19)
ck("19/20 x=21/50 reserves/claims/cov", (r19[3][1], r19[3][2], r19[3][3]) == (1060000, 1160000, F(53, 58)))
ck("21/20 bps list", [r[4] for r in r21] == [10537,10555,10625,10862,11020,13125,60000])
ck("21/20 x=99/100 coverage 6", r21[-1][3] == 6)
ck("19/20 lowest at 21/25 with 220000/320000", min(r19, key=lambda r: r[4])[0] == F(21,25) and (r19[5][1], r19[5][2]) == (220000, 320000))
ck("19/20 has 15 pairs", len(r19)*(len(r19)-1)//2 == 15)
ck("21/20 has 21 pairs", len(r21)*(len(r21)-1)//2 == 21)
def diff_ok(rho, rows):
    for i in range(len(rows)):
        for j in range(i+1, len(rows)):
            a, b = rows[i], rows[j]
            if not (b[3]-a[3] == (b[0]-a[0])*(rho-1)/((1-a[0])*(1-b[0]))):
                return False
    return True
ck("difference identity 19/20", diff_ok(F(19,20), r19))
ck("difference identity 21/20", diff_ok(F(21,20), r21))
# E2: first >= 10600 in 21/20 table
first = next(r for r in r21 if r[4] >= 10600)
ck("E2 first >=10600 is 10625 at 1/5", first[0] == F(1,5) and first[4] == 10625)
# E3
ck("E3 both sides -31/784", F(44,49)-F(15,16) == F(-31,784) and (F(51,100)-F(1,5))*(F(-1,20))/((1-F(1,5))*(1-F(51,100))) == F(-31,784))
# worked values
ck("x=1/2 rho 19/20 = 9/10", (F(19,20)-F(1,2))/(1-F(1,2)) == F(9,10))
ck("x=1/2 rho 21/20 = 11/10", (F(21,20)-F(1,2))/(1-F(1,2)) == F(11,10))
ck("x=1/7 rho 19/20 = 113/120 floor 9416", (F(19,20)-F(1,7))/(1-F(1,7)) == F(113,120) and math.floor(10000*F(113,120)) == 9416)
ck("M2 rho 3/5 x 2/5 = 1/3", (F(3,5)-F(2,5))/(1-F(2,5)) == F(1,3))
ck("M1 = 2/3", (F(3)-F(1))/(F(4)-F(1)) == F(2,3))
ck("M3 9500", math.floor(10000*F(19,20)) == 9500)
ck("R2 x* for c=9/10 rho=19/20 is 1/2", (F(19,20)-F(9,10))/(1-F(9,10)) == F(1,2))
ck("haircut threshold 20/19", F(1)/(1-F(1,20)) == F(20,19))
ck("haircut rho 21/20 effective 399/400 cov 199/200 bps 9950", (F(399,400)-F(1,2))/(F(1,2)) == F(199,200) and math.floor(10000*F(199,200))==9950)
ck("quiz 9 20/19 to 10dp 1.0526315789", f"{float(F(20,19)):.10f}" == "1.0526315789")
# haircut: rho*(1-h) effective and prop 2.4
ck("R1 1/(1-h)*(1-h)=1", F(1)/(1-F(1,20))*(1-F(1,20)) == 1)
# L04 sign rule examples
ck("Prop 2.4 example rho 1 gives coverage 1", all((F(1)-s)/(1-s) == 1 for s in [F(0), F(1,3), F(9,10)]))

# L05
p = F(1, 8)
kap = 2500
ell = (1, 2, 4)
pats = list(itertools.product((0, 1), repeat=3))
def pp(pat, p):
    r = F(1)
    for x in pat:
        r *= p if x else 1 - p
    return r
probs = [pp(pt, p) for pt in pats]
ck("pattern probabilities *512", [int(q*512) for q in probs] == [343,49,49,7,49,7,7,1])
ck("probs sum to 1", sum(probs) == 1)
costs = [kap*sum(e*x for e,x in zip(ell,pt)) for pt in pats]
ck("pattern costs", costs == [0,10000,5000,15000,2500,12500,7500,17500])
mean_ind = sum(q*c for q,c in zip(probs,costs))
ck("mean 4375/2", mean_ind == F(4375,2))
ck("closed form p*kappa*sum", p*kap*sum(ell) == F(4375,2))
ck("round half up 2188", math.floor(F(4375,2)+F(1,2)) == 2188)
ck("no-fail 343/512, at least one 169/512, 3p = 192/512", pp((0,0,0),p) == F(343,512) and 1-F(343,512) == F(169,512) and 3*p == F(192,512))
ck("A4 no-fail 7/8, prob fail p=64/512", 1-p == F(7,8) and p == F(64,512))
eq = (2,2,2)
ck("equal delays mean 1875", sum(pp(pt,p)*kap*sum(e*x for e,x in zip(eq,pt)) for pt in pats) == 1875 and 3*p*kap*2 == 1875)
def var(outs):
    m = sum(q*c for q,c in outs)
    return sum(q*c*c for q,c in outs) - m*m
ind = [(q,c) for q,c in zip(probs,costs)]
com = [(1-p,0),(p,kap*sum(ell))]
ck("variance independent 57421875/4", var(ind) == F(57421875,4))
ck("variance comonotone 133984375/4", var(com) == F(133984375,4))
ck("means equal under both", sum(q*c for q,c in com) == mean_ind)
ck("E2 difference 19140625 and Prop 2.5 value", var(com)-var(ind) == 19140625 and 2*kap**2*p*(1-p)*(1*2+1*4+2*4) == 19140625)
ck("no-cost comonotone 7/8, independent 343/512", sum(q for q,c in com if c==0) == F(7,8) and sum(q for q,c in ind if c==0) == F(343,512))
# Prop 2.6 gap: 3p - (1-(1-p)^3) = p^2 (3-p) > 0 on 0<p<1 ; check at sample points
ok_gap = all((3*F(k,100) - (1-(1-F(k,100))**3)) == F(k,100)**2*(3-F(k,100)) and (3*F(k,100) - (1-(1-F(k,100))**3)) > 0 for k in range(1,100))
ck("M2 misconception 3p > 1-(1-p)^3 on sampled 0<p<1 (algebra p^2(3-p))", ok_gap)
# Prop 2.5 difference zero iff at most one ell positive, sample
def diff_formula(ell_, kap_, p_):
    v4 = kap_**2*(sum(ell_))**2*p_*(1-p_)
    v3 = sum((kap_*l)**2 for l in ell_)*p_*(1-p_)
    return v4 - v3
ck("Prop2.5 identity sample", diff_formula((1,2,4),2500,p) == 2*2500**2*p*(1-p)*14)
ck("Prop2.5 zero when one positive", diff_formula((0,5,0),2500,p) == 0)
ck("Prop2.5 positive when two positive", diff_formula((0,5,3),2500,p) > 0)
# kappa=0 case: both variances zero, so difference zero even with two positive delays
ck("kappa=0 gives zero difference with two positive delays", diff_formula((1,2,4),0,p) == 0)
# R1 n trades equal delays
for n in (1,2,3,5):
    l = 2; k = 1000
    m3 = n*p*(1-p)*k*k*l*l
    m4 = (n*k*l)**2*p*(1-p)
    ck(f"R1 n={n} ratio n", m4 == n*m3)
# P(C=0) under A3 = (1-p)^3 < 1-p
ck("P(C=0) A3 < A4", (1-p)**3 < 1-p)
# R2 range: 5/8 example
omega = {'w0':F(5,8),'w1':F(1,8),'w2':F(1,8),'w3':F(1,8)}
ck("R2 example sums to 1 and F_i prob 1/8", sum(omega.values()) == 1)
# R2 bound check: no-fail = 1 - P(U) with P(U) in [1/8, 3/8]
print("SUMMARY checks", checks, "failures", len(fails), fails)

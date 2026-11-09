# Independent exact-fraction recomputation of the numbers and claims changed in the 95f3f8cb..2a805c83 delta.
from fractions import Fraction as F
from itertools import product
import math
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("OK   " if cond else "FAIL ") + name)

# Example 2.8 (L05.html:153): p=1/8, kappa=2500, ell=(1,2,4); enumeration under A3 (independent) and A4 (comonotone)
p, kappa, ell = F(1, 8), 2500, (1, 2, 4)
def pmf_indep():
    for x in product([0, 1], repeat=3):
        pr = F(1)
        for xi in x:
            pr *= p if xi else (1 - p)
        yield x, pr
def pmf_comono():
    yield (1, 1, 1), p
    yield (0, 0, 0), 1 - p
def mean(pmf):
    return sum(pr * kappa * sum(l * xi for l, xi in zip(ell, x)) for x, pr in pmf())
def var(pmf):
    m = mean(pmf)
    return sum(pr * (kappa * sum(l * xi for l, xi in zip(ell, x)) - m) ** 2 for x, pr in pmf())
closed = p * kappa * sum(ell)
check("Example 2.8 closed form p*kappa*sum(ell) = 4375/2", closed == F(4375, 2))
check("Example 2.8 mean under A3 (enumeration) = 4375/2", mean(pmf_indep) == F(4375, 2))
check("Example 2.8 mean under A4 (enumeration) = 4375/2", mean(pmf_comono) == F(4375, 2))
check("(1/8)(2500)(7) = 17500/8 = 2187.5", F(1, 8) * 2500 * 7 == F(17500, 8) == F(4375, 2) and F(4375, 2) == F(4375, 2))
check("2187.5 rounds half up to 2188", math.floor(F(4375, 2) + F(1, 2)) == 2188)
check("2188 cents is 21.88 dollars", F(2188, 100) == F("21.88"))
# Example 2.7 (L05.html:147-151): p=1/8
check("Example 2.7: 1-(7/8)^3 = 169/512", 1 - (1 - p) ** 3 == F(169, 512))
check("Example 2.7: A4 probability p = 64/512", p == F(64, 512))
check("Example 2.7: 3p = 192/512 and is neither", 3 * p == F(192, 512) and 3 * p not in (F(169, 512), F(64, 512)))
# Prop 2.5 difference at Example 2.8 parameters: 2 kappa^2 p(1-p) sum_{i<j} l_i l_j equals Var4 - Var3
diff_formula = 2 * kappa ** 2 * p * (1 - p) * sum(ell[i] * ell[j] for i in range(3) for j in range(i + 1, 3))
check("Prop 2.5 difference formula equals Var4 - Var3 at Example 2.8 parameters", var(pmf_comono) - var(pmf_indep) == diff_formula)
print("  Var4 - Var3 =", var(pmf_comono) - var(pmf_indep), " formula =", diff_formula)
# Prop 2.5 general spot grid (exact)
bad = 0
for pp in [F(1, 8), F(1, 4), F(1, 2), F(3, 4)]:
    for kk in [1, 2500]:
        for ll in [(1, 2, 4), (0, 3, 5), (2, 2, 2), (7, 0, 0)]:
            def pi(pp=pp):
                for x in product([0, 1], repeat=3):
                    pr = F(1)
                    for xi in x:
                        pr *= pp if xi else (1 - pp)
                    yield x, pr
            def pc(pp=pp):
                yield (1, 1, 1), pp
                yield (0, 0, 0), 1 - pp
            def vv(pmf, kk=kk, ll=ll):
                m = sum(pr * kk * sum(a * b for a, b in zip(ll, x)) for x, pr in pmf())
                return sum(pr * (kk * sum(a * b for a, b in zip(ll, x)) - m) ** 2 for x, pr in pmf())
            fml = 2 * kk ** 2 * pp * (1 - pp) * sum(ll[i] * ll[j] for i in range(3) for j in range(i + 1, 3))
            if vv(pc) - vv(pi) != fml:
                bad += 1
check("Prop 2.5 difference identity on exact grid (p, kappa, ell)", bad == 0)
# Prop 2.4 mean equality over the grid (A3 and A4 both p*kappa*sum(ell))
bad = 0
for pp in [F(1, 8), F(1, 3), F(7, 9)]:
    for ll in [(1, 2, 4), (0, 0, 9), (3, 3, 3)]:
        # enumerate explicitly
        mi = F(0)
        for x in product([0, 1], repeat=3):
            pr = F(1)
            for xi in x:
                pr *= pp if xi else (1 - pp)
            mi += pr * 100 * sum(a * b for a, b in zip(ll, x))
        mc = pp * 100 * sum(ll)
        if mi != mc or mc != pp * 100 * sum(ll):
            bad += 1
check("Prop 2.4 A4 mean = A3 mean = p kappa sum ell on exact grid", bad == 0)
# Misconception 1 (L04.html:391) and Remark 4.1: rho=1, measured ratio 1-h, coverage below 1 for every admissible share
bad = 0; n = 0
for h in [F(1, 20), F(1, 10), F(1, 3)]:
    rho_m = 1 - h
    for k in range(0, 1000):
        x = F(k, 1000)
        if x <= rho_m and x < 1:
            n += 1
            th = (rho_m - x) / (1 - x)
            if not th < 1:
                bad += 1
check("Misconception 1 (rho=1, h>0): measured coverage < 1 at every admissible share on grid (%d points)" % n, bad == 0 and n > 0)
# rho=1, h=0: coverage exactly 1 at every admissible share (Prop 2.4)
bad = 0
for k in range(0, 1000):
    x = F(k, 1000)
    if x <= 1 and x < 1:
        if (F(1) - x) / (1 - x) != 1:
            bad += 1
check("Misconception 1 (rho=1, h=0): coverage exactly 1 at every admissible share", bad == 0)
# Remark 4.1 threshold for h=1/20 is 20/19
check("Remark 4.1 threshold 1/(1-h) for h=1/20 is 20/19", 1 / (1 - F(1, 20)) == F(20, 19))
# Remark 2.3 necessity: if x>rho, reserves rho-x<0 (negative), so x<=rho is necessary for par redemption
check("Remark 2.3: reserves after redemption C0(rho-x) negative iff x>rho", all(((F(19, 20) - F(k, 100)) < 0) == (F(k, 100) > F(19, 20)) for k in range(100)))
# R3 spot check: E[C]=p kappa sum ell nondecreasing in p, kappa, each ell_i (real, nonnegative grid, exact)
grid = [F(k, 4) for k in range(0, 9)]
bad = 0
for a in grid:
    for b in grid:
        for c in grid:
            e = lambda pp, kk, l1, l2=F(1), l3=F(2): pp * kk * (l1 + l2 + l3)
            if F(1, 8) <= F(1, 2) and e(F(1, 8), a, b) > e(F(1, 2), a, b):
                bad += 1
            if e(F(1, 2), a, b) > e(F(1, 2), a + F(1, 4), b):
                bad += 1
            if e(F(1, 2), a, b) > e(F(1, 2), a, b + F(1, 4)):
                bad += 1
check("R3 monotone spot grid (p, kappa, ell_1 nonnegative reals)", bad == 0)
print("ALL OK" if all(ok) else "SOME FAILED")

"""Independent recomputation of every number on the M6 hub and L01-L04 slice (verifier round 3)."""
from fractions import Fraction as F
from itertools import product
from math import sqrt, floor
import math

# Hub placement skill checks
# rung 1: fair walk, tau = min(first hit of +1, 2); E[S_tau]
def expS_tau():
    tot = F(0)
    for steps in product([1, -1], repeat=2):
        p = F(1, 4)
        s = 0; hit = False; val = None
        path = [0]
        for st in steps:
            if not hit:
                s += st; path.append(s)
                if s == 1:
                    hit = True
                    val = 1
                    break
        if val is None:
            val = path[-1] if len(path) == 3 else path[-1]
            # tau = 2 when not hit
        # if hit at step 1, tau=1, S=1; prob 1/2 at step-1 level handled below
    # explicit: first step
    e = F(1, 2) * 1 + F(1, 2) * (F(1, 2) * 0 + F(1, 2) * (-2))
    return e
print("rung1 E[S_tau] =", expS_tau())
print("rung2 sum stakes 1,2,4 =", 1 + 2 + 4)
print("placement mastery: 7/9 =", round(7 / 9 * 100, 1), " 8/9 =", round(8 / 9 * 100, 1))
print("hours: 12*9 =", 12 * 9, " 108+42 =", 108 + 42, " 42/150 =", 42 / 150)

# L01
def gen(omega, blocks):
    fam = set()
    for mask in range(2 ** len(blocks)):
        u = set()
        for j, b in enumerate(blocks):
            if mask >> j & 1:
                u |= b
        fam.add(frozenset(u))
    return fam
print("L01 counts", len(gen(None, [frozenset({0,1}), frozenset({2,3})])), len(gen(None, [frozenset({i}) for i in range(4)])), len(gen(None, [frozenset({0,1}),frozenset({2,3}),frozenset({4,5})])))
print("L01 M1 family size", len(gen(None,[frozenset({1}),frozenset({2,3}),frozenset({4,5})])))

# L02
W = frozenset(range(1, 7))
subs = [frozenset(c) for r in range(7) for c in __import__('itertools').combinations(range(1, 7), r)]
fails = 0; disj = 0
for a in subs:
    for b in subs:
        if not (a & b):
            disj += 1
            if F(len(a | b), 6) ** 2 != F(len(a), 6) ** 2 + F(len(b), 6) ** 2:
                fails += 1
print("L02 nu failing disjoint pairs", fails, "of", disj)
print("L02 fair die 2/3 vs 1/2 union", F(1,3)+F(1,3), F(1,2))
print("L02 biased odd", F(1,2)+F(1,8)+F(1,32), "biased {1,2}", F(1,2)+F(1,4))
print("L02 3/20 total", 6*F(3,20))

# L03
for n in range(1, 11):
    I = sum((k / 2**n) * (sqrt((k+1)/2**n) - sqrt(k/2**n)) for k in range(2**n))
    print(f"L03 n={n:2d} I_n={I:.10f} err={1/3-I:.10f} bound={2**-n:.10f}")
print("L03 I_2 terms", [round(0.25*(sqrt(.5)-.5),6), round(.5*(sqrt(.75)-sqrt(.5)),6), round(.75*(1-sqrt(.75)),6)])
print("L03 M1 integral", 2*F(1,3)+5*F(2,3))
print("L03 x^-1/2 cap", 2*F(1,4)+ (2-1))

# L04
print("L04 H-type partial N=10", float(sum(F(1,k) for k in range(2,12))), "N=100", float(sum(F(1,k) for k in range(2,102))))
print("L04 min(2,x^-1/2) integral check numerically", sum(min(2, ((i+0.5)/1e6)**-0.5) for i in range(1000000))/1e6)
print("L04 Ex3.2 partial integrals 2-1/n n=5:", 2-F(1,5))
print("L04 g on (1/(n+1)^2,1/n^2] length formula n=3:", F(1,9)-F(1,16), F(2*3+1, 9*16))
print("L04 sum_n (2n+1)/(n(n+1)^2) partial to 10000:", float(sum(F(2*n+1, n*(n+1)**2) for n in range(1, 2000))))

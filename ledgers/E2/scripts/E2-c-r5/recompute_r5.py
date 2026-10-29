"""Independent recomputation of L07-L09 numbers (round 5). Exact fractions; no code from the lessons."""
import itertools
from fractions import Fraction as F
from math import comb

def em_formula(n, a):
    # E[M] = -a + sum_{x=-a}^{a-1} (1 - F(x)^n), F(x) = (x+a+1)/(2a+1)
    s = F(0)
    for x in range(-a, a):
        Fx = F(x + a + 1, 2 * a + 1)
        s += 1 - Fx ** n
    return -a + s

def em_enum(n, a):
    vals = range(-a, a + 1)
    tot = F(0); cnt = 0
    for errs in itertools.product(vals, repeat=n):
        tot += max(errs); cnt += 1
    return F(tot, cnt)

print("L08 E[M](2,1) formula", em_formula(2, 1), "enum", em_enum(2, 1))
print("L08 E[M](3,1) formula", em_formula(3, 1), "enum", em_enum(3, 1))
print("L08 E[M](2,2) formula", em_formula(2, 2), "enum", em_enum(2, 2))
print("L08 E[M](3,2) formula", em_formula(3, 2), "enum", em_enum(3, 2))
m5 = em_formula(5, 2000)
print("L08 E[M](5,2000) =", m5, float(m5))
print("L08 cont analogue a(n-1)/(n+1) =", F(2000 * 4, 6), float(F(2000 * 4, 6)))
print("L08 diff discrete - continuous (cents) =", float(m5 - F(8000, 3)))
print("L08 1334 - E[M] =", float(1334 - m5), "1333 - E[M] =", float(1333 - m5))
print("L08 ceil(E[M]) =", -(-m5.numerator // m5.denominator))
# Example 2.4 distribution for n=2, a=1
print("L08 Ex2.4 E[M] n=2 a=1 =", em_enum(2, 1), "P(M=-1), P(0), P(1):", F(1, 9), F(3, 9), F(5, 9))

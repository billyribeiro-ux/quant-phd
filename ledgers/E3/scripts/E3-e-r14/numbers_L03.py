"""Independent recomputation of the L03 lab grid values and prose numbers (verifier round 14, slice e)."""
import math
from fractions import Fraction as F

P = [(5000, 0.25), (10000, 0.5), (20000, 0.25)]


def ce(g):
    if g == 1:
        return math.exp(sum(p * math.log(x) for x, p in P))
    s = 1 - g
    return sum(p * x ** s for x, p in P) ** (1 / s)


for g in (0, 0.25, 0.5, 1, 2, 4):
    print("gamma", g, "CE", round(ce(g), 4), "rounded", math.floor(ce(g) + 0.5))
print("gamma 2 exact", F(1) / sum(F(q) / x for x, q in [(5000, F(1, 4)), (10000, F(1, 2)), (20000, F(1, 4))]))
print("expected prize", sum(F(q) * x for x, q in [(5000, F(1, 4)), (10000, F(1, 2)), (20000, F(1, 4))]))
print("E3 emp-2 M", F(1, 5000) / 4 + F(1, 20000) * 0 + F(1, 2) / 10000 + F(1, 4) / 20000)
print("Example 2.5 g=2", F(1, 2) / 1000 + F(1, 2) / 4000, "CE", 1 / (F(1, 2) / 1000 + F(1, 2) / 4000), "g=1", math.exp(0.5 * math.log(1000) + 0.5 * math.log(4000)))
print("M2 M", F(1, 4) / 1000 + F(3, 4) / 9000, "CE", 1 / (F(1, 4) / 1000 + F(3, 4) / 9000))
print("M3 3X M", F(1, 4) / 3000 + F(3, 4) / 27000, "CE", 1 / (F(1, 4) / 3000 + F(3, 4) / 27000))
print("lab hypothesis 80000/9 =", float(F(80000, 9)))
# R1 numeric sanity: gamma 0.5 with x1 -> 0 CE stays positive; gamma 2 CE -> 0
for x1 in (1e-2, 1e-4, 1e-6):
    print("x1", x1, "g=2 CE", (0.5 * x1 ** -1 + 0.5 * 100.0 ** -1) ** -1, "g=0.5 CE", ce_two := (0.5 * x1 ** 0.5 + 0.5 * 100 ** 0.5) ** 2)
# Remark 2.8 bound check at k=10 for the lab prizes
print("bound (k+1)/2 at k=10 =", 11 / 2)
# CRRA check M1 at gamma=1/2: r_A(4)
print("M1 r_A(4) =", 0.5 / 4)

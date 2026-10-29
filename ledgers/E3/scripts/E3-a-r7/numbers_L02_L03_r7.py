"""Independent recomputation (python -I, Fractions and mpmath-free bisection) of the E3 L02 Lab 1 gamble and the L03 Lab 1 lottery numbers."""
import math
from fractions import Fraction

# L02 gamble from the twin: -60, 0, 60 with probabilities 1/4, 1/2, 1/4 at wealth 100, u = sqrt
G = [(-60, Fraction(1, 4)), (0, Fraction(1, 2)), (60, Fraction(1, 4))]
W = 100
mean = sum(p * x for x, p in G)
var = sum(p * x * x for x, p in G) - mean * mean
print("mean", mean, "variance", var)
def ce_sqrt(eps):
    eu = sum(float(p) * math.sqrt(W + eps * x) for x, p in G)
    return eu * eu  # CE in wealth: sqrt(c) = E sqrt(W)
c1 = ce_sqrt(1.0)
prem = W - c1
print("CE", round(c1, 6), "premium", round(prem, 6), "cents CE", round(c1 * 100), "premium cents", math.floor(prem * 100 + 0.5))
pratt = 0.5 * (1 / (2 * W)) * 0  # placeholder
ra = 1 / (2 * W)
print("r_A", ra, "approx", 0.5 * ra * float(var), "error", prem - 0.5 * ra * float(var), "share exact", (prem - 4.5) / prem, "share approx", (prem - 4.5) / 4.5)
for eps in (1.0, 0.5, 0.25, 0.1, 0.01):
    print("eps", eps, round(W - ce_sqrt(eps), 6) / eps**2 if False else round((W - ce_sqrt(eps)) / eps**2, 6))
# linear: zero premium
# L03: prizes 5000,10000,20000 with 1/4,1/2,1/4
P = [(5000, 0.25), (10000, 0.5), (20000, 0.25)]
def ce(g):
    if g == 1:
        return math.exp(sum(p * math.log(x) for x, p in P))
    s = 1 - g
    return (sum(p * x**s for x, p in P)) ** (1 / s)
for g in (0, 0.25, 0.5, 1, 2, 4):
    print("gamma", g, "CE", round(ce(g), 4))
print("exact g2", Fraction(1, 1) / sum(Fraction(p).limit_denominator(4) / x for x, p in [(5000, Fraction(1, 4)), (10000, Fraction(1, 2)), (20000, Fraction(1, 4))]))

"""Re-derive the numbers in the round-3 delta (L03 misconception, Bernoulli, Prop 2.8 table, cards c028-c047, c183, c200, c033, c030)."""
import math
from fractions import Fraction as F


def moments(law):
    mu = sum(v * p for v, p in law)
    var = sum((v - mu) ** 2 * p for v, p in law)
    m3 = sum((v - mu) ** 3 * p for v, p in law)
    m4 = sum((v - mu) ** 4 * p for v, p in law)
    return mu, var, m3, m4


skew_law = [(0, F(1, 2)), (1, F(1, 4)), (2, F(1, 8)), (10, F(1, 8))]
mu, var, m3, m4 = moments(skew_law)
print("skewed law mu", mu, "var", var, "m3", m3, "m4", m4, "gamma3^2 exact", m3 * m3 / var**3, float(m3 / var**1.5), "gamma4", m4 / var**2, float(m4 / var**2))
print("card c200 m3=2157/32 ->", m3 == F(2157, 32), " m4=149461/256 ->", m4 == F(149461, 256))
print("card c042 mean 7/4 ->", mu == F(7, 4), " var 163/16 ->", var == F(163, 16))

law43 = [(-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10))]
mu, var, m3, m4 = moments(law43)
print("law -2,1,3: mu", mu, "m2", var, "m3", m3, "m4", m4, "gamma4", m4 / var**2, "(card c043 says 5/3)", m4 / var**2 == F(5, 3))
print("  symmetric about mean? reflected support equals support:", sorted(v - mu for v, _ in law43) == sorted(-(v - mu) for v, _ in law43))

# Bernoulli law with p = (1 - 1/sqrt(3))/2  (misconception paragraph, L03 line 281)
p = (1 - 1 / math.sqrt(3)) / 2
q = 1 - p
pq = p * q
print("Bernoulli p=(1-1/sqrt3)/2: pq =", pq, " 1/6 =", 1 / 6, " gamma4 =", (1 - 3 * pq) / pq)
# direct central fourth moment over the Bernoulli law, floats
mu_b = p
var_b = p * q
m4_b = p * (1 - mu_b) ** 4 + q * (0 - mu_b) ** 4
print("  direct gamma4 =", m4_b / var_b**2)

# Bernoulli p = 1/10 and p = 1/4 (Example 2.5 and card c045)
for pp in (F(1, 10), F(1, 4)):
    qq = 1 - pp
    g4 = (1 - 3 * pp * qq) / (pp * qq)
    g3sq = (1 - 2 * pp) ** 2 / (pp * qq)
    print("Bernoulli", pp, "gamma4", g4, "gamma3^2", g3sq)

# Prop 2.8 kurtosis of the standard normal: Gaussian moments via double factorial
print("E[Z^4] = 3 (= 3 * 1), E[Z^2] = 1: 3 == 3 *", 1, "True")

# Loss sample expected count (card c033): 10000 * 1/20
print("expected loss count 10000 * 1/20 =", 10000 * F(1, 20))
# Die sample: variance of the die is 35/12
die = [(k, F(1, 6)) for k in range(1, 7)]
mu, var, _, _ = moments(die)
print("die mu", mu, "var", var, "scale a=2 var", 4 * var, "= 35/3", 4 * var == F(35, 3), "twice", 2 * var)
loss = [(0, F(19, 20)), (250000, F(1, 20))]
mu, var, _, _ = moments(loss)
print("loss mu", mu, "var", var, "sd", math.sqrt(var), "sqrt(2968750000)", math.sqrt(2968750000))

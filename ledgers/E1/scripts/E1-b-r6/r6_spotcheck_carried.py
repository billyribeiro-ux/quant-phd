"""Round-6 spot checks (verifier-written) of carried-page numbers that the changed cards and prose cite."""
from fractions import Fraction as F
import math

# L04 reference market: a = 120, b = 2, d = 1; F(p, a) = a - b p - d p^2 = 0
a, b, d = F(120), F(2), F(1)
delta_sq = b * b + 4 * a * d
p = (-b + F(math.isqrt(int(delta_sq)))) / (2 * d)
print("L04 p(120) =", p, "delta =", math.isqrt(int(delta_sq)), "dp/da = 1/delta =", F(1, math.isqrt(int(delta_sq))),
      "elasticity of p wrt a =", (a / p) * F(1, math.isqrt(int(delta_sq))), "check equilibrium:", a - b * p - d * p * p == 0)

# L06 Lemma 2.4 / Proposition 2.8: reaction R(x) = max(0, (D - x)/2), d = 100, iteration x_{t+1} = R(x_t), x_0 = 0
dd = F(100)
R = lambda x: max(F(0), (dd - x) / 2)
x = F(0)
first = None
errs_ok = True
for t in range(0, 31):
    closed = dd / 3 * (1 - F(-1, 2) ** t)
    errs_ok = errs_ok and (x == closed) and (abs(x - dd / 3) == dd / 3 * F(1, 2) ** t)
    if first is None and abs(x - dd / 3) <= F(1, 10**6):
        first = t
    x = R(x)
print("L06 Prop 2.8 closed form = iteration for t=0..30:", errs_ok, "first t with error <= 1e-6:", first)

# L06 Proposition 4.1 differences at (120, 1, 20), d = 100
a, b, c = F(120), F(1), F(20)
d = a - b * c
print("L06 Q_C - Q_m =", 2 * d / 3 - d / 2, "(d/6)", d / 6, "; Q_B - Q_C =", d - 2 * d / 3, "(d/3)", d / 3)
print("fee m, C, B:", (a + b * c) / (2 * b), (a + 2 * b * c) / (3 * b), c)
print("profit m - C:", d * d / (4 * b) - 2 * d * d / (9 * b), "(d^2/(36b))", d * d / (36 * b))

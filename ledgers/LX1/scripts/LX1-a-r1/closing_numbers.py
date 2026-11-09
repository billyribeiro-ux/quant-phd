"""Independent re-derivation of the L01 problem-set numbers (closing delta round 1). Exact Fractions only."""
from fractions import Fraction as Fr
import math

def rhu(x):
    return math.floor(x + Fr(1, 2))

def F(d1, r, g, t):
    return Fr(d1) * (1 + g) ** t / (r - g)

# Mechanics 1
r, g = Fr(10, 100), Fr(4, 100)
F0 = F(250, r, g, 0)
print("Mech1 F0 =", F0, "=", float(F0), "half-up cents", rhu(F0))
# Mechanics 2
F3 = F(250, r, g, 3)
print("Mech2 1.04^3 =", (1 + g) ** 3, "numerator", 250 * (1 + g) ** 3, "F3 =", float(F3), "half-up", rhu(F3))
# Mechanics 3
r, g, d1 = Fr(5, 100), Fr(5, 100), Fr(100)
q = (1 + g) / (1 + r)
print("Mech3 q =", q, "term0 = d1/(1+r) =", d1 / (1 + r), "S10 =", sum(d1 * (1 + g) ** (k - 1) / (1 + r) ** k for k in range(1, 11)), "=", float(sum(d1 * (1 + g) ** (k - 1) / (1 + r) ** k for k in range(1, 11))))
print("  1000/1.05 =", Fr(1000) / Fr(105, 100), " 20000/21 =", Fr(20000, 21), float(Fr(20000, 21)))
print("  N d1/(1+r) at N=10:", 10 * d1 / (1 + r))
# Proof 2 identity, check for several d1 including 0 and negative, and t>=1
r, g = Fr(9, 100), Fr(3, 100)
ok = True
for d1 in [Fr(0), Fr(400), Fr(-250), Fr(1, 3)]:
    for t in range(1, 15):
        if F(d1, r, g, t) != (1 + g) * F(d1, r, g, t - 1):
            ok = False
print("Proof2 identity F_t = (1+g) F_{t-1} for d1 in {0,400,-250,1/3}, t=1..14:", ok)
# direct sum check of closed form at d1=0 and at t=1 with d1=400 (series truncated large N, exact partial sums)
def S(d1, r, g, t, N):
    return sum(Fr(d1) * (1 + g) ** (t + k - 1) / (1 + r) ** k for k in range(1, N + 1))
print("S_N(0) for d1=400 at 3pc, N=200 rounds to", rhu(S(400, r, g, 0, 200)), "closed form", rhu(F(400, r, g, 0)))
# Emp 3: fundamental at t=9 with 400 cents at 9pc and 3pc
f9 = F(400, Fr(9, 100), Fr(3, 100), 9)
print("Emp3 F9 =", float(f9), "half-up", rhu(f9), "gap unrounded 0.25F =", float(Fr(1, 4) * f9), "2175/8698 =", float(Fr(2175, 8698)), "pct", round(100 * 2175 / 8698, 4))
print("  price 1.25 * F9 rounded", rhu(Fr(5, 4) * f9), "minus printed F 8698 =", rhu(Fr(5, 4) * f9) - 8698)
# Research 1
gs = Fr(9, 100) - Fr(400, 6000)
print("Res1 g* =", gs, float(gs), "check benchmark at g*:", F(400, Fr(9, 100), gs, 0))
# Emp 1 and 2 from printed lab output counts
print("Emp1 share 9/13 =", float(Fr(9, 13)), "4dp 0.6923")
print("Emp2 difference 13-9 =", 13 - 9)
# Quiz checks quickly (not in problem set): F2 for d1=400 r=9 g=3, q
print("quiz F2 =", float(F(400, Fr(9, 100), Fr(3, 100), 2)), "q =", float((1 + Fr(3, 100)) / (1 + Fr(9, 100))))
# Prop 2.2 witness
print("witness F0(1%)", F(400, Fr(9, 100), Fr(1, 100), 0), "F0(3%)", float(F(400, Fr(9, 100), Fr(3, 100), 0)), "gap at 6000 under 1%:", 6000 - F(400, Fr(9,100), Fr(1,100), 0), "under 3%:", float(6000 - F(400, Fr(9,100), Fr(3,100), 0)))
# Proof 1 monotonic: F0(g) strictly increasing on (-1, r)
vals = [F(250, Fr(9, 100), Fr(k, 100), 0) for k in range(-99, 9)]
print("Proof1 spot check monotone on grid:", all(a < b for a, b in zip(vals, vals[1:])))

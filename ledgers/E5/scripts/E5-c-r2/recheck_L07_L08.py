"""Independent recomputation of L07 and L08 numbers (verifier round 2, E5 slice c)."""
from fractions import Fraction as F
import math

# L07 rule
rn, tgt, pp, py = F(1), F(2), F(3, 2), F(1, 2)
def i(pi, y, phi=pp): return rn + pi + phi * (pi - tgt) + py * y
print("L07 A gap0", [str(i(F(p), F(0))) for p in range(1, 6)])
print("L07 A gap-2", [str(i(F(p), F(-2))) for p in range(1, 6)])
print("L07 A gap2", [str(i(F(p), F(2))) for p in range(1, 6)])
print("L07 worked pi3 y-1", i(F(3), F(-1)), "neutral", i(F(2), F(0)))
print("L07 E1 pi5 y2", i(F(5), F(2)), "E2 diff", i(F(3), F(-2)) - i(F(3), F(0)))
print("L07 M1", F(2) + 4 + F(1, 2) * 2 + F(1, 4) * -4)
print("L07 M3 y", (4 - (1 + 3 + F(3, 2) * 1)) / F(1, 2))
print("L07 R2 1/phi", 1 / pp, float(1 / pp))
print("L07 R3 y at pi=1 zero", -1)
print("L07 P1 slope", 1 + pp)
# Prop 2.2 difference for phi in grid
for phi in [F(0), F(1, 2), F(1), F(3, 2), F(-1, 2)]:
    d = (i(F(3), F(0), phi) - F(3)) - (i(F(2), F(0), phi) - F(2))
    print("diff phi", phi, d, "==phi*(1)", d == phi)

# L08
c = F(3, 5)
dG = 10000
def S(n): return sum(dG * c**k for k in range(n))
print("stage amounts", [dG * c**k for k in range(5)])
print("running", [S(n) for n in range(1, 6)], "S20", S(20), "S10", S(10))
tot = F(dG) / (1 - c)
print("total", tot)
for n in (1, 5, 10, 20, 30):
    g = tot - S(n)
    print("gap", n, float(g), f"{float(g):.6f}")
print("0.6^20", float(c**20), "gap20/25000", float(F(dG) * 0 + (tot - S(20)) / 25000), "1-c^20", float(1 - c**20))
print("share 23056/25000", F(23056, 25000), "E1 share 1-0.6^20 6dp", f"{float(1 - c**20):.6f}")
print("0.6^9", float(c**9), "0.6^10", float(c**10), "R3 N", next(n for n in range(1, 100) if c**n <= F(1, 100)))
print("R2 mult", 1 / (1 - c * (1 - F(1, 2))), "lump", 1 / (1 - c))
print("M1 L08", 1 / (1 - F(1, 2)), S(3) if False else None)
c1 = F(1, 2); print("M1 stages", [40 * c1**k for k in range(3)], sum(40 * c1**k for k in range(3)), F(40) * (1 - c1**3) / (1 - c1))
print("M2", -F(3, 4) * 100 / F(1, 4), "M3 spend", F(50) / F(1, 5), "tax", -F(4, 5) * 50 / F(1, 5), "sum", F(50) / F(1, 5) - F(4, 5) * 50 / F(1, 5))
print("tax -15000 check", -c * 10000 / (1 - c), "Y before/after", (20000 + 15000 + 30000) / (1 - c), (20000 + 15000 + 40000) / (1 - c))
print("E2 ratio", F(-15000, 25000))
print("Bernoulli bound check N=1..30 holds:", all(c**n <= 1 / (1 + n * (1 / c - 1)) for n in range(1, 31)))
print("Lab B gap exact check N=1..30 holds:", all(tot - S(n) == dG * c**n / (1 - c) for n in range(1, 31)))
print("R2 L08 claim 1-c(1-tau) > 1-c:", 1 - c * (1 - F(1, 2)) > 1 - c)
print("L08 misconception tax cut +15000 =", -(-c * -10000 / (1 - c)) if False else c * 10000 / (1 - c))

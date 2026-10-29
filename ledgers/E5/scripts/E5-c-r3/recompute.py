"""Independent re-derivation of every number in E5 L07 and L08 prose (verifier E5-c round 3)."""
from fractions import Fraction as F

# L07: rule and checks
r_n, target, phi_pi, phi_y = F(1), F(2), F(3, 2), F(1, 2)
def i_rule(pi, y, phi=phi_pi, py=phi_y):
    return r_n + pi + phi * (pi - target) + py * y
print("L07 M1", F(2) + 4 + F(1, 2) * 2 + F(1, 4) * (-4), "expect 6")
print("L07 M3 y for i=4 at pi=3:", (F(4) - (1 + 3 + F(3, 2) * 1)) / F(1, 2), "expect -3")
print("L07 E1 pi5 y2:", i_rule(F(5), F(2)), "expect 23/2")
print("L07 E2 pi3 y0,y-2:", i_rule(F(3), F(0)), i_rule(F(3), F(-2)), "expect 11/2 9/2")
print("L07 R2 1/phi:", float(1 / phi_pi), "expect 0.6667")
print("L07 R3 pi1 y=-2:", i_rule(F(1), F(-2)), " negative threshold y<-1 check:", i_rule(F(1), F(-1)))
print("L07 worked pi3 y-1:", i_rule(F(3), F(-1)), "neutral:", i_rule(F(2), F(0)))
print("L07 quiz q2 explain:", 1 + 3 + F(3, 2) * 1 + F(1, 2) * (-1))
print("L07 why-it-matters gap example: 2 at trend 10 pct =", F(2, 10) * 100, "; 3 at 100 pct =", F(3, 100) * 100)
print("L07 nominal grid row y=0:", [str(i_rule(F(p), F(0))) for p in range(1, 6)])
print("L07 M2 1+1/4, 1/4:", 1 + F(1, 4), F(1, 4))

# L08: stages and multiplier
c = F(3, 5); dG = 10000; a = 20000; I = 15000; G = 30000
S = lambda n: sum(dG * c**k for k in range(n))
print("L08 running totals 1..5:", [str(S(n)) for n in range(1, 6)], "expect 10000 16000 19600 21760 23056")
total = F(dG) / (1 - c)
print("L08 multiplier total:", total)
for n in (1, 5, 10, 20, 30):
    gap = total - S(n)
    print(f"L08 gap N={n}: exact {float(gap):.10f} printed-6dp {float(gap):.6f}")
print("L08 c^9:", float(c**9), "c^10:", float(c**10), "R3 N=10 ok:", c**10 <= F(1, 100) < c**9)
print("L08 E1 c^20 =", float(c**20), "gap/25000 =", 0.914040 / 25000, "1-c^20 6dp =", f"{float(1 - c**20):.6f}")
print("L08 E3 23056/25000 =", F(23056, 25000), float(F(23056, 25000)) * 100)
print("L08 E2 -15000/25000 =", F(-15000, 25000))
print("L08 R2 mult proportional tax:", 1 / (1 - c * (1 - F(1, 2))))
print("L08 M1 c=1/2:", 1 / (1 - F(1, 2)) * 40, sum(F(40) * F(1, 2)**k for k in range(3)))
print("L08 M2 tax c=3/4:", -(F(3, 4)) * 100 / (1 - F(3, 4)))
print("L08 M3 c=4/5:", F(50) / (1 - F(4, 5)), -(F(4, 5)) * 50 / (1 - F(4, 5)))
print("L08 Y before/after:", (a + I + G) / (1 - c), (a + I + G + dG) / (1 - c))
print("L08 tax change:", -c * 10000 / (1 - c))
print("L08 quiz q4 closed form:", dG * (1 - c**5) / (1 - c))
print("L08 S1/(dG/(1-c)):", (dG) / total)
print("L08 stage amounts:", [str(dG * c**k) for k in range(5)], "tax stages:", [str(-c * 10000 * c**k) for k in range(3)])
print("L08 Prop 2.3 bound N=1..5 holds:", all(c**N <= 1 / (1 + N * (1 / c - 1)) for N in range(1, 200)))
print("L08 Prop 2.1 identity N=1..30:", all(S(N) == dG * (1 - c**N) / (1 - c) for N in range(1, 31)))

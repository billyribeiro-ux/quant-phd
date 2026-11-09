# Round-5 independent re-derivation of the prose numbers in L04-L06 (exact Fractions and floats).
from fractions import Fraction as F
import math
D = F(9, 10)
S = 100 + F(20) / (D**3)
print("L04 R1 spot exact", S, "=", float(S), "=", round(float(S), 5))
print("L04 R3 exercise d3 PV", float(10 * D**3), "hold PV", float(50 * D**4))
print("E2.5 hold PV", float(10 * D**4), "ex1 PV", float(20 * D), "put d3 PV", float(20 * D**3))
print("ln(10/9)", math.log(10 / 9), "e^-r", math.exp(-math.log(10 / 9)))
print("L04 E2 put PV t=2,3,4:", float(10 * D**2), float(20 * D**3), float(10 * D**4))
print("L05 R2 bound", 120 - math.exp(0.1) * 100)
print("L05 S5 bound", 100 * math.exp(-0.1) - 50)
R = F(5, 4); u = F(3, 2); d = F(1, 2)
q = (R - d) / (u - d)
print("L06 q", q)
print("L06 E3 cash today", -28 + 30 - 2, "payoffs up", F(50) - F(75) + 25 + F(5, 2), "down", 0 - 25 + 25 + F(5, 2))
print("L06 R1 payoffs", [150 * 1 - 100, 100 * 1 - 100, 50 * 1 - 100], "R_f B", -100, "B", -100 / R)
print("L06 R2 R=1: q", (1 - d) / (u - d), "V0", ((1 - d) / (u - d) * 50), "B", (u * 0 - d * 50) / (u - d))
u2 = F(2)
q2 = (R - d) / (u2 - d)
V0 = (q2 * 100) / R
B2 = (u2 * 0 - d * 100) / ((u2 - d) * R)
Dl = F(100) / ((u2 - d) * 100)
print("M1 q", q2, "V0", V0, "Delta", Dl, "B", B2, "Delta*S0+B", Dl * 100 + B2)
V11 = (q2 * 300) / R
print("M3 V11", V11, "V00", (q2 * V11) / R)
print("E2 doubled V0", (F(3, 4) * 100) / R)
w = [q**2, 2 * q * (1 - q), (1 - q) ** 2]
S2 = [225, 75, 25]
print("E[S2]", sum(a * b for a, b in zip(w, S2)), "E[payoff]", sum(a * max(b - 100, 0) for a, b in zip(w, S2)),
      "disc of payoff at E[S2]", F(5625, 100) * F(16, 25))
print("ex3.4 V00", (q * (q * 125)) / R**2, "closed", R**-2 * (q**2) * 125)

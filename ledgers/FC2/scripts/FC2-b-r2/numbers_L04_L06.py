"""FC2-b round 2: independent recomputation of the numbers printed or stated in L04, L05 and L06 (exact Fractions)."""
import math
from fractions import Fraction as F

def e(x):  # exp as float for the displayed-decimal checks
    return math.exp(x)

print("L04 Example 2.5 call hold PV:", round(10 * e(-0.4), 4), "exercise at 1 PV:", round(20 * e(-0.1), 4), "put best PV:", round(20 * e(-0.3), 4))
print("L04 Lab part 2 hold PV by date:", [round(10 * e(-0.1 * (4 - t)), 4) for t in range(5)])
print("L04 1000 e^-0.4 cents:", round(1000 * e(-0.4), 2))
print("L04 R1 threshold 100+20e^0.3:", round(100 + 20 * e(0.3), 5))
print("L04 R3 path hold PV 50e^-0.4:", round(50 * e(-0.4), 2), " put-path exercise 10e^-0.3:", round(10 * e(-0.3), 2))
print("L04 E3 put at 2 PV 10e^-0.2:", round(10 * e(-0.2), 2))

D = F(9, 10)
K = [80, 90, 100, 110, 120]
C = [max(100 - D * k, 0) + F(max(100 - k, 0), 10) for k in K]
P = [c - 100 + D * k for c, k in zip(C, K)]
print("L05 calls USD", [str(c) for c in C], "puts USD", [str(p) for p in P])
print("L05 E1 second differences 90,100,110 (cents):", [int(100 * (C[i - 1] - 2 * C[i] + C[i + 1])) for i in (1, 2, 3)])
print("L05 E3 put at 120 vs DK-S:", P[4], D * 120 - 100, " call at 120 vs max(S-DK,0):", C[4], max(100 - D * 120, 0))
print("L05 M1 put:", 8 - 100 + F(97, 100) * 105)
print("L05 M2 bound, position value:", max(50 - F(19, 20) * 40, 0), 3 - 50 + F(19, 20) * 40)
print("L05 M3 chord, second difference:", (F(15) + 4) / 2, 15 - 2 * 9 + 4)
print("L05 canon 40.48:", round(100 * e(-0.1) - 50, 2))
print("L05 R2 r=-0.1 bound:", round(120 - e(0.1) * 100, 2))

q = (F(5, 4) - F(1, 2)) / (F(3, 2) - F(1, 2))
Rf = F(5, 4); u = F(3, 2); d = F(1, 2)
print("L06 q example 1.5:", q, " V0 = dS0 + B:", F(1, 2) * 100 - 20, " (3/4*50)/(5/4):", (q * 50) / Rf)
Delta = F(50, 100); B = (u * 0 - d * 50) / ((u - d) * Rf)
print("L06 Delta, B:", Delta, B, "replicate up/down:", Delta * 150 + Rf * B, Delta * 50 + Rf * B)
print("L06 E[S2]:", q * q * 225 + 2 * q * (1 - q) * 75 + (1 - q) ** 2 * 25, " R_f^2 S0:", Rf ** 2 * 100)
print("L06 expected payoff before discount:", q * q * 125, " payoff at expected price discounted:", (F(15625, 100) - 100) * F(16, 25))
print("L06 Ex3.4 V(1,1), V(0,0):", q * 125 / Rf, (q * (q * 125 / Rf)) / Rf)
print("L06 M1 q,V0:", (Rf - d) / (2 - d), ((F(1, 2)) * 100) / Rf)
print("L06 M2 Delta,B:", F(100) / ((2 - d) * 100), (2 * 0 - d * 100) / ((2 - d) * Rf), "sum:", F(100) / ((2 - d) * 100) * 100 + (2 * 0 - d * 100) / ((2 - d) * Rf))
print("L06 M3 V(0,0):", (F(1, 2) * (F(1, 2) * 300 / Rf)) / Rf)
print("L06 E2 doubled V0:", (q * 100) / Rf)
print("L06 E3 quote 28: up", 50 - 75 + 25 + F(5, 2), "down", 0 - 25 + 25 + F(5, 2), "today", -28 + 50 - 20 - 2)
print("L06 R2 R_f=1: q, V0, B:", (1 - d) / (F(3, 2) - d), (F(1, 2) * 50) / 1, (0 - d * 50) / ((u - d) * 1))
print("L06 lab time-0: shares", F(75) / 100, "bond", (0 - d * 75) / ((u - d) * Rf), "cost", F(3, 4) * 100 - 30)

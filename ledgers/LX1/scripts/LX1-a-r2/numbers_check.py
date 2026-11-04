"""Independent recomputation of every number in LX1 slice a (hub, L01, L02). Exact Fractions; rounding half up."""
import math
from fractions import Fraction as F


def rhu(x):
    return math.floor(x + F(1, 2))


def dec(x, p):
    return f"{float(x):.{p}f}"


out = []
def say(label, value):
    out.append(f"{label}: {value}")

# L01 Part A and Theorem 1.3
d1, r, g = 400, F(9, 100), F(3, 100)
F0 = F(d1) / (r - g)
q = (1 + g) / (1 + r)
say("L01 F0 exact", F0)
say("L01 F0 rounded", rhu(F0))
say("L01 q", q)
say("L01 q to 6dp", dec(q, 6))
for N in (10, 60, 200):
    S = sum(F(d1) * (1 + g) ** (s - 1) / (1 + r) ** s for s in range(1, N + 1))
    say(f"L01 S_{N} rounded", rhu(S))
    say(f"L01 identity S_{N} == F0(1-q^N)", S == F0 * (1 - q ** N))
    say(f"L01 F0 q^{N} rounded", rhu(F0 * q ** N))
# Fundamental path and printed numbers
for t in (2, 9):
    Ft = F(d1) * (1 + g) ** t / (r - g)
    say(f"L01 F_{t} exact decimal", dec(Ft, 6))
    say(f"L01 F_{t} rounded", rhu(Ft))
say("L01 F_9 exact (1.03^9 * 400/0.06)", float(F(400) * (F(103, 100) ** 9) / F(6, 100)))
# Prop 2.2 witness
say("L01 F0(1%)", F(400) / (F(9, 100) - F(1, 100)))
say("L01 F0(3%)", F(400) / (F(9, 100) - F(3, 100)))
say("L01 gap at 6000 under 1%", 6000 - F(400) / (F(9, 100) - F(1, 100)))
say("L01 gap at 6000 under 3%", F(6000) - F(400) / (F(9, 100) - F(3, 100)))
# Empirical 3 printed integers
say("L01 2175/8698", dec(F(2175, 8698), 8))
say("L01 2175/8698 6dp", dec(F(2175, 8698), 6))
say("L01 2175/8698 pct 2dp", dec(100 * F(2175, 8698), 2))
f9 = F(400) * (F(103, 100) ** 9) / F(6, 100)
say("L01 unrounded F_9", float(f9))
say("L01 unrounded 0.25*F_9 (gap)", float(F(1, 4) * f9))
say("L01 wedge t=9 price rounded", rhu(f9 * F(125, 100)))
# Research 1 threshold
gstar = F(9, 100) - F(400, 6000)
say("L01 g* exact", gstar)
say("L01 g* pct", float(100 * gstar))
# Mechanics
say("L01 mech1 F0 = 250/0.06 rounded", rhu(F(250) / F(6, 100)))
say("L01 mech2 F3 = 250*1.04^3/0.06", float(F(250) * F(104, 100) ** 3 / F(6, 100)))
say("L01 mech2 rounded", rhu(F(250) * F(104, 100) ** 3 / F(6, 100)))
say("L01 mech3 S10 = 20000/21", float(sum(F(100) / F(105, 100) for _ in range(10))))
# Canon-breaks example
say("L01 400/1.09", float(F(400) / F(109, 100)))
say("L01 400/1.09 rounded", rhu(F(400) / F(109, 100)))
say("L01 closed form at 3% rounded", rhu(F0))
# Quiz numbers
say("L01 F2 rounded to 2dp", dec(F(400) * F(103, 100) ** 2 / F(6, 100), 2))
say("L01 g* 6dp", dec(gstar, 6))
say("L01 9/13 4dp", dec(F(9, 13), 4))
say("L01 13-9", 13 - 9)
say("L01 1.25 wedge pct", 0.25)

# L02
P = [F(100)]
changes = [-1, 1, 1, 3, -4, -1, 2, -4, -3, 3, 2, -4]
for c in changes:
    P.append(P[-1] * (1 + F(c, 100)))
D = 1_000_000
V = [F(D) * P[0] / p for p in P]
say("L02 P12 unrounded", float(P[12]))
say("L02 P12 unrounded 8dp", dec(P[12], 8))
say("L02 P12 4dp display", dec(P[12], 4))
say("L02 V12/V0 6dp", dec(V[12] / V[0], 6))
say("L02 P0/P12 unrounded 8dp", dec(P[0] / P[12], 8))
say("L02 P0/P12 from printed 94.7051 6dp", dec(F(100) / F(947051, 10000), 6))
say("L02 printed-ratio minus unrounded-ratio", float(F(100) / F(947051, 10000) - P[0] / P[12]))
say("L02 V1 rounded", rhu(V[1]))
say("L02 V1 exact decimal", dec(V[1], 4))
say("L02 M1 V1", F(2000) * 100 / 80)
say("L02 M2 V2/V1", F(90, 85))
say("L02 M3 V1 exact", F(2000) * 100 / 95)
say("L02 M3 V1 rounded", rhu(F(2000) * 100 / 95))
say("L02 E2 V1", F(1000000) * 100 / 99)
say("L02 E2 V1 rounded", rhu(F(1000000) * 100 / 99))
say("L02 quiz 18/17 10dp", dec(F(18, 17), 10))
say("L02 E3 100/94.7051", dec(F(100) / F(947051, 10000), 8))
say("L02 1 kappa 2/5 gram price", 1 / F(2, 5))
say("L02 count falls", sum(1 for c in changes if c < 0))
say("L02 count rises", sum(1 for c in changes if c > 0))
say("L02 falls at", [t + 1 for t, c in enumerate(changes) if c < 0])
say("L02 rises at", [t + 1 for t, c in enumerate(changes) if c > 0])
steps = [rhu(V[t]) - rhu(V[t - 1]) for t in range(1, 13)]
say("L02 cent steps", steps)
say("L02 largest step (index,value)", (max(range(12), key=lambda i: steps[i]) + 1, max(steps)))
say("L02 P1 99 exact", P[1] == 99)
say("L02 real values rounded", [rhu(v) for v in V])
say("L02 V12 cents", rhu(V[12]))
for line in out:
    print(line)

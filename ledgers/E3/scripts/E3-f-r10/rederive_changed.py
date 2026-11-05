"""Round 10: independent re-derivation of the numbers in the changed or new slice-f cards.

Usage: python3 -I -W error rederive_changed.py
Exact Fractions only, plus a float check for c180. Prints each derived value next to the card's claim.
"""
import math
from fractions import Fraction as F

# E3-c180: CRRA CE at gamma = 1 of 1000 or 4000 with probability 1/2 each (Proposition 2.4, gamma = 1)
ce1 = math.exp(0.5 * math.log(1000) + 0.5 * math.log(4000))
print("c180 exp(0.5 ln 1000 + 0.5 ln 4000) =", round(ce1, 9), "claim 2000 ->", abs(ce1 - 2000) < 1e-9)

# E3-c183: Example 2.6, X = 1000 or 5000 w.p. 1/2; Y = 3000 sure. I(t) = E (t - Z)^+
def I(points, t):
    return sum(p * max(F(t) - x, F(0)) for x, p in points)

X = [(F(1000), F(1, 2)), (F(5000), F(1, 2))]
Y = [(F(3000), F(1))]
meanX = sum(x * p for x, p in X)
meanY = sum(x * p for x, p in Y)
print("c183 means", meanX, meanY)
bad = [t for t in range(0, 6001, 25) if I(Y, t) > I(X, t)]
print("c183 I_Y(t) <= I_X(t) on the grid 0..6000 step 25 (cents):", not bad, "violations", bad[:5])
supp = sorted({x for x, _ in X + Y})
print("c183 support", [int(s) for s in supp], "I_X", [str(I(X, s)) for s in supp], "I_Y", [str(I(Y, s)) for s in supp])

def F_(points, t):
    return sum(p for x, p in points if x <= t)

fo_xy = all(F_(X, t) <= F_(Y, t) for t in supp)
fo_yx = all(F_(Y, t) <= F_(X, t) for t in supp)
print("c183 first-order X dominates Y:", fo_xy, " Y dominates X:", fo_yx, "(both False expected)")

# E3-c050 / Remark 2.8: floor(v + 1/2) rounds halves up for v >= 0
for v in [F(0), F(1, 2), F(3, 2), F(10615801, 1000)]:
    print("c050 floor(v+1/2) at", v, "=", math.floor(v + F(1, 2)))

# E3-c022: sanity on u = ln with a two-point lottery (illustration of CE <= E X, not the proof)
xs = [2.0, 5.0]
ps = [0.5, 0.5]
m = sum(p * x for x, p in zip(xs, ps))
CE = math.exp(sum(p * math.log(x) for x, p in zip(xs, ps)))
print("c022 sanity: CE", round(CE, 6), "E X", m, "CE <= E X:", CE <= m)

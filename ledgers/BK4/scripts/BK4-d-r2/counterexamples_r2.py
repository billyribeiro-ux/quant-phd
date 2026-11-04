"""Round-2 verifier counterexamples for two cards whose unqualified answers are checked here (stdlib only).

Usage: python3 -I ledgers/BK4/scripts/BK4-d-r2/counterexamples_r2.py
(1) BK4-c075: 'After half of the claims are redeemed, does the coverage halve? No.' Under Assumptions 1 to 3 and
    the admissible share x = 1/2 (x <= rho), theta = (rho - 1/2)/(1/2) = 2 rho - 1; it equals rho/2 at rho = 2/3.
(2) BK4-c089: 'is the chance that at least one trade fails equal to 3p? No.' stated with A1 only (no joint law).
    Disjoint failure events F_1, F_2, F_3 on a 4-point space, each of probability p = 1/8, satisfy A1 and give
    P(at least one fails) = 3/8 = 3p, so the unqualified 'No' needs A3 or A4 in the front.
"""
from fractions import Fraction as F

rho = F(2, 3)
x = F(1, 2)
theta = (rho - x) / (1 - x)
print("c075 at rho = 2/3, x = 1/2: theta =", theta, "; rho/2 =", rho / 2, "; equal:", theta == rho / 2)
print("c075 admissible (x <= rho):", x <= rho, "; 0 <= x < 1:", 0 <= x < 1)
rho19 = F(19, 20)
print("c075 at rho = 19/20: theta =", (rho19 - x) / (1 - x), "; rho/2 =", rho19 / 2)

p = F(1, 8)
prob = {"w0": F(5, 8), "w1": F(1, 8), "w2": F(1, 8), "w3": F(1, 8)}
F_sets = {1: {"w1"}, 2: {"w2"}, 3: {"w3"}}
marg = [sum(prob[w] for w in F_sets[i]) for i in (1, 2, 3)]
union = sum(prob[w] for w in ("w1", "w2", "w3"))
print("c089 marginals:", marg, "(all equal p:", all(m == p for m in marg), ")")
print("c089 P(at least one fails) on disjoint law:", union, "; 3p =", 3 * p, "; equal:", union == 3 * p)

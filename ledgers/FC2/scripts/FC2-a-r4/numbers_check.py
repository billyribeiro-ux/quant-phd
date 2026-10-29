"""FC2-a round 4: independent recomputation of the prose and quiz numbers in index, L01, L02, L03.

Written from the page text, not from the lab twins. Run as: python -I numbers_check.py
"""
import math
from fractions import Fraction as Fr
from itertools import product

print("== hub")
print("placement 7/9 =", round(7 / 9 * 100, 2), "% ; 8/9 =", round(8 / 9 * 100, 2), "%")
print("NPV 100 invest, 60,60 at 10%:", round(-100 + 60 / 1.1 + 60 / 1.21, 6))
print("1/1.05^2 =", round(1 / 1.05**2, 6), "; 1/1.1025 =", round(1 / 1.1025, 6))
print("100 e^0.05 =", round(100 * math.exp(0.05), 6))
print("lesson hours sum:", 6 + 8 + 9 + 7 + 8 + 8 + 8 + 6, "; 30/90 =", round(30 / 90 * 100, 4), "%; 60/90 =", round(60 / 90 * 100, 4))
print("parity skill check:", 10 - 4 - (100 - 105 * 0.95))

print("== L01")
q = Fr(1)
psi_u = (q - Fr(9, 10)) / 2
psi_d = (Fr(27, 10) - q) / 2
print("Ex3.4 q=1 psi_u, psi_d =", psi_u, psi_d, "sum", psi_u + psi_d)
print("E1 B holding (-5,9): cost", Fr(-5) * Fr(9, 10) + 9 * Fr(1, 2), "payoff u", -5 + 9 * 3, "d", -5 + 9)
print("B state prices psi_u, psi_d for q=1/2:", (Fr(1, 2) - Fr(9, 10)) / 2, (Fr(27, 10) - Fr(1, 2)) / 2)
print("misc1 (-2 bonds, 1 stock) cost", -2 * Fr(9, 10) + 1, "payoff", (-2 + 3, -2 + 1))
print("M1 (2 bonds, -1 stock) cost", 2 * Fr(9, 10) - 1, "payoff", (2 - 3, 2 - 1))
print("M2 q=1 bond 4/5: psi_u", (Fr(1) - Fr(4, 5)) / 2, "psi_d", Fr(4, 5) - (Fr(1) - Fr(4, 5)) / 2 * 0 - (Fr(1) - Fr(4, 5)) / 2 * 0)
pu = (Fr(1) - Fr(4, 5)) / 2
print("   M2 explicit: psi_u =", pu, "psi_d =", Fr(4, 5) - pu)
print("Q6 upper end 27/10 =", float(Fr(27, 10)), "; Q8 cost (1 bond, -2 stocks) at q=1 =", Fr(9, 10) - 2)
print("R1 (3rd state) q=1 eps interval check: positive at eps=0.1?")
for q1, eps in [(Fr(1), Fr(1, 10))]:
    pu3 = (q1 - Fr(9, 10) - eps) / 2
    pd3 = (Fr(27, 10) - q1 - eps) / 2
    print("   psi_u", pu3, "psi_d", pd3, "bond check", pu3 + pd3 + eps, "stock check", 3 * pu3 + eps * 2 + pd3)
print("R1 q<=9/10 portfolio (-1,1) payoffs u,m,d:", -1 + 3, -1 + 2, -1 + 1, " cost", -Fr(9, 10) + 1)
print("R1 q>=27/10 portfolio (3,-1) payoffs u,m,d:", 3 - 3, 3 - 2, 3 - 1, " cost", 3 * Fr(9, 10) - Fr(27, 10))
print("Misc mispriced check: state prices for bond 9/10 stock 1/2 applied to (22,4):",
      Fr(-1, 5) * 22 + Fr(11, 10) * 4)

# lab-independent arbitrage box count for A and B (own implementation, own loops)
def count_box(prices, pay):
    n = 0
    lst = []
    for x, y in product(range(-10, 11), repeat=2):
        c = x * prices[0] + y * prices[1]
        p_u = x * pay[0][0] + y * pay[0][1]
        p_d = x * pay[1][0] + y * pay[1][1]
        if c <= 0 and p_u >= 0 and p_d >= 0 and (c < 0 or p_u > 0 or p_d > 0):
            n += 1
            lst.append((x, y))
    return n, lst

pay = [[Fr(1), Fr(3)], [Fr(1), Fr(1)]]
nA, _ = count_box([Fr(9, 10), Fr(1)], pay)
nB, lB = count_box([Fr(9, 10), Fr(1, 2)], pay)
print("box counts A, B:", nA, nB)
zc = [(x, y) for (x, y) in product(range(-10, 11), repeat=2) if Fr(9, 10) * x + Fr(1, 2) * y == 0 and x + 3 * y > 0 and x + y > 0]
print("first zero-cost strictly-positive holding (own loop, lex order):", zc[0] if zc else None)

# dominance pair counts, own implementation
def dom(prices, pay):
    S = range(-2, 3)
    hs = list(product(S, S))
    def pv(h):
        return [h[0] * pay[s][0] + h[1] * pay[s][1] for s in range(2)]
    def cv(h):
        return h[0] * prices[0] + h[1] * prices[1]
    d = 0
    b = 0
    for a in hs:
        for bb in hs:
            pa, pb = pv(a), pv(bb)
            if all(x >= y for x, y in zip(pa, pb)):
                d += 1
                if cv(a) < cv(bb):
                    b += 1
    return d, b
print("dominance A:", dom([Fr(9, 10), Fr(1)], pay), " B:", dom([Fr(9, 10), Fr(1, 2)], pay))

print("== L02")
F = 5000 * math.exp(0.025)
print("L02 fair (cents)", round(F, 6), "dollars", round(50 * math.exp(0.025), 6))
print("Part C net payoff 5200-F =", round(5200 - F, 6))
print("Part E value:", round(5300 - F * math.exp(-0.0125), 6), " discounted fair", round(F * math.exp(-0.0125), 6))
print("M1 50 e^0.025 =", round(50 * math.exp(0.025), 7), "e^0.025", round(math.exp(0.025), 10))
print("M2 80 e^0.01 =", round(80 * math.exp(0.01), 6), "e^0.01", round(math.exp(0.01), 10), "profit", round(81 - 80 * math.exp(0.01), 6))
print("M3 104 - 100 e^-0.015 =", round(104 - 100 * math.exp(-0.015), 6), "e^-0.015", round(math.exp(-0.015), 8))
print("P1 example: none numeric")
print("R3 annual 1.05^2 =", 1.05**2, " e^0.1 =", round(math.exp(0.1), 7), " diff", round(math.exp(0.1) - 1.1025, 6))
print("Q9 e^0.1 4dp:", round(math.exp(0.1), 4))
print("Q7 profit 0.20 check:", round(81 - 80 * math.exp(0.01), 2))
print("R1 band example none numeric")

print("== L03")
path = [5000]
import random
rng = random.Random(20261028)
for _ in range(10):
    path.append(path[-1] + rng.randint(-40, 40))
print("path (own rng replica):", path)
mg = [path[i] - path[i - 1] for i in range(1, 11)]
print("margins:", mg, "sum", sum(mg), "losses", sum(1 for m in mg if m < 0))
print("M1 margins 3,-4,2 balances", 3 - 4, 3 - 4 + 2)
print("M2 1.06^-3 =", round(1.06**-3, 7), "1/1.191016 =", round(1 / 1.191016, 7))
dfs = [1 / 1.06, 1 / 1.1236, 1 / 1.191016]
print("M3 dfs", dfs, "sum", sum(dfs), "displayed sum", 0.943396 + 0.889996 + 0.839619)
print("M3 value per notional", (0.06 - 0.05) * sum(dfs), " per 100 dollars", 100 * (0.06 - 0.05) * sum(dfs))
zr = [Fr(3, 100), Fr(7, 200), Fr(4, 100), Fr(9, 200), Fr(5, 100)]
D = [Fr(1)] + [Fr(1) / (1 + z) ** i for i, z in enumerate(zr, 1)]
ann = sum(D[1:], Fr(0))
R = (1 - D[5]) / ann
print("DFs", [round(float(x), 6) for x in D[1:]], "annuity", float(ann))
print("par rate", R, float(R), "6dp", round(float(R), 6))
print("payment cents", float(R) * 100_000_000)
print("value per payer struck R+1%:", float(-Fr(1, 100) * ann * 100_000_000))
print("R3 flat pieces: 1/1.03", 1 / 1.03, "1.03^-2", 1.03**-2)
d1 = 1 / 1.03
d2 = d1 / 1.05
print("R3 DF2", d2, "R_par", (1 - d2) / (d1 + d2), "f1", 1 / d1 - 1, "f2", d1 / d2 - 1)
print("P3 counterexample B2 with rho:", "1+rho")
print("E1 largest loss", min(mg), "day", mg.index(min(mg)) + 1)
print("E3 par 4dp", round(float(R) * 100, 4), "payment dollars", float(R) * 1_000_000)
print("Q6 DF1 1/1.03 6dp", round(1 / 1.03, 6))
print("Q5/ A8 counter DF: DF1=1/2, DF2=-1/2: sum", Fr(1, 2) + Fr(-1, 2), "RHS 1-DF2", 1 - Fr(-1, 2))
print("A8 coupon relation check: 1+L1 =", 1 / Fr(1, 2), " 1+L2 =", Fr(1, 2) / Fr(-1, 2))

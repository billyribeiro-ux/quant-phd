"""Independent recomputation of the LX2 numbers that cards and prose state (run: python3 -I numbers_check.py).

Written from the lesson text, not from the lab code: the L04 path is regenerated from random.Random(20261103) with the
stated draw order, the Part D probabilities are counted by enumeration, the L01 state table is rebuilt from the
readings in Section 4, and the L03 ratios and identity arithmetic are recomputed from the printed counts.
"""

import random
from fractions import Fraction as F

# ---- L04: outcomes measures on the SIMULATED path (seed 20261103, H = 24, U_t in -6..6 then V_t in -4..4)
rng = random.Random(20261103)
path = []
for t in range(24):
    u = rng.randint(-6, 6)
    v = rng.randint(-4, 4)
    y = 100 + u
    yhat = 101 + v
    path.append((yhat - y))
hits = sum(1 for e in path if abs(e) <= 2)
print("L04 A: errors", path)
print("L04 A: hits", hits, "of 24; hit rate", F(hits, 24), "=", round(hits / 24, 4))
print("L04 A: sum of errors", sum(path), "bias", F(sum(path), 24), "=", round(sum(path) / 24, 4))
print("L04 B: first 12 hit rate", F(sum(abs(e) <= 2 for e in path[:12]), 12), "bias", F(sum(path[:12]), 12))
print("L04 B: last 12 hit rate", F(sum(abs(e) <= 2 for e in path[12:]), 12), "bias", F(sum(path[12:]), 12))
print("L04 A: mean absolute error", F(sum(abs(e) for e in path), 24))
# Part C hand path
pc = [3, -3, 3, -3]
print(
    "L04 C: bias", F(sum(pc), 4), "hit rate", F(sum(abs(e) <= 2 for e in pc), 4), "MAE", F(sum(abs(e) for e in pc), 4)
)
# Part D: pairs (V, U): e = 1 + V - U, V in -4..4, U in -6..6
pairs = [1 + v - u for v in range(-4, 5) for u in range(-6, 7)]
print(
    "L04 D: pairs",
    len(pairs),
    "P(hit at band 2)",
    F(sum(abs(e) <= 2 for e in pairs), len(pairs)),
    "E[e]",
    F(sum(pairs), len(pairs)),
)
for b in range(0, 4):
    print("L04 R2: band", b, "hit count", sum(abs(e) <= b for e in pairs), "of 117")
print("L04 E1: hits in periods 13-24 =", sum(abs(e) <= 2 for e in path[12:]), "(lesson: 6 of 12)")
print("L04 E2: sum of errors periods 1-12 =", sum(path[:12]), "(lesson: 44)")
print(
    "L04 E3: Var(e) =",
    F(81 - 1, 12) + F(169 - 1, 12),
    "; SE =",
    round(((F(81 - 1, 12) + F(169 - 1, 12)) / 24) ** 0.5, 4),
)
gap = F(41, 12) - 1
print("L04 E3: gap", gap, "=", float(gap), "; SEs", round(float(gap) / ((F(62, 3) / 24) ** 0.5), 3))
print("L04 M2: -7/3 rounded", -round(7 / 3, 4))

# ---- L01: state table from the Section 4 readings
STATUSES = ["unregistered", "filed", "refused", "effective", "stop_order"]
LISTINGS = ["not_listed", "listed"]
states = [(s, l) for s in STATUSES for l in LISTINGS]
offer = lambda s: s[0] in ("filed", "effective")
sale = lambda s: s[0] == "effective"
r13 = lambda s: s[1] == "listed"
r15 = lambda s: s[0] in ("effective", "stop_order") and s[1] == "not_listed"
print(
    "L01: states",
    len(states),
    "sale",
    sum(sale(s) for s in states),
    "offer",
    sum(offer(s) for s in states),
    "R13",
    sum(r13(s) for s in states),
    "R15",
    sum(r15(s) for s in states),
    "both",
    sum(r13(s) and r15(s) for s in states),
    "sale-no-offer",
    sum(sale(s) and not offer(s) for s in states),
)
print("L01: 22 transitions = 6*2 + 2*5 =", 6 * 2 + 2 * 5)

# ---- L03: ratios and identity arithmetic from the printed counts
counts = {0: (6, 97), 1: (3, 104), 2: (10, 34 * 0 + 68), 3: (12, 58), 4: (17, 50), 5: (21, 37)}
for t, (c, f) in counts.items():
    print("L03 trader", t, "ratio", F(c, f), "flag at 2:", F(c, f) > 2)
print("L03: 3*97 =", 3 * 97, " 6*104 =", 6 * 104)
print(
    "L03: fills total 414 = 2 * 207:",
    414 == 2 * 207,
    "; identity check 170 + 2*4060 + 30 + 2020 =",
    170 + 2 * 4060 + 30 + 2020,
)
print("L03 E3: 5/34 vs 6/29 difference", F(6, 29) - F(5, 34), "; 59/986 =", F(59, 986))
print("L03 E1: 21*50 =", 21 * 50, " 17*37 =", 17 * 37)
print("L03 M3 / quiz: C_t = 1000 - 120 - 2*300 - 40 =", 1000 - 120 - 2 * 300 - 40)
print("L03 orders sum", 68 + 63 + 53 + 53 + 48 + 46, "cancels sum", 6 + 3 + 10 + 12 + 17 + 21)
print(
    "L02 pattern check: none (classifier output reproduced by the lab twin in run_labs; see out/twin_lab-LX2-L02-1.txt)"
)

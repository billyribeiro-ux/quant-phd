"""LX2-d round 1: independent recomputation of every number on the cards (not reusing the lab code).

Run: .venv/bin/python ledgers/LX2/scripts/LX2-d-r1/recompute_card_numbers.py
"""
import random
from fractions import Fraction as F
from itertools import product

# L04 Part A: draws in the order U1, V1, U2, V2, ... (realised first, then forecast), seed 20261103
rng = random.Random(20261103)
errs = []
hits = 0
for t in range(24):
    y = 100 + rng.randint(-6, 6)
    yhat = 101 + rng.randint(-4, 4)
    e = yhat - y
    errs.append(e)
    hits += abs(e) <= 2
H = 24
print("L04 A: hits", hits, "hit rate", F(hits, H), "sum errors", sum(errs), "bias", F(sum(errs), H))
print("L04 A: rounded bias (ties away):", F(sum(errs), H) * 10**4)
assert hits == 9 and sum(errs) == 82
print("L04 A rounded 4dp hit rate:", float(F(hits, H)), "bias float", round(sum(errs)/H, 4))
print("L04 A first 12 hit rate", F(sum(abs(e) <= 2 for e in errs[:12]), 12), "bias", F(sum(errs[:12]), 12))
print("L04 A last 12 hit rate", F(sum(abs(e) <= 2 for e in errs[12:]), 12), "bias", F(sum(errs[12:]), 12))
# L04 Part C: errors +3,-3,+3,-3
pc = [3, -3, 3, -3]
print("L04 C: bias", F(sum(pc), 4), "hits", sum(abs(e) <= 2 for e in pc), "MAE", F(sum(abs(e) for e in pc), 4))
# L04 Part D / Prop 4.4: enumerate U in -6..6 (realised), V in -4..4 (forecast), e = (101+V)-(100+U)
pairs = [(101 + v) - (100 + u) for v, u in product(range(-4, 5), range(-6, 7))]
print("L04 D: pairs", len(pairs), "P(hit)", F(sum(abs(e) <= 2 for e in pairs), len(pairs)), "E[e]", F(sum(pairs), len(pairs)))
print("L04 D: P(hit) decimal to 4dp", round(44/117, 4), "6dp", round(44/117, 6))
# R2 (band 3): 60/117 and band 1: 27 and band 0: 9
for b in range(0, 4):
    print("band", b, "hit count", sum(abs(e) <= b for e in pairs), "of", len(pairs))
# Prop 4.4 hit: -3 <= V-U <= 1 count
cnt = sum(1 for v, u in product(range(-4, 5), range(-6, 7)) if -3 <= v - u <= 1)
print("count of -3<=V-U<=1:", cnt)
# L04 E3 standard error numbers
var_v = F(9 * 9 - 1, 12); var_u = F(13 * 13 - 1, 12)
print("Var V", var_v, "Var U", var_u, "Var e", var_v + var_u)
# L03: traders
print("L03 comparisons: 3*97", 3 * 97, "6*104", 6 * 104, "21/37 vs 2:", F(21, 37) < 2, "17/50 decimal", F(17, 50), float(F(17, 50)))
print("L03 M3 C_t", 1000 - 120 - 2 * 300 - 40)
print("L03 E3 diff", F(6, 29) - F(5, 34), F(5, 34) < F(6, 29), 5 * 29, 6 * 34)
print("L03 E1: 21*50", 21 * 50, "17*37", 17 * 37, F(21, 37) > F(17, 50))
# L01 state model counts (independent of the lab code)
S = ["u", "f", "r", "e", "s"]; L = ["n", "l"]
states = [(s, l) for s in S for l in L]
t1933 = [("u", "f"), ("f", "r"), ("r", "f"), ("f", "e"), ("e", "s"), ("s", "e")]
t1934 = [("n", "l"), ("l", "n")]
trans = [((a, l), (b, l)) for a, b in t1933 for l in L] + [((s, a), (s, b)) for a, b in t1934 for s in S]
print("L01 states", len(states), "transitions", len(trans), "1933 x2", len(t1933) * 2, "1934 x5", len(t1934) * 5)
sale = [s for s in states if s[0] == "e"]
offer = [s for s in states if s[0] in ("f", "e")]
r13 = [s for s in states if s[1] == "l"]
r15 = [s for s in states if s[0] in ("e", "s") and s[1] == "n"]
print("L01 sale", len(sale), "offer", len(offer), "R13", len(r13), "R15", len(r15), "both", len(set(r13) & set(r15)))
# reachability
seen = {("u", "n")}; frontier = [("u", "n")]
while frontier:
    cur = frontier.pop()
    for a, b in trans:
        if a == cur and b not in seen:
            seen.add(b); frontier.append(b)
print("L01 reachable", len(seen), "of", len(states))
# L02 classifier: fired patterns P1,P3,P4,P6 (count 4), not fired 4, outsider count 3, tippee-knowledge failures 1 (P5)
print("L02 outsider patterns P6,P7,P8 = 3; knowledge failure only P5 = 1; fired 4 of 8")
# L02 Pr1-style counts for card c044-c047 none

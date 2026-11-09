"""Independent re-derivation of L07 Lab 1 and L08 Lab 1 numbers (no import of the lab twins)."""
from fractions import Fraction as F
from itertools import product

# ---------- L07 ----------
H7 = 4
G7 = (0, 100, 200, 300, 400)
R7 = {0: 0, 100: 60, 200: 100, 300: 120, 400: 130}  # consumption (cents) -> utils

def feas7(w):
    return [c for c in G7 if c <= w]

V = {H7: {w: w // 100 for w in G7}}
for t in range(H7 - 1, -1, -1):
    V[t] = {w: max(R7[c] + V[t + 1][w - c] for c in feas7(w)) for w in G7}
print("L07 Part A table (t, W0..W400):")
for t in range(H7 + 1):
    print(" ", t, [V[t][w] for w in G7])
print("W400 column:", [V[t][400] for t in range(H7 + 1)])

# brute force: all sequences of consumption from GRID; feasible iff each c <= wealth
def brute7(t, w):
    best = None
    cnt = 0
    for plan in product(G7, repeat=H7 - t):
        wl = w
        tot = 0
        ok = True
        for c in plan:
            if c > wl:
                ok = False
                break
            tot += R7[c]
            wl -= c
        if not ok:
            continue
        cnt += 1
        tot += wl // 100
        best = tot if best is None or tot > best else best
    return best, cnt

allm = True
for t in range(H7):
    for w in G7:
        b, _ = brute7(t, w)
        allm = allm and b == V[t][w]
print("L07 recursion == brute force for all 20 (t,w):", allm)
print("L07 feasible sequences from (0,400) (independent count):", brute7(0, 400)[1])
# stars and bars check: number of (c1..c4) in {0..4} with sum<=4 = C(8,4)
from math import comb
print("C(8,4) =", comb(8, 4))

# closed optimal plan and greedy
w = 400
plan = []
for t in range(H7):
    c = max(feas7(w), key=lambda x: R7[x] + V[t + 1][w - x])
    plan.append(c)
    w -= c
print("L07 optimal plan from (0,400):", plan)
greedy = []
w = 400
for _ in range(H7):
    c = max(feas7(w), key=lambda x: R7[x])
    greedy.append(c)
    w -= c
gt = sum(R7[c] for c in greedy) + (w // 100)
print("L07 greedy plan:", greedy, "total", gt, "fraction of optimum", F(gt, V[0][400]), float(F(gt, V[0][400])))
print("L07 optimal total", V[0][400])
print("L07 V0(400)-V3(400)=", V[0][400] - V[3][400])
print("L07 differences W400:", [V[t][400] - V[t + 1][400] for t in range(4)])
# quiz claim: plan 200,100,100 from (1,400) attains V1(400)=220
w = 400
tot = 0
for c in [200, 100, 100]:
    tot += R7[c]
    w -= c
tot += w // 100
print("L07 plan (200,100,100) from (1,400) total:", tot, "V1(400)=", V[1][400])

# Remark 2.5 counterexample (H=2), Fraction-free integer check
# V1(y)=0; V0(x)=max(0+0,1+0)=1 ; plan (a,c): 0 < 1
print("Remark 2.5: V0(x)=", max(0 + 0, 1 + 0))

# Remark 1.3/R1 sup check: totals a in (0,1) -> sup 1 not attained (qualitative)

# M1 .. P2 two-period problem check (L07 problem set)
S = {'x', 'y'}
A = {'x': ['u', 'v'], 'y': ['w']}
f = {('x', 'u'): 'y', ('x', 'v'): 'x', ('y', 'w'): 'y'}
r = {('x', 'u'): 3, ('x', 'v'): 5, ('y', 'w'): 2}
B = {'x': 0, 'y': 1}
import itertools
plans = []
for a0 in A['x']:
    s1 = f[('x', a0)]
    for a1 in A[s1]:
        tot = r[('x', a0)] + r[(s1, a1)] + B[f[(s1, a1)]]
        plans.append(((a0, a1), tot))
print("L07 M3 plans:", plans)
V1x = max(r[('x', a)] + B[f[('x', a)]] for a in A['x'])
V1y = r[('y', 'w')] + B['y']
V0x = max(r[('x', a)] + (V1y if f[('x', a)] == 'y' else V1x) for a in A['x'])
print("L07 M1 V1x,V1y,V0x:", V1x, V1y, V0x)
